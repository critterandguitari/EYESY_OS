import time
import mido

# Open MIDI input port
input_port = mido.open_input('ttymidi:MIDI in 128:0')  # Replace with your actual MIDI port name

# Functions to handle specific MIDI message types
def handle_note(message):
    print(f"Note message: {message}")

def handle_control_change(message):
    print(f"Control Change message: {message}")

def handle_program_change(message):
    print(f"Program Change message: {message}")

# Function to check for MIDI messages
def check_midi():
    messages = []
    for message in input_port.iter_pending():  # Non-blocking iteration
        messages.append(message)
    return messages

# Main loop to check and process MIDI messages
try:
    print("Listening for MIDI messages... Press Ctrl+C to quit.")
    while True:
        midi_messages = check_midi()
        for message in midi_messages:
            if message.type == 'note_on' or message.type == 'note_off':
                handle_note(message)
            elif message.type == 'control_change':
                handle_control_change(message)
            elif message.type == 'program_change':
                handle_program_change(message)
        time.sleep(0.05)  # Run approximately 20 times per second (50 ms per iteration)
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    input_port.close()

