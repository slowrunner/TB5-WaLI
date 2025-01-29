# TB5-WaLI Configuration

TurtleBot "5" WaLI is a Create3 with Raspberry Pi 5 running:
- TurtleBot 4 lite code with modifications
- WaLI behaviors and functionality

Turtlebot 4 code modifications:
- SLAMTEC RPLIDAR C1 instead of the A1M8 LIDAR (launch file and executable)
- LIDAR is mounted atop WALL-E character instead of the Create3 baseplate (urdf)
- WALL-E character replaces the Turtlebot 4 lite camera mount (urdf)
- Uncommented /stop_status in Create3 /opt/ros/jazzy/share/turtlebot4_bringup/config/republisher.yaml (for odometer node)
- Raspberry Pi 5 instead of Raspberry Pi 4 - custom OS setup
- TEMP: modified /opt/ros/jazzy/share/turtlebot4_description/urdf/lite/turtlebot4.urdf.xacro for LIDAR and camera locations
- TEMP: modified /opt/ros/jazzy/share/turtlebot4_bringup/config/turtlebot4.yaml  set power_saver: false

Raspberry Pi 5 configurations:
- setup RTC battery charging (in device tree)
- Setup USB usb_max_current_enable=1 in config.txt
- disabled IPv6 in cmdline.txt
- setup lifelog, cleanlifelog in crontab
- setup nohup_wali in crontab



NOTE:  After running ```sudo apt update && sudo apt upgrade -y``` run:
```
install_republisher.yaml.sh   (enable /stop_status for the odometer)
install_turtlebot4_description_urdf.sh  (proper LIDAR and Camera transforms)
install_turtlebot4_yaml.sh      (turn power_saver function off till Luxonis Jazzy depthai_ros_driver won't crash on /stop_camera)
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


4) Build
- cd ~/TB5-WaLI/wali_ws
- ./rebuild.sh
- . ss.sh  (source /opt/ros/jazzy/setup.bash and ~/TB5-WaLI/wali_ws/install/setup.bash)
- Confirm turtlebot4_bringup location is the built file
ros2 pkg prefix turtlebot4_bringup 
/home/ubuntu/TB5-WaLI/wali_ws/install/turtlebot4_bringup

5) turtlebot4-setup: set new WORKSPACE_PATH
- turtlebot4-setup

