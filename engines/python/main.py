import pygame
import time
import etc_system
import traceback
import sys
import psutil
#from pygame.locals import *
import osc
import sound
import osd
import liblo
import os
print "starting..."

# create etc object
# this holds all the data (mode and preset names, knob values, midi input, sound input, current states, etc...)
# it gets passed to the modes which use the audio midi and knob values
etc = etc_system.System()

# just to make sure
etc.clear_flags()

# setup osc and callbacks
osc.init(etc)

# setup alsa sound
sound.init(etc)

# init pygame, this has to happen after sound is setup
# but before the graphics stuff below
pygame.init()
clocker = pygame.time.Clock() # for locking fps

print "pygame version " + pygame.version.ver

# on screen display and other screen helpers
osd.init(etc)
osc.send("/led", 7) # set led to running

# init fb and main surfaces
print "opening frame buffer..."
#os.putenv('SDL_VIDEODRIVER', "directfb")
#hwscreen = pygame.display.set_mode(etc.RES,  pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED, 32)
hwscreen = pygame.display.set_mode(etc.RES,  pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
#hwscreen = pygame.display.set_mode(etc.RES,  pygame.FULLSCREEN | pygame.DOUBLEBUF, 32)
screen = pygame.Surface(hwscreen.get_size())
etc.xres=hwscreen.get_width()
etc.yres=hwscreen.get_height()
print "opened screen at: " + str(hwscreen.get_size())
screen.fill((0,0,0)) 
hwscreen.blit(screen, (0,0))
pygame.display.flip()
hwscreen.blit(screen, (0,0))
pygame.display.flip()
osd.loading_banner(hwscreen, "")
time.sleep(2)

# etc gets a refrence to screen so it can save screen grabs 
etc.screen = screen
print str(etc.screen) + " " +  str(screen)

# load modes, post banner if none found
if not (etc.load_modes()) :
    print "no modes found."
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
print "running setup..."
for i in range(0, len(etc.mode_names)) :
    print etc.mode_root
    try :
        etc.set_mode_by_index(i)
        mode = sys.modules[etc.mode]
    except AttributeError :
        print "mode not found, probably has error"
        continue 
    try : 
        osd.loading_banner(hwscreen,"Loading " + str(etc.mode) )
        print "setup " + str(etc.mode)
        mode.setup(screen, etc)
        etc.memory_used = psutil.virtual_memory()[2]
    except :
        print "error in setup, or setup not found"
        continue

# load screen grabs
etc.load_grabs()

# load scenes
etc.load_scenes()

# used to measure fps
start = time.time()

# get total memory consumed, cap at 75%
etc.memory_used = psutil.virtual_memory()[2]
etc.memory_used = (etc.memory_used / 75) * 100
if (etc.memory_used > 100): etc.memory_used = 100

# set initial mode
etc.set_mode_by_index(0)
mode = sys.modules[etc.mode]

midi_led_flashing = False

def exitexit() :
    print "EXIT exiting\n"
    pygame.display.quit()
    pygame.quit()
    sys.exit()

while 1:
    
    # check for OSC
    osc.recv()

    # send get midi and knobs for next time
    #osc.send("/nf", 1) 

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

    # quit on esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitexit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exitexit()

    # measure fps
    etc.frame_count += 1
    if ((etc.frame_count % 50) == 0):
        now = time.time()
        etc.fps = 1 / ((now - start) / 50)
        start = now

    # check for sound
    sound.recv()

    # set the mode on which to call draw
    try : 
        mode = sys.modules[etc.mode]
    except :
        etc.error = "Mode " + etc.mode  + " not loaded, probably has errors."
        print etc.error
        # no use spitting these errors out at 30 fps
        pygame.time.wait(200)

    # save a screen shot before drawing stuff
    if (etc.screengrab_flag):
        osc.send("/led", 3) # flash led yellow
        etc.screengrab()
        osc.send("/led", 7)
        
    # see if save is being held down for deleting scene
    etc.update_scene_save_key()

    # clear it with bg color if auto clear enabled
    if etc.auto_clear :
        screen.fill(etc.bg_color) 
    
    # run setup (usually if the mode was reloaded)
    if etc.run_setup :
        etc.error = ''
        try :
            mode.setup(screen, etc)
        except Exception, e:
            etc.error = traceback.format_exc()
            print "error with setup: " + etc.error
   
    # draw it
    try :
        mode.draw(screen, etc)
    except Exception, e:   
        etc.error = traceback.format_exc()
        print "error with draw: " + etc.error
        # no use spitting these errors out at 30 fps
        pygame.time.wait(200)
        
    hwscreen.blit(screen, (0,0))
    
    # osd
    if etc.osd :
        osd.render_overlay_480(hwscreen)

    if etc.shift :
        osd.render_shift_overlay(hwscreen)
    
    pygame.display.flip()

    if etc.quit :
        exitexit()
    
    # clear all the events
    etc.clear_flags()
    osc_msgs_recv = 0
    
    #draw the main screen, limit fps 30
    clocker.tick(30)

time.sleep(1)

print "Quit"

