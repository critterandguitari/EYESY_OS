# main_menu.py

from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenMainMenu(Screen):
    def __init__(self, eyesy):
        super().__init__(eyesy)
        #self.title = "Settings         " + chr(0x2680) + "           " + chr(0x2681) + "         " + chr(0x2682) + "          " + chr(0x2683)
        self.title = "Settings"
        self.footer =  chr(0x2680) + "     = Cancel     " + chr(0x2682) + "   = Up/Down     " + chr(0x2683) + "  = Enter"
        self.menu = WidgetMenu(eyesy, [
            MenuItem('Video Settings  ▶', self.goto_video_settings),
            MenuItem('Audio MIDI Settings  ▶', self.goto_midi_settings),
            MenuItem('Color Palette  ▶', self.goto_palette),
            MenuItem('WiFi  ▶', self.goto_wifi),
            MenuItem('Hardware Test  ▶', self.goto_test),
            MenuItem('Logs  ▶', self.goto_applogs),
            MenuItem('◀  Exit', self.exit_menu)
        ])
        self.menu.visible_items = 8
        self.menu.off_y = 43

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def render(self, surface):
        self.menu.render(surface)

    def goto_palette(self):
        self.eyesy.switch_menu_screen("palette")

    def goto_midi_settings(self):
        self.eyesy.switch_menu_screen("midi_settings")

    def goto_video_settings(self):
        self.eyesy.switch_menu_screen("video_settings")

    def goto_test(self):
        self.eyesy.switch_menu_screen("test")

    def goto_applogs(self):
        self.eyesy.switch_menu_screen("applogs")

    def goto_wifi(self):
        self.eyesy.switch_menu_screen("wifi")

    def exit_menu(self):
        self.eyesy.exit_menu()

