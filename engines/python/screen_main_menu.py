# main_menu.py

from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenMainMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "Settings"
        self.menu = WidgetMenu(app_state, [
            MenuItem('MIDI Ch 16', self.exit_menu),
            MenuItem('Gain 100%', self.exit_menu),
            MenuItem('Screen Size  ▶', self.goto_res),
            MenuItem('WiFi  ▶', self.goto_wifi),
            MenuItem('Test  ▶', self.goto_test),
            MenuItem('Color Palette  ▶', self.goto_palette),
            MenuItem('◀  Exit', self.exit_menu)
        ])
        self.menu.visible_items = 8

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def render(self, surface):
        self.menu.render(surface)

    def goto_palette(self):
        self.app_state.switch_menu_screen("palette")

    def goto_res(self):
        self.app_state.switch_menu_screen("res")

    def goto_test(self):
        self.app_state.switch_menu_screen("test")


    def goto_wifi(self):
        self.app_state.switch_menu_screen("wifi")

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

