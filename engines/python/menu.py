# menu.py

import pygame

class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action  # Function to call when item is selected

# menu.py

class Menu:
    def __init__(self, app_state, items):
        self.app_state = app_state
        self.items = items  # List of MenuItem instances
        self.selected_index = 0
        self.font = pygame.font.Font("font.ttf", 24)  # Customize font and size as needed

    def handle_events(self):
        self.selected_index = int(self.app_state.knob1 * len(self.items))
        #if self.app_state.key4_press:
        #    self.selected_index = (self.selected_index - 1) % len(self.items)
        #elif self.app_state.key5_press:
        #    self.selected_index = (self.selected_index + 1) % len(self.items)
        if self.app_state.key4_press:
            self.items[self.selected_index].action()

    def render(self, surface):
        #surface.fill((0, 0, 0))  # Clear screen with black
        for index, item in enumerate(self.items):
            color = (200, 200, 200)
            if index == self.selected_index:
                color = (255, 215, 0)  # Highlight selected item
            text_surface = self.font.render(item.text, True, color, (0,0,0))
            surface.blit(text_surface, (100, 100 + index * 40))

