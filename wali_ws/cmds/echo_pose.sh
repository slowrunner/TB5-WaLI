#/bin/bash

echo -e "\n*** ECHO /amcl_pose ROS Heading +/-180 (from docked 0 set by cmds/set_pose_docked.sh)"
# echo -e "ros2 topic echo --once --flow-style /amcl_pose"
# ros2 topic echo --once --flow-style -l 1  /amcl_pose
# echo " "
echo -e "ros2 run wali echo_pose"
ros2 run wali echo_pose

