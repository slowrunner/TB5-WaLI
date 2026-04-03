#!/bin/bash
/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'nav_wali_tour.sh executing'
echo -e "ros2 run wali wali_tour"
uptime
ros2 run wali wali_tour
uptime
