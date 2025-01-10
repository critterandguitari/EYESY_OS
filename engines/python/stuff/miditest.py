
import mido

print("Available input ports:", mido.get_input_names())
print("Available output ports:", mido.get_output_names())

with mido.open_input('ttymidi:MIDI in 128:0') as inport:
    for msg in inport:
        print(msg)
