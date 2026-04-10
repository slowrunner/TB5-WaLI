#!/bin/bash

/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_test_costmap_filter.sh executing'

ros2 launch wali costmap_filter_info.launch.py \
   keepout_map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.keepout.yaml \
   keepout_params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/costmap_fileter_keepout_params.yaml
