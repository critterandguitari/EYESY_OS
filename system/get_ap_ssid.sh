#!/bin/bash

AP_FILE="/sdcard/System/ap.txt"

if [ -f "$AP_FILE" ]; then
#    echo "$AP_FILE exists"
    NET=$(head -n 1 $AP_FILE)
    PW=$(tail -n 1 $AP_FILE)
else 
#    echo "$AP_FILE does not exist, using default"
    NET=EYESY
    PW=coolmusic
fi

echo $NET


