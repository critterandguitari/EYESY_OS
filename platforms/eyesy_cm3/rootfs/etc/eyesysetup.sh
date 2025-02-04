#!/bin/sh -e

# keep it fast
echo -n performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# disable status led after bootup
echo none | sudo tee /sys/class/leds/ACT/trigger

# Check HDMI status using kmsprint
if kmsprint | grep -q "HDMI-A-1 (connected)"; then
    echo "HDMI is connected, skipping composite activation."
else
    echo "HDMI not connected, enabling composite video."
    echo "on" | sudo tee /sys/class/drm/card0-Composite-1/status
fi

# redirect 80 to 8080 for the web server
iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080

exit 0
