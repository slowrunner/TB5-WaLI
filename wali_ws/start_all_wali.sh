#!/bin/bash

echo -e "START_ALL_WALI.SH EXECUTING"

if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
    echo -e "sourced /opt/ros/jazzy setup.bash"
fi

if [ -f /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash ]; then
    source /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash
    echo -e "sourced wali_ws install setup.bash"
fi


echo -e "\n*** Start odometer node"
echo '*** ros2 run wali odometer & '
ros2 run wali odometer &

echo -e "\nsleep 5 for odometer node startup"
sleep 5

echo -e "\n*** Start wali.say_node"
echo '*** ros2 run wali say_node &'
ros2 run wali say_node &

echo -e "\n *** STARTING WALI "
echo -e "executing: ros2 run wali wali_node &"
ros2 run wali wali_node &

echo -e "Done Start_All_WaLI.sh \n"
