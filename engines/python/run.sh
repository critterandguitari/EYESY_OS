#!/bin/bash
cd /home/music/EYESY_OS/engines/python 
export DISPLAY=:0
stdbuf -o0 python main.py &> /tmp/video.log 
