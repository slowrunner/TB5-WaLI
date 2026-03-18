#!/bin/bash

# loop printing cpu usage
# uses "100 - idle_time" from vmstat

while [ 1 ]
do
  d=`date +"%H:%M:%S" `
  read -a arr <<< "$(vmstat 1 2 | tail -n 1)"
  # declare -p arr
  idle_index=14
  idle=${arr[idle_index]}
  cpu=$(bc <<< "100 - $idle")
  echo -e "$d total cpu usage: $cpu% of RPi 5 CPU"
  free -h
  echo " *** "
  sleep 5
done
