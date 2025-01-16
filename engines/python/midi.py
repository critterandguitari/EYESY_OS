import time
import mido

input_port = None

def _handle_note(etc, message):
    #print(f"Note message: {message}")
    ch = message.channel
    if ch == 0 or ch == etc.config["midi_channel"]:
        num = message.note 
        val = message.velocity
        if val > 0 :
            etc.midi_notes[num] = 1
        else :
            etc.midi_notes[num] = 0

def _handle_control_change(etc, message):
    #print(f"Control Change message: {message}")
    ch = message.channel
    if ch == 0 or ch == etc.config["midi_channel"]:
        num = message.control
        val = message.value
        if message.control == etc.config["knob1_cc"] : etc.knob_hardware[0] = val / 127.
        if message.control == etc.config["knob2_cc"] : etc.knob_hardware[1] = val / 127.
        if message.control == etc.config["knob3_cc"] : etc.knob_hardware[2] = val / 127.
        if message.control == etc.config["knob4_cc"] : etc.knob_hardware[3] = val / 127.
        if message.control == etc.config["knob5_cc"] : etc.knob_hardware[4] = val / 127.
        if message.control == etc.config["knob5_cc"] : 
            if val > 64 :
                etc.auto_clear = True
            else:
                etc.auto_clear = False
        

def _handle_program_change(etc, message):
    print(f"Program Change message: {message}")

def init():
    global input_port
    try:
        input_port = mido.open_input('ttymidi:MIDI in 128:0')  # Replace with your actual MIDI port name
    except Exception as e:
        print(f"Error initializing input port: {e}")
        input_port = None

def close():
    global input_port
    try:
        if input_port:
            input_port.close()
    except Exception as e:
        print(f"Error closing input port: {e}")

def recv(etc):
    global input_port
    if not input_port:
        #print("Input port is not initialized.")
        return

    try:
        messages = []
        for message in input_port.iter_pending():  # Non-blocking iteration
            messages.append(message)

        for message in messages:
            try:
                if message.type == 'note_on' or message.type == 'note_off':
                    _handle_note(etc, message)
                elif message.type == 'control_change':
                    _handle_control_change(etc, message)
                elif message.type == 'program_change':
                    _handle_program_change(etc, message)
            except Exception as e:
                print(f"Error processing message {message}: {e}")
    except Exception as e:
        print(f"Error receiving messages: {e}")

