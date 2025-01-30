#/bin/bash

echo -e "\n*** ECHO SCAN"
echo -e "ros2 topic echo --flow-style --once /scan"

# result=$(ros2 topic echo --once --flow-style --field ranges /scan )
# front=$(echo "$result" | cut -d ',' -f3)
# left=$(echo "$result" | cut -d ',' -f128)
# rear=$(echo "$result" | cut -d ',' -f253)
# right=$(echo "$result" | cut -d ',' -f378)
# echo -e "front: ${front:0:5}"
# echo -e "right: ${right:0:5}"
# echo -e "rear: ${rear:0:5}"
# echo -e "left: ${left:0:5}"

while [ 1 ]
 do
    echo -e "\n"
    result=$(ros2 topic echo --once --flow-style --field ranges /scan )
    front=$(echo "$result" | cut -d ',' -f3)
    left=$(echo "$result" | cut -d ',' -f128)
    rear=$(echo "$result" | cut -d ',' -f253)
    right=$(echo "$result" | cut -d ',' -f378)
    echo -e "front: ${front:0:5}"
    echo -e "right: ${right:0:5}"
    echo -e "rear: ${rear:0:5}"
    echo -e "left: ${left:0:5}"
    sleep 1
done

