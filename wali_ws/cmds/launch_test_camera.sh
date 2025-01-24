#!/bin/bash

dt=`(uptime)`
echo -e "\n ${dt}"
echo -e "LAUNCHING OAK-D-LITE camera.launch.py WITH params/test.yaml (mod of oakd_lite.yaml)"
echo -e "ros2 launch depthai_ros_driver camera.launch.py camera_model:=OAK-D-LITE params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.yaml\n"
ros2 launch depthai_ros_driver camera.launch.py camera_model:=OAK-D-LITE params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.yaml
dt=`(uptime)`
echo -e "${dt}\n"
