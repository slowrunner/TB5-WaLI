#!/bin/bash


while true; \
do echo -e "\n********** TB5-WaLI MONITOR ******************************"; \
echo -n `date +"%A %D"`; \
echo ""; \
uptime; \
vcgencmd measure_temp && vcgencmd measure_clock arm && vcgencmd get_throttled; \
free -h; \
# Print stats on particular process
ps -o %cpu,%mem,cmd $(pgrep -f "/usr/bin/python3 /opt/ros/jazzy/bin/ros2 launch turtlebot4_navigation"); \
sleep 5; \
echo " "; \
done
