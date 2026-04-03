#!/bin/bash


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_tb4_nav_nav2.sh executing'
echo -e "Launch TB4 Navigation Nav2"
echo -e "ros2 launch turtlebot4_navigation nav2.launch.py"
ros2 launch turtlebot4_navigation nav2.launch.py \
  params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/wali.nav2.yaml \
  use_sim_time:=false \
  bond_timeout:=10.0
# ros2 launch turtlebot4_navigation nav2.launch.py
