#!/bin/bash

/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'pub_drive_turn_ready.sh executing'
echo -e "\n*** Pub Drive Turn Ready"
echo -e "*** Driving 20cm forward"
ros2 action send_goal /drive_distance irobot_create_msgs/action/DriveDistance "{distance: 0.2, max_translation_speed: 0.10}"


echo -e "\n*** Turning 45 right"
echo -e 'ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: -0.7854 ,max_rotation_speed: 0.5}"'
ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: -0.7854, max_rotation_speed: 0.5}"
echo -e "*** DONE ***\n"
