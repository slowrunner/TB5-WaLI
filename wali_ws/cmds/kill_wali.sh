#!/bin/bash

# FILE: kill_wali.sh

# Stops only the Wali node  
# by sending "KeyboardInterrupt" which is SIGINT

echo -e "\n**** KILL WALI_NODE"
pkill --signal SIGINT wali_node 2> /dev/null

echo -e "\n**** DONE"
