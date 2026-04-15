#!/bin/bash

echo -e "\n*** PUB 45"
echo -e 'ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: 0.775,max_rotation_speed: 0.5}"'
ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: 0.775,max_rotation_speed: 0.5}"

