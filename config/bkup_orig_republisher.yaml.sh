#!/bin/bash

# Note the create3_republisher is in /opt/ros/jazzy but is started with the param file in robot_fork/turtlebot4_bringup

echo -e "cp ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/republisher.yaml ~/TB5-WaLI/config/orig_files/republisher.yaml"
cp ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/republisher.yaml ~/TB5-WaLI/config/orig_files/republisher.yaml
