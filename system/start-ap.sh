#!/bin/bash
systemctl stop wpa_supplicant
systemctl stop dhcpcd

AP_FILE="/sdcard/System/ap.txt"

if [ -f "$AP_FILE" ]; then
    echo "$AP_FILE exists"
    NET=$(head -n 1 $AP_FILE)
    PW=$(tail -n 1 $AP_FILE)
else 
    echo "$AP_FILE does not exist, using default"
    NET=EYESY
    PW=coolmusic
fi

/home/music/EYESY_OS/system/create_ap --no-virt -n wlan0 $NET $PW

