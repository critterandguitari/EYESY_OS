# screen.py
import pygame

class Screen:
    def __init__(self, app_state):
        self.app_state = app_state
        self.font = pygame.font.Font("font.ttf", 16)

    def handle_events(self):
        """Handle input events."""
        pass

    def update(self):
        """Update the screen's state."""
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
        pygame.draw.rect(surface, (200,200,200), (20, 20, 620, 420), width=1)
        pygame.draw.rect(surface, (0,0,0), (21, 21, 618, 418))
        self.render(surface)

    def render(self, surface):
        """Render the screen."""
        pass

