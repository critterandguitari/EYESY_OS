import pygame

def ok_callback():
    print("OK")

def cancel_callback():
    print("CANCEL")

class WidgetDialog():

    def __init__(self, app_state, ok_callback=ok_callback, cancel_callback=cancel_callback):
        self.app_state = app_state
        # Initialize text, surfaces, fonts, etc.
        self.message = "Disconnect from Dogs?"
        self.keyboard_surface = pygame.Surface((300, 50))
        self.dialog_surface = pygame.Surface((300, 100))
        self.ok_callback = ok_callback
        self.cancel_callback = cancel_callback
        # Define the keyboard layout for lowercase and uppercase
        self.lower_keys = [
            ['Cancel','Yes']
        ]
        self.flat_keys_lower = [key for row in self.lower_keys for key in row]

        self.total_keys = len(self.flat_keys_lower)
        self.rows = len(self.lower_keys)  # 5
        # The top 4 rows have 10 columns each, the last row has 3
        self.cols_top = 2
        self.selected_index = 0
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font("font.ttf", 16)

    def draw_keyboard(self, surface):
        keys = self.lower_keys

        total_width = surface.get_width()
        total_height = surface.get_height()

        # Define colors
        key_color = (0,0,0)
        highlight_color = (100, 100, 100)
        text_color = (200,200,200)

        index = 0
        for row_idx, row in enumerate(keys):
            if row_idx < 4:
                # Top four rows: 10 keys each
                key_width = total_width // self.cols_top
                key_height = total_height // self.rows
                for col_idx, key in enumerate(row):
                    x = col_idx * key_width
                    y = row_idx * key_height
                    rect = pygame.Rect(x, y, key_width, key_height)

                    # Highlight the selected key
                    pygame.draw.rect(surface, highlight_color if self.selected_index == index else key_color, rect)

                    text_surf = self.font.render(key, True, text_color)
                    text_rect = text_surf.get_rect(center=rect.center)
                    surface.blit(text_surf, text_rect)
                    index += 1

    def get_key(self, index):
        """
        Returns the key character at the specified index,
        taking into account the shift state.
        """
        flat_keys = self.flat_keys_lower

        if 0 <= index < len(flat_keys):
            return flat_keys[index]
        else:
            return None

    def draw_textbox(self, surface, x, y, size, string, font):
        """
        Draws a textbox on the surface at position (x, y) of given size.
        Displays the string as-is (no hiding).
        Left-justifies the text.
        """
        textbox_rect = pygame.Rect(x, y, size[0], size[1])
        #pygame.draw.rect(surface, (0, 0, 0), textbox_rect)  
        #pygame.draw.rect(surface, (200,200,200), textbox_rect, width=1)

        # Render the display string
        text_surf = font.render(string, True, (200,200,200))
        text_rect = text_surf.get_rect()
        # Left-justify: place text_rect left side inside the textbox with some padding
        text_rect.left = textbox_rect.left + 12
        text_rect.centery = textbox_rect.centery
        surface.blit(text_surf, text_rect)

    def handle_events(self):
        # Handle other events if needed
        app_data = self.app_state

        # Example navigation (assuming app_data.keyX_press are booleans):
        if app_data.key6_press:
            self.selected_index -= 1
        if app_data.key7_press:
            self.selected_index += 1

        # Wrap around
        if self.selected_index >= self.total_keys:
            self.selected_index = 0
        if self.selected_index < 0:
            self.selected_index = self.total_keys - 1

        # Key selection/activation
        if app_data.key8_press:
            selected_key = self.get_key(self.selected_index)
            if selected_key:
                if self.selected_index == 0:
                    self.cancel_callback()
                elif self.selected_index == 1:
                    self.ok_callback()

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        self.keyboard_surface.fill((0, 0, 0))
        self.dialog_surface.fill((0, 0, 0))

        # Draw the keyboard onto the keyboard_surface
        self.draw_keyboard(self.keyboard_surface)

        # Blit the keyboard_surface onto the dialog surface
        self.dialog_surface.blit(self.keyboard_surface, (0, 50))
        pygame.draw.rect(self.dialog_surface, (200,200,200), (0, 0, 299, 99), width=1)
        x_offset = 90
        y_offset = 120

        # Draw the textbox onto the dialog surface
        textbox_x = 0
        textbox_y = 0
        self.draw_textbox(self.dialog_surface, textbox_x, textbox_y, (300, 40), self.message, self.font)
        surface.blit(self.dialog_surface, (100, 100))

    def goto_home(self):
        pass
        # self.app_state.current_screen = self.app_state.menu_screens["info"]

