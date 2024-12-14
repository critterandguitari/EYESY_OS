#!/bin/bash

# make sure log ownership is not root
sudo chown music:music /tmp/video.log

# end old one
pkill -f "sudo stdbuf -o0 python -u main.py"

sleep 1

cd /home/music/EYESY_OS/engines/python 
nohup sudo stdbuf -o0 python -u main.py &> /tmp/video.log &

