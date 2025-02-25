#!/bin/bash

echo -e "\n*** Calling C1 LIDAR's /stop_motor service"
echo -e "ros2 service call /stop_motor std_srvs/Empty"
ros2 service call /stop_motor std_srvs/Empty
