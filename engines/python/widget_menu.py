import pygame

class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action  # Function to call when item is selected

class WidgetMenu:
    VISIBLE_ITEMS = 8  # Number of menu items visible at a time
    
    def __init__(self, app_state, items):
        self.app_state = app_state
        self.items = items  # List of MenuItem instances
        self.selected_index = 0
        self.font = pygame.font.Font("font.ttf", 16)
        self.off_x = 50
        self.off_y = 70
        
        # Use a system font (like Arial) for the arrow indicators

        # This determines which item in the list is at the top of the visible window
        self.start_index = 0

    def set_selected_index(self, index):
        """Externally set the selected index, ensuring it is visible."""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self._adjust_view()

    def handle_events(self):
        if self.app_state.key6_press:
            # Move up if not at the top already
            if self.selected_index > 0:
                self.selected_index -= 1
                self._adjust_view()
        elif self.app_state.key7_press:
            # Move down if not at the bottom already
            if self.selected_index < len(self.items) - 1:
                self.selected_index += 1
                self._adjust_view()
        elif self.app_state.key8_press:
            self.items[self.selected_index].action()

    def _adjust_view(self):
        # Ensure the selected item is always visible
        if self.selected_index < self.start_index:
            self.start_index = self.selected_index
        elif self.selected_index >= self.start_index + self.VISIBLE_ITEMS:
            self.start_index = self.selected_index - self.VISIBLE_ITEMS + 1
        
        max_start = max(0, len(self.items) - self.VISIBLE_ITEMS)
        if self.start_index > max_start:
            self.start_index = max_start

    def render(self, surface):

        # Determine the visible slice of items
        visible_slice = self.items[self.start_index:self.start_index+self.VISIBLE_ITEMS]

        # Render each visible menu item
        for i, item in enumerate(visible_slice):
            index = self.start_index + i
            color = (200, 200, 200)
            bgcolor = (0,0,0)
            if index == self.selected_index:
                bgcolor = (100,100,100)  # Highlight selected item

            # Add spaces before and after the text
            display_text = f" {item.text} "
            text_surface = self.font.render(display_text, True, color, bgcolor)
            y_pos = 30 + self.off_y + i * 25
            surface.blit(text_surface, (self.off_x, y_pos))

        # Draw "up" arrow if there are items above the current view
        if self.start_index > 0:
            up_arrow = self.font.render(" ▲", True, (200, 200, 200))
            surface.blit(up_arrow, (self.off_x, self.off_y))  # Positioned above the first visible item

        # Draw "down" arrow if there are items below the current view
        if self.start_index + self.VISIBLE_ITEMS < len(self.items):
            down_arrow = self.font.render(" ▼", True, (200, 200, 200))
            bottom_y = self.off_y + (len(visible_slice)-1)*25 + 60
            surface.blit(down_arrow, (self.off_x, bottom_y))

