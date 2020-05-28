#!/bin/bash

# make sure log ownership is not root
sudo chown music:music /tmp/video.log

cd /home/music/EYESY_OS/engines/python 
stdbuf -o0 python main.py &> /tmp/video.log 
