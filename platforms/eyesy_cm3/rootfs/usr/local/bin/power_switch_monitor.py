#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import os
import imp

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(1)

while True:
        if not GPIO.input(13):
            print("SHUTTING DOWN")
            os.system("systemctl stop eyesypy.service")
            os.system("systemctl stop eyesyhw.service")
            os.system("systemctl stop eyesyweb.service") 
            os.system("systemctl stop ttymidi.servic")
            os.system("systemctl stop eyesysetup.service") 
            os.system("shutdown -h now")
        time.sleep(1)


