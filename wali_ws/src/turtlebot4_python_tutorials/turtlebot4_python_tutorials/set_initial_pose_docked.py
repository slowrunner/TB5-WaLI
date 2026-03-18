
# FILE: set_initial_pose_docked.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#
# - Docked per map (0.022, -0.372)

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


    navigator.info('Want to start docked.  Checking...')
    # Start on dock
    if not navigator.getDockedStatus():
         navigator.info('Error: Use set_initial_pose_docked only when docked')
    else:

        # Set initial pose as docked
        # initial_pose = navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
        initial_pose = navigator.getPoseStamped([0.022, -0.372], TurtleBot4Directions.NORTH)
        navigator.info('Setting Initial Pose to dock position facing positive X')
        navigator.setInitialPose(initial_pose)


    navigator.info('Exiting set_initial_pose_docked.py')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
