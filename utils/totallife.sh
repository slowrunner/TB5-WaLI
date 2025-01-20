#!/bin/bash
#
# totallife.sh    print total hours and sessions of life in life.log
#
# requires bc  (sudo apt-get install bc)
#
# Counted Keys:
#   Playtimes:           " Docking: success "
#   Sessions:            "- boot -"              ( "\- boot \-" search string )
#   Safety shutdowns:    "safety shutdown"

echo "(Cleaning life.log first)"
/home/ubuntu/TB5-WaLI/plib/cleanlifelog.py
echo " "
fn="/home/ubuntu/TB5-WaLI/logs/life.log"
ofn='/home/ubuntu/TB5-WaLI/logs/odometer.log'
# fn="/home/pi/wali_pi5/utils/test_life.log"
# totalAwake=`(awk -F':' '{sum+=$3}END{print sum;}' $fn)`
totalAwake=`(awk -F'execution:' '{sum+=$2}END{print sum;}' $fn)`
totalNaps=`(awk -F'nap for' '{sum+=$2}END{print sum;}' $fn)`
totalLife=`(echo "scale=1; ($totalAwake + $totalNaps)" | bc)`
echo "*** TB5-WaLI TOTAL LIFE STATISTICS ***"
echo "Total Awake:  " $totalAwake " hrs"
echo "Total Naps:    " $totalNaps " hrs"
echo "Total Life:   " $totalLife " hrs (since Jan 09, 2025)"
echo "Playtimes (Undocked-Docked):" `(grep -c " Docking: success " $fn)`
last5playtimes=`(grep " hrs playtime " $fn | tail -5 | awk -F" after "  '{sum+=$2}END{print sum;}' )`
last5avePlaytime=`(echo "scale=1; $last5playtimes / 5" | bc)`
echo "Average playtime (last five)" $last5avePlaytime "hrs "
last2dockedtimes=`(grep " docked for " $fn | tail -2 | awk -F" for "  '{sum+=$2}END{print sum;}' )`
last2aveDockedtime=`(echo "scale=1; $last2dockedtimes / 2" | bc)`
echo "Average docked time (last two)" $last2aveDockedtime "hrs "
booted=`(grep -c "\- boot \-" $fn)`
echo "Sessions (boot): " `(grep -c "\- boot \-" $fn)`
aveSession=`(echo "scale=1; ($totalAwake / $booted)" | bc -l)`
echo "Average Session: " $aveSession "hrs"
safetyShutdowns=`(grep -c "safety shutdown" $fn)`
echo "Safety Shutdowns: " $safetyShutdowns 
totalMoved=`(awk -F'moved:' '{sum+=$2}END{printf "%.1f", sum;}' $ofn)`
totalMovedFt=`(echo "scale=1; ($totalMoved / 0.3048)" | bc)`
echo "Total Travel: " $totalMoved "meters" $totalMovedFt "feet"

