#!/bin/bash

if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
    echo -e "sourced /opt/ros/jazzy setup.bash"
fi

if [ -f ~/TB5-WaLI/wali_ws/install/setup.bash ]; then
    source ~/TB5-WaLI/wali_ws/install/setup.bash
    echo -e "sourced wali_ws install setup.bash"
fi

if [ -f ~/TB5-WaLI/dai_ws/install/setup.bash ]; then
    source ~/TB5-WaLI/dai_ws/install/setup.bash
    echo -e "sourced dai_ws install setup.bash"
fi

export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
# export FASTRTPS_DEFAULT_PROFILES_FILE=/home/pi/wali_pi5/configs/super_client_configuration_file.xml
export ROS_DISCOVERY_SERVER=127.0.0.1:11811

# Set to only communicate via the republisher
# export FASTRTPS_DEFAULT_PROFILES_FILE=~/wali_pi5/configs/fastdds-passive-unicast.xml
# ros2 daemon stop

# ros2 topic list
# ros2 topic list