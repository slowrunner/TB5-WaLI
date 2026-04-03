#!/bin/bash


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_test_localization.sh executing'
echo -e "Launch TB4 Navigation Localization (On map from TB4 Async SLAM with params/test.localization.yaml)"
ros2 launch turtlebot4_navigation localization.launch.py \
  map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.yaml \
  params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.localization.yaml
# echo -e "ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/floorplan.map.yaml"
# ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/floorplan.map.yaml
