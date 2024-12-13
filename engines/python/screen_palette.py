
from screen import Screen
from menu import Menu, MenuItem

import pygame

def draw_color_palette(surface, app_state):
    
    width, height = 300, 50  # Dimensions of the preview
    xoff = 50
    yoff = 400
    for i in range(width):
        # Get the color using the color_picker function
        color = app_state.color_picker(i / width)
        # Draw a vertical line (1 pixel wide)
        #pygame.draw.line(surface, color, (i+xoff, yoff), (i+xoff, height - 1 + yoff))
        pygame.draw.line(surface, color, (i+xoff, yoff), (i+xoff, height - 1 + yoff))

# Function to handle palette selection
def select_palette(app_state, index):
    app_state.palette = index
    print(f"Selected palette: {app_state.palettes[index]['name']}")

# Function to dynamically create a menu based on palettes
def create_palette_menu(app_state):
    menu_items = []
    for i, palette in enumerate(app_state.palettes):
        # Create a menu item for each palette
        menu_items.append(MenuItem(palette['name'], lambda i=i: select_palette(app_state, i)))

    # Return the menu object
    return Menu(app_state, menu_items)

class PaletteMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = create_palette_menu(app_state)
        self.menu.items.append(MenuItem('< Exit', self.goto_home))

    def handle_events(self):
        self.menu.handle_events()
        self.app_state.palette = min(len(self.app_state.palettes)-1, self.menu.selected_index)
        if self.app_state.key8_press:
            self.exit_menu()
    
    def update(self):
        pass  # Update logic if needed

    def render(self, surface):
        self.menu.render(surface)
        draw_color_palette(surface, self.app_state)

    def before(self):
        print("entering color palette")
        self.menu.selected_index = self.app_state.palette

    def goto_home(self):
        self.app_state.current_screen = self.app_state.menu_screens["home"]

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

