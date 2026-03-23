# Nav2 Notes


Configuration:
- LIDAR Scan from RPLidar C1
- Turtlebot4 Jazzy Branch (diagnostics disabled)
- ROS 2 Jazzy Jalisco
- Ubuntu 24.04 Noble Numbat
- Raspberry Pi 5 8GB with Pi Cooler
- Stereo-Depth Camera NOT USED


- TB5-WaLI Nav2 Benchmarking:

1) WaLI Idle: 5% max CPU  14% demand
2) WaLI + Loc initialized: 5% to 7% CPU  18-22% demand
3) WaLI + Loc + Nav2 initialized:  36% max  77-224% demand
4) WaLI+Loc+Nav2 navigating: 59% max  233% demand
5) WaLI+Loc+Nav2 idle again: 37% max  175% demand


Experiments:
- default wali.nav2.yaml:  0.05 x 16 voxel height (rug crossing caused "out of map verticle bounds" by 10cm)  
- wali.nav2.yaml.increase_voxel_height_and_max_height (size to 0.1  number to 10 = 1 meter)  eliminated rug crossing out of bounds  
- wali.nav2.tune_global_cost_and_inflation: Gemini   <--- Using 3/18/26  
  - recommended values to make WaLI less likely to go close to obstacles - navigation nearly always succeeds)  
- wali.nav2.2D_Layers: (rejected)  
  - global_costmap is already 2D, but local costmap is voxel/3D planned.  Prediction was 2D planning would significantly save CPU usage  
  - Result: no detectable CPU usage reduction, increased local cost map localization, introduced goal failures  
- wali.nav2.composition:  (rejected)  
  - ROS 2 Nav2 issue pushed to later versions to solve: parameters on late launched nodes do not get passed parameter file values  
  - Seg Faults easily  
  -  Using composition doesn't load costmap parameters from yaml file #4011 https://github.com/ros-navigation/navigation2/issues/4011  
- wali.nav2.relax:  
  - reduced cycle rate, increased timeouts, to prevent slow planner cancelations, and early declaration of failure.   

### 2D vs 3D Nav

```
Lessons Learned: WaLI 2D vs. 3D Navigation
Mechanical Reality > Theory: Because the LiDAR isn't perfectly horizontal, 
its "coned" scan provides high-value vertical diversity. 
The Voxel Layer integrates this into a robust 3D "object," whereas 2D treats it as unstable noise.

Algorithmic Filtering: The 3D Voxel Layer’s Mark/Clear thresholds are superior at filtering "flicker" 
caused by rug transitions and sensor tilt, leading to much more stable localization in congested areas.

The CPU Paradox: On the Raspberry Pi 5, the computational cost of 3D raytracing is 
negligible compared to the DDS communication overhead and Lifecycle Management complexity. 
Moving to 2D yielded no significant CPU savings.

System Stability: The Nav2 "3D Local / 2D Global" default is a proven sweet spot. 
Forcing a "Double-2D" stack triggered Lifecycle Bond Timeouts, 
proving the stack is more stable when operating in its intended 3D-aware mode.

Optimized Configuration: A 0.1m resolution with 10 voxels (1.0m height) is the ideal balance 
for WaLI—it handles the 34cm LiDAR line's vertical "shimmer" 
without the performance hit of the original 0.05m resolution.
```

### Relaxed Nav2: (THIS IS HUGE IMPROVEMENT)

```
WaLI performed seven successful navigations, including the very challenging exit from the laundry room, 
and was able to "walk and chew gum at the same time". I could ask him to echo his /battery_state 
and he kept right on planning, driving the plan, 
and he didn't stop to butt heads with the bar stools, or investigate any walls.
(Additionally all this with remote test tool running, which previously would cause goal failures.)

These are the changes I made to the nav2.yaml file for this major improvement in navigation performance:

ubuntu@TB5WaLI:~/TB5-WaLI/wali_ws/params$ diff test.nav2.yaml wali.nav2.yaml

7,10c7,10

<     bt_loop_duration: 100  # 10 Hz , 10 ms 100 Hz by default
<     default_server_timeout:  1000  # 20 ms by default
<     wait_for_service_timeout: 2000 # 1000 by default
<     action_server_result_timeout: 1800.0 # 900.0

---

>     bt_loop_duration: 10
>     default_server_timeout: 20
>     wait_for_service_timeout: 1000
>     action_server_result_timeout: 900.0

20,22d19

< lifecycle_manager_navigation:
<   ros__parameters:
<     bond_timeout: 10.0

```
Why These Changes Fix Nav2:

The BT Loop (100ms vs 10ms): By dropping to 10Hz, you freed up a huge amount of overhead. 
The bt_navigator isn't constantly nagging the other nodes, 
which lets the Raspberry Pi prioritize the Controller (driving).

The 1000ms Server Timeout: This is likely why he didn't "butt heads with the bar stools" 
If a costmap update took 50ms instead of 10ms, the old settings would have aborted the plan. 
Now, WaLI just waits a heartbeat and keeps going.

The Bond Timeout (10.0s): This is your safety net. 
It ensures that even if the Pi hits a 100% CPU spike while processing a heavy 
/battery_state request or a complex scan, the lifecycle_manager won't pull the plug on the whole operation.
