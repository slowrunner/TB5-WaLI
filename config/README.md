# TB5-WaLI Configuration

TurtleBot "5" WaLI is a Create3 with Raspberry Pi 5 running:
- TurtleBot 4 lite code with modifications
- WaLI behaviors and functionality

Turtlebot 4 code modifications:
- SLAMTEC RPLIDAR C1 instead of the A1M8 LIDAR (turtlebot4_bringup/launch/rplidar.launch.py  )
- LIDAR is mounted atop WALL-E character instead of the Create3 baseplate (urdf)
- WALL-E character replaces the Turtlebot 4 lite camera mount (urdf)
- Uncommented /stop_status in /turtlebot4_bringup/config/republisher.yaml (for odometer node)
- Raspberry Pi 5 instead of Raspberry Pi 4 - custom OS setup
- modified turtlebot4_description/urdf/lite/turtlebot4.urdf.xacro:
  - LIDAR location higher and orientation (0 facing rear vs left side in TB4)
  - camera locations
- modified turtlebot4_bringup/config/turtlebot4.yaml  
  - set power_saver: false
  - added mapping for dock/undock  to Logitech F710 Logitech button like TB4 controller home button
- modified nav2.yaml params_file (and copied to params/wali.nav2.yaml)
  - removed all use_sim_time: true
- modified localization.yaml params file
  - removed all use_sim_time: true
 
Raspberry Pi 5 configurations:
- setup RTC battery charging (in device tree)
- Setup USB usb_max_current_enable=1 in config.txt
- disabled IPv6 in cmdline.txt
- setup lifelog, cleanlifelog in crontab
- setup nohup_wali in crontab



NOTE:  After running ```sudo apt update && sudo apt upgrade -y``` run:
```
turtlebot4-service-restart
```
Then wait till oakd container is up with "camera ready"

```
systemctl status turtlebot4.service
...
Jan 27 23:12:23 TB5WaLI turtlebot4-start[28955]: [component_container-10] [INFO] [1738037543.688332834] [oakd]: Camera ready!
```
and then find the PID to kill the camera (this is the workaround till the Luxonis Jazzy depthai_ros_driver will /stop_camera without crashing):
```
ps -ef | grep oak
ubuntu     29110   28955 12 23:12 ?        00:00:01 /opt/ros/jazzy/lib/rclcpp_components/component_container --ros-args -r __node:=oakd_container -r __ns:=/
kill 29110
```
(if need the camera ```cmds/launch_camera.sh```)


### Configuring Turtlebot4 Overlays for TB5-WaLI Modification

To make changes to Turtlebot4 code, with the ability to compare the changed code base with the source repositories,  
the following Turtlebot4 repositories will be "forked" and brought down to the local robot's ROS 2 workspace:
- jazzy branch turtlebot4
- jazzy branch turtlebot4_robot

1) Setup jazzy turtlebot4 code in TB5-WaLI workspace (separately managed from TB5-WaLI repo)
- Browse to https://github.com/turtlebot/turtlebot4
- Click Fork 
  - set name slowrunner/turtlebot4_fork_for_TB5-WaLI
  - unclick Copy the humble branch only
  - Click Create Fork
- In the created fork
  - Click Code button
  - Click the "Copy Icon" to right of the https://...  
- On TB5-Wali
  - cd ~/TB5-Wali/wali_ws/src
  - git clone -b jazzy https://github.com/slowrunner/turtlebot4_robot_fork_for_TB5-WaLI.git
  - cd turtlebot4_fork_for_TB5-WaLI
  - git status (will say matches origin - the origin is the jazzy branch of the forked repository)
  - cd ..  (back to ~/TB5-WaLI/wali_ws/src)
  - git status   (will show turtlebot4_fork_for_TB5-WaLI/ untracked.  It will be tracked by the fork)
  - nano ~/TB5-WaLI/.gitignore
    - add turtlebot4_fork_for_TB5-WaLI/ at end of file


2) Setup jazzy turtlebot4_robot code in TB5-WaLI workspace (separately managed from TB5-WaLI repo)
- Browse to https://github.com/turtlebot/turtlebot4_robot
- Click Fork 
  - set name slowrunner/turtlebot4_robot_fork_for_TB5-WaLI
  - unclick Copy the humble branch only
  - Click Create Fork
- In the created fork
  - Click Code button
  - Click the "Copy Icon" to right of the https://...  
