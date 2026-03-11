#!/bin/bash


sudo cp modified_files/snes_slow.config.yaml /opt/ros/jazzy/share/teleop_twist_joy/config/
sudo cp modified_files/F710.config.yaml /opt/ros/jazzy/share/teleop_twist_joy/config/
echo -e "snes_slow.config.yaml and F710.config.yaml copied to /opt/ros/jazzy/share/teleop_twist_joy/config/"
