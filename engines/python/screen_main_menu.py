# main_menu.py

from screen import Screen
from menu import Menu, MenuItem

class MainMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = Menu(app_state, [
            MenuItem('Audio Settings', self.goto_audio_settings),
            MenuItem('MIDI Settings', self.goto_midi_settings),
            MenuItem('Exit', self.exit_app)
        ])

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        self.menu.render(surface)

    def goto_audio_settings(self):
        self.app_state.current_screen = self.app_state.menu_screens["audio"]
        self.app_state.current_screen.menu.selected_index = 0

    def goto_midi_settings(self):
        self.app_state.current_screen = self.app_state.menu_screens["midi"]

    def exit_app(self):
        self.app_state.running = False