- On TB5-Wali
  - cd ~/TB5-Wali/wali_ws/src
  - git clone -b jazzy https://github.com/slowrunner/turtlebot4_fork_for_TB5-WaLI.git
  - cd turtlebot4_fork_for_TB5-WaLI
  - git status (will say matches origin - the origin is the jazzy branch of the forked repository)
  - cd ..  (back to ~/TB5-WaLI/wali_ws/src)
  - git status   (will show turtlebot4_robot_fork_for_TB5-WaLI/ untracked.  It will be tracked by the fork)
  - nano ~/TB5-WaLI/.gitignore
    - add turtlebot4_fork_for_TB5-WaLI/ at end of file
 
3) Install TB5-WaLI changes
- URDF: 
  - cd ~/TB5-Wali/wali_ws/src/turtlebot4_fork_for_TB5-WaLI/turtlebot4_description/urdf/lite/
  - cp turtlebot4.urdf.xacro  turtlebot4.urdf.xacro
  - cp ~/TB5-WaLI/config/turtlebot4.urdf.xacro .  (or use ~/TB5-WaLI/config/install_turtlebot4_description_urdf.sh)
  - git add turtlebot4.urdf.xacro turtlebot4.urdf.xacro.orig
  - git commit -m "TB5-WaLI mods to URDF"
  - git push

- power_save in turtlebot4.yaml:
  - cd ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/
  - cp turtlebot4.yaml turtlebot4.yaml.orig
  - cp ~/TB5-WaLI/config/turtlebot4.yaml .  (or use ~/TB5-WaLI/config/install_turtlebot4_yaml.sh)
  - git add turtlebot4.yaml turtlebot4.yaml.orig
  - git commit -m "TB5-WaLI mod to turn off power save till Luxonis depthai_ros_driver issue with stop_camera fixed"
  - git push

- publish stop_status in republisher.yaml for odometer node:
  - cd ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/config/
  - cp republisher.yaml republisher.yaml.orig
  - cp ~/TB5-WaLI/config/republisher.yaml .  (or use ~/TB5-WaLI/config/install_republisher_yaml.sh)
  - git add republisher.yaml republisher.yaml.orig
  - git commit -m "TB5-WaLI mod to enable stop_status topic for odometer node"
  - git push

- RPLidar C1
  - cd ~/TB5-WaLI/wali_ws/src/turtlebot4_robot_fork_for_TB5-WaLI/turtlebot4_bringup/launch
  - cp rplidar.launch.py rplidar.launch.py.orig
  - cp ~/TB5-WaLI/config/rplidar.launch.py .  (or use ~/TB5-WaLI/config/install_rplidar_launch.sh)
  - git add rplidar.launch.py rplidar.launch.py.orig
  - git commit -m "TB5-WaLI mod for C1 lidar"
  - git push

4) Build
- cd ~/TB5-WaLI/wali_ws
- ./rebuild.sh
- . ss.sh  (source /opt/ros/jazzy/setup.bash and ~/TB5-WaLI/wali_ws/install/setup.bash)
- Confirm turtlebot4_bringup location is the built file
ros2 pkg prefix turtlebot4_bringup 
/home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_bringup

5) turtlebot4-setup: set new WORKSPACE_PATH
- Find install/setup.bash path, verify permissions
```
$ ros2 pkg prefix turtlebot4_bringup 
/home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_bringup

$ ls -al /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash
-rw-rw-r-- 1 ubuntu ubuntu 1139 Jan 29 00:23 /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash
```
- copy full path to clipboard (/home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash)
- turtlebot4-setup
  - ROS Setup
    - Bash Setup
      - WORKSPACE_SETUP  (default /opt/ros/jazzy/setup.bash)
        - Paste full path from clipboard (/home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash)
      - Save
    - Robot Upstart
      - Restart
      - Status
