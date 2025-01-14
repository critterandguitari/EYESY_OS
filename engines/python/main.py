
import os
from multiprocessing import Process, Array, Value
from ctypes import c_float
import time
import sys
import psutil
import traceback
import liblo
import pygame
from pygame.locals import *
import midi
import etc_system
import osc
import sound
import osd

print("starting...")

# create etc object
# this holds all the data (mode and preset names, knob values, midi input, sound input, current states, etc...)
# it gets passed to the modes which use the audio midi and knob values
etc = etc_system.System()

# just to make sure
etc.clear_flags()

# load config
etc.load_config_file()

# setup osc and callbacks
osc.init(etc)

# midi 
midi.init()

# setup alsa sound shared resources
BUFFER_SIZE = 100
shared_buffer = Array(c_float, BUFFER_SIZE, lock=True)  # Circular buffer
write_index = Value('i', 0)  # Write index for the buffer
lock = shared_buffer.get_lock()  # Lock for thread-safe access

# Start the audio processing in a separate process
audio_process = Process(target=sound.audio_processing, args=(shared_buffer, write_index, lock))
audio_process.start()

# init pygame, this has to happen after sound is setup
# but before the graphics stuff below
pygame.init()
pygame.mouse.set_visible(False)
clocker = pygame.time.Clock() # for locking fps

print("pygame version " + pygame.version.ver)

# on screen display and other screen helpers
osc.send("/led", 7) # set led to running

# init fb and main surfaces
print("opening frame buffer...")
os.putenv('SDL_VIDEODRIVER', "directfb")
hwscreen = pygame.display.set_mode(etc.RES)
etc.xres = hwscreen.get_width()
etc.yres = hwscreen.get_height()
print("opened screen at: " + str(hwscreen.get_size()))
hwscreen.fill((0,0,0)) 
pygame.display.flip()
osd.loading_banner(hwscreen, "")
time.sleep(2)

# etc gets a refrence to screen so it can save screen grabs 
etc.screen = hwscreen
print(str(etc.screen) + " " +  str(hwscreen))

# load modes, post banner if none found
if not (etc.load_modes()) :
    print("no modes found.")
    osd.loading_banner(hwscreen, "No Modes found.  Insert USB drive with Modes folder and restart.")
    while True:
        # quit on esc
        for event in pygame.event.get():
            if event.type == QUIT:
                exitexit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitexit()
        time.sleep(1)

# run setup functions if modes have them
print("running setup...")
for i in range(0, len(etc.mode_names)) :
    print(etc.mode_root)
    try :
        etc.set_mode_by_index(i)
        mode = sys.modules[etc.mode]
    except AttributeError :
        print("mode not found, probably has error")
        continue 
    try : 
        osd.loading_banner(hwscreen,"Loading " + str(etc.mode) )
        print("setup " + str(etc.mode))
        mode.setup(hwscreen, etc)
        etc.memory_used = psutil.virtual_memory()[2]
    except :
        print("error in setup, or setup not found")
        continue

# load screen grabs
etc.load_grabs()

# load scenes
etc.load_scenes()

# used to measure fps
start = time.time()

# set font for system stuff
etc.font = pygame.font.Font("font.ttf", 16)

# get total memory consumed, cap at 75%
etc.memory_used = psutil.virtual_memory()[2]
etc.memory_used = (etc.memory_used / 75) * 100
if (etc.memory_used > 100): etc.memory_used = 100

# set initial mode
etc.set_mode_by_index(0)
mode = sys.modules[etc.mode]

# for flashing the LED
midi_led_flashing = False

def exitexit():
    print("EXIT exiting\n")
    pygame.display.quit()
    pygame.quit()
    print("stopping audio process")
    if audio_process.is_alive():  # Check if the process is still running
        audio_process.terminate()  # Terminate the process
        audio_process.join()       # Ensure the process has fully terminated
    print("closing audio")
    audio_process.close()  # Now it's safe to close the process
    midi.close()
    sys.exit(0)

def exitexit_restart():
    print("EXIT for restart\n")
    pygame.display.quit()
    pygame.quit()
    print("stopping audio process")
    if audio_process.is_alive():  # Check if the process is still running
        audio_process.terminate()  # Terminate the process
        audio_process.join()       # Ensure the process has fully terminated
    print("closing audio")
    audio_process.close()  # Now it's safe to close the process
    midi.close()
    sys.exit(1)

# menu screens
osd.loading_banner(hwscreen,"Loading menu")
try :
    from screen_main_menu import ScreenMainMenu
    from screen_test import ScreenTest
    from screen_video_settings import ScreenVideoSettings
    from screen_palette import ScreenPalette
    from screen_wifi import ScreenWiFi
    from screen_applogs import ScreenApplogs
    from screen_midi_settings import ScreenMIDISettings
    from screen_midi_pc_mapping import ScreenMIDIPCMapping

    etc.menu_screens["home"] = ScreenMainMenu(etc)
    etc.menu_screens["test"] = ScreenTest(etc)
    etc.menu_screens["video_settings"] = ScreenVideoSettings(etc)
    etc.menu_screens["palette"] = ScreenPalette(etc)
    etc.menu_screens["wifi"] = ScreenWiFi(etc)
    etc.menu_screens["applogs"] = ScreenApplogs(etc)
    etc.menu_screens["midi_settings"] = ScreenMIDISettings(etc)
    etc.menu_screens["midi_pc_mapping"] = ScreenMIDIPCMapping(etc)
    etc.switch_menu_screen("home")
except Exception as e:
    print(traceback.format_exc())
    print("error loading menu screens")
    exitexit()

