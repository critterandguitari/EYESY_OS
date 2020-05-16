#!/usr/bin/env python

"""Contains an example of midi input, and a separate example of midi output.

By default it runs the output example.
python midi.py --output
python midi.py --input

"""

import sys
import os
import time
import pygame
import pygame.midi
from pygame.locals import *

def parse_midi(midi):
    etc_ch = 1

    for msg in midi:
        midi_msg = msg[0]
        msg_status = int(midi_msg[0])
        msg_channel = msg_status & 0xf
        msg_type = (msg_status >> 4) & 0xf
        print "channel: " + str(msg_channel) + " type: " + str(msg_type)
   
        # global message clock tick
        if (msg_status == 248) :
            print "new clock"

        # global message clock start
        if (msg_status == 250) :
            print "new start"

        # channel messages
        if (msg_channel == etc_ch) :
            if (msg_type == 0xB) :
                print "new CC"

            if (msg_type == 0x8) :
                print "new note off"

            if (msg_type == 0x9) :
                print "new note on"

            if (msg_type == 0xC) :
                print "new pgm"


def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))

#def input_main(device_id = None):
#pygame.init()

pygame.midi.init()

_print_device_info()

device_id = None

if device_id is None:
    input_id = pygame.midi.get_default_input_id()
else:
    input_id = device_id

print ("using input_id :%s:" % input_id)
i = pygame.midi.Input( input_id )

going = True
while going:

    if i.poll():
        midi_events = i.read(100)
        parse_midi(midi_events)

    time.sleep(.03)
del i
pygame.midi.quit()


