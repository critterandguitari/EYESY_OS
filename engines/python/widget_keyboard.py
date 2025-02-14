import pygame

class WidgetKeyboard():

    def __init__(self, eyesy, connect_callback=None, cancel_callback=None):
        self.eyesy = eyesy
        # Initialize text, surfaces, fonts, eyesy.
        self.text_box_text = ""
        self.keyboard_surface = pygame.Surface((400, 200))
        self.keyboard_surface.fill((0, 0, 0))
        self.textbox_font = pygame.font.Font("font.ttf", 20)
        self.connect_callback = connect_callback
        self.cancel_callback = cancel_callback

        # Define the keyboard layout for lowercase and uppercase
        self.lower_keys = [
            ['1','2','3','4','5','6','7','8','9','0'],
            ['a','b','c','d','e','f','g','h','i','j'],
            ['k','l','m','n','o','p','q','r','s','t'],
            ['u','v','w','x','y','z',';',',','.','/'],
            ['^','_','<'],
            ['Cancel','Connect']
        ]
        self.upper_keys = [
            ['!','@','#','$','%','^','&','*','(',')'],
            ['A','B','C','D','E','F','G','H','I','J'],
            ['K','L','M','N','O','P','Q','R','S','T'],
            ['U','V','W','X','Y','Z',':','<','>','?'],
            ['^','_','<'],
            ['Cancel','Connect']
        ]
        
        self.flat_keys_lower = [key for row in self.lower_keys for key in row]
        self.flat_keys_upper = [key for row in self.upper_keys for key in row]

        # Total keys: 4 rows x 10 keys = 40 + 1 row x 3 keys = 43
        self.total_keys = len(self.flat_keys_lower)
        # Dimensions
        self.rows = len(self.lower_keys)  # 5
        # The top 4 rows have 10 columns each, the last row has 3
        self.cols_top = 10
        self.cols_bottom = 3

        self.selected_index = 0
        self.row_index = 0 # for nav
        self.col_index = 0

        # Track shift state internally
        self.shift = False

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font("font.ttf", 20)
        self.font16 = pygame.font.Font("font.ttf", 16)

    def draw_keyboard(self, surface):
        """
        Draws the keyboard on the given surface.
        Uses self.shift to determine which case to display.
        """
        keys = self.upper_keys if self.shift else self.lower_keys

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
            elif row_idx == 4:
                # Bottom row: 3 keys each taking one-third of the width
                key_width = total_width // self.cols_bottom
                key_height = total_height // self.rows
                for col_idx, key in enumerate(row):
                    x = col_idx * key_width
                    y = row_idx * key_height
                    rect = pygame.Rect(x, y, key_width, key_height)

                    pygame.draw.rect(surface, highlight_color if self.selected_index == index else key_color, rect)

                    text_surf = self.font.render(key, True, text_color)
                    text_rect = text_surf.get_rect(center=rect.center)
                    surface.blit(text_surf, text_rect)
                    index += 1
            elif row_idx == 5:
                # Bottom row: 3 keys each taking one-third of the width
                key_width = total_width // 2
                key_height = total_height // self.rows
                for col_idx, key in enumerate(row):
                    x = col_idx * key_width
                    y = row_idx * key_height + 5
                    rect = pygame.Rect(x, y, key_width, key_height)

                    pygame.draw.rect(surface, highlight_color if self.selected_index == index else key_color, rect)

                    text_surf = self.font16.render(key, True, text_color)
                    text_rect = text_surf.get_rect(center=rect.center)
                    surface.blit(text_surf, text_rect)
                    index += 1

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

    def draw_textbox(self, surface, x, y, size, string, font):
        """
        Draws a textbox on the surface at position (x, y) of given size.
        Displays the string as-is (no hiding).
        Left-justifies the text.
        """
        textbox_rect = pygame.Rect(x, y, size[0], size[1])
        pygame.draw.rect(surface, (0, 0, 0), textbox_rect)  
        pygame.draw.rect(surface, (200,200,200), textbox_rect, width=1)

        # Render the display string
        text_surf = font.render(string, True, (200,200,200))
        text_rect = text_surf.get_rect()
        # Left-justify: place text_rect left side inside the textbox with some padding
        text_rect.left = textbox_rect.left + 5
        text_rect.centery = textbox_rect.centery
        surface.blit(text_surf, text_rect)

    def handle_events(self):
        # Handle other events if needed
        eyesy = self.eyesy

        # navigate using rows and columns
        if eyesy.key4_press:
            if self.col_index > 0 :
                self.col_index -= 1

        if eyesy.key5_press:
            if self.col_index < len(self.lower_keys[self.row_index])-1 :
                self.col_index += 1

        if eyesy.key6_press:
            if self.row_index > 0 :
                self.row_index -= 1
                # correct column when moving to new row with dif len
                if self.row_index == 3:
                    self.col_index = int(self.col_index * (10/3))
                if self.row_index == 4:
                    self.col_index = int(self.col_index * (3/2))

        if eyesy.key7_press:
            if self.row_index < 5 :
                self.row_index += 1 
                # correct column when moving to new row with dif len
                if self.row_index == 4 :
                    self.col_index = int(self.col_index / (10/3))
                if self.row_index == 5 :
                    self.col_index = int(self.col_index / (3/2))

        # get index from row col index
        # handle last 2 rows separately
        if self.row_index < 4:
            self.selected_index = self.col_index + self.row_index * 10
        elif self.row_index == 4 :
            self.selected_index = 40 + self.col_index
        elif self.row_index == 5 : 
            self.selected_index = 43 + self.col_index
        
        # for using knob for navigation
        # self.selected_index = int(self.eyesy.knob1 * (len(self.flat_keys_lower) - 1))
        
        # Key selection/activation
        if eyesy.key8_press:
            selected_key = self.get_key(self.selected_index)
            if selected_key:
                lower_key = selected_key.lower()
                # Index 40: shift
                if self.selected_index == 40:
                    self.shift = not self.shift
                # Index 41: space ('_')
                elif self.selected_index == 41:
                    self.text_box_text += ' '
                # Index 42: backspace ('<')
                elif self.selected_index == 42:
                    if len(self.text_box_text) > 0:
                        self.text_box_text = self.text_box_text[:-1]
                elif self.selected_index == 43:
                    self.cancel_callback()
                elif self.selected_index == 44:
                    self.connect_callback(self.text_box_text)
                else:
                    # Append the selected key character
                    self.text_box_text += selected_key

    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        """
        Handles keyboard rendering.
        """
        # Clear the keyboard surface before drawing
        self.keyboard_surface.fill((0, 0, 0))

        # Draw the keyboard onto the keyboard_surface
        self.draw_keyboard(self.keyboard_surface)

        # Blit the keyboard_surface onto the main surface
        x_offset = 90
        y_offset = 200
        surface.blit(self.keyboard_surface, (x_offset, y_offset))

        # Draw the textbox onto the main surface
        textbox_x = x_offset
        textbox_y = 130  # 10 pixels padding below keyboard
        self.draw_textbox(surface, textbox_x, textbox_y, (400, 40), self.text_box_text, self.textbox_font)

    def goto_home(self):
        pass
        # self.eyesy.current_screen = self.eyesy.menu_screens["info"]

