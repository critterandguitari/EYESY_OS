import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

def wha(): print("wha")

class ScreenMIDISettings(Screen):

    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "MIDI PC Mapping"
        self.pc_map = [0] * 128  # for holding mappings before saving
        self.menu = self.create_midi_mapping_menu()
        self.menu.visible_items = 8
        self.menu.off_y = 43
        self.menu.visible_items = 12  
        self.key6_td = 0      # timer used for key repeats
        self.key7_td = 0      # timer used for key repeats

    def create_midi_mapping_menu(self):
        menu_items = []

        for i in range(128):
            # Create a menu item for each palette
            
            scene = self.app_state.config["pc_map"].get(str(i),0)
            item = MenuItem(f"{i} -> {scene}", wha)
            item.adjustable = True
            item.value = scene
            menu_items.append(item)

        # Return the menu object
        return WidgetMenu(self.app_state, menu_items)


    def render(self, surface):
        self.menu.render(surface)

    def menu_dec(self):
        if self.menu.selected_index > 0:
            self.menu.selected_index -= 1
            self.menu._adjust_view()

    def menu_inc(self):
        if self.menu.selected_index < len(self.menu.items) - 1:
            self.menu.selected_index += 1
            self.menu._adjust_view()

    def handle_events(self):
        # press and hold speed around menu
        if self.app_state.key6_press: 
            self.menu_dec()
            self.key6_td = 0
        if self.app_state.key6_status:
            self.key6_td += 1
            if self.key6_td > 15 : self.menu_dec()

        if self.app_state.key7_press: 
            self.menu_inc()
            self.key7_td = 0
        if self.app_state.key7_status:
            self.key7_td += 1
            if self.key7_td > 15 : self.menu_inc()

        item = self.menu.items[self.menu.selected_index]
        if item.adjustable:
            if self.app_state.key4_press:
                item.value -= 1
                if item.value < 0: item.value = 0
                item.text = f"Scene {item.value}"
            if self.app_state.key5_press:
                item = self.menu.items[self.menu.selected_index]
                item.value += 1
                if item.value > len(self.menu.items) - 1: item.value = len(self.menu.items) - 1
                item.text = f"PGM {self.menu.selected_index} : Scene {item.value}"

        #self.menu.selected_index = int(self.app_state.knob1 * len(self.menu.items))
        self.menu._adjust_view()
       
        if self.app_state.key8_press:
            self.menu.items[self.menu.selected_index].action()

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

