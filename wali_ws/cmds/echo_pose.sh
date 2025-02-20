#/bin/bash

echo -e "\n*** ECHO ODOM"
echo -e "ros2 topic echo --once --flow-style /amcl_pose"
ros2 topic echo --once --flow-style -l 1  /amcl_pose



