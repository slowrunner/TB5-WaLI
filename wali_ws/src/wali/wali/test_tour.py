#!/usr/bin/env python3
"""
test_tour.py  –  WaLI package  –  TurtleBot4 / ROS 2 Jazzy
=============================================================
Drives the robot through a fixed sequence of goal poses using
Nav2's NavigateToPose action directly (no waypoint follower).
After every goal attempt (success or failure) the node pauses
30 s before proceeding to the next one.

Recovery tracking
─────────────────
RecoveryStatus is removed in Jazzy.  Recovery behaviour names
and timing are obtained by subscribing to /behavior_tree_log
(nav2_msgs/BehaviorTreeLog), whose BehaviorTreeStatusChange[]
event_log entries carry:
    • node_name       – BT node name (string)
    • previous_status – "IDLE" | "RUNNING" | "SUCCESS" | "FAILURE"
    • current_status  – same options

A recovery is detected when a known recovery-class BT node
transitions to RUNNING, and considered complete when it leaves
RUNNING.  The count from NavigateToPose feedback
(number_of_recoveries) is used as a cross-check / fallback.

Battery
───────
/battery_status (sensor_msgs/BatteryState) is checked before
every goal.  If percentage ≤ 30 % the tour terminates.

Log file
────────
~/TB5-WaLI/logs/tmp/<YYYY-MM-DD_HH-MM>_test_tour.log

Requires
--------
sudo apt install python3-transforms3d
sudo apt install ros-jazzy-tf-transformations
"""

import math
import signal
import sys
import time
from datetime import datetime
from enum import IntEnum
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from nav2_msgs.msg import BehaviorTreeLog          # event_log: BehaviorTreeStatusChange[]
from sensor_msgs.msg import BatteryState

from tf_transformations import euler_from_quaternion   # apt: python3-transforms3d


# ─────────────────────────────────────────────────────────────
#  BT node names classified as recovery behaviours.
#  These match the XML node names in Nav2's default BTs.
# ─────────────────────────────────────────────────────────────
RECOVERY_BT_NODES: frozenset = frozenset({
    "BackUp",
    "Spin",
    "Wait",
    "ClearEntireCostmap",
    "ClearCostmapAroundRobot",
    "ClearCostmapExceptRegion",
    "ClearLocalCostmap-Context",
    "ClearLocalCostmap-Subtree",
    "ClearGlobalCostmap-Context",
    "ClearGlobalCostmap-Subtree",
    "NavigateRecovery",        # top-level recovery sub-tree node
})


# ─────────────────────────────────────────────────────────────
#  Direction enum
# ─────────────────────────────────────────────────────────────
class WaLI_Dir(IntEnum):
    """
    WaLI compass heading enum.  The integer value is the yaw
    angle in degrees that is converted to a quaternion when
    building PoseStamped goal messages.

    SOUTH (0 deg)  -> robot faces map +X axis.
    Values increase counter-clockwise.
    """
    SOUTH      =   0
    SOUTH_EAST =  45
    EAST       =  90
    NORTH_EAST = 135
    NORTH      = 180
    NORTH_WEST = 225
    WEST       = 270
    SOUTH_WEST = 315


def wali_dir_to_quaternion(direction: WaLI_Dir):
    """Return (qx, qy, qz, qw) for a pure yaw rotation."""
    yaw = math.radians(int(direction))
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


def quaternion_to_ros_heading(qx, qy, qz, qw) -> int:
    """Return yaw in whole degrees, range -180 to +180."""
    _, _, yaw = euler_from_quaternion([qx, qy, qz, qw])
    deg = math.degrees(yaw)
    deg = (deg + 180.0) % 360.0 - 180.0
    return int(round(deg))


# ─────────────────────────────────────────────────────────────
#  Tour goal list
# ─────────────────────────────────────────────────────────────
GOALS = [
    # ( name,          x,      y,      direction          )
    ("Front Door",   3.000,  3.990,  WaLI_Dir.SOUTH     ),
    ("Kitchen",      3.710,  1.040,  WaLI_Dir.NORTH_WEST),
    ("Ready",       -0.208, -0.317,  WaLI_Dir.NORTH_EAST),
]

