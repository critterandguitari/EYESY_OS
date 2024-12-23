
from screen import Screen
from menu import Menu, MenuItem
from screen_dialog import DialogScreen

class ResMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.state = "idle"  # states are idle and confirm
        self.dialog = DialogScreen(app_state)
        self.menu = Menu(app_state, [
            MenuItem(' 640x480 ', self.confirm),
            MenuItem(' 1280x720 ', self.confirm),
            MenuItem(' < Back ', self.goto_home)
        ])

    def before(self):
        self.state = "idle"

    def handle_events(self):
        if self.state == "idle":
            self.menu.handle_events()
        elif self.state == "confirm":
            self.dialog.handle_events()

    def render(self, surface):
        if self.state == "idle":
            self.menu.render(surface)
        if self.state == "confirm":
            self.dialog.render(surface)

    def goto_home(self):
        self.app_state.switch_menu_screen("home")

    def confirm(self):
        self.state = "confirm"
        
