import time
import mido

# Open MIDI input port
input_port = mido.open_input('ttymidi:MIDI in 128:0')  # Replace with your actual MIDI port name

# Function to check for MIDI messages
def check_midi():
    messages = []
    for message in input_port.iter_pending():  # Non-blocking iteration
        messages.append(message)
    return messages

# Main loop to check MIDI messages
try:
    print("Listening for MIDI messages... Press Ctrl+C to quit.")
    while True:
        midi_messages = check_midi()
        for message in midi_messages:
            print(message)  # Print each MIDI message to the console
        time.sleep(0.05)  # Run approximately 20 times per second (50 ms per iteration)
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    input_port.close()

