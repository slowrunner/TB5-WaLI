#!/usr/bin/env python3

# FILE: wali/wali/echo_pose.py
# USE: ros2 run wali echo_pose
# or : cmds/echo_pose.sh


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
from geometry_msgs.msg import PoseWithCovarianceStamped
import math
import sys

class AmclPoseOnce(Node):
    def __init__(self):
        super().__init__('amcl_pose_once')

        qos = QoSProfile(
            depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE
        )

        self.sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            qos
        )

    def pose_callback(self, msg):
        x  = msg.pose.pose.position.x
        y  = msg.pose.pose.position.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        yaw_deg = math.degrees(2.0 * math.atan2(qz, qw))      # ROS heading +/-180 from docked 0

        compass_deg = 180.0 - yaw_deg  # Compass is 0-360 from North (180 from docked)


        print("/amcl_pose received by wali.echo_pose")

        print(f"x: {x:.3f}  y: {y:.3f}  ROS heading: {yaw_deg:.0f}°  Compass heading: {compass_deg:.0f}°")


        self.destroy_node()
        rclpy.shutdown()
        sys.exit(0)

def main():
    rclpy.init()
    node = AmclPoseOnce()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass

if __name__ == '__main__':
    main()
