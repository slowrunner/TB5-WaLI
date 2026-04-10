# Costmap_Filter Keep Out Zones


Need:  Nav2 will plan shortest path from current position to goal,  
       which may be through the living room, which is undesirable:  
       - Living Room has a rug - TB5-WaLI leaves marks on the rugs  
       - Living Room is congested causing navigation failures  

Solution:
1) Create keepout map (pgm yaml) from localization map  
   - maps/tb5wali_current.keepout.yaml  
     with full path to image:  
     /home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.keepout.pgm

<img src="https://github.com/slowrunner/TB5-WaLI/blob/main/wali_ws/maps/tb5wali_current.keepout.jpg" />

2) Create costmap_filter_info params file:
   - params/costmap_filter_keepout_params.yaml  
     with full path to keepout map in filter_mask_server.yaml_filename  
     "/home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.keepout.yaml"  

3) Create wali/launch/costmap_filter_info.launch.py  
   - with lifecycle manager that launches only  
     costmap_filter_info_server  and  
     filter_mask_server  
   - with filter_mask_server remapping of /map to /keepout_filter_mask  

4) To see the keepout zones in rViz2:  
   - add by topic /keepout_filter_mask  
     changed Alpha from 0.7 default to 0.4  

5) Launch 
   - cmds/launch_localization.sh  
```
#!/bin/bash


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_localization.sh executing'
echo -e "Launch TB4 Navigation Localization (On map from TB4 Async SLAM with default params)"
echo -e "ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb4_nav_async_w_chrony.map.
yaml"
ros2 launch turtlebot4_navigation localization.launch.py \
  map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.map.yaml 
```
   - cmds/launch_test_costmap_filter.sh  
```
#!/bin/bash

/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_test_costmap_filter.sh executing'

ros2 launch wali costmap_filter_info.launch.py \
   keepout_map:=/home/ubuntu/TB5-WaLI/wali_ws/maps/tb5wali_current.keepout.yaml \
   keepout_params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/costmap_fileter_keepout_params.yaml
```

   - cmds/launch_test_nav2.sh
```
#!/bin/bash


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'launch_test_nav2.sh executing'
echo -e "Launch TB4 Navigation Nav2 with test.nav2.yaml"
echo -e "ros2 launch turtlebot4_navigation nav2.launch.py params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.nav2.yaml"
ros2 launch turtlebot4_navigation nav2.launch.py \
  params_file:=/home/ubuntu/TB5-WaLI/wali_ws/params/test.nav2.yaml 
```

<img src="https://github.com/slowrunner/TB5-WaLI/blob/main/graphics/Costmap_Filter_Info_rViz2.jpg" height="630" />
