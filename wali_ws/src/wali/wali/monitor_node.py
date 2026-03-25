#!/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import BatteryState
from irobot_create_msgs.msg import DockStatus
import os
import subprocess
import time
import psutil


class WaliMonitor(Node):
    def __init__(self):
        super().__init__('wali_monitor_node')
        
        # QoS setup to match your script
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # State variables
        self.batt_msg = None
        self.dock_msg = None

        # Subscriptions
        self.create_subscription(BatteryState, '/battery_state', self.battery_callback, qos)
        self.create_subscription(DockStatus, '/dock_status', self.dock_callback, qos)

        # Timer to print to console (e.g., every 10 seconds)
        self.create_timer(10.0, self.report_status)
        self.get_logger().info("TB5-WaLI Monitor Node Started...")

    def battery_callback(self, msg):
        self.batt_msg = msg

    def dock_callback(self, msg):
        self.dock_msg = msg

    def get_sys_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        except:
            return "N/A"


    def report_status(self):
        if not self.batt_msg:
            print("Waiting for /battery_state...")
            return

        # System stats
        temp = self.get_sys_cmd("vcgencmd measure_temp").replace("temp=", "")
        clock_raw = self.get_sys_cmd("vcgencmd measure_clock arm").split("=")[-1]
        clock_mhz = int(clock_raw) // 1000000 if clock_raw.isdigit() else 0
        throttled = self.get_sys_cmd("vcgencmd get_throttled")
        
        # Load Averages (formatted to 2 decimal places)
        load1, load5, load15 = os.getloadavg()
        cpu_demand = (load1 / 4.0) * 100
        
        # CPU usage
        sys_cpu = psutil.cpu_percent(interval=0.1)

        # Memory
        mem = self.get_sys_cmd("free -h | grep Mem").split()
        
        # Power Calculations
        volt = self.batt_msg.voltage
        curr = self.batt_msg.current
        watts = volt * curr
        batt_pct = self.batt_msg.percentage
        is_docked = self.dock_msg.is_docked if self.dock_msg else "Unknown"

        # Output (Refined for 2-decimal precision)
        print("\n********** TB5-WaLI MONITOR NODE ******************************")
        print(time.strftime("%A %m/%d/%y"))
        print(f"{time.strftime('%H:%M:%S')} up {self.get_sys_cmd('uptime -p').replace('up ', '')}")
        print(f"temp={temp}  frequency(0)={clock_raw}  {throttled}")
        print(f"Mem:   {mem[1]} total, {mem[2]} used, {mem[3]} free")
        print(f"1m load: {load1:.2f}  {cpu_demand:.1f}% demand on RPi 5's four cores")
        print(f"\nTotal CPU Usage: {sys_cpu:.1f}%")
        print("-" * 55)
        print(f"Voltage: {volt:.2f}  Current: {curr:.2f}  Watts: {watts:.2f}")
        print(f"Battery: {batt_pct:.2f}  Docked: {is_docked}")



def main(args=None):
    rclpy.init(args=args)
    node = WaliMonitor()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        # This catch is the "quiet exit" for Ctrl+C
        pass
    finally:
        # Check if context is still valid before trying to destroy/shutdown
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
