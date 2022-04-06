#!/bin/bash

/usr/bin/pd -nogui -alsamidi -midiindev 1 -midioutdev 1 -noaudio eyesy.pd &> /dev/null 

