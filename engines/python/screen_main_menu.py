# main_menu.py

from screen import Screen
from menu import Menu, MenuItem

class MainMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = Menu(app_state, [
            MenuItem(' Info ', self.goto_info),
            MenuItem(' MIDI Ch 16 ', self.exit_menu),
            MenuItem(' Gain 100% ', self.exit_menu),
            MenuItem(' WiFi > ', self.goto_wifi),
            MenuItem(' Test > ', self.goto_test)
        ])

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        self.menu.render(surface)

    def goto_test(self):
        self.app_state.current_screen = self.app_state.menu_screens["test"]


    def goto_wifi(self):
        self.app_state.current_screen = self.app_state.menu_screens["wifi"]

    def goto_info(self):
        pass
        #self.app_state.current_screen = self.app_state.menu_screens["info"]

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

