#!/bin/bash
#export XAUTHORITY=/var/tmp/.Xauthority_$USER
cd /home/music/EYESY_OS/engines/python 
stdbuf -o0 python main.py &> /tmp/video.log 
