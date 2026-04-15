#/bin/bash

#
echo -e "\n*** ECHO Create3 ODOM +/- 180 from 0 docked (set to 0 by cmds/reset_create3_odom.sh)"
# echo -e "ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom"
# ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile  /odom
echo -e "ros2 run wali echo_odom"
ros2 run wali echo_odom



