#!/bin/bash

echo -e "nohup_wali.sh started"

if [ -f /opt/ros/jazzy/setup.bash ]; then
    . /opt/ros/jazzy/setup.bash
    echo -e "sourced /opt/ros/jazzy setup.bash"
fi

if [ -f /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash ]; then
    . /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash
    echo -e "sourced wali_ws install setup.bash"
fi

export ROS_DOMAIN_ID=5

echo -e "\n*** Start odometer node"
echo '*** ros2 run wali odometer & '
nohup ros2 run wali odometer &

echo -e "\nsleep 5 for odometer node startup"
sleep 5

echo -e "\n*** Start wali.say_node"
echo '*** ros2 run wali say_node &'
nohup ros2 run wali say_node &

echo -e "\n *** STARTING WALI "
echo -e "executing: ros2 run wali wali_node &"
nohup ros2 run wali wali_node > /home/ubuntu/TB5-WaLI/logs/wali_node.log &

echo -e "Done nohup_wali.sh \n"
