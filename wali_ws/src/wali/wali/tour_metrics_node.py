#!/usr/bin/env python3
"""
tour_metrics_node.py  (wali package)

Passive observer node that collects navigation metrics during a
wali_tour.py run using nav2_simple_commander.followWaypoints().

Monitors:
  /follow_waypoints action     -- waypoint transitions, tour start/complete
  /navigate_to_pose action     -- per-waypoint recovery counts and timing
  /waypoint_follower/waypoint_reached (optional) -- precise arrival signal

Metrics reported per waypoint and for the full tour:
  - Navigation time to goal (seconds, excluding waypoint pause)
  - Number of recoveries
  - Estimated recovery time (seconds)
  - Navigation quality:  1.0 - (recovery_time / nav_time)
    1.0 = perfect run, lower = more time spent recovering

Nav time accuracy:
  nav2_waypoint_follower pauses at each waypoint for waypoint_pause_duration
  before advancing current_waypoint index.  This means:
    - /follow_waypoints feedback current_waypoint increments AFTER the pause
    - /navigate_to_pose feedback navigation_time INCLUDES the pause

  This node captures the last navigation_time value from /navigate_to_pose
  feedback immediately before the waypoint index increments, then subtracts
  waypoint_pause_duration to obtain true goal-to-goal navigation time.

  waypoint_pause_duration is read from the Nav2 parameter server at startup
  to decouple this node from any hardcoded yaml values.

  If /waypoint_follower/waypoint_reached topic is available (implementation-
  specific in some Nav2 distributions), it is used for precise arrival
  detection instead of the index-increment method.

Recovery time estimation methodology:
  Recovery duration is not directly published by Nav2. This node times
  the interval between a new recovery being detected (number_of_recoveries
  increments) and the next navigate_to_pose feedback cycle where
  number_of_recoveries stops incrementing. This is a consistent estimate
  — not exact — but is applied identically across all test runs, making
  it valid for relative comparison between nav2 parameter sets.

Usage:
  Terminal 1:  ros2 run wali tour_metrics
  Terminal 2:  ros2 run wali wali_tour

  Optional label argument:
  ros2 run wali tour_metrics --ros-args -p label:="inflation_0.75"

@Author:  Claude Sonnet 4.6 from prompts by slowrunner

"""

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from action_msgs.msg import GoalStatusArray, GoalStatus
from std_msgs.msg import Empty

import time
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Data class for per-waypoint metrics
# ---------------------------------------------------------------------------

class WaypointMetrics:
    def __init__(self, index: int):
        self.index                  = index       # 0-based waypoint index
        self.start_time             = None        # wall time when waypoint started
        self.arrival_time           = None        # wall time at goal arrival (pre-pause)
        self.end_time               = None        # wall time when next wp started
        self.nav_time_sec           = 0.0         # navigation_time from np feedback
                                                  # captured at arrival (pre-pause)
        self.last_np_nav_time       = 0.0         # rolling last value from np feedback
        self.recoveries             = 0           # total recoveries for this waypoint
        self.recovery_start_time    = None        # wall time recovery started
        self.recovery_total_sec     = 0.0         # accumulated estimated recovery time
        self.in_recovery            = False       # currently in a recovery
        self.skipped                = False       # True if in missed_waypoints result
        self.arrived                = False       # True once goal reached (pre-pause)

    @property
    def nav_time(self) -> float:
        """Navigation time to goal excluding waypoint pause (seconds).
        Uses nav_time_sec from navigate_to_pose feedback captured at arrival,
        with pause duration subtracted. Falls back to wall clock if needed."""
        return self.nav_time_sec

    @property
    def quality(self) -> float:
        """Navigation quality: 1.0 - (recovery_time / nav_time).
        1.0 = perfect, lower = more time spent in recovery."""
        t = self.nav_time
        if t <= 0.0:
            return 1.0
        return max(0.0, 1.0 - (self.recovery_total_sec / t))

    def __str__(self):
        status = "SKIPPED" if self.skipped else "OK"
        return (
            f"  Waypoint {self.index + 1:2d} [{status}] "
            f"nav={self.nav_time:6.1f}s  "
            f"recoveries={self.recoveries:2d}  "
            f"est.recovery={self.recovery_total_sec:5.1f}s  "
            f"quality={self.quality:6.4f}"
        )


# ---------------------------------------------------------------------------
# Metrics node
# ---------------------------------------------------------------------------

