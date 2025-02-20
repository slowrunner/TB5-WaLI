#!/bin/bash



echo -e "Launch TB4 Navigation Localization (On map from TB4 Async SLAM)"
echo -e "ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.yaml"
ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.yaml

# echo -e "ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/floorplan.map.yaml"
# ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/floorplan.map.yaml
