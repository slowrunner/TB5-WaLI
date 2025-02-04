# Turtlebot4 Cartographer

With another of my ROS 2 robots, I was able to create a great map of my house using turtlebot3_cartographer, where my efforts to create a map with slam_toolbox were stymied.

With TB5-WaLI I ran the turtlebot4_navigation async SLAM and created a map, and for comparison have created turtlebot4_cartographer and built a map.

With turtlebot4_cartographer:
- Processor load (total):  about 2.5 (about 63% of Pi5 CPU)
- cartographer_node:  55% of Pi5  using about 400MB memory
- Total Battery Load: 12.9W  (12.8W usual playtime w/o cartographer_node)

```
********** TB5-WaLI MONITOR ******************************
Monday 02/03/25
 23:39:53 up 3 days, 23:00,  2 users,  load average: 1.96, 2.77, 2.47
temp=68.1'C
frequency(0)=2100027776
throttled=0x0
               total        used        free      shared  buff/cache   available
Mem:           7.8Gi       1.4Gi       4.1Gi        15Mi       2.5Gi       6.4Gi
Swap:             0B          0B          0B

55.2  4.6 /opt/ros/jazzy/lib/cartographer_ros/cartographer_node -configuration_directory /home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_cartographer/share/turtlebot4_cartographer/config -configuration_basename turtlebot4_lds_2d.lua --ros-args -r __node:=cartographer_node --params-file /tmp/launch_params_m9majweq
```
- Generated Map:


