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
        self.font = pygame.font.Font("font.ttf", 16)  # Customize font and size as needed

    def handle_events(self):
        self.selected_index = int(self.app_state.knob1 * len(self.items) * .99 ) 
        #if self.app_state.key4_press:
        #    self.selected_index = (self.selected_index - 1) % len(self.items)
        #elif self.app_state.key5_press:
        #    self.selected_index = (self.selected_index + 1) % len(self.items)
        if self.app_state.key2_press:
            self.items[self.selected_index].action()

    def render(self, surface):
        pygame.draw.rect(surface, (0,0,0), (20, 20, 600, 440))
        for index, item in enumerate(self.items):
            color = (200, 200, 200)
            bgcolor = (0,0,0)
            if index == self.selected_index:
                bgcolor = (100,100,100)  # Highlight selected item
            text_surface = self.font.render(item.text, True, color, bgcolor)
            surface.blit(text_surface, (50, 50 + index * 25))

