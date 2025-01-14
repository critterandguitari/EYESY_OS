import fileinput
import random
import math
import pygame
import traceback
import imp
import os
import glob
import sys
import time
import json
import helpers
import file_operations
import csv
import color_palettes
import config

class System:

    GRABS_PATH = "/sdcard/Grabs/"
    MODES_PATH = "/sdcard/Modes/Python/"
    SCENES_PATH = "/sdcard/Scenes/"
    SYSTEM_PATH = "/sdcard/System/"
    
    RESOLUTIONS = [
        { "name" : "640 x 480",
          "res"  : (640,480)
        },
        { "name" : "720 x 480",
          "res"  : (720,480)
        },
        { "name" : "800 x 600",
          "res"  : (800,600)
        },
        { "name" : "1280 x 720",
          "res"  : (1280,720)
        },
        { "name" : "1920 x 1080 - slow",
          "res"  : (1920,1080)
        }
    ]

    DEFAULT_CONFIG = {
        "video_resolution": 0,
        "audio_gain": 50,
        "trigger_source":0,
        "fg_palette": 0,
        "bg_palette": 0,
        "midi_channel": 1,
        "knob1_cc": 20,
        "knob2_cc": 21,
        "knob3_cc": 22,
        "knob4_cc": 23,
        "knob5_cc": 24,
        "auto_clear_cc": 25,
        "pc_map": {}
    }
   
    trigger_sources = ["MIDI Clock", "MIDI Note", "Audio"]
    config = {}

    RES =  (0,0)

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

    font = None

    # screen grabs
    lastgrab = None
    lastgrab_thumb = None
    tengrabs_thumbs = []
    grabcount = 0
    grabindex = 0
    screengrab_flag = False
    screen = None  # ref to main surface, for doing screenshots

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
    save_key_time = 0  # for timing how long save key held 
    scene_set = False
    next_numbered_scene = 1
    
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
    new_midi = False
    usb_midi_name = ''
    usb_midi_present = False

    # system stuff 
    memory_used = 0
    ip = ''
    auto_clear = True
    bg_color = (0, 0, 0)
    quit = False
    restart = False
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
    key4_status = False  
    key5_status = False  
    key6_status = False  
    key7_status = False  

    # color stuff
    palettes = color_palettes.abcd_palettes
    fg_palette = 0;
    bg_palette = 0;

    def load_config_file(self) :
        config_file = self.SYSTEM_PATH + "config.json"
        if not(os.path.isdir(self.SYSTEM_PATH)) :
            print('No system folder, creating...')
            os.system('mkdir ' + self.SYSTEM_PATH)

        try:
            # Load configuration, raising errors for file or JSON issues
            self.config = config.load_config(config_file, self.DEFAULT_CONFIG)
        except FileNotFoundError as e:
            print(f"Error loading configuration: {e}")
            print("Using all default values. Saving File.")
            self.config = self.DEFAULT_CONFIG
            config.save_config(config_file, self.config)
        except ValueError as e:
            print(f"Error loading configuration: {e}")
            print("Using all default values.")
            self.config = self.DEFAULT_CONFIG

        self.validate_config()
        print("Current Configuration:", self.config)

        try:
            # set values from configg
            self.RES = self.RESOLUTIONS[self.config["video_resolution"]]["res"]
            self.bg_palette = self.config["bg_palette"]
            self.fg_palette = self.config["fg_palette"]
        except :
            print("Error setting config value")
    
    def _validate_config_int(self, field, minv, maxv) :
        self.config[field] = (
            self.config.get(field)
            if isinstance(self.config.get(field), int) and minv <= self.config[field] <= maxv
            else self.DEFAULT_CONFIG[field]
        )

    def validate_config(self):
        # Validate each field in self.config, falling back to defaults if needed
        self._validate_config_int("midi_channel", 1, 16)
        self._validate_config_int("video_resolution", 0, len(self.RESOLUTIONS))
        self._validate_config_int("audio_gain", 0, 300)
        self._validate_config_int("fg_palette", 0, len(self.palettes)-1)
        self._validate_config_int("bg_palette", 0, len(self.palettes)-1)
        self._validate_config_int("trigger_source", 0, len(self.trigger_sources)-1)
        self._validate_config_int("knob1_cc", 0, 127)
        self._validate_config_int("knob2_cc", 0, 127)
        self._validate_config_int("knob3_cc", 0, 127)
        self._validate_config_int("knob4_cc", 0, 127)
        self._validate_config_int("knob5_cc", 0, 127)
        self._validate_config_int("auto_clear_cc", 0, 127)


    def save_config_file(self) :
        config_file = self.SYSTEM_PATH + "config.json"
        config.save_config(config_file, self.config)

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

    def next_bg_palette (self) :
        self.bg_palette += 1
        if self.bg_palette >= len(self.palettes) : 
            self.bg_palette = 0

    def prev_bg_palette (self) :
        self.bg_palette -= 1
        if self.bg_palette < 0 : 
            self.bg_palette = len(self.palettes) - 1

    def next_fg_palette (self) :
        self.fg_palette += 1
        if self.fg_palette >= len(self.palettes) : 
            self.fg_palette = 0

    def prev_fg_palette (self) :
        self.fg_palette -= 1
        if self.fg_palette < 0 : 
            self.fg_palette = len(self.palettes) - 1

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
        pygame.image.save( self.screen ,imagepath)
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
            elapsed_time = time.time() - self.save_key_time
            if (elapsed_time > 1) : # held down for 1 seconds, delete the scene
                self.delete_current_scene()
                self.save_key_status = False

    def save_or_delete_scene(self, key_stat):
        if key_stat > 0 :
            self.save_key_status = True
            self.save_key_time = time.time()  # start timer
        else :
            if (self.save_key_status) :  # key release before delete happens
                self.save_key_status = False
                self.save_scene()
            self.save_key_status = False
                
    def delete_current_scene(self):
        print("deleting scene")
        if len(self.scenes) > 0:    
            # delete from list and delete folder
            file_path = self.SCENES_PATH + self.scenes[self.scene_index]['name']
            file_operations.delete(file_path)
            print("deleted scene " + file_path)
            del self.scenes[self.scene_index]
            if self.scene_index >= len(self.scenes):
                self.scene_index = len(self.scenes) - 1
            if self.scene_index < 0:  # deleted last scene
                self.scene_index = 0
                self.scene_set = False
            else:
                self.recall_scene(self.scene_index)

    def save_scene(self):
        print("Saving scene")
       
        # make scenes dir if no exist
        os.makedirs(self.SCENES_PATH, exist_ok=True)

        # Use zero-padded numbering, e.g. scene-0001 for scene folder
        while True:
            folder_path = os.path.join(self.SCENES_PATH, f"scene-{self.next_numbered_scene:04d}")
            if not os.path.exists(folder_path):
                break
            self.next_numbered_scene += 1
        os.makedirs(folder_path)
        scene_file = os.path.join(folder_path, "scene.json")
        imagepath = os.path.join(folder_path, "scene.jpg")

        new_scene = {
            "mode": self.mode,
            "knob1": self.knob1,
            "knob2": self.knob2,
            "knob3": self.knob3,
            "knob4": self.knob4,
            "knob5": self.knob5,
            "auto_clear": self.auto_clear,
            "bg_palette": self.bg_palette,
            "fg_palette": self.fg_palette,
        }
        self.scenes.append(new_scene)
        
        try:
            with open(scene_file, 'w') as f:
                json.dump(new_scene, f, indent=4)
            print(f"Scene saved to {scene_file}")
        except Exception as e:
            print(f"Failed to save scene file: {e}")

        thumb = pygame.Surface((128, 72))
        pygame.transform.scale(self.screen, (128, 72), thumb)
        pygame.image.save(thumb, imagepath)
        print("saved scene screenshot " + imagepath)

        # add name and thumbnail fields after saving file (allows user to change scene folder names later)
        self.scenes[-1]["name"] = os.path.basename(folder_path)
        self.scenes[-1]["thumbnail"] = imagepath
       

    def _load_scene(self, folder_path):
        scene_file = os.path.join(folder_path, "scene.json")
        if not os.path.isfile(scene_file):
            print(f"No scene.json in {folder_path}")
            return None
        
        # Load JSON
        try:
            with open(scene_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read scene.json in {folder_path}: {e}")
            return None
        
        # Validate
        try:
            if not (0 <= float(data["knob1"]) <= 1): print(f"knob1 invalid in {folder_path}"); return None
            if not (0 <= float(data["knob2"]) <= 1): print(f"knob2 invalid in {folder_path}"); return None
            if not (0 <= float(data["knob3"]) <= 1): print(f"knob3 invalid in {folder_path}"); return None
            if not (0 <= float(data["knob4"]) <= 1): print(f"knob4 invalid in {folder_path}"); return None
            if not (0 <= float(data["knob5"]) <= 1): print(f"knob5 invalid in {folder_path}"); return None
            if not isinstance(data["auto_clear"], bool): print(f"auto_clear invalid in {folder_path}"); return None
            if not isinstance(data["mode"], str): print(f"mode invalid in {folder_path}"); return None
            if not (0 <= int(data["bg_palette"]) < len(self.palettes)): print(f"bg_palette invalid in {folder_path}"); return None
            if not (0 <= int(data["fg_palette"]) < len(self.palettes)): print(f"fg_palette invalid in {folder_path}"); return None
        except Exception as e:
            print(f"Validation error in {folder_path}: {e}")
            return None

        # Build scene dict
        new_scene = {
            "mode": data["mode"],
            "knob1": float(data["knob1"]),
            "knob2": float(data["knob2"]),
            "knob3": float(data["knob3"]),
            "knob4": float(data["knob4"]),
            "knob5": float(data["knob5"]),
            "auto_clear": data["auto_clear"],
            "bg_palette": int(data["bg_palette"]),
            "fg_palette": int(data["fg_palette"]),
            "name": os.path.basename(folder_path),
            "thumbnail": os.path.join(folder_path, "scene.jpg")
        }
        return new_scene


    def load_scenes(self):
        self.scenes = []
        self.next_numbered_scene = 1
        
        if not os.path.isdir(self.SCENES_PATH):
            print(f"Scenes path {self.SCENES_PATH} does not exist.")
            return
        
        try:
            folders = os.listdir(self.SCENES_PATH)
        except Exception as e:
            print(f"Failed to list {self.SCENES_PATH}: {e}")
            return

        # Determine highest zero-padded "scene-####" number
        for folder in folders:
            if folder.startswith("scene-"):
                try:
                    number = int(folder.replace("scene-", ""))
                    if number >= self.next_numbered_scene:
                        self.next_numbered_scene = number + 1
                except Exception as e:
                    print(f"Bad folder name {folder}: {e}")

        folders.sort()
        for folder in folders:
            folder_path = os.path.join(self.SCENES_PATH, folder)
            if os.path.isdir(folder_path):
                try:
                    scene_data = self._load_scene(folder_path)
                    if scene_data:
                        self.scenes.append(scene_data)
                except Exception as e:
                    print(f"Failed loading scene from {folder_path}: {e}")

    def recall_scene(self, index) :
        print("recalling scene " + str(index))
        try :
            scene = self.scenes[index]
            self.scene_index = index
            self.override_all_knobs()
            self.knob[0] = scene["knob1"]
            self.knob[1] = scene["knob2"]
            self.knob[2] = scene["knob3"]
            self.knob[3] = scene["knob4"]
            self.knob[4] = scene["knob5"]
            self.auto_clear = scene["auto_clear"]
            self.bg_palette = scene["bg_palette"]
            self.fg_palette = scene["fg_palette"]
            self.set_mode_by_name(scene["mode"])
            self.scene_set = True
        except :
            print("probably no scenes")

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

    def get_color_from_palette(self, t, a, b, c, d):
        # a, b, c, and d should be iterables of length 3: (x, y, z)
        # t is a float.
        # The formula: a + b * cos( 2π * (c*t + d) )
        return [
            a[i] + b[i] * math.cos(6.283185 * (c[i] * t + d[i]))
            for i in range(3)
        ]
    
    def color_picker( self, val ):

        # first slot legacy color pickers
        if self.fg_palette == 0 : return self.color_picker_original(val)
        
        c = float(val)

        t = c

        ci = self.fg_palette
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

        # first slot legacy color pickers
        if self.bg_palette == 0 : return self.color_picker_bg_original(val)

        c = float(val)

        t = c

        ci = self.bg_palette
        a = self.palettes[ci]["a"]
        b = self.palettes[ci]["b"]
        c = self.palettes[ci]["c"]
        d = self.palettes[ci]["d"]
   
        #print(self.palettes[ci]["name"])
        color = self.get_color_from_palette(t, a, b, c, d)

        color2 = (max(0, min(1,color[0])) * 255, max(0, min(1,color[1])) * 255, max(0, min(1,color[2])) * 255)
        self.bg_color = color2
        return color2
        
    # legacy color picker used for first palette slot 
    def color_picker_original( self, val ):
        # convert knob to 0-1
        c = float(val)

        # all the way down random bw
        rando = random.randrange(0, 2)
        color = (rando * 255, rando * 255, rando * 255)

        # random greys
        if c > .02 :
            rando = random.randrange(0,255)
            color = (rando, rando, rando)
        # grey 1
        if c > .04 :
            color = (50, 50, 50)
        # grey 2
        if c > .06 :
            color = (100, 100 ,100)
        # grey 3
        if c > .08 :
            color = (150, 150 ,150)
        # grey 4
        if c > .10 :
            color = (150, 150 ,150)
            
        # grey 5
        if c > .12 :
            color = (200, 200 ,200)
        # white
        if c > .14 :
            color = (250, 250 ,250)
        #colors
        if c > .16 :
            
            #r = float(control) / 1024 * 255
            #g = float((control * 2) % 1024) / 1024 * 255
            #b = float((control * 4) % 1024) / 1024 * 255
            
            r = math.sin(c * 2 * math.pi) * .5 + .5
            g = math.sin(c * 4 * math.pi) * .5 + .5
            b = math.sin(c * 8 * math.pi) * .5 + .5
            color = (r * 255,g * 255,b * 255)
        # full ranoms
        if c > .96 :
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        # primary randoms
        if c > .98 :
            r = random.randrange(0, 2) * 255
            g = random.randrange(0, 2) * 255
            b = random.randrange(0, 2) * 255
            color = (r,g,b)
        
        color2 = (color[0], color[1], color[2])
        return color2
 
    # legacy color picker used for first palette slot 
    def color_picker_bg_original( self, val):
        c = float(val)
        r = (1 - (math.cos(c * 3 * math.pi) * .5 + .5)) * c
        g = (1 - (math.cos(c * 7 * math.pi) * .5 + .5)) * c
        b = (1 - (math.cos(c * 11 * math.pi) * .5 + .5)) * c
        
        color = (r * 255,g * 255,b * 255)
        
        self.bg_color = color
        return color 

    def dispatch_key_event(self, k, v):
        
        # the shift key
        if k == 2 :
            if v > 0 : self.key2_status = True
            else : self.key2_status = False
        
        if k == 6 :
            if v > 0 : self.key6_status = True
            else : self.key6_status = False
        if k == 7 :
            if v > 0 : self.key7_status = True
            else : self.key7_status = False
        if k == 4 :
            if v > 0 : self.key4_status = True
            else : self.key4_status = False
        if k == 5 :
            if v > 0 : self.key5_status = True
            else : self.key5_status = False
 
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
            else :      # shift key down
                if (k == 4 and v > 0) : self.prev_fg_palette()
                if (k == 5 and v > 0) : self.next_fg_palette()
                if (k == 6 and v > 0) : self.prev_bg_palette()
                if (k == 7 and v > 0) : self.next_bg_palette()
                 

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



