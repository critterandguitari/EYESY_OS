#!/bin/bash

# make sure log ownership is not root
sudo chown music:music /tmp/video.log

# cd and run it
cd /home/music/EYESY_OS/engines/python 
nohup stdbuf -o0 python -u main.py &> /tmp/video.log 

