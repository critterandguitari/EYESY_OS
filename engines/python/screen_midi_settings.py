import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

def wha(): print("wha")

class ScreenMIDISettings(Screen):

    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "MIDI PC Mapping"
        self.menu = WidgetMenu(app_state, [
            MenuItem('Scene 1:    None        ', wha),
            MenuItem('Scene 2:    None        ', wha),
            MenuItem('Scene 3:    Program 33  ', wha),
            MenuItem('Scene 4:    Program 34  ', wha),
            MenuItem('Scene 5:    Program 35  ', wha),
            MenuItem('Scene 6:    None        ', wha),
            MenuItem('Scene 7:  ◀ Program 7 ▶ ', wha),
            MenuItem('Scene 8:    Program 8   ', wha),
            MenuItem('Scene 9:    Program 9   ', wha),
            MenuItem('Scene 10:   Program 10  ', wha),
            MenuItem('Scene 11:   None        ', wha),
            MenuItem('Scene 12:   None        ', wha),
            MenuItem('Scene 13:   None        ', wha),
            MenuItem('Scene 14:   None        ', wha),
            MenuItem('Scene 15:   None        ', wha),
            MenuItem('Scene 16:   None        ', wha),
            MenuItem('Scene 17:   None        ', wha),
            MenuItem('Scene 18:   None        ', wha),
        ])
        self.menu.visible_items = 8
        self.menu.off_y = 43
        self.menu.visible_items = 12  

    def render(self, surface):
        self.menu.render(surface)

    def handle_events(self):
        self.menu.handle_events()

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

