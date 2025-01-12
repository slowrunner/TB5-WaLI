# TB5-WaLI Pi5 Setup

Create Jazzy Jalisco - Ubuntu 24.04 TurtleBot4 Raspberry Pi 5  

REF: https://github.com/turtlebot/turtlebot4_setup/tree/jazzy  

## Initial Image Creation  
- Raspberry Pi Imager - Other OS->Ubuntu 24.04.1 LTS (64-BIT) Server  
- Customize Settings:  
  -  US, hostname TB5WaLI, wireless SSID (Case matters), username: ubuntu, services SSH


## Login (via ssh over WiFi)  
```
   ssh ubuntu@x.x.x.x
```
If complains:
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:............
Please contact your system administrator.
Add correct host key in /Users/tovli/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/tovli/.ssh/known_hosts:51
Host key for xx.x.x.xxx has changed and you have requested strict checking.
Host key verification failed.

Then:  
   ssh-keygen -R x.x.x.x
```

Now login via ssh:  
```
   ssh ubuntu@x.x.x.xxx  
```

=== Optional: Disable IPv6 (Sometimes update/upgrade failures over IPv6 will prevent setup)  
```
sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.bak
```

Then:  (note the necessary space before the added stanza)  
```
sudo nano /boot/firmware/cmdline.txt
```
add " ipv6.disable=1" to the end of line  
```
more /boot/firmware/cmdline.txt
```


=== Optional: get iwconfig - confirm on 5GHz WiFi

```
sudo apt install wireless-tools
iwconfig
```
Confirm 5GHz WiFi connection  



### Security Step To Prevent Exposing FreeText WiFi Password  
```
sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.bak
```
Optional: Save your net password SHA somewhere handy
```
   password: .....SHA.....
```

### Perform update/upgrade/reboot to ensure kernel is up to date  
(kernel update will cause turtlebot4_setup.sh  failure)

```
sudo apt update
sudo apt upgrade -y
sudo reboot
```

### === Shutdown and Backup before continuing:    
```
sudo shutdown -h now

diskutil list  
sudo dd bs=1m if=/dev/rdisk8 of=YYYY-MM-DD_TB5WaLI_b4_TB4_setup.dmg  
  (ctrl-t for status while executing backup)  
sudo diskutil eject /dev/rdisk8  
```


To Restore later:  
``` 
diskutil list  
diskutil unmountDisk /dev/rdisk8  
sudo dd bs=1m of=/dev/rdisk8 if=BkupYYYY-MM-DD_TB5WaLI_b4_TB4_setup.dmg  
```

=== ReBoot / Boot (if performed backup) to pick up IPv6 disable  




### === Setup turtlebot 4 software (will install ROS 2 Jazzy Base )  

REF:  https://github.com/turtlebot/turtlebot4_setup/tree/jazzy  

```
wget -qO - https://raw.githubusercontent.com/turtlebot/turtlebot4_setup/jazzy/scripts/turtlebot4_setup.sh | bash
```



=== Run turtlebot4-setup only for WiFi setup first

REF: https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_setup.html#configuration-tools

```
turtlebot4-setup
```

### OPTIONAL: Edit to keep WiFi setup

```
sudo cp /etc/netplan/50-wifis.yaml /etc/netplan/50-wifis.yaml.ap

sudo nano /etc/netplan/50-wifis.yaml
```
Make it look like (with your SSID and NET_PWD_SHA):
```
# This file was automatically created by the turtlebot4-setup tool and should not be manually modified

network:
    version: 2
    wifis:
        renderer: NetworkManager
        wlan0:
            access-points:
                YOUR_NET_SSID:
                    band: 5GHz
                    password: YOUR_NET_SHA
            dhcp4: true

