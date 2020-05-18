#!/bin/bash

# make sure the log file exists 
touch /tmp/video.log
killall node
cd node
node websockettailer.js &
cd ..
cherryd -i cpapp -c prod.conf 

