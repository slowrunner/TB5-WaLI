#!/usr/bin/env python3

# FILE: nav_to_laundry.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#
# Navigate to laundry  
# - Laundry room facing kitchenette per map (4.89, -1.59,SOUTH))

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

from time import sleep
from enum import IntEnum

# from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Navigator

class WaLI_Dir(IntEnum):
    SOUTH = 0         # NORTH
    SOUTH_WEST = 315  # NORTH_EAST
    WEST = 270        # EAST
    NORTH_EAST = 135  # SOUTH_WSST
    NORTH = 180       # SOUTH
    NORTH_WEST = 225  # SOUTH_EAST
    EAST = 90         # WEST
    SOUTTH_EAST = 45  # NORTH_WEST



#  1) front door:  ( 3.39 ,  3.99, "NORTH"     )
#  2) Laundry:     ( 2.7 , -1.47,  "SOUTH"     )
#  3) Dining:      (-2.6  , -0.5 , "WEST"      )
#  4) kitchen:     ( 3.71 ,  1.04, "SOUTH_EAST")
#  5) office:      (-4.56 , -0.01, "SOUTH_EAST")
#  6) Ready:  :    (-0.03 , -0.37, "SOUTH"     )
#
#  Note: undocked: (-0.010 , -0.372, "SOUTH"   )




def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    # navigator.info('Waiting For Nav2 Active')
    # navigator.waitUntilNav2Active()

    # Set goal poses
    goal_pose = navigator.getPoseStamped([2.7, -1.47], WaLI_Dir.SOUTH)

    # Go to each goal pose
    navigator.info('Start navigation to goal')
    navigator.startToPose(goal_pose)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