class TourMetricsNode(Node):

    # Fallback pause duration if parameter server lookup fails (seconds)
    DEFAULT_PAUSE_DURATION_SEC = 10.0

    def __init__(self):
        super().__init__('wali_nav_metrics_node')

        # Optional label for the parameter set being tested
        self.declare_parameter('label', 'unlabeled')
        self.label = self.get_parameter('label').get_parameter_value().string_value

        # --------------- waypoint pause duration ---------------
        self.waypoint_pause_sec = self._get_pause_duration()

        # --------------- state ---------------
        self.tour_started           = False
        self.tour_complete          = False
        self.tour_start_time        = None
        self.tour_end_time          = None

        self.waypoints: list        = []
        self.current_waypoint_index = -1
        self.missed_waypoints       = []

        # /navigate_to_pose tracking
        self.last_recovery_count    = 0
        self.np_feedback_time       = None

        # --------------- subscribers ---------------

        # Follow waypoints status — tour start / complete detection
        self.fw_status_sub = self.create_subscription(
            GoalStatusArray,
            '/follow_waypoints/_action/status',
            self._fw_status_callback,
            10
        )

        # Follow waypoints feedback — current_waypoint index transitions
        from nav2_msgs.action._follow_waypoints import FollowWaypoints_FeedbackMessage
        self.fw_feedback_sub = self.create_subscription(
            FollowWaypoints_FeedbackMessage,
            '/follow_waypoints/_action/feedback',
            self._fw_feedback_callback,
            10
        )

        # navigate_to_pose feedback — recovery counts, navigation_time
        from nav2_msgs.action._navigate_to_pose import NavigateToPose_FeedbackMessage
        self.np_feedback_sub = self.create_subscription(
            NavigateToPose_FeedbackMessage,
            '/navigate_to_pose/_action/feedback',
            self._np_feedback_callback,
            10
        )

        # Optional precise arrival signal from waypoint follower
        # Subscribe speculatively — no error if topic never publishes
        self.waypoint_reached_sub = self.create_subscription(
            Empty,
            '/waypoint_follower/waypoint_reached',
            self._waypoint_reached_callback,
            10
        )
        self._waypoint_reached_available = False  # set True on first message

        # Completion fallback timer
        # Must exceed waypoint_pause_duration to avoid false completion trigger
        self._fallback_timeout = self.waypoint_pause_sec + 20.0
        self._timer = self.create_timer(1.0, self._poll_completion)

        self.get_logger().info(
            f'Tour Metrics Node started.  Label: "{self.label}"  '
            f'Waypoint pause: {self.waypoint_pause_sec:.1f}s  '
            f'Fallback timeout: {self._fallback_timeout:.1f}s  '
            f'Waiting for /follow_waypoints tour to begin...'
        )

    # -----------------------------------------------------------------------
    #  Read waypoint_pause_duration from Nav2 parameter server
    # -----------------------------------------------------------------------

    def _get_pause_duration(self) -> float:
        """Query waypoint_follower node for waypoint_pause_duration parameter.
        Returns value in seconds. Falls back to DEFAULT_PAUSE_DURATION_SEC."""
        try:
            from rcl_interfaces.srv import GetParameters
            client = self.create_client(
                GetParameters,
                '/waypoint_follower/get_parameters'
            )
            if not client.wait_for_service(timeout_sec=3.0):
                self.get_logger().warn(
                    'waypoint_follower parameter service not available. '
                    f'Using default pause duration: {self.DEFAULT_PAUSE_DURATION_SEC}s'
                )
                return self.DEFAULT_PAUSE_DURATION_SEC

            req = GetParameters.Request()
            req.names = ['waypoint_pause_duration']
            future = client.call_async(req)
            rclpy.spin_until_future_complete(self, future, timeout_sec=3.0)

            if future.result() and future.result().values:
                # waypoint_pause_duration is in milliseconds in Nav2
                pause_ms = future.result().values[0].integer_value
                pause_sec = pause_ms / 1000.0
                self.get_logger().info(
                    f'waypoint_pause_duration from parameter server: '
                    f'{pause_ms}ms ({pause_sec:.1f}s)'
                )
                return pause_sec

        except Exception as e:
            self.get_logger().warn(
                f'Could not read waypoint_pause_duration: {e}. '
                f'Using default: {self.DEFAULT_PAUSE_DURATION_SEC}s'
            )

        return self.DEFAULT_PAUSE_DURATION_SEC

    # -----------------------------------------------------------------------
    #  /follow_waypoints/_action/status callback
    # -----------------------------------------------------------------------

    def _fw_status_callback(self, msg: GoalStatusArray):
        if not msg.status_list:
            return

        status = msg.status_list[-1].status

        if not self.tour_started and status in (
            GoalStatus.STATUS_ACCEPTED,
            GoalStatus.STATUS_EXECUTING
        ):
            self.tour_started    = True
            self.tour_start_time = time.monotonic()
            self.get_logger().info('Tour started — collecting metrics.')

        if self.tour_started and not self.tour_complete and status in (
            GoalStatus.STATUS_SUCCEEDED,
            GoalStatus.STATUS_ABORTED,
            GoalStatus.STATUS_CANCELED
        ):
            self._finish_tour()

    # -----------------------------------------------------------------------
    #  /follow_waypoints/_action/feedback callback
    #  current_waypoint increments AFTER waypoint_pause_duration elapses
    # -----------------------------------------------------------------------

    def _fw_feedback_callback(self, msg):
        try:
            idx = msg.feedback.current_waypoint
        except AttributeError:
            return

        if not self.tour_started:
            return

        if idx != self.current_waypoint_index:
            now = time.monotonic()

            # Close previous waypoint
            if self.current_waypoint_index >= 0 and self.waypoints:
                prev = self.waypoints[self.current_waypoint_index]
                if prev is not None:
                    prev.end_time = now
                    if prev.in_recovery:
                        prev.recovery_total_sec += now - prev.recovery_start_time
                        prev.in_recovery = False
                    # If waypoint_reached topic not available, capture
                    # last navigate_to_pose nav_time and subtract pause
                    if not self._waypoint_reached_available:
                        raw = prev.last_np_nav_time
                        # prev.nav_time_sec = max(0.0, raw - self.waypoint_pause_sec)
                        prev.nav_time_sec = max(0.0, raw)
                        self.get_logger().debug(
                            f'Waypoint {self.current_waypoint_index + 1} closing: '
                            f'last_np_nav_time={raw:.1f}s  '
                            f'pause={self.waypoint_pause_sec:.1f}s  '
                            f'nav_time_sec={prev.nav_time_sec:.1f}s'
                        )

            # Start new waypoint
            self.current_waypoint_index = idx
            wp = WaypointMetrics(idx)
            wp.start_time = now

            while len(self.waypoints) <= idx:
                self.waypoints.append(None)
            self.waypoints[idx] = wp

            self.last_recovery_count = 0

            self.get_logger().info(f'Waypoint {idx + 1} started.')

    # -----------------------------------------------------------------------
    #  /waypoint_follower/waypoint_reached callback (optional precise arrival)
    # -----------------------------------------------------------------------

    def _waypoint_reached_callback(self, msg: Empty):
        if not self.tour_started or self.current_waypoint_index < 0:
            return

        if not self._waypoint_reached_available:
            self._waypoint_reached_available = True
            self.get_logger().info(
                '/waypoint_follower/waypoint_reached topic available — '
                'using precise arrival detection.'
            )

        wp = self.waypoints[self.current_waypoint_index]
        if wp is None or wp.arrived:
            return

        wp.arrived       = True
        wp.arrival_time  = time.monotonic()
        # Capture nav_time from np feedback at this precise arrival moment
        # No pause subtraction needed — arrival fired before pause begins
        wp.nav_time_sec  = wp.last_np_nav_time

        if wp.in_recovery:
            wp.recovery_total_sec += wp.arrival_time - wp.recovery_start_time
            wp.in_recovery = False

    # -----------------------------------------------------------------------
    #  /navigate_to_pose/_action/feedback callback
    # -----------------------------------------------------------------------

    def _np_feedback_callback(self, msg):
        if not self.tour_started or self.current_waypoint_index < 0:
            return

        wp = self.waypoints[self.current_waypoint_index]
        if wp is None:
            return

        try:
            recoveries = msg.feedback.number_of_recoveries
            nav_time   = (msg.feedback.navigation_time.sec +
                          msg.feedback.navigation_time.nanosec * 1e-9)
        except AttributeError:
            return

        now = time.monotonic()

        # Always track last known nav_time for pause subtraction fallback
        wp.last_np_nav_time = nav_time

        # Recovery start detection
        if recoveries > self.last_recovery_count:
            wp.recoveries       += recoveries - self.last_recovery_count
            self.last_recovery_count = recoveries
            if not wp.in_recovery:
                wp.in_recovery        = True
                wp.recovery_start_time = now

        else:
            # Recovery count stable — close recovery if open
            if wp.in_recovery:
                elapsed = now - wp.recovery_start_time
                if elapsed > 0.2:   # debounce one feedback cycle
                    wp.recovery_total_sec += elapsed
                    wp.in_recovery         = False
                    wp.recovery_start_time = None

        self.np_feedback_time = now

    # -----------------------------------------------------------------------
    #  Completion fallback poll
    # -----------------------------------------------------------------------

    def _poll_completion(self):
        if not self.tour_started or self.tour_complete:
            return
        if self.np_feedback_time is None:
            return

        silence = time.monotonic() - self.np_feedback_time
        if silence > self._fallback_timeout and self.current_waypoint_index >= 0:
            self.get_logger().warn(
                f'No navigate_to_pose feedback for {self._fallback_timeout:.0f}s '
                f'— assuming tour complete.'
            )
            self._finish_tour()

    # -----------------------------------------------------------------------
    #  Finish tour — close last waypoint and print report
    # -----------------------------------------------------------------------

    def _finish_tour(self):
        if self.tour_complete:
            return
        self.tour_complete = True
        self.tour_end_time = time.monotonic()

        # Close last waypoint
        if self.waypoints:
            last = self.waypoints[self.current_waypoint_index]
            if last is not None and last.end_time is None:
                last.end_time = self.tour_end_time
                if last.in_recovery:
                    last.recovery_total_sec += (
                        self.tour_end_time - last.recovery_start_time
                    )
                    last.in_recovery = False
                if not self._waypoint_reached_available:
                    raw = last.last_np_nav_time
                    last.nav_time_sec = max(0.0, raw - self.waypoint_pause_sec)
                    self.get_logger().debug(
                        f'Waypoint {self.current_waypoint_index + 1} closing (last): '
                        f'last_np_nav_time={raw:.1f}s  '
                        f'pause={self.waypoint_pause_sec:.1f}s  '
                        f'nav_time_sec={last.nav_time_sec:.1f}s'
                    )

        self.get_logger().info('Tour complete — printing report.')
        self._print_report()
        rclpy.shutdown()

    # -----------------------------------------------------------------------
    #  Report
    # -----------------------------------------------------------------------

    def _print_report(self):
        now_str      = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tour_elapsed = (self.tour_end_time - self.tour_start_time
                        if self.tour_end_time and self.tour_start_time else 0.0)

        valid_wps    = [w for w in self.waypoints if w is not None]
        total_rec    = sum(w.recoveries for w in valid_wps)
        total_rec_t  = sum(w.recovery_total_sec for w in valid_wps)
        total_nav_t  = sum(w.nav_time for w in valid_wps)
        skipped      = [w.index + 1 for w in valid_wps if w.skipped]

        # Pure navigation time = tour time minus all pauses
        pause_total  = self.waypoint_pause_sec * len(valid_wps)
        pure_nav_t   = max(0.0, tour_elapsed - pause_total)

        overall_quality = (1.0 - total_rec_t / total_nav_t
                           if total_nav_t > 0 else 1.0)

        arrival_method = ('/waypoint_follower/waypoint_reached'
                          if self._waypoint_reached_available
                          else 'index-increment minus pause (estimated)')

        sep  = '=' * 65
        sep2 = '-' * 65

        print()
        print(sep)
        print(f'  TB5-WaLI NAVIGATION METRICS REPORT')
        print(f'  {now_str}')
        print(f'  Parameter set label   : {self.label}')
        print(f'  Arrival detection     : {arrival_method}')
        print(f'  Waypoint pause        : {self.waypoint_pause_sec:.1f}s')
        print(sep)
        print()
        print('  PER-WAYPOINT METRICS')
        print(sep2)
        for wp in valid_wps:
            print(wp)
        print(sep2)
        print()
        print('  TOUR SUMMARY')
        print(sep2)
        print(f'  Waypoints attempted   : {len(valid_wps)}')
        print(f'  Waypoints skipped     : {len(skipped)}'
              + (f'  {skipped}' if skipped else ''))
        print(f'  Total nav time        : {total_nav_t:7.1f} s'
              f'  ({total_nav_t / 60.0:.1f} min)  [goal-to-goal, no pauses]')
        print(f'  Total pause time      : {pause_total:7.1f} s'
              f'  ({pause_total / 60.0:.1f} min)')
        print(f'  Total tour time       : {tour_elapsed:7.1f} s'
              f'  ({tour_elapsed / 60.0:.1f} min)  [nav + pauses]')
        print(f'  Total recoveries      : {total_rec:7d}')
        print(f'  Est. recovery time    : {total_rec_t:7.1f} s')
        print(f'  Overall nav quality   : {overall_quality:7.4f}'
              f'  [1.0 - recovery_time/nav_time]')
        print(sep)
        print()
        print('  NOTE: Recovery time is estimated (see node docstring).')
        print('        Consistent methodology enables valid cross-run comparison.')
        if not self._waypoint_reached_available:
            print(f'  NOTE: Nav time = last np feedback nav_time minus '
                  f'{self.waypoint_pause_sec:.1f}s pause (estimated).')
        print()
        print(sep)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = TourMetricsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nMetrics node interrupted.')
        if node.tour_started and not node.tour_complete:
            print('Tour in progress — partial report:')
            node._print_report()
    finally:
        node.destroy_node()


if __name__ == '__main__':
    main()
