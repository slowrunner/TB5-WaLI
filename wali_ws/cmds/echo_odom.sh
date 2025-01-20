#/bin/bash

echo -e "\n*** ECHO ODOM"
echo -e "ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom"
ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile  /odom



