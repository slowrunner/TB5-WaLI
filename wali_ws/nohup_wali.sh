#!/bin/bash

echo -e "nohup_wali.sh started" > /home/ubuntu/TB5-WaLI/logs/wali_node.log

export ROBOT_SETUP=/etc/turtlebot4/setup.bash
source $ROBOT_SETUP
echo -e "sourced /etc/turtlebot4/setup.bash" > /home/ubuntu/TB5-WaLI/logs/wali_node.log

echo -e "\n*** Start odometer node" > /home/ubuntu/TB5-WaLI/logs/wali_node.log
echo '*** ros2 run wali odometer & '
nohup ros2 run wali odometer > /home/ubuntu/TB5-WaLI/logs/wali_node.log &

echo -e "\nsleep 5 for odometer node startup"
sleep 5

echo -e "\n*** Start wali.say_node" > /home/ubuntu/TB5-WaLI/logs/wali_node.log
echo '*** ros2 run wali say_node &'
nohup ros2 run wali say_node > /home/ubuntu/TB5-WaLI/logs/wali_node.log &

echo -e "\n *** STARTING WALI NODE" > /home/ubuntu/TB5-WaLI/logs/wali_node.log
echo -e "executing: ros2 run wali wali_node &"
nohup ros2 run wali wali_node > /home/ubuntu/TB5-WaLI/logs/wali_node.log &

echo -e "Done nohup_wali.sh \n" > /home/ubuntu/TB5-WaLI/logs/wali_node.log
