#!/bin/bash

# ros2 run rclcpp_components component_container --ros-args -r __node:=nav2_container
ros2 run rclcpp_components component_container --ros-args --params-file ~/TB5-WaLI/wali_ws/params/wali.nav2.yaml  -r __node:=nav2_container
