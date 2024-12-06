import pygame
from screen import Screen



def draw_controls(surface):
    WHITE = (255, 255, 255)

    # Panel dimensions and position
    panel_x, panel_y = 50, 50
    panel_width, panel_height = 355, 200

    # Draw panel outline
    pygame.draw.rect(surface, WHITE, (panel_x, panel_y, panel_width, panel_height), width=1)

    # Define a grid on the panel
    # For example, a 10 x 10 grid
    grid_rows = 11
    grid_cols = 11

    cell_width = panel_width / grid_cols
    cell_height = panel_height / grid_rows

    # Helper function to get pixel coordinates from grid coords
    # Using (row, col) indexing, top-left is (0,0).
    def grid_pos(row, col):
        x = panel_x + (col + 0.5)*cell_width
        y = panel_y + (row + 0.5)*cell_height
        return (int(x), int(y))

    # Circle radii
    button_radius = 12
    knob_radius = 16

    # Top row buttons
    top_button_positions = [(2, 1), (2, 6), (2, 8)]
    for (r, c) in top_button_positions:
        px, py = grid_pos(r, c)
        pygame.draw.circle(surface, WHITE, (px, py), button_radius, width=1)

    # Middle row knobs
    # Let's use half steps by adding 0.5 to columns for more natural centering
    mid_knob_positions = [(5, 1), (5, 3), (5, 5), (5, 7), (5, 9)]
    for (r, c) in mid_knob_positions:
        # Since c might be float, just handle it directly
        px = int(panel_x + (c + 0.5)*cell_width)   # shift by +0.5 cell_width for center
        py = int(panel_y + (r + 0.5)*cell_height)
        pygame.draw.circle(surface, WHITE, (px, py), knob_radius, width=1)

    # Bottom row buttons
    bottom_button_positions = [(8, 1), (8, 2), (8, 4), (8, 5), (8, 6), (8, 8), (8, 9)]
    for (r, c) in bottom_button_positions:
        px = int(panel_x + (c + 0.5)*cell_width)
        py = int(panel_y + (r + 0.5)*cell_height)
        pygame.draw.circle(surface, WHITE, (px, py), button_radius, width=1)



class TestScreen(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        # Initialize any necessary variables here

    def handle_events(self):
        if self.app_state.key4_press:
            self.app_state.current_screen = self.app_state.menu_screens["home"]
        
    def update(self):
        pass  # No dynamic updates needed for this screen

    def render(self, surface):
        surface.fill((0, 0, 0))  # Clear the screen with black
        draw_controls(surface)
