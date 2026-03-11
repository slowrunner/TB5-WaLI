#!/bin/bash

echo "diff snes_slow.config.yaml and F710.config.yaml"
diff modified_files/snes_slow.config.yaml /opt/ros/jazzy/share/teleop_twist_joy/config/snes_slow.config.yaml

diff modified_files/F710.config.yaml /opt/ros/jazzy/share/teleop_twist_joy/config/F710.config.yaml

echo "diff republisher.yaml (in turtlebot4_fork/turtlebot4_bringup)"
diff ~/TB5-WaLI/config/modified_files/republisher.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/republisher.yaml

echo "diff rplidar.launch.py (in turtlebot4_robot_fork/turtlebot4_bringup)"
diff ~/TB5-WaLI/config/modified_files/rplidar.launch.py ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/launch/rplidar.launch.py

# echo "diff /opt/ros/jazzy turtlebot4.urdf.xacro with WaLI changes"
# diff ~/TB5-WaLI/config/modified_files/turtlebot4.urdf.xacro /opt/ros/jazzy/share/turtlebot4_description/urdf/lite/turtlebot4.urdf.xacro

echo "diff turtlebot4_fork turtlebot4.urdf.xacro with WaLI changes"
diff ~/TB5-WaLI/config/modified_files/turtlebot4.urdf.xacro ~/TB5-WaLI/wali_ws/src/turtlebot4_fork_for_TB5-WaLI/turtlebot4_description/urdf/lite/turtlebot4.urdf.xacro

# echo "diff nav2.yaml in turtlebot4_fork / turtlebot4_navigation"
# diff ~/TB5-WaLI/config/modified_files/nav2.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_fork_for_TB5-WaLI/turtlebot4_navigation/config/nav2.yaml

echo "diff nav2.yaml in wali_ws/params/wali.nav2.yaml"
diff ~/TB5-WaLI/config/modified_files/nav2.yaml ~/TB5-WaLI/wali_ws/params/wali.nav2.yaml

echo "diff localization.yaml in turtlebot4_fork / turtlebot4_navigation"
diff  ~/TB5-WaLI/config/modified_files/localization.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_fork_for_TB5-WaLI/turtlebot4_navigation/config/localization.yaml

echo "diff turtlebot4.yaml in turtlebot4_robot_fork / turtlebot4_bringup"
diff ~/TB5-WaLI/config/modified_files/turtlebot4.yaml ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/turtlebot4.yaml


