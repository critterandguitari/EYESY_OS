import pygame
from screen import Screen
from widget_applogs import WidgetApplogs

class ScreenApplogs(Screen):

    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.title = "Logs"
        self.applogs = WidgetApplogs(eyesy)
        self.applogs.x_offset = 50
        self.applogs.y_offset = 50

    def before(self):
        self.applogs.before()

    def render(self, surface):
        self.applogs.render(surface)

    def handle_events(self):
        pass

    def exit_menu(self):
        self.eyesy.switch_menu_screen("home")

