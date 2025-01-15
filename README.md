# TB5-WaLI

Raspberry Pi 5 based ROS 2 Robot "Wallfollower Looking for Intelligence" loosely based on TurtleBot 4 Lite  

- TB5-WaLI ROS 2 Nodes  
  - wali_node  
    - Manage battery: Undock at 99% battery, rotate to face dock at 18%, Dock at 15%)   
  - odometer  (Log all robot travel)  
  - say_node  (espeak-ng TTS server)  
- TurtleBot4 ROS 2 Jazzy Jalisco  
- Ubuntu 24.04 LTS (64-bit) Server  
- Raspberry Pi 5 8GB  
- Create3 running "ROS 2 Iron Firmware"  
  - Iron Firmware is the last release before iRobot discontinued selling Create3  
  - Certified to work with ROS 2 Jazzy nodes  
  - Communicates with RPi5 using Ethernet-over-USB  

<img src="https://github.com/slowrunner/TB5-WaLI/blob/main/graphics/WaLI_Waiting_For_Create3.JPG" width="378" height="504" />
