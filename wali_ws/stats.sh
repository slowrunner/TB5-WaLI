#!/bin/bash

~/TB5-WaLI/utils/totallife.sh
echo -e "\nLast Dock and UnDock:"
tail ~/TB5-WaLI/logs/life.log | grep -E 'Docking: success | Undocking: success'
batt=$(    ros2 topic echo --once --field percentage /battery_state)
batt="${batt:0:4}"
echo "Battery: $batt"
