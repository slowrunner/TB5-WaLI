#!/bin/bash

# echo -e "Current: ros2 param get turtlebot4_node power_saver"
# ros2 param get turtlebot4_node power_saver

# not dynamic - must be set in turtlebot4_bringup/config/turtlebot4.yaml
# echo -e "ros2 param set turtlebot4_node power_saver false"
# ros2 param set turtlebot4_node power_saver false

echo -e "turtlebot4_bringup/config/turtlebot4.yaml turtlebot4_node power_saver param:"
echo -e "   ros2 param get turtlebot4_node power_saver"
ros2 param get turtlebot4_node power_saver

