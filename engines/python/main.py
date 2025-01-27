import os
from multiprocessing import Process, Array, Value, Lock
from ctypes import c_float
import time
import sys
import psutil
import traceback
import liblo
import pygame
from pygame.locals import *
import midi
import eyesy
import osc
import sound
import osd
from screen_main_menu import ScreenMainMenu
from screen_test import ScreenTest
from screen_video_settings import ScreenVideoSettings
from screen_palette import ScreenPalette
from screen_wifi import ScreenWiFi
from screen_applogs import ScreenApplogs
from screen_midi_settings import ScreenMIDISettings
from screen_midi_pc_mapping import ScreenMIDIPCMapping

def exitexit(code):
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
    osc.close()
    sys.exit(code)

print("starting...")

# create eyesy object
# this holds all the data (mode and preset names, knob values, midi input, sound input, current states, eyesy...)
# it gets passed to the modes which use the audio midi and knob values
eyesy = eyesy.Eyesy()

# begin init
try :     
    
    # load config
    eyesy.load_config_file()

    # setup osc and callbacks
    osc.init(eyesy)

    # midi 
    midi.init()

    # setup alsa sound shared resources
    BUFFER_SIZE = 100
    shared_buffer = Array(c_float, BUFFER_SIZE + 1, lock=True)  # Circular buffer, size + 1, last entry for trigger value
    write_index = Value('i', 0)     # Write index for the buffer
    atrig = Value('i', 0)           # audio trigger
    gain = Value('f', 0)
    lock = Lock()

    # Start the audio processing in a separate process
    audio_process = Process(target=sound.audio_processing, args=(shared_buffer, write_index, atrig, gain, lock))
    audio_process.start()

    # init pygame, this has to happen after sound is setup
    # but before the graphics stuff below
    pygame.init()
    pygame.mouse.set_visible(False)
    clocker = pygame.time.Clock() # for locking fps

    print("pygame version " + pygame.version.ver)

    # set led to running
    osc.send("/led", 0) 

    # init fb and main surface hwscreen
    print("opening frame buffer...")
    hwscreen = pygame.display.set_mode(eyesy.RES)
    eyesy.xres = hwscreen.get_width()
    eyesy.yres = hwscreen.get_height()
    print("opened screen at: " + str(hwscreen.get_size()))
    hwscreen.fill((0,0,0)) 
    pygame.display.flip()

    # screen for mode to draw on
    mode_screen = pygame.Surface((eyesy.xres,eyesy.yres))

    # eyesy gets a refrence to screen so it can save screen grabs 
    eyesy.screen = mode_screen#hwscreen
    print(str(eyesy.screen) + " " +  str(hwscreen))

    # load modes, post banner if none found
    if not (eyesy.load_modes()) :
        print("no modes found.")
        osd.loading_banner(hwscreen, "No Modes found.  Insert USB drive with Modes folder and restart.")
        while True:
            # quit on esc
            for event in pygame.event.get():
                if event.type == QUIT:
                    exitexit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exitexit(0)
            time.sleep(1)

    # run setup functions if modes have them
    print("running setup...")
    for i in range(0, len(eyesy.mode_names)) :
        print(eyesy.mode_root)
        try :
            eyesy.set_mode_by_index(i)
            mode = sys.modules[eyesy.mode]
        except AttributeError :
            print("mode not found, probably has error")
            continue 
        try : 
            osd.loading_banner(hwscreen,"Loading " + str(eyesy.mode) )
            print("setup " + str(eyesy.mode))
            mode.setup(hwscreen, eyesy)
            eyesy.memory_used = psutil.virtual_memory()[2]
        except :
            print("error in setup, or setup not found")
            continue

    # load screen grabs
    eyesy.load_grabs()

    # load scenes
    eyesy.load_scenes()

    # set font for system stuff
    eyesy.font = pygame.font.Font("font.ttf", 16)

    # get total memory consumed, cap at 75%
    eyesy.memory_used = psutil.virtual_memory()[2]
    eyesy.memory_used = (eyesy.memory_used / 75) * 100
    if (eyesy.memory_used > 100): eyesy.memory_used = 100

    # set initial mode
    eyesy.set_mode_by_index(0)
    mode = sys.modules[eyesy.mode]

    # for flashing the LED
    midi_led_flashing = False

    # menu screens, need to load after pygame
    eyesy.menu_screens["home"] = ScreenMainMenu(eyesy)
    eyesy.menu_screens["test"] = ScreenTest(eyesy)
    eyesy.menu_screens["video_settings"] = ScreenVideoSettings(eyesy)
    eyesy.menu_screens["palette"] = ScreenPalette(eyesy)
    eyesy.menu_screens["wifi"] = ScreenWiFi(eyesy)
    eyesy.menu_screens["applogs"] = ScreenApplogs(eyesy)
    eyesy.menu_screens["midi_settings"] = ScreenMIDISettings(eyesy)
    eyesy.menu_screens["midi_pc_mapping"] = ScreenMIDIPCMapping(eyesy)
    eyesy.switch_menu_screen("home")
    
    # used to measure fps
    start = time.time()

