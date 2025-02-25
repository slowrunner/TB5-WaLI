#!/bin/bash

ps -e -o %cpu,%mem,cmd | grep  'CPU\|MEM\|CMD\|rplidar\|robot\|joint\|oak\|nav\|slam\|turtlebot4\|wali' | grep -v "grep" | sort -rk 1 
