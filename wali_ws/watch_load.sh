#!/bin/bash

# loop printing 1 minute average load
# /proc/loadavg is updated every 5 seconds

while [ 1 ]
do
  d=`date +"%H:%M:%S" `
  load=`cat /proc/loadavg`
  load="${load%% *}"
  cpu=`(echo " ($load / 4.0 * 100)" | bc -l)`
  cpu="${cpu:0:3}"
  echo -e "$d 1m load: $load  $cpu% of RPi 5 CPU"
  sleep 5
done
