#!/bin/bash


while true; \
do echo -e "\n********** TB5-WaLI MONITOR ******************************"; \
echo -n `date +"%A %D"`; \
echo ""; \
uptime; \
vcgencmd measure_temp && vcgencmd measure_clock arm && vcgencmd get_throttled; \
free -h; \
echo ""; \


ps -e -o %cpu,%mem,cmd | grep  'CPU\|MEM\|CMD\|rplidar\|robot\|joint\|oak\|nav\|slam\|turtlebot4\|wali' | grep -v "grep" | sort -rk 1 ; \
sleep 5; \
echo " "; \
done
