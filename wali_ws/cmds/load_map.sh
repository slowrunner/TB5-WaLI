#!/bin/bash


# call map_server /load_map service
echo -e "Calling map_server /load_map service with map.yaml"
ros2 service call /map_server/load_map nav2_msgs/srv/LoadMap "{map_url: /home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.map.yaml}"

