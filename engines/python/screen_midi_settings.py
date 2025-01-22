import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

def wha(): print("wha")

class ScreenMIDISettings(Screen):

    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.title = "MIDI Settings"
        self.menu = WidgetMenu(eyesy, [])
        self.menu.items.append(MenuItem('MIDI PC Mapping  ▶', self.goto_midi_pc_mapping))
        
        self.menu.items.append(self.create_adjustable_menu_item("midi_channel", 1, 16,  "MIDI Channel: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("knob1_cc", 0, 127,  "Knob 1 CC: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("knob2_cc", 0, 127,  "Knob 2 CC: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("knob3_cc", 0, 127,  "Knob 3 CC: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("knob4_cc", 0, 127,  "Knob 4 CC: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("knob5_cc", 0, 127,  "Knob 5 CC: {value}"))
        self.menu.items.append(self.create_adjustable_menu_item("auto_clear_cc", 0, 127,  "Screen Clear On/Off CC: {value}"))

        self.menu.items.append(MenuItem('◀  Exit', self.exit_menu))
        self.menu.visible_items = 8
        self.menu.off_y = 43

        # key press timer for repeats
        self.key4_td = 0
        self.key5_td = 0

    def create_adjustable_menu_item(self, name, minv, maxv, format_string) :
        item = MenuItem("", self.save_config)
        item.adjustable = True
        item.name = name
        item.min_value = minv
        item.max_value = maxv
        item.value = item.min_value
        item.format_string = format_string
        item.text = item.format_string.format(value=item.value)
        return item
    
    def get_item_index(self, target_name):
        for i, item in enumerate(self.menu.items):
            if item.name == target_name:
                return i
        return -1

    # set from config
    def before(self):
        for key in self.eyesy.config:
            i = self.get_item_index(key)
            if i >= 0:
                item = self.menu.items[i]
                item.value = self.eyesy.config[key]
                item.text = item.format_string.format(value=item.value)

    def render(self, surface):
        self.menu.render(surface)

    def handle_events(self):

        self.menu.handle_events()

        item = self.menu.items[self.menu.selected_index]
        if item.adjustable:
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
     
    def menu_dec_value(self, item):
        item.value -= 1
        if item.value < item.min_value: item.value = item.min_value
        item.text = item.format_string.format(value=item.value)

    def menu_inc_value(self, item):
        item.value += 1
        if item.value > item.max_value: item.value = item.max_value
        item.text = item.format_string.format(value=item.value)

    def save_config(self):
        # save to config
        for key in self.eyesy.config:
            i = self.get_item_index(key)
            if i >= 0:
                item = self.menu.items[i]
                self.eyesy.config[key] = item.value
        self.eyesy.save_config_file()
        self.exit_menu()
    
    def goto_midi_pc_mapping(self):
        self.eyesy.switch_menu_screen("midi_pc_mapping")
    def exit_menu(self):
        self.eyesy.switch_menu_screen("home")

