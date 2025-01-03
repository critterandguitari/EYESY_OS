
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

import pygame

def draw_color_palette(surface, app_state):
    
    # bg
    width, height = 260, 260  
    xoff = 350
    yoff = 100
    for i in range(height):
        # Get the color using the color_picker function
        color = app_state.color_picker_bg(i / height)
        # Draw a horizontal line (1 pixel high)
        pygame.draw.line(surface, color, (xoff, i + yoff), (width - 1 + xoff, i + yoff))

    # fg
    width, height = 160, 160  
    xoff = 420
    yoff = 170
    for i in range(height):
        # Get the color using the color_picker function
        color = app_state.color_picker(i / height)
        # Draw a horizontal line (1 pixel high)
        pygame.draw.line(surface, color, (xoff, i + yoff), (width - 1 + xoff, i + yoff))


# Function to handle palette selection, not really necessary to set them since they get set with each selection anyway?
def select_palette(app_state, index):
    pass

# Function to dynamically create a menu based on palettes
def create_palette_menu(app_state):
    menu_items = []
    for i, palette in enumerate(app_state.palettes):
        # Create a menu item for each palette
        menu_items.append(MenuItem(palette['name'], lambda i=i: select_palette(app_state, i)))

    # Return the menu object
    return WidgetMenu(app_state, menu_items)

class ScreenPalette(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "Color Palette"
        self.fg_menu = create_palette_menu(app_state)
        self.bg_menu = create_palette_menu(app_state)
        self.fg_menu.off_y = 50
        self.bg_menu.off_y = 250
        #self.menu.items.append(MenuItem('◀ Exit', self.goto_home))

    def handle_events(self):
        self.bg_menu.handle_events()
        self.fg_menu.handle_events_k4_k5()
        self.app_state.fg_palette = min(len(self.app_state.palettes)-1, self.fg_menu.selected_index)
        self.app_state.bg_palette = min(len(self.app_state.palettes)-1, self.bg_menu.selected_index)
        if self.app_state.key8_press:
            self.exit_menu()
    
    def render(self, surface):
        self.fg_menu.render(surface)
        self.bg_menu.render(surface)
        draw_color_palette(surface, self.app_state)

    def before(self):
        self.fg_menu.set_selected_index(self.app_state.fg_palette)
        self.bg_menu.set_selected_index(self.app_state.bg_palette)

    def goto_home(self):
        self.app_state.current_screen = self.app_state.menu_screens["home"]

    def exit_menu(self):
        self.app_state.osd_menu_select = 0
        self.app_state.show_osd = False
        self.app_state.show_menu = False

