#!/bin/bash

# redirect 80 -> 8080
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080

# Stop previously running instance of waitress-serve for this app
pkill -f "waitress-serve --port=8080 app:app"

# Start a new one in the background, directing all output to /tmp/web.log
nohup /home/music/.local/bin/waitress-serve --port=8080 app:app > /tmp/web.log 2>&1 &

echo "Application restarted with Waitress and logging to /tmp/web.log"

