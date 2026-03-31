#!/usr/bin/env python3

# FILE:  wali_tour.py

# Assumes: Undocked pose, initial_pose set

# Visits:  Directions are IntEnum from WaLI_Dir class - e.g. WaLI_Dir.SOUTH
#  1) front door:  ( 3.39 ,  3.99, "SOUTH"     )
#  2) Laundry:     ( 2.7 , -1.4,   "SOUTH"     )
#  3) Dining:      (-2.6  , -0.5 , "EAST"      )
#  4) kitchen:     ( 3.71 ,  1.04, "NORTH_WEST")
#  5) office:      (-4.56 , -0.01, "NORTH_WEST")
#  6) Ready:  :    (-0.03 , -0.37, "NORTH"     )
#
#  Note: undocked: (-0.010 , -0.372, "NORTH"   )

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


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    front_door = navigator.getPoseStamped([3.39, 3.99],    WaLI_Dir.SOUTH)      # TurtleBot4Directions.NORTH)
    laundry    = navigator.getPoseStamped([4.2, -1.47],    WaLI_Dir.NORTH)      # TurtleBot4Directions.SOUTH)
    dining     = navigator.getPoseStamped([-2.6, -0.5],    WaLI_Dir.EAST)       # TurtleBot4Directions.WEST)
    kitchen    = navigator.getPoseStamped([3.71, 1.04],    WaLI_Dir.NORTH_WEST) # TurtleBot4Directions.SOUTH_EAST)
    office     = navigator.getPoseStamped([-4.56, -0.01],  WaLI_Dir.NORTH_WEST) # TurtleBot4Directions.SOUTH_EAST)
    ready      = navigator.getPoseStamped([-0.030, -0.372],WaLI_Dir.NORTH)      # TurtleBot4Directions.SOUTH)



    navigator.info('Want to set initial pose docked.  Checking to see if docked ...')
    # Start on dock
    if not navigator.getDockedStatus():
         navigator.info('No, so docking ...')
         navigator.dock()
         sleep(20)
    

    # Set initial pose as docked
    docked = navigator.getPoseStamped([0.022, -0.372], WaLI_Dir.SOUTH)   # TurtleBot4Directions.NORTH)
    navigator.info('Setting Initial Pose to docked position facing WaLI_Dir.SOUTH - positive X')
    navigator.setInitialPose(docked)    # Start off dock
    sleep(20)
    navigator.setInitialPose(docked)    # Start off dock
    sleep(20)
    navigator.undock()
    sleep(20)

    # Wait for Nav2
    navigator.waitUntilNav2Active()

    # Set goal poses
    # goal_pose = []
    # goal_pose.append(front_door)
    # goal_pose.append(laundry)
    # goal_pose.append(dining)
    # goal_pose.append(kitchen)
    # goal_pose.append(office)
    # goal_pose.append(ready)

    # Follow Waypoints
    # navigator.startFollowWaypoints(goal_pose)
    navigator.info("nav to see front door")
    navigator.startToPose(front_door)
    sleep(30)

    navigator.info("nav to laundry")
    navigator.startToPose(laundry)
    sleep(30)

    navigator.info("nav to dining")
    navigator.startToPose(dining)
    sleep(30)

    navigator.info("nav to kitchen")
    navigator.startToPose(kitchen)
    sleep(30)

    navigator.info("nav to office")
    navigator.startToPose(office)
    sleep(30)

    navigator.info("nav to ready")
    navigator.startToPose(ready)
    sleep(30)
 
    navigator.info("Done Wali Tour")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
