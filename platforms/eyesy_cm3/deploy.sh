#!/bin/bash

# copy files
mkdir tmp
cp -r rootfs tmp/
chown -R root:root tmp/rootfs
chown -R music:music tmp/rootfs/home/music
cp -fr --preserve=mode,ownership tmp/rootfs/* /
rm -fr tmp
sync

# configure systemd stuff
systemctl enable eyesy-oflua.service  
systemctl enable cherrypy.service  
systemctl enable eyesy-pd.service  
systemctl disable eyesy-python.service  
systemctl enable splashscreen.service  
systemctl enable ttymidi.service  

# networking started by eyesy-pd
systemctl disable dhcpcd.service
systemctl disable wpa_supplicant.service
systemctl disable createap.service  

systemctl daemon-reload
