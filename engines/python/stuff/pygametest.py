import pygame
import os

# Force Pygame to use KMSDRM (if running headless)
os.environ["SDL_VIDEODRIVER"] = "KMSDRM"

# Initialize Pygame
pygame.init()

# Get screen size (automatically detects resolution)
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

# Create fullscreen Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Define colors
RED = (255, 0, 0)

# Square properties
square_size = min(WIDTH, HEIGHT) // 4  # Make it 1/4th of the smallest screen dimension
square_x = (WIDTH - square_size) // 2
square_y = (HEIGHT - square_size) // 2

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen (black background)
    screen.fill((0, 0, 0))

    # Draw red square in the center
    pygame.draw.rect(screen, RED, (square_x, square_y, square_size, square_size))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

