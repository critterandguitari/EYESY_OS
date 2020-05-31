import time
import RPi.GPIO as GPIO
import os
import imp

fw_dir = os.getenv("FW_DIR")

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(1)

while True:
        if not GPIO.input(13):
            os.system("shutdown -h now")
        time.sleep(1)


