# My TurtleBot4 History

This Incarnation: TB5-WaLI Jan 2025 - Create3 plus Raspberry Pi 5, RPLidar C1, Oak-D-Lite
- Philosophy:  "Be a TurtleBot4 with a Raspberry Pi 5 SBC"
- May swap in Oak-D-W-97 wide-angle, same resolution RGB and Depth cameras eventually)

Consolation Period:  Implemented TurtleBot3 Cartographer and Navigation for GoPiGo3-Dave robot

Second Incarnation: Create3-WaLI Dec 2023 - Mar 2024 (Returned Crashed running RTABmap)
- Built Raspberry Pi 4 with Ubuntu 22.04 / ROS 2 Humble
    - Created ir2scan node which uses IR obstacle sensors to publish /scan topic
    - Able to create map of house with slam_toolbox using the ir2scan /scan topics
    - Built "safe" Wanderer to prevent Create3 getting stuck under kitchen cabinets
    - Needed auxiliary 5v supply with Pi4 for Oak-D-Lite
    - Created "say_node" to serve PiperTTS for /say topic
    - Create3 dead-reckoning characterized - really amazing
    - Integrated Virtual Wall to "Safe Wander"
    - RTABmap crashed Create3
- Built Raspberry Pi 5 with ROS 2 Humble in Docker
    - Worked with iRobot to find workaround to RTABmap crashes
        - Application configurations
        - Discovery Server partitioning
        - Basic Republisher
    - Tested Pi5 "Naps" - cooler fan runs at full speed while napping!
- Prior Life as Create3-WaLi from 12/2023 to 3/12/2024
    -    Total Awake:   1962.57  hrs
    -    Total Naps:     248.85  hrs
    -    Total Life:    2211.42  hrs 
    -    Playtimes (Undocked-Docked): 361
    -    Average playtime (last five) 2.4 hrs
    -    Average docked time (last five) 5.3 hrs 
- Ended up returning - no solution to RTABmap crashes
    - Lamented returning it greatly.
    - Noticed iRobot Education released Jazzy Simulation Oct 2024
    - Oct 2024: Alberto Soragno mentions TurtleBot4 Republisher Official in Jazzy

First Incarnation: TurtleBot4 Nov 2022 (Returned Immediately - Damage in Shipment)


Beta Program: Create3 Simulation Beta Oct 2021
- Built Raspberry Pi 4 with ROS 2 Galactic to test Create3 Simulation Beta
    - Created Odometer node to log all travels
    - Tested:
        - WallFollowing
        - Coverage Server
        - Dock/Undock Action Server
        - All published and subscribed topics
- Applied for "Hardware Beta" Program, not selected
