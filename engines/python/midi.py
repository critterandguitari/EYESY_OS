import time
import traceback
import mido

input_port = None
input_port_usb = None
midi_clock_count = 0

def _handle_note(eyesy, message):
    #print(f"Note message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        num = message.note 
        val = message.velocity
        if val > 0 :
            eyesy.midi_notes[num] = 1
            # 1 is trigger source for note
            if eyesy.config["trigger_source"] == 1: eyesy.trig = True 
            # select mode from note 
            if eyesy.config["notes_change_mode"] == 1:
                eyesy.mode_index = num % len(eyesy.mode_names)
                eyesy.set_mode_by_index(eyesy.mode_index)
        else :
            eyesy.midi_notes[num] = 0

def _handle_control_change(eyesy, message):
    #print(f"Control Change message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        num = message.control
        val = message.value
        if not eyesy.menu_mode : # don't update knobs in menu mode (interferes with test)
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
        if message.control == eyesy.config["fg_palette_cc"] : 
            eyesy.fg_palette = val % len(eyesy.palettes)
        if message.control == eyesy.config["bg_palette_cc"] : 
            eyesy.bg_palette = val % len(eyesy.palettes)
        if message.control == eyesy.config["mode_cc"] : 
            eyesy.mode_index = val % len(eyesy.mode_names)
            eyesy.set_mode_by_index(eyesy.mode_index)
       
def _handle_program_change(eyesy, message):
    #print(f"Program Change message: {message}")
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        if f"pgm_{message.program + 1}" in eyesy.config["pc_map"]:
            scene = eyesy.config["pc_map"][f"pgm_{message.program + 1}"]
            print(f"attempting to load scene {scene}")
            eyesy.recall_scene_by_name(scene)

def _handle_clock(eyesy, message):
    global midi_clock_count
    ts = eyesy.config["trigger_source"]
    if ts > 1:
        if ts == 2:
            if (midi_clock_count % 6) == 0: eyesy.trig = True
        elif ts == 3:
            if (midi_clock_count % 12) == 0: eyesy.trig = True
        elif ts == 4:
            if (midi_clock_count % 24) == 0: eyesy.trig = True
        elif ts == 5:
            if (midi_clock_count % 96) == 0: eyesy.trig = True
    midi_clock_count += 1

def init():
    global input_port, input_port_usb

    # first ttymidi
    try:
        input_port = mido.open_input('ttymidi:MIDI in 128:0') 
    except Exception as e:
        print(f"Error initializing ttymidi input port: {e}")
        input_port = None

    # try to get a USB midi port
    input_ports = mido.get_input_names()
    valid_port = next((port for port in input_ports if not port.startswith(("Midi Through", "ttymidi"))), None)
    try:
        input_port_usb = mido.open_input(valid_port) 
    except Exception as e:
        print(f"Error initializing input port: {e}")
        input_port_usb = None

def close():
    global input_port
    try:
        if input_port:
            input_port.close()
    except Exception as e:
        print(f"Error closing input port: {e}")

def recv(eyesy, input_port):
    if not input_port:
        #print("Input port is not initialized.")
        return

    try:
        messages = []
        for message in input_port.iter_pending():  # Non-blocking iteration
            messages.append(message)

        for message in messages:
            try:
                if message.type == 'clock':
                    _handle_clock(eyesy, message)
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

def recv_ttymidi(eyesy):
    global input_port
    recv(eyesy, input_port)

def recv_usbmidi(eyesy):
    global input_port_usb
    recv(eyesy, input_port_usb)
