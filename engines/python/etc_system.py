import fileinput
import random
import math
import pygame
import traceback
import imp
import os
import glob
import sys
import helpers
import csv
import color_palettes

class System:

    GRABS_PATH = "/sdcard/Grabs/"
    MODES_PATH = "/sdcard/Modes/Python/"
    SCENES_PATH = "/sdcard/Scenes.csv"

    #RES =  (720,480)
    #RES =  (800,600)
    #RES =  (320,240)
    RES =  (1280,720)
    #RES =  (1920,1080)
    #RES =  (640,480)
    #RES =  (0,0)

    # this is just an alias to the screen in main loop
    screen = None

    fps = 0
    frame_count = 0
    
    xres = 1280
    yres = 720

    # some colors we use
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LGRAY = (200, 200, 200)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    OSDBG = (0,0,255)

    # screen grabs
    lastgrab = None
    lastgrab_thumb = None
    tengrabs_thumbs = []
    grabcount = 0
    grabindex = 0
    screengrab_flag = False
    
    # modes
    mode_names = []  # list of mode names pupulated from Modes folder on USB drive
    mode_index = 0   # index of current mode
    mode = ''        # name of current mode
    mode_root = ''   # root path of current mode
    error = ''       # errors that happend during setup() or run()
    run_setup = False # flag to signal main loop to run setup() usually if a mode was reloaded

    #scenes
    scenes = []     # 
    scene_index = 0
    save_key_status = False
    save_key_count = 0
    scene_set = False
    
    # audio
    audio_in = [0] * 100
    audio_peak = 0
    audio_trig = False
    audio_scale = 1.0
    audio_trig_enable = True

    # knobs a used by mode 
    knob1 = 0
    knob2 = 1
    knob3 = 1
    knob4 = 1
    knob5 = 1
   
    # knob values used internally
    knob = [.2] * 5
    knob_hardware = [.2] * 5
    knob_snapshot = [.2] * 5
    knob_override = [False] * 5

    # midi stuff (CC gets updated into knobs
    midi_notes = [0] * 128
    midi_notes_last = [0] * 128
    midi_note_new = False
    midi_pgm = 0
    midi_pgm_last = 0
    midi_clk = 0
    midi_ch = 1
    new_midi = False
    usb_midi_name = ''
    usb_midi_present = False

    # system stuff 
    memory_used = 0
    ip = ''
    auto_clear = True
    bg_color = (0, 0, 0)
    quit = False
    show_osd = False
    show_menu = False
    osd_menu_select = 0  # 0 for regular, 1 for OSD overlay, 2 for settings menu
    osd_first = False # when osd is first turned on this is used to gather info
    trig_button = False # if the button is held down or not

    # menu stuff
    current_screen = None
    menu_screens = {}
    # Key flags
    key1_press = False
    key2_press = False
    key3_press = False
    key4_press = False
    key5_press = False
    key6_press = False
    key7_press = False
    key8_press = False
    key9_press = False
    key10_press = False
    
    key2_status = False  # shift key pressed or not

    # color stuff
    palettes = color_palettes.abcd_palettes
    palette = 0;

    def update_trig_button(self, stat) :
        if (stat > 0 ):
            self.audio_trig = True
            self.trig_button = True
        else :
            self.trig_button = False

    def set_osd(self, stat) :
        self.show_osd = stat
        self.osd_first = True

    def toggle_menu(self) :
        if self.show_menu:
            self.show_menu = False
            self.set_osd(False)
        else :
            self.set_osd(False)
            self.show_menu = True
            self.switch_menu_screen("home")
            print("enable menu home screen")
       
    # run the pre and post logic function for a screen when entering / leaving
    def switch_menu_screen(self,s) :
        if self.current_screen is not None: self.current_screen.after()
        self.current_screen = self.menu_screens[s]
        self.current_screen.before()

    def toggle_osd(self) :
        if self.show_osd or self.show_menu:
            self.show_menu = False
            self.set_osd(False)
        else :
            self.set_osd(True)
            self.show_menu = False

        #self.osd_menu_select += 1
        #if self.osd_menu_select == 3: self.osd_menu_select = 0

        #if self.osd_menu_select == 0:
        #    self.set_osd(False)
        #    self.show_menu = False

        #if self.osd_menu_select == 1:
        #    self.set_osd(True)
        #    self.show_menu = False

        #if self.osd_menu_select == 2:
        #    self.set_osd(False)
        #    self.show_menu = True

    def toggle_auto_clear(self):
        if not self.auto_clear :
            self.auto_clear = True
        else :
            self.auto_clear = False

    def set_mode_by_index (self, index) :
        self.mode_index = index
        self.mode = self.mode_names[self.mode_index]
        self.mode_root = self.MODES_PATH + self.mode + "/"
        print("setting mode: " + self.mode_root)
        self.error = ''

    def set_mode_by_name (self, name) :
        self.mode = name 
        self.mode_index = self.mode_names.index(name)
        self.mode_root = self.MODES_PATH + self.mode + "/"
        print("setting mode: " + self.mode_root)
        self.error = ''

    def next_mode (self) :
        self.mode_index += 1
        if self.mode_index >= len(self.mode_names) : 
            self.mode_index = 0
        self.set_mode_by_index(self.mode_index)
        self.scene_set = False

    def prev_mode (self) :
        self.mode_index -= 1
        if self.mode_index < 0 : 
            self.mode_index = len(self.mode_names) - 1
        self.set_mode_by_index(self.mode_index)
        self.scene_set = False

    def next_palette (self) :
        self.palette += 1
        if self.palette >= len(self.palettes) : 
            self.palette = 0

    def prev_palette (self) :
        self.palette -= 1
        if self.palette < 0 : 
            self.palette = len(self.palettes) - 1

    def override_all_knobs(self) :
        for i in range(0,5):
            self.knob_override[i] = True
            self.knob_snapshot[i] = self.knob_hardware[i]
    
    def cc_override_knob(self, i, v) :
        self.knob_override[i] = True
        self.knob_snapshot[i] = self.knob_hardware[i]
        self.knob[i] = v

    # then do this for the modes 
    def update_knobs_and_notes(self) :
        for i in range(0, 5) :
            if self.knob_override[i] :
                if abs(self.knob_snapshot[i] - self.knob_hardware[i]) > .05 :
                    self.knob_override[i] = False
                    self.knob[i] = self.knob_hardware[i]
                    self.scene_set = False
            else : 
                self.knob[i] = self.knob_hardware[i]

        # fill these in for convinience
        self.knob1 = self.knob[0]
        self.knob2 = self.knob[1]
        self.knob3 = self.knob[2]
        self.knob4 = self.knob[3]
        self.knob5 = self.knob[4]

        # check for new notes
        for i in range(0, 128):
            if self.midi_notes[i] > 0 and self.midi_notes_last[i] == 0:
                self.midi_note_new = True

        # very last midi note controls auto clear
        if (self.midi_notes[127] > 0 and self.midi_notes_last[127] == 0):
            if (self.auto_clear) : self.auto_clear = False
            else : self.auto_clear = True

    def foot_pressed(self) :
        if (len(self.scenes) > 0) :
            self.next_scene()
        else :
            self.next_mode()

    def check_pgm_change(self):
        if (self.midi_pgm != self.midi_pgm_last):
            print("got pgm " + str(self.midi_pgm))
            self.midi_pgm_last = self.midi_pgm
            if (len(self.scenes) > 0) :
                self.scene_index = self.midi_pgm % len(self.scenes)
                self.recall_scene(self.scene_index)
            else :
                self.mode_index = self.midi_pgm % len(self.mode_names)
                self.set_mode_by_index(self.mode_index)

    # save a screenshot
    def screengrab(self):
        filenum = 0
        imagepath = self.GRABS_PATH + str(filenum) + ".jpg"
        while os.path.isfile(imagepath):
            filenum += 1
            imagepath = self.GRABS_PATH + str(filenum) + ".jpg"
        pygame.image.save(self.screen,imagepath)
        # make sure it is saved as 'music' user, uid=gid=1000
        os.chown(imagepath, 1000, 1000)
        # add to the grabs array
        self.grabindex += 1
        self.grabindex %= 5
        pygame.transform.scale(self.screen, (128, 72), self.tengrabs_thumbs[self.grabindex] )
        self.lastgrab = self.screen.copy()
        self.lastgrab_thumb = self.tengrabs_thumbs[self.grabindex]
        print("grabbed " + imagepath)

    # load modes,  check if modes are found
    def load_modes(self):
        print("loading modes...")
        got_a_mode = False # at least one mode
        mode_folders = sorted(helpers.get_immediate_subdirectories(self.MODES_PATH), key=lambda s: s.lower() )

        for mode_folder in mode_folders :
            mode_name = str(mode_folder)
            mode_path = self.MODES_PATH+mode_name+'/main.py'
            print(mode_path)
            try :
                imp.load_source(mode_name, mode_path)
                self.mode_names.append(mode_name)
                got_a_mode = True
            except Exception as e:
                print(traceback.format_exc())
        return got_a_mode

    # load a new mode (created from web editor)
    def load_new_mode(self, new_mode) :
        print("loadeing new mode "+new_mode+"...")
        mode_path = self.MODES_PATH+new_mode+'/main.py'
        try :
            imp.load_source(new_mode, mode_path)
            self.mode_names.append(new_mode)
        except Exception as e:
            print(traceback.format_exc())
        self.set_mode_by_name(new_mode)
        self.run_setup
    
    # reload mode module
    def reload_mode(self) :
        # delete the old, and reload
        if self.mode in sys.modules:  
            del(sys.modules[self.mode]) 
        print("deleted module, reloading")
        try :
            imp.load_source(self.mode, self.mode_root+'/main.py')
            print("reloaded")
        except Exception as e:
            self.error = traceback.format_exc()
            print("error reloading: " + self.error)
        self.run_setup = True # set a flag so setup gets run from main loop
    
    # recent grabs, first check if Grabs folder is available, create if not
    def load_grabs(self):
        if not(os.path.isdir(self.GRABS_PATH)) :
            print('No grab folder, creating...')
            os.system('mkdir ' + self.GRABS_PATH)
        # make sure it is saved as 'music' user, uid=gid=1000
        os.chown(self.GRABS_PATH, 1000, 1000)
        print('loading recent grabs...')
        self.lastgrab = None
        self.lastgrab_thumb = None
        self.tengrabs_thumbs = []
        self.grabcount = 0
        self.grabindex = 0
        for i in range(0,11):
            self.tengrabs_thumbs.append(pygame.Surface((128, 72)))
        
        self.lastgrab = pygame.Surface(self.RES )
        self.lastgrab_thumb = pygame.Surface((128,72) )

        for filepath in sorted(glob.glob(self.GRABS_PATH + '*.jpg')):
            try :
                filename = os.path.basename(filepath)
                print('loading grab: ' + filename)
                img = pygame.image.load(filepath)
                img = img.convert()
                thumb = pygame.transform.scale(img, (128, 72) )
                self.lastgrab = img
                self.lastgrab_thumb = thumb
                self.tengrabs_thumbs[self.grabcount] = thumb
                self.grabcount += 1
            except Exception as e:
                self.error = traceback.format_exc()
                print("error loading grab: " + self.error)
            if self.grabcount > 10: break

    # called from main loop
    def update_scene_save_key(self):
        if self.save_key_status :
            self.save_key_count += 1
            if (self.save_key_count > 30) : # held down for 60 frames, delete the scene
                self.delete_current_scene()
                self.save_key_status = False

    def save_or_delete_scene(self, key_stat):
        if key_stat > 0 :
            self.save_key_status = True
            self.save_key_count = 0
        else :
            if (self.save_key_status) :  # key release before delete happens
                self.save_scene()
            self.save_key_status = False
                
    def delete_current_scene(self):
        print("deleting scene")
        if len(self.scenes) > 0:
            del self.scenes[self.scene_index]
            if self.scene_index >= len(self.scenes):
                self.scene_index = len(self.scenes) - 1
            self.recall_scene(self.scene_index)
            self.write_all_scenes()
        #print "deleted scene: " + str(self.scene_index)

    def save_scene(self):
        print("saving scene")
        self.scenes.append([self.mode, self.knob1, self.knob2, self.knob3, self.knob4, self.knob5, self.auto_clear])
        self.write_all_scenes()
        # and set it to most recent
        self.recall_scene(len(self.scenes) - 1)

    def write_all_scenes(self):
            # write it
        with open(self.SCENES_PATH, "wb") as f:
            writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.scenes) 
        #print "saved scenes: " + str(self.scenes)
        # make sure it is saved as 'music' user, uid=gid=1000
        os.chown(self.SCENES_PATH, 1000, 1000)

    def load_scenes(self):
        # create scene file if doesn't exits
        if not os.path.exists(self.SCENES_PATH):
            f = open(self.SCENES_PATH, "w")
            f.close()
        # make sure it is saved as 'music' user, uid=gid=1000
        os.chown(self.SCENES_PATH, 1000, 1000)
        # open it
        with open(self.SCENES_PATH, 'r') as f:
            reader = csv.reader(f)
            csvin = list(reader)
        self.scenes = []
        try :
            for row in csvin :
                scene = []
                scene.append(str(row[0]))
                scene.append(float(row[1]))
                scene.append(float(row[2]))
                scene.append(float(row[3]))
                scene.append(float(row[4]))
                scene.append(float(row[5]))
                if row[6] == 'True':
                    scene.append(True)
                else :
                    scene.append(False)
                self.scenes.append(scene)
        except:
            print("error parsing scene file")
        print("loaded scenes: " + str(self.scenes))

    def next_scene(self):
        self.scene_index += 1
        if self.scene_index >= len(self.scenes) : 
            self.scene_index = 0
        self.recall_scene(self.scene_index)

    def prev_scene (self) :
        self.scene_index -= 1
        if self.scene_index < 0 : 
            if len(self.scenes) > 0 :
                self.scene_index = len(self.scenes) - 1
            else :
                self.scene_index = 0
        self.recall_scene(self.scene_index)

    def recall_scene(self, index) :
        print("recalling scene " + str(index))
        try :
            scene = self.scenes[index]
            self.scene_index = index
            self.override_all_knobs()
            self.knob[0] = scene[1]
            self.knob[1] = scene[2]
            self.knob[2] = scene[3]
            self.knob[3] = scene[4]
            self.knob[4] = scene[5]
            self.auto_clear = scene[6]
            self.set_mode_by_name(scene[0])
            self.scene_set = True
        except :
            print("probably no scenes")

    def get_color_from_palette(self, t, a, b, c, d):
        # a, b, c, and d should be iterables of length 3: (x, y, z)
        # t is a float.
        # The formula: a + b * cos( 2π * (c*t + d) )
        return [
            a[i] + b[i] * math.cos(6.283185 * (c[i] * t + d[i]))
            for i in range(3)
        ]
    
    def color_picker( self, val ):
        # convert knob to 0-1
        c = float(val)

        t = c

        ci = self.palette
        a = self.palettes[ci]["a"]
        b = self.palettes[ci]["b"]
        c = self.palettes[ci]["c"]
        d = self.palettes[ci]["d"]
   
        #print(self.palettes[ci]["name"])
        color = self.get_color_from_palette(t, a, b, c, d)

        color2 = (max(0, min(1,color[0])) * 255, max(0, min(1,color[1])) * 255, max(0, min(1,color[2])) * 255)
        #print(color2)
        return color2
 
    def color_picker_bg( self, val):
        #c = float(val)
        #r = (1 - (math.cos(c * 3 * math.pi) * .5 + .5)) * c
        #g = (1 - (math.cos(c * 7 * math.pi) * .5 + .5)) * c
        #b = (1 - (math.cos(c * 11 * math.pi) * .5 + .5)) * c
        
        #color = (r * 255,g * 255,b * 255)
        
        #self.bg_color = color
        #return color

        c = float(val)

        t = c

        ci = self.palette
        a = self.palettes[ci]["a"]
        b = self.palettes[ci]["b"]
        c = self.palettes[ci]["c"]
        d = self.palettes[ci]["d"]
   
        #print(self.palettes[ci]["name"])
        color = self.get_color_from_palette(t, a, b, c, d)

        color2 = (max(0, min(1,color[0])) * 255, max(0, min(1,color[1])) * 255, max(0, min(1,color[2])) * 255)
        self.bg_color = color2
        return color2
        
 

    def dispatch_key_event(self, k, v):
        
        # the shift key
        if k == 2 :
            if v > 0 : self.key2_status = True
            else : self.key2_status = False
        
        # select osd or menu 
        if (k == 1 and v > 0) : 
            if self.key2_status: self.toggle_menu()
            else : self.toggle_osd()
       
        if self.show_menu :
            if (k == 2 and v > 0) : self.key2_press = True
            if (k == 3 and v > 0) : self.key3_press = True
            if (k == 4 and v > 0) : self.key4_press = True
            if (k == 5 and v > 0) : self.key5_press = True
            if (k == 6 and v > 0) : self.key6_press = True
            if (k == 7 and v > 0) : self.key7_press = True
            if (k == 8 and v > 0) : self.key8_press = True
            if (k == 9 and v > 0) : self.key9_press = True
            if (k == 10 and v > 0) : self.key10_press = True
        else :
            if not self.key2_status : 
                if (k == 3 and v > 0) : self.toggle_auto_clear()
                if (k == 4 and v > 0) : self.prev_mode()
                if (k == 5 and v > 0) : self.next_mode()
                if (k == 6 and v > 0) : self.prev_scene()
                if (k == 7 and v > 0) : self.next_scene()
                if (k == 8)           : self.save_or_delete_scene(v)
                if (k == 9 and v > 0) : self.screengrab_flag = True
                if (k == 10)          : self.update_trig_button(v)
            else :
                if (k == 4 and v > 0) : self.prev_palette()
                if (k == 5 and v > 0) : self.next_palette()
                 

    def clear_flags(self):
        self.new_midi = False
        self.audio_trig = False
        self.run_setup = False
        self.screengrab_flag = False
        self.midi_note_new = False
        for i in range(0, 128):
            self.midi_notes_last[i] = self.midi_notes[i]
        self.key1_press = False
        self.key2_press = False
        self.key3_press = False
        self.key4_press = False
        self.key5_press = False
        self.key6_press = False
        self.key7_press = False
        self.key8_press = False
        self.key9_press = False
        self.key10_press = False



