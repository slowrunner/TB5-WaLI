#!/usr/bin/env python3

# FILE:  wali_tour.py

# Assumes: Ready pose, Localization running with initial pose was set

# Wait at waypoints is set in test.nav2.yaml
# waypoint_follower:
#    wait_at_waypoint:
#       waypoint_pause_duration: 10000 # ms  was 200

# Visits:  Directions are IntEnum from WaLI_Dir class - e.g. WaLI_Dir.SOUTH

#  1)  front door:  ( 3.39  ,  3.99 , "SOUTH"     )
#  2)  couch view:  ( 0.5   ,  2.7  , "NORTH_WEST")
#  3)  Laundry:     ( 2.7   , -1.47 , "SOUTH"     )
#  4)  table:       ( 0.97  , -0.7  , "SOUTH_EAST")
#  5)  kitchen:     ( 3.71  ,  1.04 , "NORTH_WEST")
#  6)  Dining:      (-2.6   , -0.5  , "SOUTH_EAST")
#  7)  patio view:  (-3.4   ,  2.1  , "NORTH_EAST")
#  8)  office:      (-4.56  , -0.01 , "NORTH_WEST")
#  9)  hall view :  ( 2.1   ,  4.0  , "NORTH_EAST")
#  10) Ready:       (-0.208 , -0.317, "NORTH_EAST")   was 10) Ready:       (-0.332 , -0.333, "NORTH_EAST")
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

class WaLI_Dir(IntEnum):  # TurtleBot4Directions
    SOUTH = 0             # NORTH
    SOUTH_WEST = 315      # NORTH_EAST
    WEST = 270            # EAST
    NORTH_EAST = 135      # SOUTH_WSST
    NORTH = 180           # SOUTH
    NORTH_WEST = 225      # SOUTH_EAST
    EAST = 90             # WEST
    SOUTH_EAST = 45       # NORTH_WEST


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    #  1)  front door:  ( 3.39  ,  3.99 , "SOUTH"     )
    front_door = navigator.getPoseStamped([ 3.39 ,  3.99 ],    WaLI_Dir.SOUTH)      # TurtleBot4Directions.NORTH)
    #  2)  couch view:  ( 0.5   ,  2.7  , "NORTH_WEST")
    couch_view = navigator.getPoseStamped([ 0.5  ,  2.7  ],    WaLI_Dir.NORTH)      # TurtleBot4Directions.SOUTH)
    #  3)  Laundry:     ( 2.7   , -1.47 , "SOUTH"     )
    laundry    = navigator.getPoseStamped([ 2.7  , -1.47 ],    WaLI_Dir.SOUTH)      # TurtleBot4Directions.NORTH)
    #  4)  table:       ( 0.97  , -0.7  , "SOUTH_EAST")
    table      = navigator.getPoseStamped([0.97, -0.7], WaLI_Dir.SOUTH_EAST)
    #  5)  Dining:      (-2.6   , -0.5  , "SOUTH_EAST")
    dining     = navigator.getPoseStamped([-2.6  , -0.5  ],    WaLI_Dir.SOUTH_EAST) # TurtleBot4Directions.NORTH_WEST)
    #  6)  kitchen:     ( 3.71  ,  1.04 , "NORTH_WEST")
    kitchen    = navigator.getPoseStamped([ 3.71 ,  1.04 ],    WaLI_Dir.NORTH_WEST) # TurtleBot4Directions.SOUTH_EAST)
    #  7)  patio view:  (-3.4   ,  2.1  , "NORTH_EAST")
    patio_view = navigator.getPoseStamped([-3.4  ,  2.1  ],    WaLI_Dir.NORTH_EAST) # TurtleBot4Directions.SOUTH_WEST)
    #  8)  office:      (-4.56  , -0.01 , "NORTH_WEST")
    office     = navigator.getPoseStamped([-4.56 , -0.01 ],    WaLI_Dir.NORTH_WEST) # TurtleBot4Directions.SOUTH_EAST)
    #  9)  hall view :  ( 2.1   ,  4.0  , "NORTH_EAST")
    hall_view  = navigator.getPoseStamped([ 2.1  ,  4.0  ],    WaLI_Dir.NORTH_EAST) # TurtleBot4Directions.SOUTH_WEST)
    #  was 10) Ready:       (-0.332 , -0.333, "NORTH_EAST")
    # ready      = navigator.getPoseStamped([-0.332, -0.333],    WaLI_Dir.NORTH_EAST) # TurtleBot4Directions.SOUTH_WEST)
    #  10) Ready:       (-0.208 , -0.317, "NORTH_EAST")
    ready      = navigator.getPoseStamped([-0.208, -0.317],    WaLI_Dir.NORTH_EAST) # TurtleBot4Directions.SOUTH_WEST)



    # navigator.info('Want to set initial pose docked.  Checking to see if docked ...')
    # Start on dock
    # if not navigator.getDockedStatus():
    #      navigator.info('No, so docking ...')
    #      navigator.dock()
    #      sleep(20)


    # Set initial pose as docked
    # docked = navigator.getPoseStamped([0.022, -0.372], WaLI_Dir.SOUTH)   # TurtleBot4Directions.NORTH)
    # navigator.info('Setting Initial Pose to docked position facing WaLI_Dir.SOUTH - positive X')
    # navigator.setInitialPose(docked)    # Start off dock
    # sleep(20)
    # navigator.setInitialPose(docked)    # Start off dock
    # sleep(20)
    # navigator.undock()
    # sleep(20)

    # Wait for Nav2
    # navigator.waitUntilNav2Active()



    #  1)  front door:  ( 3.39  ,  3.99 , "SOUTH"     )
    #  2)  couch view:  ( 0.5   ,  2.7  , "NORTH_WEST")
    #  3)  Laundry:     ( 2.7   , -1.47 , "SOUTH"     )
    #  4)  table:       ( 0.97  , -0.7  , "SOUTH_EAST")
    #  5)  Dining:      (-2.6   , -0.5  , "SOUTH_EAST")
    #  6)  kitchen:     ( 3.71  ,  1.04 , "NORTH_WEST")
    #  7)  patio view:  (-3.4   ,  2.1  , "NORTH_EAST")
    #  8)  office:      (-4.56  , -0.01 , "NORTH_WEST")
    #  9)  hall view :  ( 2.1   ,  4.0  , "NORTH_EAST")
    #  10) Ready:       (-0.208 , -0.317, "NORTH_EAST")


    # Set goal poses
    goal_pose = []
    goal_pose.append(front_door)
    goal_pose.append(couch_view)
    goal_pose.append(laundry)
    goal_pose.append(table)
    goal_pose.append(dining)
    goal_pose.append(kitchen)
    goal_pose.append(patio_view)
    goal_pose.append(office)
    goal_pose.append(hall_view)
    goal_pose.append(ready)

    # Follow Waypoints
    navigator.info('Begin Tour: front_door, couch_view, laundry, table, dining, kitchen, patio_view, office, hall_view, ready')

    navigator.startFollowWaypoints(goal_pose)

    navigator.info("Done Wali Tour")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
