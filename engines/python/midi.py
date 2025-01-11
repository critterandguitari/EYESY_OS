import time
import mido

input_port = None

def init():
    global input_port
    input_port = mido.open_input('ttymidi:MIDI in 128:0')  # Replace with your actual MIDI port name

def close():
    global input_port
    input_port.close()

def handle_note(message):
    print(f"Note message: {message}")

def handle_control_change(message):
    print(f"Control Change message: {message}")

def handle_program_change(message):
    print(f"Program Change message: {message}")

def recv():
    global input_port
    messages = []
    for message in input_port.iter_pending():  # Non-blocking iteration
        messages.append(message)
    for message in messages:
        if message.type == 'note_on' or message.type == 'note_off':
            handle_note(message)
        elif message.type == 'control_change':
            handle_control_change(message)
        elif message.type == 'program_change':
            handle_program_change(message)