```
● turtlebot4.service - "bringup turtlebot4"
     Loaded: loaded (/usr/lib/systemd/system/turtlebot4.service; enabled; preset: enabled)
     Active: active (running) since Wed 2025-01-29 09:25:16 EST; 1min 0s ago
   Main PID: 40828 (turtlebot4-star)
      Tasks: 173 (limit: 9375)
     Memory: 334.5M (peak: 355.3M)
        CPU: 21.104s
     CGroup: /system.slice/turtlebot4.service
             ├─40828 /bin/bash /usr/sbin/turtlebot4-start
             ├─40934 /usr/bin/python3 /opt/ros/jazzy/bin/ros2 launch /tmp/turtlebot4.launch.py
             ├─40938 /home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_node/lib/turtlebot4_node/turtlebot4_node --ros-args -r __ns:=/ --params-file /tmp/tmpnc3z5gyy --params-file /tmp/launch_params_yrtumulw
             ├─40939 /opt/ros/jazzy/lib/create3_republisher/create3_republisher --ros-args -r __ns:=/ --params-file /home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_bringup/share/turtlebot4_bringup/config/republisher.yaml --params->
             ├─40940 /opt/ros/jazzy/lib/joy_linux/joy_linux_node --ros-args -r __node:=joy_linux_node -r __ns:=/ --params-file /tmp/launch_params_y_zti8r2 -r /diagnostics:=diagnostics
             ├─40941 /opt/ros/jazzy/lib/teleop_twist_joy/teleop_node --ros-args -r __node:=teleop_twist_joy_node -r __ns:=/ --params-file /tmp/tmp1lgtrj57 --params-file /tmp/launch_params_e97r4ole
             ├─40942 /opt/ros/jazzy/lib/rplidar_ros/rplidar_composition --ros-args -r __node:=rplidar_composition -r __ns:=/ --params-file /tmp/launch_params_8yqi69jn
             ├─40943 /opt/ros/jazzy/lib/robot_state_publisher/robot_state_publisher --ros-args -r __node:=robot_state_publisher -r __ns:=/ --params-file /tmp/launch_params_9b4orpji --params-file /tmp/launch_params_y30rpj_w -r /tf:=>
             ├─40944 /usr/bin/python3 /opt/ros/jazzy/lib/joint_state_publisher/joint_state_publisher --ros-args -r __node:=joint_state_publisher -r __ns:=/ --params-file /tmp/launch_params_wju5b9xi -r /tf:=tf -r /tf_static:=tf_stat>
             ├─40945 /opt/ros/jazzy/lib/diagnostic_aggregator/aggregator_node --ros-args -r __ns:=/ --params-file /tmp/tmp68nm77un -r /diagnostics:=diagnostics -r /diagnostics_agg:=diagnostics_agg -r /diagnostics_toplevel_state:=di>
             ├─40946 /usr/bin/python3 /home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_diagnostics/lib/turtlebot4_diagnostics/diagnostics_updater --ros-args -r __ns:=/ -r /diagnostics:=diagnostics -r /diagnostics_agg:=diagnostics_a>
             └─41167 /opt/ros/jazzy/lib/rclcpp_components/component_container --ros-args -r __node:=oakd_container -r __ns:=/

Jan 29 09:25:50 TB5WaLI turtlebot4-start[40934]: [INFO] [launch_ros.actions.load_composable_nodes]: Loaded node '/oakd' in container '/oakd_container'
Jan 29 09:25:51 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160751.565804664] [oakd]: Starting camera.
Jan 29 09:25:51 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160751.577950579] [oakd]: No ip/mxid specified, connecting to the next available device.
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.099982281] [oakd]: Camera with MXID: 184430101175A41200 and Name: 3.1 connected!
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.101628245] [oakd]: USB SPEED: HIGH
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.123026574] [oakd]: Device type: OAK-D-LITE
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.125828687] [oakd]: Pipeline type: RGB
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [WARN] [1738160754.745535346] [oakd]: IMU enabled but not available!
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.745715327] [oakd]: Finished setting up pipeline.
Jan 29 09:25:54 TB5WaLI turtlebot4-start[40934]: [component_container-10] [INFO] [1738160754.966952551] [oakd]: Camera ready!

```
- q to end Status
- Esc to ROS Setup
- Esc to Turtlebot4 Setup
- Apply Settings
  - Yes
