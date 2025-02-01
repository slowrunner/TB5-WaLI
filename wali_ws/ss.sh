#!/bin/bash

if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
    echo -e "sourced /opt/ros/jazzy setup.bash"
fi

if [ -f /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash ]; then
    source /home/ubuntu/TB5-WaLI/wali_ws/install/setup.bash
    echo -e "sourced wali_ws install setup.bash"
fi

if [ -f /home/ubuntu/TB5-WaLI/dai_ws/install/setup.bash ]; then
    source /home/ubuntu/TB5-WaLI/dai_ws/install/setup.bash
    echo -e "sourced dai_ws install setup.bash"
fi

echo -e "Done\n"
