import time
import traceback
import mido

input_port = None

def _handle_note(eyesy, message):
    #print(f"Note message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        num = message.note 
        val = message.velocity
        if val > 0 :
            eyesy.midi_notes[num] = 1
        else :
            eyesy.midi_notes[num] = 0

def _handle_control_change(eyesy, message):
    #print(f"Control Change message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        num = message.control
        val = message.value
        if message.control == eyesy.config["knob1_cc"] : eyesy.knob_hardware[0] = val / 127.
        if message.control == eyesy.config["knob2_cc"] : eyesy.knob_hardware[1] = val / 127.
        if message.control == eyesy.config["knob3_cc"] : eyesy.knob_hardware[2] = val / 127.
        if message.control == eyesy.config["knob4_cc"] : eyesy.knob_hardware[3] = val / 127.
        if message.control == eyesy.config["knob5_cc"] : eyesy.knob_hardware[4] = val / 127.
        if message.control == eyesy.config["auto_clear_cc"] : 
            if val > 64 :
                eyesy.auto_clear = True
            else:
                eyesy.auto_clear = False
       
def _handle_program_change(eyesy, message):
    #print(f"Program Change message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        if f"pgm_{message.program + 1}" in eyesy.config["pc_map"]:
            scene = eyesy.config["pc_map"][f"pgm_{message.program + 1}"]
            print(f"attempting to load scene {scene}")
            eyesy.recall_scene_by_name(scene)

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

def recv(eyesy):
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
                    _handle_note(eyesy, message)
                elif message.type == 'control_change':
                    _handle_control_change(eyesy, message)
                elif message.type == 'program_change':
                    _handle_program_change(eyesy, message)
            except Exception as e:
                print(traceback.format_exc())
                print(f"Error processing message {message}: {e}")
    except Exception as e:
        print(f"Error receiving messages: {e}")

