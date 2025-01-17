
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
        color = app_state.color_picker_bg_preview(i / height)
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

class ScreenPalette(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "Color Palette"
        self.fg_menu = self.create_fg_palette_menu()
        self.bg_menu = self.create_bg_palette_menu()
        self.fg_menu.off_y = 50
        self.bg_menu.off_y = 250
        #self.menu.items.append(MenuItem('◀ Exit', self.goto_home))
    
    # Function to dynamically create a menu based on palettes
    def create_fg_palette_menu(self):
        menu_items = []
        for i, palette in enumerate(self.app_state.palettes):
            # Create a menu item for each palette
            menu_items.append(MenuItem(palette['name'], self.select_fg_palette))

        # Return the menu object
        return WidgetMenu(self.app_state, menu_items)

    def create_bg_palette_menu(self):
        menu_items = []
        for i, palette in enumerate(self.app_state.palettes):
            # Create a menu item for each palette
            menu_items.append(MenuItem(palette['name'], self.select_bg_palette))

        # Return the menu object
        return WidgetMenu(self.app_state, menu_items)

    def select_fg_palette(self):
        self.app_state.fg_palette = min(len(self.app_state.palettes)-1, self.fg_menu.selected_index)

    def select_bg_palette(self):
        self.app_state.bg_palette = min(len(self.app_state.palettes)-1, self.bg_menu.selected_index)
     
    def handle_events(self):
        self.bg_menu.handle_events()
        self.fg_menu.handle_events_k4_k5()
        
        # save to config and exit on selection
        if self.app_state.key8_press:
            print("saving palette to config")
            self.app_state.config["bg_palette"] = self.app_state.bg_palette
            self.app_state.config["fg_palette"] = self.app_state.fg_palette
            self.app_state.save_config_file()
            self.exit_menu()
    
    def render(self, surface):
        self.fg_menu.render(surface)
        self.bg_menu.render(surface)
        
        # in order to preview the palettes, we need to set temporarily and then restore
        tmp_bg = self.app_state.bg_palette
        tmp_fg = self.app_state.fg_palette
        self.app_state.fg_palette =  min(len(self.app_state.palettes)-1, self.fg_menu.selected_index)
        self.app_state.bg_palette =  min(len(self.app_state.palettes)-1, self.bg_menu.selected_index)
        
        draw_color_palette(surface, self.app_state)

        self.app_state.bg_palette = tmp_bg
        self.app_state.fg_palette = tmp_fg

    def before(self):
        self.fg_menu.set_selected_index(self.app_state.fg_palette)
        self.bg_menu.set_selected_index(self.app_state.bg_palette)

    def goto_home(self):
        self.app_state.current_screen = self.app_state.menu_screens["home"]

    def exit_menu(self):
        self.app_state.exit_menu()

