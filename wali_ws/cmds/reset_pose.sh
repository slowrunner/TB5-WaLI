#!/bin/bash

# Note: not implemented in simulator, docs say "implemented in G.3.1"

echo -e '\n** Fix Odom Drift with reset_pose 0,0/0'

echo -e '** CURRENT ODOM'
echo -e 'ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom'
ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom

# ~/TB5-WaLI/utils/logMaintenance.py 'Issued reset_pose'

echo -e '** SEND RESET_POSE'
echo -e 'ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "{}"'
ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "{}"

# To Reset To particular pose:
# echo -e 'ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "pose: {position: {x: 0, y: 0, z: 0}, orientation: {x: 0, y: 0, z: 0, w: 1}}"'
# ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "pose: {position: {x: 0, y: 0, z: 0}, orientation: {x: 0, y: 0, z: 0, w: 1}}"

echo -e '** New Odom'
echo -e 'ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom'
ros2 topic echo --once --flow-style --qos-reliability best_effort --qos-durability volatile /odom


echo -e '********\n'
