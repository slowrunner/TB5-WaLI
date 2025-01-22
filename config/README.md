# TB5-WaLI Configuration

TurtleBot "5" WaLI is a Create3 with Raspberry Pi 5 running:
- TurtleBot 4 lite code with modifications
- WaLI behaviors and functionality

Turtlebot 4 code modifications:
- SLAMTEC RPLIDAR C1 instead of the A1M8 LIDAR (launch file and executable)
- LIDAR is mounted atop WALL-E character instead of the Create3 baseplate (urdf)
- WALL-E character replaces the Turtlebot 4 lite camera mount (urdf)
- Uncommented /stop_status in Create3 republisher.yaml (for odometer node)
- Raspberry Pi 5 instead of Raspberry Pi 4 - custom OS setup
- TEMP: modified turtlebot4.urdf.xacro for LIDAR and camera locations
- turtlebot4_bringup/config/turtlebot4.yaml  set power_saver: false

Raspberry Pi 5 configurations:
- setup RTC battery charging (in device tree)
- Setup USB usb_max_current_enable=1 in config.txt
- disabled IPv6 in cmdline.txt
- setup lifelog, cleanlifelog in crontab