# We'll use a simple state machine for the sequencer:
# States:
#   "stopped": Doing nothing, knobs pass through normally.
#   "recording": Key2 is held; we're recording each frame's knob values into knob_sequence.
#   "playing": Playing back the recorded sequence in a loop.
#
# Transitions:
#   stopped -> (Key2 press) -> recording (clear the old sequence and start a new one)
#   recording -> (Key2 release) -> playing (if we have recorded data, otherwise back to stopped)
#   playing -> (Key2 press) -> stopped
#
# In "stopped" state: do nothing special.
# In "recording" state: record current knob values each frame.
# In "playing" state: set knobs from the recorded sequence each frame.

knob_sequence = []
playback_index = 0
prev_key2_status = False
sequencer_state = "stopped"

def knob_sequencer(etc):
    global knob_sequence, playback_index, prev_key2_status, sequencer_state
    
    key2 = etc.key2_status

    # Detect key2 transitions
    key2_pressed = (key2 and not prev_key2_status)
    key2_released = (not key2 and prev_key2_status)

    if sequencer_state == "stopped":
        # If stopped and key2 is pressed, start recording
        if key2_pressed:
            # Clear old sequence and start fresh
            knob_sequence = []
            sequencer_state = "recording"
            playback_index = 0

    elif sequencer_state == "recording":
        # While recording, store knob values every frame
        if key2_released:
            # Key2 released, stop recording
            if len(knob_sequence) > 0:
                # If we have something recorded, start playing
                sequencer_state = "playing"
                playback_index = 0
            else:
                # Nothing recorded, go back to stopped
                sequencer_state = "stopped"
        else:
            # Still recording - add current knob values
            frame_values = (etc.knob1, etc.knob2, etc.knob3, etc.knob4, etc.knob5)
            knob_sequence.append(frame_values)

    elif sequencer_state == "playing":
        # If playing back, set knobs to the recorded sequence
        if key2_pressed:
            # Key2 pressed while playing => stop
            sequencer_state = "stopped"
        else:
            # Continue playback
            if len(knob_sequence) > 0:
                current_values = knob_sequence[playback_index]
                etc.knob1, etc.knob2, etc.knob3, etc.knob4, etc.knob5 = current_values
                
                playback_index += 1
                if playback_index >= len(knob_sequence):
                    playback_index = 0
            else:
                # No sequence data? Just stop
                sequencer_state = "stopped"

    prev_key2_status = key2

while 1:
 
    # quit on esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitexit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exitexit()

    # check for OSC
    osc.recv()

    # check MIDI
    midi.recv(etc)
    
    # stop a midi led flash if one is hapenning
    if (midi_led_flashing):
        midi_led_flashing = False
        osc.send("/led", 7)

    if (etc.new_midi) :
        osc.send("/led", 2)
        midi_led_flashing = True

    # get knobs, checking for override, and check for new note on
    etc.update_knobs_and_notes()

    # check for midi program change
    etc.check_pgm_change()
    
    # measure fps
    etc.frame_count += 1
    if ((etc.frame_count % 50) == 0):
        now = time.time()
        etc.fps = 1 / ((now - start) / 50)
        #print(etc.fps)
        start = now

    # check for sound
    with lock:
        etc.audio_in[:] = shared_buffer[:]

    # set the mode on which to call draw
    try : 
        mode = sys.modules[etc.mode]
    except :
        etc.error = "Mode " + etc.mode  + " not loaded, probably has errors."
        print(etc.error)
        # no use spitting these errors out at 30 fps
        pygame.time.wait(200)

    # save a screen shot before drawing stuff
    if (etc.screengrab_flag):
        osc.send("/led", 3) # flash led yellow
        etc.screengrab()
        osc.send("/led", 7)
        
    # see if save is being held down for deleting scene
    etc.update_scene_save_key()

    # shift - sequence the knobs
    #knob_sequencer(etc)

    # clear it with bg color if auto clear enabled
    if etc.auto_clear :
        hwscreen.fill(etc.bg_color) 
    
    # run setup (usually if the mode was reloaded)
    if etc.run_setup :
        etc.error = ''
        try :
            mode.setup(hwscreen, etc)
        except Exception as e:
            etc.error = traceback.format_exc()
            print("error with setup: " + etc.error)
   
    # draw it
    if not etc.show_menu :
        try :
            mode.draw(hwscreen, etc)
        except Exception as e:   
            etc.error = traceback.format_exc()
            print("error with draw: " + etc.error)
            # no use spitting these errors out at 30 fps
            pygame.time.wait(200)
            
        #hwscreen.blit(screen, (0,0))
        
    # osd
    if etc.show_osd :
        try :
            osd.render_overlay_480(hwscreen, etc)
        except Exception as e:   
            etc.error = traceback.format_exc()
            print("error with OSD: " + etc.error)
            pygame.time.wait(200)

    if etc.show_menu :
        try: 
            etc.current_screen.handle_events()
            etc.current_screen.render_with_title(hwscreen)
        except Exception as e:   
            etc.error = traceback.format_exc()
            print("error with Menu: " + etc.error)
            pygame.time.wait(200)
        if etc.restart :
            print("video res changed, restarting")
            exitexit_restart()
        #if etc.key8_press:
        #    print("menu screenshot")
        #    etc.screengrab()
 
    pygame.display.flip()

    if etc.quit :
        exitexit()
    
    # clear all the events
    etc.clear_flags()
    osc_msgs_recv = 0
    
    #draw the main screen, limit fps 30
    clocker.tick(30)

time.sleep(1)

print("Quit")

