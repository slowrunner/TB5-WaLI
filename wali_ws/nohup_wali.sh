#!/bin/bash

logfile="/home/ubuntu/TB5-WaLI/logs/nohup_wali.log"

sudo rm $logfile

echo -e "nohup_wali.sh started" > $logfile
echo -e "$(uptime)" >> $logfile
echo -e "user: $(whoami)" >> $logfile

export FASTRTPS_DEFAULT_PROFILES_FILE="/etc/turtlebot4/fastdds_rpi.xml"
export ROBOT_NAMESPACE=""
export ROS_DOMAIN_ID="5"
export ROS_DISCOVERY_SERVER="127.0.0.1:11811;"
export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"
export TURTLEBOT4_DIAGNOSTICS="1"
export WORKSPACE_SETUP="/home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash"
[ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False
export ROBOT_SETUP=/etc/turtlebot4/setup.bash

source $WORKSPACE_SETUP


echo -e "source /opt/ros/jazzy/setup.bash" >> $logfile
source /opt/ros/jazzy/setup.bash
echo -e "source /home/ubuntu/TB5-WaLI/wali_ws/setup.bash" >> $logfile
source /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash

# export ROBOT_SETUP=/etc/turtlebot4/setup.bash
# source $ROBOT_SETUP
# echo -e "sourced /etc/turtlebot4/setup.bash" >> $logfile

echo -e "\n*** Start odometer node" >> $logfile
echo -e '*** ros2 run wali odometer & ' >> $logfile
nohup ros2 run wali odometer >> $logfile &

echo -e "\nsleep 5 for odometer node startup" >> $logfile
sleep 5

echo -e "\n*** Start wali.say_node" >> $logfile
echo -e '*** ros2 run wali say_node &' >> $logfile
nohup ros2 run wali say_node >> $logfile &

echo -e "\n *** STARTING WALI NODE" >> $logfile
echo -e "executing: ros2 run wali wali_node &" >> $logfile
nohup ros2 run wali wali_node >> $logfile &

sudo chmod 666 $logfile

echo -e "Done nohup_wali.sh \n" >> $logfile
