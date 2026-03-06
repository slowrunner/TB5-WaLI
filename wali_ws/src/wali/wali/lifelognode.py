#!/bin/env python3

# lifelognode node subscribes to /log2lifelog containing a string
# and writes the string to TB5-WaLI's life.log

# Original code written by gemini.google.com from the prompt:
# - create a Python ROS 2 node named lifelogger, 
# that subscribes to the topic /log2lifelog containing a string. 
# When the topic arrives, the node should add the string to the lifelog 
# defined by: LIFELOGFILE = "/home/ubuntu/TB5-WaLI/logs/life.log", 
# using the format definiition:
# self.logformatter = logging.Formatter('%(asctime)s|%(filename)s| %(message)s',"%Y-%m-%d %H:%M")
# (using the python logging module

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import logging
import os
from rclpy.executors import ExternalShutdownException

LIFELOGFILE = "/home/ubuntu/TB5-WaLI/logs/life.log"

class LifeLogger(Node):
    def __init__(self):
        super().__init__('lifelognode')
        
        # 1. Ensure the directory exists to avoid FileNotFoundError
        log_dir = os.path.dirname(LIFELOGFILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 2. Configure the Logger as requested
        self.lifeLog = logging.getLogger(__name__)
        self.lifeLog.setLevel(logging.INFO)

        self.loghandler = logging.FileHandler(LIFELOGFILE)
        self.logformatter = logging.Formatter('%(asctime)s|%(filename)s| %(message)s', "%Y-%m-%d %H:%M")
        self.loghandler.setFormatter(self.logformatter)
        self.lifeLog.addHandler(self.loghandler)

        # 3. Create Subscription
        self.subscription = self.create_subscription(
            String,
            '/log2lifelog',
            self.listener_callback,
            10)

        # self.get_logger().info(f'** LifeLogger node started. Writing to: {LIFELOGFILE} **')
        print(f'** LifeLogNode node started. Writing to: {LIFELOGFILE} **')

    def listener_callback(self, msg):
        # Log the incoming string to the file using the configured logger
        self.lifeLog.info("** " + msg.data + " **")

def main(args=None):
    rclpy.init(args=args)
    node = LifeLogger()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        # Catches Ctrl-C or a system kill signal gracefully
        pass
    finally:
        # Destroy the node explicitly
        if 'node' in locals():
            node.destroy_node()

    # Only shut down if rclpy hasn't already done so
    if rclpy.ok():
        rclpy.shutdown()

if __name__ == '__main__':
    main()

