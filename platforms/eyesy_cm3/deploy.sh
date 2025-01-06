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
#systemctl enable splashscreen.service  
#systemctl enable ttymidi.service  
#systemctl daemon-reload
