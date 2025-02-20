# SLAM Notes


Configuration:
- Oak-D-Lite 
  - (Publishing RGB Preview only, no Net, no Depth) 
  - (5v supply from Create3 14.4v aux power)
- RPLidar C1 (5v supplied from RPi5 USB)
- USB Speaker/Mic (not active, 5v supplied from RPi5 USB)
- Turtlebot4 Jazzy Branch (diagnostics disabled)
- ROS 2 Jazzy Jalisco
- Ubuntu 24.04 Noble Numbat
- Raspberry Pi 5 8GB with Pi Cooler

- TB5-WaLI Processing Load
  - 0.50 (13% of Pi5): turtlebot.service, wali_node, say_node, odometer, (diagnostics disabled), LIDAR, Oak-D-Lite RGB preview, idle Create3
  - 1.00 (25% of Pi5): +localization (not moving)  12.4W total 
  - 2-3 ave 6 max (50-75 to 100% of Pi5): +navigation 14W not moving 15.6W moving 70C 2.4GHz (no throttling seen)

