# screen.py
import pygame

class Screen:
    def __init__(self, app_state):
        self.app_state = app_state
        self.title = "My Cool Screen"
        self.font = pygame.font.Font("font.ttf", 16)

    def handle_events(self):
        """Handle input events."""
        pass

    def before(self):
        """Update the screen's state."""
        print ("first time")
        pass

    def after(self):
        """Update the screen's state."""
        print ("before leaving")
        pass
    
    def render_with_title(self, surface):
        pygame.draw.rect(surface, (200,200,200), (20, 20, 600, 440), width=1) #640x480 - 40x40
        pygame.draw.rect(surface, (0,0,0), (21, 21, 598, 438))
        pygame.draw.line(surface, (200,200,200), (20, 50), (619, 50), 1)
        text_surface = self.font.render(self.title, True, (200,200,200), (0,0,0))
        surface.blit(text_surface, (32, 24))
        self.render(surface)

    def render(self, surface):
        """Render the screen."""
        pass

