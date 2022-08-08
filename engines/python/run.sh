#!/bin/bash

# make sure log ownership is not root
sudo chown music:music /tmp/video.log

sudo killall eyesy
sudo killall pd
sudo killall selector

cd /home/music/EYESY_OS/engines/python/pd
/usr/bin/pd -nogui -alsamidi -midiindev 1 -midioutdev 1 -noaudio eyesy.pd &> /dev/null &

cd /home/music/EYESY_OS/engines/python 
sudo stdbuf -o0 python main.py &> /tmp/video.log

