#!/bin/bash
cd /home/music/openFrameworks/apps/myApps/eyesy
stdbuf -o0 make run &> /tmp/video.log
