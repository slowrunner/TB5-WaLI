#!/bin/bash


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_localization.sh executing'
echo -e "Launch TB4 Navigation Localization (On map from TB4 Async SLAM with default params)"
echo -e "ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.yaml"
ros2 launch turtlebot4_navigation localization.launch.py \
  map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.map.yaml 
