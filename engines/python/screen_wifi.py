import pygame

# Global password variable
password = ""

class Keyboard:
    def __init__(self):
        # Define the keyboard layout for lowercase and uppercase
        self.lower_keys = [
            ['1','2','3','4','5','6','7','8','9','0'],
            ['q','w','e','r','t','y','u','i','o','p'],
            ['a','s','d','f','g','h','j','k','l',';'],
            ['z','x','c','v','b','n','m',',','.','/'],
            ['^','_','<']
        ]
        self.upper_keys = [
            ['!','@','#','$','%','^','&','*','(',')'],
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L',':'],
            ['Z','X','C','V','B','N','M','<','>','?'],
            ['^','_','<']
        ]

        self.flat_keys_lower = [key for row in self.lower_keys for key in row]
        self.flat_keys_upper = [key for row in self.upper_keys for key in row]

        # Total keys: 4 rows x 10 keys = 40 + 1 row x 3 keys = 43
        self.total_keys = len(self.flat_keys_lower)
        # Dimensions
        self.rows = len(self.lower_keys)  # 5
        # The top 4 rows have 10 columns, the last row has 3 columns
        self.cols_top = 10
        self.cols_bottom = 3

        # By default, no key is highlighted
        self.highlight_index = None

        # Track shift state internally
        self.shift = False

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font("font.ttf", 24)

    def draw(self, surface):
        """
        Draws the keyboard on the given surface.
        Uses self.shift to determine which case to display.
        """
        keys = self.upper_keys if self.shift else self.lower_keys

        total_width = surface.get_width()
        total_height = surface.get_height()

        # Define colors
        key_color = (0,0,0)       # Light gray for keys
        highlight_color = (100, 100, 100)     # Red for highlighted key
        text_color = (200,200,200)           # Black for key labels

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
                    if self.highlight_index == index:
                        pygame.draw.rect(surface, highlight_color, rect)
                    else:
                        pygame.draw.rect(surface, key_color, rect)

                    text_surf = self.font.render(key, True, text_color)
                    text_rect = text_surf.get_rect(center=rect.center)
                    surface.blit(text_surf, text_rect)
                    index += 1
            else:
                # Bottom row: 3 keys each taking one-third of the width
                key_width = total_width // self.cols_bottom
                key_height = total_height // self.rows
                for col_idx, key in enumerate(row):
                    x = col_idx * key_width
                    y = row_idx * key_height
                    rect = pygame.Rect(x, y, key_width, key_height)

                    if self.highlight_index == index:
                        pygame.draw.rect(surface, highlight_color, rect)
                    else:
                        pygame.draw.rect(surface, key_color, rect)

                    text_surf = self.font.render(key, True, text_color)
                    text_rect = text_surf.get_rect(center=rect.center)
                    surface.blit(text_surf, text_rect)
                    index += 1

    def highlight(self, index):
        """
        Sets the index of the key to highlight.
        """
        self.highlight_index = index

    def get_key(self, index):
        """
        Returns the key character at the specified index,
        taking into account the shift state.
        """
        if self.shift:
            flat_keys = self.flat_keys_upper
        else:
            flat_keys = self.flat_keys_lower

        if 0 <= index < len(flat_keys):
            return flat_keys[index]
        else:
            return None

def draw_textbox(surface, x, y, size, string, font):
    """
    Draws a textbox on the surface at position (x, y) of given size.
    Displays the string as-is (no hiding).
    Left-justifies the text.
    """
    # Draw the textbox rectangle
    textbox_rect = pygame.Rect(x, y, size[0], size[1])
    pygame.draw.rect(surface, (0, 0, 0), textbox_rect)  

    # Display the string as-is
    display_string = string

    # Render the display string
    text_surf = font.render(display_string, True, (200,200,200))
    text_rect = text_surf.get_rect()
    # Left-justify: place text_rect left side inside the textbox with some padding
    text_rect.left = textbox_rect.left + 5
    text_rect.centery = textbox_rect.centery
    surface.blit(text_surf, text_rect)

# Initialize static resources outside the function
keyboard_surface = pygame.Surface((400, 200))
keyboard_surface.fill((0, 0, 0))  
textbox_font = pygame.font.Font("font.ttf", 30)
keyboard = Keyboard()

def keyboard_selector(surface, app_data):
    """
    Handles keyboard interaction and displays it on the main surface.

    Parameters:
    - surface: Main Pygame surface to draw onto.
    - app_data: Object containing knob values and keys.
      app_data should have:
        app_data.knob1 (float): 0.0 to 1.0 for key selection
    """
    global password
    global keyboard_surface, keyboard

    # Map knob input to key index (0 to total_keys - 1)
    knob_value = max(0.0, min(app_data.knob1, 1.0))
    selected_index = int(knob_value * (keyboard.total_keys - 1))

    # Set the highlighted key
    keyboard.highlight(selected_index)

    # Clear the keyboard surface before drawing
    keyboard_surface.fill((0, 0, 0))  # White background

    # Draw the keyboard onto the keyboard_surface
    keyboard.draw(keyboard_surface)

    # Blit the keyboard_surface onto the main surface
    x_offset = (surface.get_width() - 400) // 2
    y_offset = (surface.get_height() - 200 - 50) // 2
    surface.blit(keyboard_surface, (x_offset, y_offset))

    # Draw the textbox onto the main surface
    textbox_x = x_offset
    textbox_y = y_offset + 200 + 10  # 10 pixels padding below keyboard
    draw_textbox(surface, textbox_x, textbox_y, (400, 50), password, textbox_font)

# Handle key selection
def handle_key_events (app_data):
    global password
    if app_data.key4_press:
        app_data.current_screen = app_data.menu_screens["home"]
    if app_data.key8_press:
        selected_key = keyboard.get_key(keyboard.highlight_index)
        if selected_key:
            lower_key = selected_key.lower()
            if keyboard.highlight_index == 40:
                # Toggle shift mode
                keyboard.shift = not keyboard.shift
            elif keyboard.highlight_index == 41:
                # Add a space
                password += ' '
            elif keyboard.highlight_index == 42:
                # Remove last character if any
                if len(password) > 0:
                    password = password[:-1]
            else:
                # Append the selected key character
                password += selected_key

from screen import Screen

class WiFiScreen(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)

    def handle_events(self):
        handle_key_events(self.app_state)
        # Handle other keys if needed

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        keyboard_selector(surface, self.app_state)

    def goto_home(self):
        pass
        #self.app_state.current_screen = self.app_state.menu_screens["info"]

