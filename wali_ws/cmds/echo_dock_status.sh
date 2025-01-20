#!/bin/bash

echo -e "\n*** ECHO DOCK STATUS"
echo -e "ros2 topic echo --once /dock_status"
ros2 topic echo --once --qos-reliability best_effort --qos-durability volatile /dock_status 
