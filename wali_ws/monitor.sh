#!/bin/bash


while true; \
do echo -e "\n********** TB5-WaLI MONITOR ******************************"; \
echo -n `date +"%A %D"`; \
echo ""; \
uptime; \
vcgencmd measure_temp && vcgencmd measure_clock arm && vcgencmd get_throttled; \
free -h; \
echo ""; \

curr=$(ros2 topic echo --once --field current --qos-reliability best_effort --qos-durability volatile /battery_state); \
curr="${curr:0:5}"; \
# echo "Current: $curr"; \

volt=$(ros2 topic echo --once --field voltage --qos-reliability best_effort --qos-durability volatile /battery_state); \
volt="${volt:0:5}"; \
echo "Voltage: $volt  Current: $curr"; \


# ps -e -o %cpu,%mem,cmd | grep  'CPU\|MEM\|CMD\|rplidar\|robot\|joint\|oak\|nav\|slam\|turtlebot4\|wali' | grep -v "grep" | sort -rk 1 ; \
# sleep 5; \
echo " "; \
done
