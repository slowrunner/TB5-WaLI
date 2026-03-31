
# FILE: set_initial_pose_undocked.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#

# Map map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.yaml

# - Docked per map (0.022, -0.372) Facing "NORTH" - 0 radians
# - UnDocked per map (-0.010, -0.372) Facing "SOUTH" - 1 Pi radians (3.14159)
# Copyright 2022 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

import rclpy
import time


from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()


    navigator.info('Want to set pose undocked.  Checking...')
    # Start off dock
    if navigator.getDockedStatus():
         navigator.info('Error: Use set_initial_pose_undocked only when undocked')
    else:

        # Set initial pose as undocked
        # initial_pose = navigator.getPoseStamped([0.022, -0.372], TurtleBot4Directions.NORTH)
        initial_pose = navigator.getPoseStamped([-0.0104, -0.372], TurtleBot4Directions.SOUTH)
        navigator.info('Setting Initial Pose to undock position facing SOUTH negative X')
        navigator.setInitialPose(initial_pose)


    navigator.info('Exiting set_initial_pose_undocked.py')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
