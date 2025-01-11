#!/bin/bash


echo -e "\n*** Switching to ~/TB5-WaLI/wali_ws"
cd ~/TB5-WaLI/wali_ws

echo -e "\n*** Sourcing install/setup.bash"
. ~/TB5-WaLI/wali_ws/install/setup.bash

echo -e "\n*** Start odometer node"
echo '*** ros2 run wali odometer & '
ros2 run wali odometer &