except Exception as e:
    print(traceback.format_exc())
    print("error with EYESY init")
    exitexit(0)

while 1:
 
    # quit on esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitexit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exitexit(0)
    # main loop
    try :
        # check for OSC
        # key events will be dispatched from here
        osc.recv()

        # for repeating keys held down
        eyesy.update_key_repeater()

        # check MIDI
        midi.recv(eyesy)

        # get knobs, checking for override, and check for new note on
        # for the knobs, only changes are assinged
        eyesy.update_knobs_and_notes()

        # sequence the knobs    
        # only changes assigned 
        eyesy.knob_seq_run()
        
        # fills in eyesy.knob1 etc, for the modes
        eyesy.set_knobs()

        # measure fps
        eyesy.frame_count += 1
        if ((eyesy.frame_count % 30) == 0):
            now = time.time()
            eyesy.fps = 1 / ((now - start) / 30)
            start = now
        
        # update new led
        if (eyesy.new_led) :
            osc.send("/led", eyesy.led)

        # get sound and trigger
        tmptrig = False
        with lock:
            eyesy.audio_in[:] = shared_buffer[:]
            gain.value = float(eyesy.config["audio_gain"] / 100)
            tmptrig = atrig.value
      
        # update audio trig 
        if eyesy.config["trigger_source"] == 0 and tmptrig: eyesy.trig = True
        
        # set the mode on which to call draw
        try : 
            mode = sys.modules[eyesy.mode]
        except :
            eyesy.error = "Mode " + eyesy.mode  + " not loaded, probably has errors."
            print(eyesy.error)
            # no use spitting these errors out at 30 fps
            pygame.time.wait(200)

        # save a screen shot before drawing stuff
        if (eyesy.screengrab_flag):
            eyesy.screengrab()
            
        # see if save is being held down for deleting scene
        eyesy.update_scene_save_key()

        # clear it with bg color if auto clear enabled
        if eyesy.auto_clear :
            #hwscreen.fill(eyesy.bg_color) 
            mode_screen.fill(eyesy.bg_color) 
        
        # run setup (usually if the mode was reloaded)
        if eyesy.run_setup :
            eyesy.error = ''
            try :
                mode.setup(hwscreen, eyesy)
            except Exception as e:
                eyesy.error = traceback.format_exc()
                print("error with setup: " + eyesy.error)
      
        # draw it
        if not eyesy.menu_mode :
            try :
                #mode.draw(hwscreen, eyesy)
                mode.draw(mode_screen, eyesy)
            except Exception as e:   
                eyesy.error = traceback.format_exc()
                print("error with draw: " + eyesy.error)
                # no use spitting these errors out at 30 fps
                pygame.time.wait(200)
                
            hwscreen.blit(mode_screen, (0,0))
            
        # osd
        if eyesy.show_osd and not eyesy.menu_mode:
            try :
                osd.render_overlay_480(hwscreen, eyesy)
            except Exception as e:   
                eyesy.error = traceback.format_exc()
                print("error with OSD: " + eyesy.error)
                pygame.time.wait(200)

        if eyesy.menu_mode :
            try: 
                eyesy.current_screen.handle_events()
                eyesy.current_screen.render_with_title(hwscreen)
            except Exception as e:   
                eyesy.error = traceback.format_exc()
                print("error with Menu: " + eyesy.error)
                pygame.time.wait(200)
            # menu might signal restart
            if eyesy.restart :
                print("video res changed, restarting")
                exitexit(1)
            # menu exits, clear screen
            if not eyesy.menu_mode :
                hwscreen.fill(eyesy.bg_color) 
        
        '''txt_str = " FPS:  "   + str(int(eyesy.fps)) + " "
        text = eyesy.font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.centery = 10
        hwscreen.blit(text, text_rect)'''
     
        pygame.display.flip()
        
        # clear all the events
        eyesy.clear_flags()
        osc_msgs_recv = 0
         
    except Exception as e:   
        eyesy.error = traceback.format_exc()
        print("problem in main loop")
        pygame.time.wait(200)
   
    # limit fps 30
    clocker.tick(30)

time.sleep(1)

print("Quit")

