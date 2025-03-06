#!/bin/bash

d=`(date +"%Y-%m-%d")`
echo -e $d
cp life.log ${d}_life.log
cp odometer.log ${d}_odometer.log
cp say.log ${d}_say.log

