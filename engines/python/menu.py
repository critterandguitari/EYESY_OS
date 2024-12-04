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
        if self.app_state.key_nav_up:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif self.app_state.key_nav_down:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        elif self.app_state.key_nav_select:
            self.items[self.selected_index].action()
        # Left and right keys will be handled in the screen's handle_events method

    def render(self, surface):
        #surface.fill((0, 0, 0))  # Clear screen with black
        for index, item in enumerate(self.items):
            color = (255, 255, 255)
            if index == self.selected_index:
                color = (255, 215, 0)  # Highlight selected item
            text_surface = self.font.render(item.text, True, color)
            surface.blit(text_surface, (100, 100 + index * 40))

