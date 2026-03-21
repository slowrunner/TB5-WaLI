#!/bin/env python3

import psutil

sys_cpu = psutil.cpu_percent(interval=0.1)
print(f"System total: {sys_cpu:.1f}%")

