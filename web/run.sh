#!/bin/bash

# make sure the log file exists 
touch /tmp/video.log
killall node
cd node
node websockettailer.js &
cd ..
# redirect 80 -> 8080
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080
/usr/sbin/cherryd -i cpapp -c prod.conf 

