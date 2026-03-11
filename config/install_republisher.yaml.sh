#!/bin/bash

# Note the create3_republisher is in /opt/ros/jazzy but is started with the param file in robot_fork/turtlebot4_bringup

# echo -e "sudo cp ~/TB5-WaLI/config/modified_files/republisher.yaml /opt/ros/jazzy/share/turtlebot4_bringup/config/republisher.yaml"
# sudo cp ~/TB5-WaLI/config/republisher.yaml /opt/ros/jazzy/share/turtlebot4_bringup/config/republisher.yaml
echo -e "cp ~/TB5-WaLI/config/modified_files/republisher.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/"
cp ~/TB5-WaLI/config/modified_files/republisher.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/