POST_GOAL_PAUSE_S = 30          # seconds to wait after each goal
BATTERY_MIN       = 0.30        # terminate if battery <= 30 %


# ─────────────────────────────────────────────────────────────
#  Dual console + file logger
# ─────────────────────────────────────────────────────────────
class TourLogger:
    def __init__(self):
        log_dir = Path.home() / "TB5-WaLI" / "logs" / "tmp"
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self._path = log_dir / f"{ts}_test_tour.log"
        self._fh = open(self._path, "w", buffering=1)   # line-buffered
        self.info(f"=== WaLI Test Tour Log  started {datetime.now().isoformat()} ===")
        self.info(f"Log path: {self._path}\n")

    def info(self, msg: str = ""):
        print(msg)
        self._fh.write(msg + "\n")

    def close(self):
        self._fh.flush()
        self._fh.close()

    @property
    def path(self):
        return self._path


# ─────────────────────────────────────────────────────────────
#  Per-goal recovery tracker fed from /behavior_tree_log
# ─────────────────────────────────────────────────────────────
class RecoveryTracker:
    """
    Watches BehaviorTreeLog messages published during a single
    goal run and records:
      - which recovery BT nodes ran (by name)
      - how long each one ran (wall-clock seconds)

    Usage:
        tracker = RecoveryTracker()
        # feed each BehaviorTreeLog message:
        tracker.handle_bt_log(msg)
        # at goal end:
        tracker.close_open_recoveries()
        recs = tracker.result()       # list[(name, duration_s)]
    """

    def __init__(self):
        # name -> wall-clock time when node entered RUNNING
        self._active: dict = {}
        # completed: list of (name, duration_s)
        self._completed: list = []

    def handle_bt_log(self, msg: BehaviorTreeLog):
        """Process one BehaviorTreeLog message (called from subscriber cb)."""
        now = time.monotonic()
        for ev in msg.event_log:
            name = ev.node_name
            prev = ev.previous_status   # "IDLE" | "RUNNING" | "SUCCESS" | "FAILURE"
            curr = ev.current_status

            if name not in RECOVERY_BT_NODES:
                continue

            if curr == "RUNNING" and prev != "RUNNING":
                # Recovery just started; record start time
                self._active[name] = now

            elif prev == "RUNNING" and curr != "RUNNING":
                # Recovery just ended
                if name in self._active:
                    duration = now - self._active.pop(name)
                else:
                    # Missed the start (subscriber was late); record 0 s
                    duration = 0.0
                self._completed.append((name, duration))

    def close_open_recoveries(self):
        """
        Close any recoveries still marked RUNNING at goal-end
        (e.g. goal succeeded mid-recovery, or we were cancelled).
        """
        now = time.monotonic()
        for name, start in list(self._active.items()):
            self._completed.append((name, now - start))
        self._active.clear()

    def result(self):
        """Return list of (node_name, duration_s) tuples."""
        return list(self._completed)

    def total_recovery_time(self) -> float:
        return sum(d for _, d in self._completed)


