import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

def wha(): print("wha")

class ScreenMIDIPCMapping(Screen):

    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.title = "MIDI PC Mapping"
        self.menu = self.create_midi_mapping_menu()
        self.menu.visible_items = 8
        self.menu.off_y = 43
        self.menu.visible_items = 12  
        self.key4_td = 0      # timer used for key repeats
        self.key5_td = 0      # timer used for key repeats
        self.update_thumb_flag = False
    
    # see if scene name is in the current list of scenes
    def get_scene_index(self, target_name):
        for i, scene in enumerate(self.eyesy.scenes):
            if scene["name"] == target_name:
                return i
        return -1

    def create_midi_mapping_menu(self):
        menu_items = []

        for i in range(128):
            item = MenuItem(f"wha", wha)
            item.adjustable = True
            menu_items.append(item)

        # Return the menu object
        return WidgetMenu(self.eyesy, menu_items)

    # called before entering screen.  item vaule is -1 if no mapping, otherwise it is the index of scenes list
    def update_midi_mapping_menu(self):
        for i,item in enumerate(self.menu.items) :
            scene = self.eyesy.config["pc_map"].get(f"pgm_{i + 1}",None)
            # -1 if scene not found
            item.value = self.get_scene_index(scene)
            # dump entries that aren't found
            if scene is not None and item.value < 0 :
                scene = None
            item.text = f"pgm {i + 1} -> {scene}"

    def before(self):
        self.update_midi_mapping_menu()

    def render(self, surface):
        self.menu.render(surface)
        if True: #self.update_thumb_flag:
            self.update_thumb_flag = False
            item = self.menu.items[self.menu.selected_index]
            if item.value >= 0:
                thumb_path = self.eyesy.scenes[item.value]['thumbnail']
                self.show_thumb(surface, (300,150), thumb_path)

    def menu_inc_value(self, item):
        item.value += 1
        if item.value > len(self.eyesy.scenes) - 1: item.value = len(self.eyesy.scenes) - 1
        item.text = f"pgm {self.menu.selected_index + 1} -> {self.eyesy.scenes[item.value]['name']}"
        self.update_thumb_flag = True

    def menu_dec_value(self, item):
        item.value -= 1
        if item.value < -1: item.value = -1
        if item.value >= 0:
            item.text = f"pgm {self.menu.selected_index + 1} -> {self.eyesy.scenes[item.value]['name']}"
        else:
            item.text = f"pgm {self.menu.selected_index + 1} -> None"

    def handle_events(self):

        self.menu.handle_events()

        item = self.menu.items[self.menu.selected_index]
        if item.adjustable and len(self.eyesy.scenes) > 0:
            if self.eyesy.key4_press: 
                self.menu_dec_value(item)
                self.key4_td = 0
            if self.eyesy.key4_status:
                self.key4_td += 1
                if self.key4_td > 10 : self.menu_dec_value(item)

            if self.eyesy.key5_press: 
                self.menu_inc_value(item)
                self.key5_td = 0
            if self.eyesy.key5_status:
                self.key5_td += 1
                if self.key5_td > 10 : self.menu_inc_value(item)
     
      
        # save to config, delete any unmapped
        if self.eyesy.key8_press:
            for i,item in enumerate(self.menu.items) :
                if item.value >= 0:
                    self.eyesy.config["pc_map"][f"pgm_{i + 1}"] = self.eyesy.scenes[item.value]["name"]
                else:
                    self.eyesy.config["pc_map"].pop(f"pgm_{i + 1}", None)
            self.eyesy.save_config_file()
            self.exit_menu()
     
    def show_thumb(self, surface, position, filepath):
        try:
            image = pygame.image.load(filepath)
            x, y = position
            surface.blit(image, (x, y))
        except pygame.error as e:
            print(f"Error loading image at {filepath}: {e}")
    
    def exit_menu(self):
        self.eyesy.switch_menu_screen("home")

