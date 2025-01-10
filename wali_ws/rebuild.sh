#/bin/bash

echo -e "\n** SOURCE .bashrc"
. ~/.bashrc

echo -e "** CHANGE to ~/TB5-WaLI/wali_ws"
cd ~/TB5-WaLI/wali_ws

echo -e "** CHECK ROS DEPENDENCIES **"
rosdep install -i --from-path src

echo -e "** COLCON BUILD w/SYMLINK-INSTALL"
colcon build --symlink-install

echo -e "** SOURCE BUILT SETUP.BASH"
. install/setup.bash
