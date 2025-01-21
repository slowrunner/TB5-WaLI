#!/bin/bash



if [ "$#" -ne 1 ] ;
	then echo 'Usage:  ./say.sh "string to speak" '
	exit
fi


~/TB5-WaLI/wali_ws/cmds/call_say_svc.sh "$@"

