#!/bin/bash
export LUA_PATH="/home/music/EYESY_OS/engines/oflua/?.lua;;"

# make sure log ownership is not root
sudo chown music:music /tmp/video.log

cd /home/music/EYESY_OS/engines/oflua/eyesy
stdbuf -o0 bin/eyesy &> /tmp/video.log
