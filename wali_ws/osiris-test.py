#!/bin/env python3

import psutil
import subprocess

for p in psutil.process_iter(["cmdline"]):
  try:
    if "osiris_node" in " ".join(p.info["cmdline"] or []):
      cpu = p.cpu_percent(interval=0.5)
      cores = psutil.cpu_count()
      sys_cpu = psutil.cpu_percent(interval=0.1)
      print(f"Osiris: {cpu/cores:.1f}% of system ({cpu:.1f}% of 1 core)")
      print(f"System total: {sys_cpu:.1f}%")
      break
  except: pass

