import pygame
import pygame.midi
from pygame.locals import *

midi_input = None
etc = None
cc_last = [0] * 5
pgm_last = 0

def parse_midi(midi):
    global etc, cc_last, pgm_last

    for msg in midi:
        midi_msg = msg[0]
        msg_status = int(midi_msg[0])
        msg_channel = msg_status & 0xf
        msg_type = (msg_status >> 4) & 0xf
   
        # global message clock tick
        if (msg_status == 248) :
            etc.new_midi = True
            etc.midi_clk += 1
            if (etc.midi_clk >= 24) : etc.midi_clk = 0

        # global message clock start
        if (msg_status == 250) :
            etc.new_midi = True
            etc.midi_clk = 0

        # channel messages
        if ( (msg_channel == (etc.midi_ch - 1)) or (etc.midi_ch == 0)) :
            
            # CC
            if (msg_type == 0xB) :
                etc.new_midi = True
                for i in range(0,5) :
                    if (midi_msg[1] == 21 + i) :
                        cc = midi_msg[2]
                        if cc != cc_last[i] :
                            etc.cc_override_knob(i, float(cc) / 127)
                            cc_last[i] = cc
 
            # note OFF
            if (msg_type == 0x8) :
                etc.new_midi = True
                etc.midi_notes[midi_msg[1]] = 0

            # note ON
            if (msg_type == 0x9) :
                etc.new_midi = True
                if (midi_msg[2] > 0) :
                    etc.midi_notes[midi_msg[1]] = 1
                else :
                    etc.midi_notes[midi_msg[1]] = 0

            # PGM
            if (msg_type == 0xC) :
                etc.new_midi = True
                pgm = midi_msg[1]
                if (pgm != pgm_last):
                    etc.midi_pgm = pgm
                    pgm_last = pgm


def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        etc.usb_midi_name = name
    
        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))


def init(etc_obj) :
    global etc, midi_input
    etc = etc_obj

    pygame.midi.init()

    try :
        _print_device_info()

        input_id = pygame.midi.get_default_input_id()

        print ("using input_id :%s:" % input_id)
        midi_input = pygame.midi.Input( input_id )
        etc.usb_midi_present = True
    except :
        print "no usb midi found"
        etc.usb_midi_present = False

def poll():
    global midi_input
    if (etc.usb_midi_present) :
        if midi_input.poll():
            midi_events = midi_input.read(100)
            try :
                parse_midi(midi_events)
            except :
                print "problem with usb midi"
