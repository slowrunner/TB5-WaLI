#!/bin/bash

# loop printing 1 minute average load and total cpu usage
# /proc/loadavg is updated every 5 seconds
# uses "100 - idle_time" from vmstat for total cpu usage

while [ 1 ]
do
  d=`date +"%H:%M:%S" `
  load=`cat /proc/loadavg`
  load="${load%% *}"
  cpu=`(echo " ($load / 4.0 * 100)" | bc -l)`
  cpu="${cpu:0:3}"
  echo -e "$d 1m load: $load  $cpu% demand on RPi 5's four cores"

  read -a arr <<< "$(vmstat 1 2 | tail -n 1)"
  # declare -p arr
  idle_index=14
  idle=${arr[idle_index]}
  cpu=$(bc <<< "100 - $idle")
  echo -e "$d total cpu usage: $cpu% of RPi 5 CPU"
  echo " "
  free -h
  echo " *** "
  echo " "
  sleep 5
done
