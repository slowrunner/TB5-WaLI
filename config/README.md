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


