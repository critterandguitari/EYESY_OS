#!/bin/bash

# make sure the log file exists 
touch /tmp/video.log
killall node
cd node
node websockettailer.js &
cd ..
/home/music/.local/bin/cherryd -i cpapp -c prod.conf 

