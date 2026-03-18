#!/bin/bash

# lines with the exact substring 'safety shutdown' are counted by totallife.sh

echo "logging 'safety shutdown' to life.log"
/home/ubuntu/TB5-WaLI/utils/logMaintenance "safety shutdown"
