#!/bin/bash

# Visits:  Directions are IntEnum from WaLI_Dir class - e.g. WaLI_Dir.SOUTH

#  1)  front door:  ( 3.39  ,  3.99 , "SOUTH"     )
#  2)  couch view:  ( 0.5   ,  2.7  , "NORTH_WEST")
#  3)  Laundry:     ( 2.7   , -1.47 , "SOUTH"     )
#  4)  table:       ( 0.97  , -0.7  , "SOUTH_EAST")
#  5)  kitchen:     ( 3.71  ,  1.04 , "NORTH_WEST")
#  6)  Dining:      (-2.6   , -0.5  , "SOUTH_EAST")
#  7)  patio view:  (-3.4   ,  2.1  , "NORTH_EAST")
#  8)  office:      (-4.56  , -0.01 , "NORTH_WEST")
#  9)  hall view :  ( 2.1   ,  4.0  , "NORTH_EAST")
#  10) Ready:       (-0.208 , -0.317, "NORTH_EAST")   was 10) Ready:       (-0.332 , -0.333, "NORTH_EAST")
#
#  Note: undocked: (-0.010 , -0.372,  "NORTH"     )
#  Note: docked:   ( 0.022 , -0.372,  "SOUTH"     )


/home/ubuntu/TB5-WaLI/utils/logMaintenance.py 'nav_wali_tour.sh executing'
echo -e "ros2 run wali wali_tour"
uptime
ros2 run wali wali_tour
uptime
