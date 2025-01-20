#/bin/bash

echo -e "\n*** ECHO BATTERY STATE"
echo -e "ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile /battery_state"
ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile /battery_state
echo -en "\nPercentage: "
ros2 topic echo --once --field percentage --qos-reliability best_effort --qos-durability volatile /battery_state



