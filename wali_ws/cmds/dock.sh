#!/bin/bash

echo -e "\n** DOCK **"
echo -e '** ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"'
ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'Manual Docking: success (assumed)'

/home/ubuntu/TB5-WaLI/wali_ws/cmds/reset_pose.sh


