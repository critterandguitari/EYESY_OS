#!/bin/bash

# connect ttymidi input to Pd
aconnect "ttymidi:0" "Pure Data:0"

# check for usb midi device and connect first one found
python usbmidi.py
