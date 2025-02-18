#!/bin/bash

# copy files
mkdir tmp
cp -r rootfs tmp/
chown -R root:root tmp/rootfs
cp -fr --preserve=mode,ownership tmp/rootfs/* /
rm -fr tmp
sync

# configure systemd stuff
#systemctl enable splashscreen.service  
systemctl enable ttymidi.service  
systemctl enable eyesyweb.service
systemctl enable eyesyhw.service
systemctl enable eyesysetup.service
systemctl enable eyesypy.service
systemctl enable eyesypower.service

# configure other stuff
#systemctl disable NetworkManager-wait-online.service

systemctl daemon-reload
