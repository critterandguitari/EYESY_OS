
from screen import Screen
from menu import Menu, MenuItem

class ResMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = Menu(app_state, [
            MenuItem(' 320x240 ', self.exit_menu),
            MenuItem(' 640x480 ', self.exit_menu),
            MenuItem(' 720x480 ', self.goto_wifi),
            MenuItem(' 1280x720 ', self.goto_test),
            MenuItem(' 1920x1080 ', self.exit_menu),
            MenuItem(' < Back ', self.goto_home)
        ])

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        self.menu.render(surface)

    def goto_home(self):
        self.app_state.current_screen = self.app_state.menu_screens["home"]


    def goto_test(self):
        self.app_state.current_screen = self.app_state.menu_screens["test"]


    def goto_wifi(self):
        self.app_state.current_screen = self.app_state.menu_screens["wifi"]

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

