#!/usr/bin/env python3

# FILE: nav_to_kitchen.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#
# Navigate from docked to kitchen  
# - Docked per map (0.022, -0.372)
# - Center of Kitchen per map (3.550, 0.968)

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

from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    # Start on dock
    if not navigator.getDockedStatus():
        navigator.info('Docking before intialising pose')
        navigator.dock()

    # Set initial pose
    # initial_pose = navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
    initial_pose = navigator.getPoseStamped([0.022, -0.372], TurtleBot4Directions.NORTH)
    navigator.setInitialPose(initial_pose)

    # Wait for Nav2
    navigator.waitUntilNav2Active()

    # Set goal poses
    # goal_pose = navigator.getPoseStamped([-13.0, 9.0], TurtleBot4Directions.EAST)
    goal_pose = navigator.getPoseStamped([3.550, 0.968], TurtleBot4Directions.EAST)

    # Undock
    navigator.undock()

    # Go to each goal pose
    navigator.startToPose(goal_pose)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
