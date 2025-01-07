# main_menu.py

from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenMainMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "Settings"
        self.menu = WidgetMenu(app_state, [
#            MenuItem('MIDI Ch 16', self.exit_menu),
#            MenuItem('Gain 100%', self.exit_menu),
            MenuItem('Video Settings  ▶', self.goto_video_settings),
            MenuItem('WiFi  ▶', self.goto_wifi),
            MenuItem('Color Palette  ▶', self.goto_palette),
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
        self.app_state.switch_menu_screen("palette")

    def goto_video_settings(self):
        self.app_state.switch_menu_screen("video_settings")

    def goto_test(self):
        self.app_state.switch_menu_screen("test")

    def goto_applogs(self):
        self.app_state.switch_menu_screen("applogs")

    def goto_wifi(self):
        self.app_state.switch_menu_screen("wifi")

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

