#!/bin/bash

# end old one
pkill -f "controls"

nohup ./controls &> /dev/null &
