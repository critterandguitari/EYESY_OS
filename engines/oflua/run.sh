#!/bin/bash
export LUA_PATH="/home/music/EYESY_OS/engines/oflua/?.lua;;"
cd /home/music/openFrameworks/apps/myApps/eyesy
stdbuf -o0 make run &> /tmp/video.log
