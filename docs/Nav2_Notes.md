# Nav2 Notes


Configuration:
- LIDAR Scan from RPLidar C1
- Turtlebot4 Jazzy Branch (diagnostics disabled)
- ROS 2 Jazzy Jalisco
- Ubuntu 24.04 Noble Numbat
- Raspberry Pi 5 8GB with Pi Cooler
- Stereo-Depth Camera NOT USED


- TB5-WaLI Nav2 Benchmarking: using ```ros2 run wali monitor```

1) WaLI Idle: 5% max CPU  14% demand
2) WaLI + Loc initialized: 5% to 7% CPU  18-22% demand
3) WaLI + Loc + Nav2 initialized:  36% max  77-224% demand
4) WaLI+Loc+Nav2 navigating: 59% max  233% demand
5) WaLI+Loc+Nav2 idle again: 37% max  175% demand


### Current Changed Params From Jazzy TurtleBot4_navigation/config/nav2.yaml

```
ubuntu@TB5WaLI:~/TB5-WaLI/wali_ws/params$ diff test.nav2.yaml wali.nav2.yaml.pre-tuning 
156,159c156,158
<         z_resolution: 0.1  # was 0.05 - making it 0.1 will lower CPU usage
<         z_voxels: 20       # was 16 (16x0.05=0.80 getting sensor origin out of map bounds so upped to 2.0 meter)
<         max_obstacle_height: 0.40 # was 2.0  WaLI is only 35 cm high
<         min_obstacle_height: 0.05 # was not included - added to ignore floor returns
---
>         z_resolution: 0.05
>         z_voxels: 16
>         max_obstacle_height: 2.0
164c163
<           max_obstacle_height: 1.0 # was 2.0 getting sensor origin out of map bounds
---
>           max_obstacle_height: 2.0
215,216c214,215
<         cost_scaling_factor: 1.25
<         inflation_radius: 1.25
---
>         cost_scaling_factor: 4.0
>         inflation_radius: 0.35
```

Experiments:
- default wali.nav2.yaml.pre-tuining:  0.05 x 16 voxel height (rug crossing caused "out of map verticle bounds" by 10cm)  

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

Using 2D:Obstacle_Layer instead of Voxel_Layer: 
- showed no visible average CPU usage or demand reduction
- Did not reliably navigate to goals as when using voxel layer

### Relaxed Nav2: (This is a huge improvement in robustness, but lower reliability reaching goal)

```
WaLI performed seven successful navigations, including the very challenging exit from the laundry room, 
and was able to "walk and chew gum at the same time". I could ask him to echo his /battery_state 
and he kept right on planning, driving the plan, 
and he didn't stop to butt heads with the bar stools, or investigate any walls.
(Additionally all this with remote test tool running, which previously would cause goal failures.)

These are the changes I made to the nav2.yaml file for this major improvement in navigation performance:

```
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
