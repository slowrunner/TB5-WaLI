#!/bin/bash



echo -e "Launch TB4 Async SLAM"
echo -e "ros2 launch turtlebot4_navigation slam.launch.py sync:=false params:=/home/ubuntu/TB5-WaLI/wali_ws/params/tb4_slam.yaml"
ros2 launch turtlebot4_navigation slam.launch.py sync:=false params:=/home/ubuntu/TB5-WaLI/wali_ws/params/tb4_slam.yaml
