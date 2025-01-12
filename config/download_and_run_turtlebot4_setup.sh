#!/bin/bash

# REF: https://github.com/turtlebot/turtlebot4_setup/tree/jazzy
# Script will install ROS 2 Jazzy Base and Turtlebot4 software

wget -qO - https://raw.githubusercontent.com/turtlebot/turtlebot4_setup/jazzy/scripts/turtlebot4_setup.sh | bash

#
echo -e "Be sure to add RTC and USB Current mods to /boot/firmware/config.txt now"
echo -e "Add ipv6.disable=1 to /boot/firmware/cmdline.txt now"
echo -e "Check /etc/netplan/50-cloud-init.yaml for WiFi setup"
echo -e "then reboot"
echo -e "then run: turtlebot4-setup"
