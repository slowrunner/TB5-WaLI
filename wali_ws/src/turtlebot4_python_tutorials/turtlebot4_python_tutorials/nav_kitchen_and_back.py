
# FILE: nav_to_kitchen.py
#
# @author slowrunner (slowrunner@noreply.github.com)
#
# Navigate from docked to kitchen  
# - Docked per map (0.022, -0.372)
# - Center of Kitchen per map (3.550, 0.968)
# - Breakfast Area Waiting Spot (1.0,-0.23) NORTH
# - Breakfast Area Waiting Spot (0.5,-0.23) NORTH
# - Ready To Dock / undocked position (-0.116, -0.275) SOUTH


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


    # Set goal poses
    # goal_pose = navigator.getPoseStamped([-13.0, 9.0], TurtleBot4Directions.EAST)
    kitchen_pose = navigator.getPoseStamped([3.550, 0.968], TurtleBot4Directions.SOUTH_EAST)


    # - Breakfast Area Waiting Spot (0.5,-0.23) NORTH
    breakfast_wait_pose = navigator.getPoseStamped([0.5, -0.23], TurtleBot4Directions.NORTH)  # WaLI undock/docking ready

    # undocked 
    undocked_pose = navigator.getPoseStamped([-0.104, -0.472], TurtleBot4Directions.SOUTH)  # WaLI undock/docking ready

    # Looking at dock position
    looking_at_dock_pose = navigator.getPoseStamped([-0.104, -0.472], TurtleBot4Directions.NORTH)  



    # Go to breakfast wait area
    navigator.info('Start journey to breakfast wait area')
    navigator.startToPose(breakfast_wait_pose)

    # Wait for Breakfast for a minute
    navigator.info('Waiting for breakfast for 30s')
    time.sleep(30)

    # Go to kitchen
    navigator.info('Continue to kitchen')
    navigator.startToPose(kitchen_pose)

    # Sit in kitchen for a minute
    navigator.info('Rest in kitchen for 30s')
    time.sleep(30)

    # Go back facing dock
    navigator.info('Start return to looking at dock pose')
    navigator.startToPose(looking_at_dock_pose)
    time.sleep(30)

    # Turn to undocked pose
    navigator.info('Turn around to undocked pose')
    navigator.startToPose(undocked_pose)
    time.sleep(30)

    navigator.info('Journey Complete, Exiting')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
