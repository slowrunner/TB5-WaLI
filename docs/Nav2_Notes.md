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
