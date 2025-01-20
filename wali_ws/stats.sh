#!/bin/bash

~/TB5-WaLI/utils/totallife.sh
echo -e "\nLast Dock and UnDock:"
tail ~/TB5-WaLI/logs/life.log | grep -E 'Docking: success | Undocking: success'

echo -e "\nChecking Battery State"
batt=$(ros2 topic echo --once --field percentage --qos-reliability best_effort --qos-durability volatile /battery_state)
batt="${batt:0:4}"
echo "Battery: $batt"

echo -e "\nChecking Docking State"
docked=$(ros2 topic echo --once --field is_docked --qos-reliability best_effort --qos-durability volatile /dock_status)
echo -e "Docked: $docked"
