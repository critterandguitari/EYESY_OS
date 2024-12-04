# screen.py

class Screen:
    def __init__(self, app_state):
        self.app_state = app_state

    def handle_events(self, events):
        """Handle input events."""
        pass

    def update(self):
        """Update the screen's state."""
        pass

    def render(self, surface):
        """Render the screen."""
        pass

