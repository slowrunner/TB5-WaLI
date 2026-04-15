#!/usr/bin/env python3

# FILE:  wali/wali/echo_odom.py
# USE:  ros2 run wali echo_odom
# or :  cmds/echo_odom.sh

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
# from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
import math
import sys

class OdomPoseOnce(Node):
    def __init__(self):
        super().__init__('odom_pose_once')

        qos = QoSProfile(
            depth=1,
            # Note Durablity and Reliability setting required
            durability=QoSDurabilityPolicy.VOLATILE,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.pose_callback,
            qos
        )

    def pose_callback(self, msg):
        x  = msg.pose.pose.position.x
        y  = msg.pose.pose.position.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        yaw_deg = math.degrees(2.0 * math.atan2(qz, qw))        # ROS Heading +/-180 from docked 0 deg

        compass_deg = 180.0 - yaw_deg  # reversed and 0-360 from North (180 to docked heading)

        print("/odom received by wali.echo_odom")
        # print(f"x: {x:.4f}  y: {y:.4f}  heading: {yaw_deg:.2f}°")
        print(f"x: {x:.3f}  y: {y:.3f}  ROS heading: {yaw_deg:.0f}°  Compass heading: {compass_deg:.0f}°")

        self.destroy_node()
        rclpy.shutdown()
        sys.exit(0)

def main():
    rclpy.init()
    node = OdomPoseOnce()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass

if __name__ == '__main__':
    main()
