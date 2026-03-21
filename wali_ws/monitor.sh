#!/bin/bash


while true; \
do echo -e "Collecting ROS Info"; \

# Check Battery Percentage
batt=$(ros2 topic echo --once --field percentage --qos-reliability best_effort --qos-durability volatile /battery_state)
batt="${batt:0:4}"

# Checking Docking State
docked=$(ros2 topic echo --once --field is_docked --qos-reliability best_effort --qos-durability volatile /dock_status)

curr=$(ros2 topic echo --once --field current --qos-reliability best_effort --qos-durability volatile /battery_state); \
curr="${curr:0:5}"; \
# echo "Current: $curr"; \

volt=$(ros2 topic echo --once --field voltage --qos-reliability best_effort --qos-durability volatile /battery_state); \
volt="${volt:0:5}"; \
watts=`(echo "scale=1; ($volt * $curr)" | bc -l)`; \
watts="${watts:0:5}"; \

echo -e "\n********** TB5-WaLI MONITOR ******************************"; \

echo -n `date +"%A %D"`; \
echo ""; \
uptime; \
vcgencmd measure_temp && vcgencmd measure_clock arm && vcgencmd get_throttled; \

load=`cat /proc/loadavg` ; \
load="${load%% *}"; \
cpu=`(echo " ($load / 4.0 * 100)" | bc -l)`; \
cpu="${cpu:0:3}"; \
echo -e "$d 1m load: $load  $cpu% demand on RPi 5's four cores"; \

read -a arr <<< "$(vmstat 1 2 | tail -n 1)"; \
# declare -p arr
idle_index=14; \
idle=${arr[idle_index]}; \
cpu=$(bc <<< "100 - $idle"); \
echo -e "$d total cpu usage: $cpu% of RPi 5 CPU"; \
echo " "; \


free -h; \
echo ""; \
echo "Voltage: $volt  Current: $curr  Watts: $watts"; \
echo "Battery: $batt  Docked: $docked"; \


# ps -e -o %cpu,%mem,cmd | grep  'CPU\|MEM\|CMD\|rplidar\|robot\|joint\|oak\|nav\|slam\|turtlebot4\|wali' | grep -v "grep" | sort -rk 1 ; \
# sleep 5; \
echo " "; \
done
