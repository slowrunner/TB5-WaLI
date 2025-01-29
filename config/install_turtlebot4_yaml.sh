#!/bin/bash

echo -e "sudo cp ~/TB5-WaLI/config/turtlebot4.urdf.xacro /opt/ros/jazzy/share/turtlebot4_description/urdf/lite/"
# sudo cp ~/TB5-WaLI/config/turtlebot4.yaml /opt/ros/jazzy/share/turtlebot4_bringup/config/turtlebot4.yaml
cp ~/TB5-WaLI/config/turtlebot4.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_fork_for_TB5-WaLI/turtlebot4_bringup/config/
