#!/bin/sh -e

# keep it fast
echo -n performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# disable status led after bootup
#echo none > /sys/class/leds/led0/trigger

# redirect 80 to 8080 for the web server
iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080

exit 0
