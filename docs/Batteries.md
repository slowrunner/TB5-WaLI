# Batteries For TB5-WaLI  

### New Battery 2026-03-23  

- Morpilot i7 Amazon $40  
- 3200mAh 46wH  
- Start: 2052 dockings 10310 hours total life  
- /battery_state on first use:  

```
*** ECHO BATTERY STATE
Mon Mar 23 11:52:52 EDT 2026
ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile /battery_state
header:
  stamp:
    sec: 1774281177
    nanosec: 364273385
  frame_id: ''
voltage: 15.777000427246094
temperature: 31.049999237060547
current: 0.6489999890327454
charge: 1.3250000476837158
capacity: 2.5
design_capacity: 2.5
percentage: 0.5299999713897705
power_supply_status: 0
power_supply_health: 0
power_supply_technology: 0
present: true
cell_voltage: []
cell_temperature: []
location: ''
serial_number: ''
---

```

### Original (used) battery came with the Create3 

- First use at 2200 hrs 361 dockings (prior Create3-WaLI final life)  
- Dockings on this battery: 1691  
- Life on this battery: 8099 hours  
- /battery_state on final night used:  

```
*** ECHO BATTERY STATE
Sun Mar 22 13:56:46 EDT 2026
ros2 topic echo --once --flow-style -l 1 --qos-reliability best_effort --qos-durability volatile /battery_state
header:
  stamp:
    sec: 1774202212
    nanosec: 132654215
  frame_id: ''
voltage: 15.472999572753906
temperature: 39.45000076293945
current: 0.5139999985694885
charge: 0.4690000116825104
capacity: 1.0
design_capacity: 1.0
percentage: 0.4699999988079071
power_supply_status: 0
power_supply_health: 0
power_supply_technology: 0
present: true
cell_voltage: []
cell_temperature: []
location: ''
serial_number: ''
---

```