```
    _             _        ___      _   _   _                                                                                                                                                                                           
   /_\  _ __ _ __| |_  _  / __| ___| |_| |_(_)_ _  __ _ ___                                                                                                                                                                             
  / _ \| '_ \ '_ \ | || | \__ \/ -_)  _|  _| | ' \/ _` (_-<                                                                                                                                                                             
 /_/ \_\ .__/ .__/_|\_, | |___/\___|\__|\__|_|_||_\__, /__/                                                                                                                                                                             
       |_|  |_|     |__/                          |___/                                                                                                                                                                                 
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                        
Bash Settings:                                                                                                                                                                                                                          
  WORKSPACE_SETUP: /opt/ros/jazzy/setup.bash -> /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash                                                                                                                                        
                                                                                                                                                                                                                                        
Apply these settings?                                                                                                                                                                                                                   
                                                                                                                                                                                                                                        
**Notes**                                                                                                                                                                                                                               
- Changes applied to ROS_DOMAIN_ID, ROBOT_NAMESPACE, RMW_IMPLEMENTATION,                                                                                                                                                                
  or ROS_DISCOVERY_SERVER  will be applied to the Create 3 as well.                                                                                                                                                                     
- Changes applied to Wi-Fi will cause SSH sessions to hang.                                                                                                                                                                             
                                                                                                                                                                                                                                        
Press Q, Esc, or CTRL+C to go back.                                                                                                                                                                                                     
------------------------------------------------------------------------------------------------                                                                                                                                        
> Yes                                                                                                                                                                                                                                   
  No                                                                                                                                                                                                                                    


```
- View Settings
  - /etc/turtlebot4/setup.bash
```
  /etc/turtlebot4/discovery.conf                                                                                                                                                                                                        
  /etc/turtlebot4/cyclonedds_rpi.xml                                                                                                                                                                                                    
  /etc/turtlebot4/chrony.conf                                                                                                                                                                                                           
  /etc/turtlebot4/fastdds_rpi.xml                                                                                                                                                                                                       
  /etc/turtlebot4/discovery.sh                                                                                                                                                                                                          
  /etc/turtlebot4/fastdds_discovery_create3.xml                                                                                                                                                                                         
  /etc/turtlebot4/aliases.bash                                                                                                                                                                                                          
  /etc/turtlebot4/system                                                                                                                                                                                                                
> /etc/turtlebot4/setup.bash                                                                                                                                                                                                            
  /etc/netplan/50-wifis.yaml                                                                                                                                                                                                            
  /etc/netplan/40-ethernets.yaml                                                                                                                                                                                                        
  /etc/netplan/50-wifis.yaml.ap                                                                                                                                                                                                         
  /etc/netplan/50-cloud-init.yaml.bak                                                                                                                                                                                                   
┌── preview ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ export CYCLONEDDS_URI="/etc/turtlebot4/cyclonedds_rpi.xml"                                                                                                                                                                           ││ export FASTRTPS_DEFAULT_PROFILES_FILE="/etc/turtlebot4/fastdds_rpi.xml"                                                                                                                                                              ││ export ROBOT_NAMESPACE=""                                                                                                                                                                                                            ││ export ROS_DOMAIN_ID="5"                                                                                                                                                                                                             ││ export ROS_DISCOVERY_SERVER="127.0.0.1:11811;"                                                                                                                                                                                       ││ export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"                                                                                                                                                                                         ││ export TURTLEBOT4_DIAGNOSTICS="1"                                                                                                                                                                                                    ││ export WORKSPACE_SETUP="/home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash"                                                                                                                                                            ││ [ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False                                                                                                                                                            ││ export ROBOT_SETUP=/etc/turtlebot4/setup.bash                                                                                                                                                                                        ││                                                                                                                                                                                                                                      ││ source $WORKSPACE_SETUP                                                                                                                                                                                                              ││                                                                                                                                                                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```
  - Esc back to Turtlebot4 Setup
- About
```
TurtleBot 4 Open Source Robotics Platform.                                                                                                                                                                                              
                                                                                                                                                                                                                                        
Model: lite                                                                                                                                                                                                                             
Version: 2.0.2                                                                                                                                                                                                                          
ROS: Jazzy                                                                                                                                                                                                                              
Hostname: TB5WaLI                                                                                                                                                                                                                       
IP: 10.0.0.178                                                                                                                                                                                                                          
The TurtleBot 4 was created in a partnership between Open Robotics and Clearpath Robotics.                                                                                                                                              
                                                                                                                                                                                                                                        
Press Q, Esc, or CTRL+C to go back.                                                                                                                                                                                                     
------------------------------------------------------------------------------------------                                                                                                                                              
> Model                                                                                                                                                                                                                                 
  Hostname                                                                                                                                                                                                                              
                                                                                                                                                                                                                                        
  Save                                                              
```
- Esc to Turtlebot4 Setup
- Esc to exit completely

Confirm TB5-WaLI changes are effective:
- path to turtlebot4_node in turtlebot4-setup status:  /home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_node/lib/turtlebot4_node/turtlebot4_node
- power_saver is now off:  
```
$ ros2 param get /turtlebot4_node power_saver
Boolean value is: False
```
- /stop_status is published:
```
$ ros2 topic echo --once /stop_status
header:
  stamp:
    sec: 1738161162
    nanosec: 389609705
  frame_id: base_link
is_stopped: true
---

```
- URDF is modified: 
  - rviz2
    - RobotModel: Description Source->Topic, Description Topic->/robot_description
    - TFs: base_link, oakd_link, rplidar_link
<img src="https://github.com/slowrunner/TB5-WaLI/blob/main/graphics/2025-01-29_URDF_Confirmation.jpg" height="400" />
