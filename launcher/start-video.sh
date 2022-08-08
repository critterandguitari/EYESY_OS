#!/bin/bash


if [ -f /sdcard/System/engine.txt ]; then
    echo "checking engine file"
    read -r firstline</sdcard/System/engine.txt
    echo $firstline
    if [ $firstline == "oflua" ]; then
        echo "starting oflua"
    	/home/music/EYESY_OS/engines/oflua/run.sh
    else 
        echo "starting python"
    	/home/music/EYESY_OS/engines/python/run.sh
    fi
else
    echo "engine file not found, defaulting to python"
    /home/music/EYESY_OS/engines/python/run.sh
    exit 0
fi