```


### IF DID NOT MODIFY /etc/netplan/50-wifis.yaml: Reboot into AP mode 

```
sudo reboot
```

use ipad connect WiFi to Turtlebot4, use termius to ssh to turtlebot4
(use ubuntu password setup with Raspberry Pi Imager)


$ turtlebot4-setup
- WiFi Setup
 - client
 - SSID (case sensitive)
 - WiFi Passwd (or better yet WiFi Password SHA if copied it down somewhere)
 - Save
 - Apply Settings
 - yes

RPi will reboot and connect to WiFi DHCP

SSH back in (iPad no longer needed) 
```
ssh ubuntu@xx.x.x.xxx
```

### FIX NET PASSWORD IN FREE TEXT
```
sudo nano /etc/netplan/50-wifis.yaml
```
Replace free text password with SHA password

=== CONFIGURE PASSWORD-LESS SUDO
```
sudo nano /etc/sudoers
```
make sudo group look like:
```
# Allow members of group sudo to execute any command
%sudo	ALL=(ALL:ALL) NOPASSWD: ALL
```

=== Continue turtlebot4-setup for ROS and Robot

```
turtlebot4-setup
```

1) Bash Setup:
 - ROBOT_NAMESPACE	[]
 - ROS_DOMAIN_ID	[5]  (press enter, type 5, press enter)
 - (others leave defaults)
 - Save
2) Discovery Server:
 - Enabled no, all others leave untouched
 - save
3) Robot Upstart:
 - Install
 - Start
 - Status
 - ESC
5) Back at main menu
 - Apply Settings
 - yes
 - ctrl-C




==== Status ====
source ~/.bashrc
ros2 node list

=== F710 Gamepad Test
 - Put switch in either position
 - Left Enable X: +/- 0.2 meters/second AngularZ: +/- 0.5 radians/second
 - Right Enable X: +/- 1.9 meters/second AngularZ: +/- 1.9 radians/second 
```
ros2 topic echo /cmd_vel
```

=== ros2 node list
```
ros2 node list
/analyzers
/create3_repub
/joint_state_publisher
/joy_linux_node
/launch_ros_3665
/oakd
/oakd_container
/robot_state_publisher
/rplidar_composition
/teleop_twist_joy_node
/turtlebot4_diagnostics
/turtlebot4_node
```

=== Republisher Info
```
ubuntu@TB5WaLI:~/TB5-WaLI/wali_ws$ ros2 node info /create3_repub
/create3_repub
  Subscribers:
    /cmd_audio: irobot_create_msgs/msg/AudioNoteVector
    /cmd_lightring: irobot_create_msgs/msg/LightringLeds
    /cmd_vel: geometry_msgs/msg/TwistStamped
    /cmd_vel_unstamped: geometry_msgs/msg/Twist
    /parameter_events: rcl_interfaces/msg/ParameterEvent
  Publishers:
    /battery_state: sensor_msgs/msg/BatteryState
    /dock_status: irobot_create_msgs/msg/DockStatus
    /imu: sensor_msgs/msg/Imu
    /interface_buttons: irobot_create_msgs/msg/InterfaceButtons
    /odom: nav_msgs/msg/Odometry
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /tf: tf2_msgs/msg/TFMessage
    /tf_static: tf2_msgs/msg/TFMessage
    /wheel_status: irobot_create_msgs/msg/WheelStatus
  Service Servers:
    /create3_repub/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /create3_repub/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /create3_repub/get_parameters: rcl_interfaces/srv/GetParameters
    /create3_repub/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /create3_repub/list_parameters: rcl_interfaces/srv/ListParameters
    /create3_repub/set_parameters: rcl_interfaces/srv/SetParameters
    /create3_repub/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
    /e_stop: irobot_create_msgs/srv/EStop
    /reset_pose: irobot_create_msgs/srv/ResetPose
    /robot_power: irobot_create_msgs/srv/RobotPower
  Service Clients:

  Action Servers:
    /audio_note_sequence: irobot_create_msgs/action/AudioNoteSequence
    /dock: irobot_create_msgs/action/Dock
    /drive_arc: irobot_create_msgs/action/DriveArc
    /drive_distance: irobot_create_msgs/action/DriveDistance
    /led_animation: irobot_create_msgs/action/LedAnimation
    /navigate_to_position: irobot_create_msgs/action/NavigateToPosition
    /rotate_angle: irobot_create_msgs/action/RotateAngle
    /undock: irobot_create_msgs/action/Undock
    /wall_follow: irobot_create_msgs/action/WallFollow
  Action Clients:
```

# ==== TB5-WaLI Specific Setup ====  


turtlebot4-setup writes /boot/firmware/config.txt. I added before the final [all]:

```
[pi5]
usb_current_limit=1A6
dtparam=rtc_bbat_vchg=3000000

```
Reboot then check:
```
sudo reboot
```

****** Checking the Create3 power supply max_current and usb_max_current_enable

```
$ xxd -g4 /proc/device-tree/chosen/power/max_current
00000000: 00001388                             ....

```

- To see the integer value
```
$ echo $((0x00001388))
5000


```

- To see the value of usb_max_current_enable  
```
$ vcgencmd get_config usb_max_current_enable
usb_max_current_enable=1

```

- Check if trickle charging RTC battery enabled (value 3000000):
```
$ cat /sys/devices/platform/soc/soc:rpi_rtc/rtc/rtc0/charging_voltage_max
4400000
$ cat /sys/devices/platform/soc/soc:rpi_rtc/rtc/rtc0/charging_voltage_min
1300000

$ cat /sys/devices/platform/soc/soc:rpi_rtc/rtc/rtc0/charging_voltage
3000000        <-- not 0 when enabled
```


=== Check memory:
```
ubuntu@TB5WaLI:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           7.8Gi       329Mi       7.3Gi       3.5Mi       242Mi       7.4Gi
Swap:             0B          0B          0B
```

=== More utils
```
sudo apt install hwinfo -y
hwinfo

sudo apt install raspi-config
```

=== install ALSA audio and check audio
```
sudo apt install alsa-utils -y
aplay -l  
sudo apt install espeak-ng -y
espeak-ng 'hello'  
```

==== BRING DOWN TB5-WaLI SPECIFIC CODE ====
(Created git repo TB5-WaLI) 

```
ubuntu@TB5WaLI:~$ git clone https://github.com/slowrunner/TB5-WaLI.git
ubuntu@TB5WaLI:~/TB5-WaLI$ git config --global user.name "slowrunner"
ubuntu@TB5WaLI:~/TB5-WaLI$ git config --global user.email "slowrunner@users.noreply.github.com"
ubuntu@TB5WaLI:~/TB5-WaLI$ git config --global credential.helper store
nano README.md
git add README.md
git commit
git push
user: slowrunner
password:  secret sauce pass code
```

=== setup life logging / totalife / logMaintenance
```
mkdir TB5-WaLI/logs
touch odometer.log
start initial life.log

sudo crontab -e  (add lines from config/crontab-e)
run utils/nohup_loglife.sh
```

=== rebuild TB5-WaLI code
```
cd ~/TB5-WaLI/wali_ws
sudo rosdep init
rosdep update

./rebuild.sh
./start_wali.sh
ros2 node list
```


=== OPTIONAL:  install gamepad config files  
```
~/TB5-WaLI/config/install_gamepad_param_files.sh
```


=== useful files to check
```
/etc/turtlebot4/setup.bash
/etc/turtlebot4/aliases.bash
```

=== useful aliased commands


- turtlebot4-help
- turtlebot4-daemon-restart
- turtlebot4-service-restart
- turtlebot4-ntpd-sync  
- turtlebot4-source
- turtlebot4-update


