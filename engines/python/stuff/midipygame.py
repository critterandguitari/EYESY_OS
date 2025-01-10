import pygame
import mido
import time

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_ROWS = 16  # Number of rows (total 128 notes / 16 rows = 8 columns)
GRID_COLS = 8   # Number of columns
NOTE_SQUARE_SIZE = 16#SCREEN_WIDTH // GRID_COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MIDI Note Visualizer")

# Open MIDI input port
input_port = mido.open_input('ttymidi:MIDI in 128:0')  # Replace with your actual MIDI port name

# State to track active notes
active_notes = [False] * 128  # 128 MIDI notes, all initially off

# Function to check for MIDI messages
def check_midi():
    for message in input_port.iter_pending():  # Non-blocking iteration
        if message.type == 'note_on' and message.velocity > 0:
            active_notes[message.note] = True
        elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
            active_notes[message.note] = False

# Function to draw the grid
def draw_grid():
    for note in range(128):
        row = note // GRID_COLS
        col = note % GRID_COLS
        x = col * NOTE_SQUARE_SIZE
        y = row * NOTE_SQUARE_SIZE
        color = RED if active_notes[note] else WHITE
        pygame.draw.rect(screen, color, (x, y, NOTE_SQUARE_SIZE, NOTE_SQUARE_SIZE), 0)
        pygame.draw.rect(screen, BLACK, (x, y, NOTE_SQUARE_SIZE, NOTE_SQUARE_SIZE), 1)  # Grid lines

# Main loop
running = True
try:
    print("Listening for MIDI messages... Press Ctrl+C to quit.")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for MIDI messages
        check_midi()

        # Draw the grid
        screen.fill(BLACK)
        draw_grid()
        pygame.display.flip()

        # Limit frame rate
        time.sleep(0.05)  # ~20 frames per second

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    input_port.close()
    pygame.quit()

