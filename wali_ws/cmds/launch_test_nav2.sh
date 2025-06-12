#!/bin/bash



echo -e "Launch TB4 Navigation Nav2"
echo -e "ros2 launch turtlebot4_navigation nav2.launch.py"
# ros2 launch turtlebot4_navigation nav2.launch.py params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.nav2.yaml  use_composition:=true
ros2 launch turtlebot4_navigation nav2.launch.py
