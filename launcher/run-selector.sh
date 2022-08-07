#!/bin/bash

sudo killall eyesy
sudo killall selector
sudo killall pd

cd /home/music/EYESY_OS/engines/oflua/pd
/usr/bin/pd -nogui -alsamidi -midiindev 1 -midioutdev 1 -noaudio eyesy.pd &> /dev/null &

cd /home/music/openFrameworks/apps/myApps/selector
stdbuf -o0 bin/selector &> /tmp/video.log &
