#!/usr/bin/env python3

# FILE: nav_to_ready.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#
# Navigate  to undocked and ready to navigate position)
# - Ready ([-0.254, -0.317], WaLI_Dir.NORTH_EAST)

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
from enum import IntEnum

# from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Navigator

class WaLI_Dir(IntEnum):
    # WaLI_Dir          TurtleBot4Directions
    SOUTH = 0         # NORTH
    SOUTH_WEST = 315  # NORTH_EAST
    WEST = 270        # EAST
    NORTH_EAST = 135  # SOUTH_WSST
    NORTH = 180       # SOUTH
    NORTH_WEST = 225  # SOUTH_EAST
    EAST = 90         # WEST
    SOUTH_EAST = 45   # NORTH_WEST


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    # Set goal poses
    # - Undocked ([-0.0104, -0.372], TurtleBot4Directions.SOUTH)
    # - Ready ([-0.254, -0.317], WaLI_Dir.NORTH_EAST)

    goal_pose = navigator.getPoseStamped([-0.254, -0.317], WaLI_Dir.NORTH_EAST)    # WaLI undocked plus 0.2 facing NE

    # Go to each goal pose
    navigator.info('Starting to ready to nav position')
    navigator.startToPose(goal_pose)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
