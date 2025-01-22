import pygame

class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action  # Function to call when item is selected
        self.adjustable = False   # adjustable value in place
        self.name = "none"
        self.value = 0
        self.min_value = 0
        self.max_value = 0
        self.format_string = ""

class WidgetMenu:
    
    def __init__(self, eyesy, items):
        self.eyesy = eyesy
        self.items = items  # List of MenuItem instances
        self.selected_index = 0
        self.font = pygame.font.Font("font.ttf", 16)
        self.off_x = 50
        self.off_y = 70
        self.visible_items = 6  # Number of menu items visible at a time
        
        self.key6_td = 0 # time pressed counters for repeating key
        self.key7_td = 0
        self.key4_td = 0
        self.key5_td = 0
        # This determines which item in the list is at the top of the visible window
        self.start_index = 0

    def set_selected_index(self, index):
        """Externally set the selected index, ensuring it is visible."""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self._adjust_view()

    # nav with key repeat
    def handle_events(self):
        if self.eyesy.key6_press: 
            self.menu_dec()
            self.key6_td = 0
        if self.eyesy.key6_status:
            self.key6_td += 1
            if self.key6_td > 10 : self.menu_dec()

        if self.eyesy.key7_press: 
            self.menu_inc()
            self.key7_td = 0
        if self.eyesy.key7_status:
            self.key7_td += 1
            if self.key7_td > 10 : self.menu_inc()
        if self.eyesy.key8_press:
            self.items[self.selected_index].action()

    def menu_dec(self):
        # Move up if not at the top already
        if self.selected_index > 0:
            self.selected_index -= 1
            self._adjust_view()

    def menu_inc(self):
        # Move down if not at the bottom already
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self._adjust_view()

    # use key 4 and 5 for scrolling instead
    def handle_events_k4_k5(self):
        if self.eyesy.key4_press: 
            self.menu_dec()
            self.key4_td = 0
        if self.eyesy.key4_status:
            self.key4_td += 1
            if self.key4_td > 10 : self.menu_dec()

        if self.eyesy.key5_press: 
            self.menu_inc()
            self.key5_td = 0
        if self.eyesy.key5_status:
            self.key5_td += 1
            if self.key5_td > 10 : self.menu_inc()
        
        if self.eyesy.key8_press:
            self.items[self.selected_index].action()


    def _adjust_view(self):
        # Ensure the selected item is always visible
        if self.selected_index < self.start_index:
            self.start_index = self.selected_index
        elif self.selected_index >= self.start_index + self.visible_items:
            self.start_index = self.selected_index - self.visible_items + 1
        
        max_start = max(0, len(self.items) - self.visible_items)
        if self.start_index > max_start:
            self.start_index = max_start

    def render(self, surface):
        # First, render your menu items as before:
        visible_slice = self.items[self.start_index:self.start_index + self.visible_items]

        for i, item in enumerate(visible_slice):
            index = self.start_index + i
            color = (200, 200, 200)
            bgcolor = (0, 0, 0)
            if index == self.selected_index:
                bgcolor = (100, 100, 100)  # highlight the selected item

            display_text = f" {item.text} "
            text_surface = self.font.render(display_text, True, color, bgcolor)
            y_pos = 30 + self.off_y + i * 25
            surface.blit(text_surface, (self.off_x, y_pos))

        # -----------------------------------------------------------------------
        # Now, let's draw a simple scrollbar on the LEFT of the menu items.
        # -----------------------------------------------------------------------
        
        total_items = len(self.items)
        visible_items = self.visible_items
        
        # If all items fit on screen, no need for a scrollbar
        if total_items <= visible_items:
            return
        
        # Scrollbar geometry:
        scrollbar_x = self.off_x - 15            # place scrollbar 15px left of text
        scrollbar_track_top = 50 + self.off_y
        track_color = (200, 200, 200)
        handle_color = (200, 200, 200)
        
        # Track height = 25 px per item * number of visible items
        track_height = 25 * (visible_items - 2) + 8
        
        # 1) Draw the track (a thin 1px vertical line)
        pygame.draw.line(
            surface,
            track_color,
            (scrollbar_x, scrollbar_track_top),
            (scrollbar_x, scrollbar_track_top + track_height),
            1
        )
        
        # 2) Compute the handle (the little rectangle)
        fraction_visible = visible_items / total_items
        handle_height = int(track_height * fraction_visible)
        # enforce a minimum handle size so it's visible
        handle_height = max(handle_height, 10) 

        max_scroll = total_items - visible_items
        scroll_ratio = self.start_index / max_scroll if max_scroll != 0 else 0.0
        
        handle_y = scrollbar_track_top + int(scroll_ratio * (track_height - handle_height))
        
        # Draw the handle as a 5px wide rectangle
        handle_rect = pygame.Rect(scrollbar_x - 2, handle_y, 5, handle_height + 2)
        pygame.draw.rect(surface, handle_color, handle_rect)
        
        # 3) Optional: draw up/down arrow text if there are items above or below
        arrow_color = (200, 200, 200)

        if self.start_index > 0:
            # Render an up-arrow character: "▲"
            up_arrow_surf = self.font.render("▲", True, arrow_color)
            # Position it just above the top of the scrollbar
            up_arrow_rect = up_arrow_surf.get_rect()
            up_arrow_rect.centerx = scrollbar_x
            # place it a few pixels above the track (10 px above in this example)
            up_arrow_rect.bottom = scrollbar_track_top + 5
            surface.blit(up_arrow_surf, up_arrow_rect)

        if self.start_index + visible_items < total_items:
            # Render a down-arrow character: "▼"
            down_arrow_surf = self.font.render("▼", True, arrow_color)
            # Position it just below the bottom of the scrollbar
            down_arrow_rect = down_arrow_surf.get_rect()
            down_arrow_rect.centerx = scrollbar_x
            # place it a few pixels below the track
            down_arrow_rect.top = scrollbar_track_top + track_height - 5
            surface.blit(down_arrow_surf, down_arrow_rect)