# ─────────────────────────────────────────────────────────────
#  Main node
# ─────────────────────────────────────────────────────────────
class TestTourNode(Node):

    def __init__(self):
        super().__init__("test_tour_node")

        self._log = TourLogger()
        self._log.info("--- WaLI Test Tour Node starting ---\n")

        # QoS profiles
        qos_sensor = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
        )
        qos_reliable = QoSProfile(
            depth=50,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )

        # ── /battery_status ───────────────────────────────────
        self._battery_pct: float = -1.0
        self._bat_sub = self.create_subscription(
            BatteryState, "/battery_state",
            self._battery_cb, qos_sensor)


        # ── /amcl_pose ────────────────────────────────────────
        self._current_pose = None
        self._pose_sub = self.create_subscription(
            PoseWithCovarianceStamped, "/amcl_pose",
            self._pose_cb, qos_sensor)

        # ── /behavior_tree_log ────────────────────────────────
        # BehaviorTreeLog is published by bt_navigator on every BT tick.
        # We forward each message into the active RecoveryTracker (if any).
        self._recovery_tracker: RecoveryTracker | None = None
        self._bt_log_sub = self.create_subscription(
            BehaviorTreeLog, "/behavior_tree_log",
            self._bt_log_cb, qos_reliable)

        # ── NavigateToPose action client ──────────────────────
        self._nav_client = ActionClient(self, NavigateToPose, "navigate_to_pose")

        # ── Tour-level accumulators ───────────────────────────
        self._tour_start       = time.monotonic()
        self._total_successes  = 0
        self._total_failures   = 0
        self._total_skipped    = 0
        self._total_recoveries = 0
        self._total_recovery_s = 0.0

        # ── SIGINT / Ctrl-C ───────────────────────────────────
        self._shutdown_requested = False
        signal.signal(signal.SIGINT, self._sigint_handler)

    # ── subscription callbacks ────────────────────────────────

    def _battery_cb(self, msg: BatteryState):
        self._battery_pct = msg.percentage

    def _pose_cb(self, msg: PoseWithCovarianceStamped):
        self._current_pose = msg

    def _bt_log_cb(self, msg: BehaviorTreeLog):
        """
        Receive BehaviorTreeLog published by bt_navigator.
        Each message contains a BehaviorTreeStatusChange[] event_log
        with fields: node_name, previous_status, current_status.
        Forward to the active recovery tracker during a goal run.
        """
        if self._recovery_tracker is not None:
            self._recovery_tracker.handle_bt_log(msg)

    # ── SIGINT handler ────────────────────────────────────────

    def _sigint_handler(self, signum, frame):
        self._shutdown_requested = True
        bat = self._battery_pct * 100.0
        self._log.info(f"\nUser terminated test, Battery at {bat:.0f}%")
        self._log.info(f"Current pose: {self._pose_summary()}")
        self._print_tour_summary()
        self._log.info("----- TEST TOUR END ----")
        self._log.close()
        rclpy.shutdown()
        sys.exit(0)

    # ── helpers ───────────────────────────────────────────────

    def _spin_some(self, duration_s: float):
        """Spin the ROS event loop for approximately duration_s seconds."""
        deadline = time.monotonic() + duration_s
        while time.monotonic() < deadline and not self._shutdown_requested:
            rclpy.spin_once(self, timeout_sec=0.05)

    def _pose_summary(self) -> str:
        if self._current_pose is None:
            return "unknown (no /amcl_pose received yet)"
        p = self._current_pose.pose.pose
        q = p.orientation
        hdg = quaternion_to_ros_heading(q.x, q.y, q.z, q.w)
        return (f"x={p.position.x:.3f} m, "
                f"y={p.position.y:.3f} m, "
                f"ROS Heading={hdg:+d} deg")

    def _make_pose_stamped(self, x: float, y: float,
                           direction: WaLI_Dir) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        qx, qy, qz, qw = wali_dir_to_quaternion(direction)
        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw
        return pose

    # ── single goal navigation ────────────────────────────────

    def _navigate_to_goal(self, name: str,
                          x: float, y: float,
                          direction: WaLI_Dir) -> dict:
        """
        Send one NavigateToPose goal, block until it completes (or
        is cancelled), and return a dict of per-goal statistics.

        Feedback fields used from NavigateToPose (Jazzy):
            current_pose, navigation_time, estimated_time_remaining,
            number_of_recoveries, distance_remaining

        Recovery *names* come from /behavior_tree_log via RecoveryTracker.
        """
        self._log.info(f"\n{'='*62}")
        self._log.info(f"  Goal: {name}  ->  "
                       f"x={x:.3f} m, y={y:.3f} m, dir={direction.name}")
        self._log.info(f"{'='*62}")

        result = {
            "name":            name,
            "status":          "Failure",
            "total_time_s":    0.0,
            "recovery_time_s": 0.0,
            "recoveries":      [],   # list[(bt_node_name, duration_s)]
            "nav_recoveries":  0,    # count from NavigateToPose feedback
            "end_pose":        None,
            "goal_x":          x,
            "goal_y":          y,
            "goal_dir":        direction,
        }

        # ── wait for action server ────────────────────────────
        self._log.info("  Waiting for navigate_to_pose action server ...")
        if not self._nav_client.wait_for_server(timeout_sec=15.0):
            self._log.info("  [!] Action server unavailable – goal Skipped")
            result["status"] = "Skipped before any movement"
            return result

        # ── arm recovery tracker (feeds from /behavior_tree_log cb) ──
        self._recovery_tracker = RecoveryTracker()
        goal_start = time.monotonic()

        # ── build and send goal ───────────────────────────────
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self._make_pose_stamped(x, y, direction)
        goal_msg.behavior_tree = ""   # use Nav2 default BT

        # Capture latest feedback (number_of_recoveries is the only
        # recovery-related field in NavigateToPose feedback in Jazzy)
        _fb_recovery_count = [0]

        def feedback_cb(feedback_msg):
            _fb_recovery_count[0] = int(
                feedback_msg.feedback.number_of_recoveries)

        send_future = self._nav_client.send_goal_async(
            goal_msg, feedback_callback=feedback_cb)

        # Spin until goal accepted / rejected
        while not send_future.done() and not self._shutdown_requested:
            rclpy.spin_once(self, timeout_sec=0.05)

        if self._shutdown_requested:
            result["total_time_s"] = time.monotonic() - goal_start
            self._recovery_tracker.close_open_recoveries()
            self._recovery_tracker = None
            return result

        goal_handle = send_future.result()
        if not goal_handle.accepted:
            self._log.info("  [!] Goal rejected – marking Skipped")
            result["status"] = "Skipped before any movement"
            result["total_time_s"] = time.monotonic() - goal_start
            self._recovery_tracker.close_open_recoveries()
            self._recovery_tracker = None
            return result

        self._log.info("  [ok] Goal accepted – navigating ...")

        # ── spin until navigation completes ───────────────────
        result_future = goal_handle.get_result_async()
        while not result_future.done() and not self._shutdown_requested:
            rclpy.spin_once(self, timeout_sec=0.05)

        total_time_s = time.monotonic() - goal_start
        result["total_time_s"]   = total_time_s
        result["nav_recoveries"] = _fb_recovery_count[0]

        # Close any recoveries still open at goal-end
        self._recovery_tracker.close_open_recoveries()

        if not self._shutdown_requested:
            nav_result  = result_future.result()
            status_code = nav_result.status
            result["status"] = (
                "Success" if status_code == GoalStatus.STATUS_SUCCEEDED
                else "Failure"
            )

        # ── harvest recovery stats from BT log ────────────────
        recs = self._recovery_tracker.result()
        result["recoveries"]      = recs
        result["recovery_time_s"] = self._recovery_tracker.total_recovery_time()
        self._recovery_tracker = None

        # ── capture end pose ──────────────────────────────────
        rclpy.spin_once(self, timeout_sec=0.15)
        result["end_pose"] = self._current_pose

        return result

    # ── per-goal report ───────────────────────────────────────

    def _report_goal(self, res: dict):
        L = self._log.info
        name   = res["name"]
        status = res["status"]

        sep = "-" * max(2, 48 - len(name))
        L(f"\n  -- Result: '{name}' {sep}")
        L(f"  Navigation Status        : {status}")
        L(f"  Total time on goal       : {res['total_time_s']:.1f} s")
        L(f"  Total recovery time      : {res['recovery_time_s']:.1f} s")
        L(f"  Recovery count (feedback): {res['nav_recoveries']}")

        recs = res["recoveries"]
        if recs:
            L("  Recoveries (from BT log) :")
            for rname, rdur in recs:
                L(f"    • {rname:<42s}  {rdur:.1f} s")
        else:
            L("  Recoveries (from BT log) : none detected")

        # ── end pose ──────────────────────────────────────────
        ep = res["end_pose"]
        if ep is not None:
            p = ep.pose.pose
            q = p.orientation
            hdg = quaternion_to_ros_heading(q.x, q.y, q.z, q.w)
            L(f"  End pose                 : "
              f"x={p.position.x:.3f} m, "
              f"y={p.position.y:.3f} m, "
              f"ROS Heading={hdg:+d} deg")

            if status == "Success":
                dx  = p.position.x - res["goal_x"]
                dy  = p.position.y - res["goal_y"]
                _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
                goal_yaw  = math.radians(int(res["goal_dir"]))
                dhdg = int(round(math.degrees(yaw - goal_yaw)))
                dhdg = (dhdg + 180) % 360 - 180
                L(f"  Distance from goal       : "
                  f"dx={dx:.3f} m, "
                  f"dy={dy:.3f} m, "
                  f"d_heading={dhdg:+d} deg")
        else:
            L("  End pose                 : unknown (no AMCL data)")

    # ── tour summary ──────────────────────────────────────────

    def _print_tour_summary(self):
        elapsed = time.monotonic() - self._tour_start
        L = self._log.info
        L("")
        L("=" * 62)
        L("  TOUR SUMMARY")
        L("=" * 62)
        L(f"  Total tour time        : {elapsed:.1f} s  "
          f"({elapsed / 60:.1f} min)")
        L(f"  Successful navigations : {self._total_successes}")
        L(f"  Failed navigations     : {self._total_failures}")
        L(f"  Goals skipped          : {self._total_skipped}")
        L(f"  Recoveries attempted   : {self._total_recoveries}")
        L(f"  Total recovery time    : {self._total_recovery_s:.1f} s")
        L("=" * 62)

    # ── main tour loop ────────────────────────────────────────

    def run_tour(self):
        self._log.info("Waiting 6s for initial sensor data ...")
        self._spin_some(6.0)  # /battery_state is only once per 5s

        for idx, (name, x, y, direction) in enumerate(GOALS, start=1):
            if self._shutdown_requested:
                break

            self._log.info(f"\n{'─'*62}")
            self._log.info(f"  Goal {idx}/{len(GOALS)}: {name}")
            self._log.info(f"{'─'*62}")

            # ── battery check ─────────────────────────────────
            self._log.info("Waiting 6s for fresh battery status")
            self._spin_some(6.0)          # allow fresh battery message
            bat = self._battery_pct
            self._log.info(f"  Battery: {bat * 100:.1f}%")

            if bat <= BATTERY_MIN:
                self._log.info(
                    "\n*** Tour Terminated Due To Battery Less Than 30% ***")
                self._print_tour_summary()
                break

            # ── navigate ──────────────────────────────────────
            res = self._navigate_to_goal(name, x, y, direction)
            self._report_goal(res)

            # ── accumulate tour-level stats ───────────────────
            if res["status"] == "Success":
                self._total_successes += 1
            elif res["status"] == "Skipped before any movement":
                self._total_skipped += 1
            else:
                self._total_failures += 1

            self._total_recoveries += len(res["recoveries"])
            self._total_recovery_s += res["recovery_time_s"]

            if self._shutdown_requested:
                break

            # ── post-goal pause (skip after last goal) ────────
            if idx < len(GOALS):
                self._log.info(
                    f"\n  Pausing {POST_GOAL_PAUSE_S} s before next goal ...")
                self._spin_some(POST_GOAL_PAUSE_S)

        # ── end-of-tour ───────────────────────────────────────
        if not self._shutdown_requested:
            self._print_tour_summary()
            self._log.info("----- TEST TOUR END ----")
            self._log.close()


# ─────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = TestTourNode()
    try:
        node.run_tour()
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
