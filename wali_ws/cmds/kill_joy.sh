#!/bin/bash

basedir=TB5-WaLI
echo -e "\n*** Switching to ~/${basedir}/wali_ws"
cd ~/$basedir/wali_ws

echo -e "\n*** Sourcing /opt/ros/jazzy/setup.bash"
. /opt/ros/jazzy/setup.bash

echo -e "\n*** Sourcing install/setup.bash"
. ~/$basedir/wali_ws/install/setup.bash

trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

echo -e "\n*** STARTING kill_joy.sh ***"
killall joy_node
killall teleop_node
echo -e  "\n*** DONE KILLING JOY ***\n"
