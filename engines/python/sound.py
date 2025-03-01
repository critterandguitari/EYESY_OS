from multiprocessing import Process, Array, Value
from ctypes import c_float
import alsaaudio
import struct
import pygame
import time

BUFFER_SIZE = 100  # Size of the circular buffer
max_peak = 0
max_peak_r = 0

def audio_processing(shared_buffer, shared_buffer_r, write_index, gain, peak, peak_r, lock):
    global max_peak, max_peak_r
    
    def find_alsa_card_index(target_name="audioinjector-pi-soundcard"):
        """Finds the correct ALSA hardware index using card names."""
        num_cards = alsaaudio.card_indexes()  # Gets actual ALSA internal indexes
        for index in num_cards:
            card_name = alsaaudio.card_name(index)[1]  # Extract name from (index, name) tuple
            print(f"card {index} : {card_name}")
            if target_name in card_name.lower():
                return index
        raise ValueError(f"Sound card '{target_name}' not found!")

    # Try to find the correct card index dynamically
    try:
        card_index = find_alsa_card_index()
        print(f"Using ALSA card index: {card_index}")
    except ValueError as e:
        print(e)
        exit(1)

    # PCM setup
    channels = 1
    format = alsaaudio.PCM_FORMAT_S16_LE
    period_size = 32
    rate = 32000  # Adjust as needed
    bytes_per_sample = 2  # S16_LE = 2 bytes per sample

    # Open PCM using the correct index
    pcm = alsaaudio.PCM(
        type=alsaaudio.PCM_CAPTURE,
        mode=alsaaudio.PCM_NORMAL,
        cardindex=card_index,  # Now using the correct ALSA index
        channels=channels,
        rate=rate,
        format=format,
        periodsize=period_size
    )

    # Print ALSA PCM configuration
    print(pcm.dumpinfo())
    
    try:
        while True:
            length, data = pcm.read()
            #print(f"{length}, {len(data)}")
            if length == 64:
                # Calculate the number of samples
                num_samples = length * bytes_per_sample

                # Unpack binary data into 16-bit signed integers
                samples = struct.unpack(f'<{num_samples}h', data)
                
                samples_l = samples[0::2]
                samples_r = samples[1::2]

                #print(len(samples))
                # Write samples to the circular buffer
                for i in range(0, len(samples_l), 16):
                    if i + 16 <= len(samples_l):
                        avg_sample = sum(samples_l[i:i+16]) / 16
                        avg_sample_r = sum(samples_r[i:i+16]) / 16

                        # Apply gain
                        avg_sample *= gain.value
                        avg_sample_r *= gain.value

                        # Clamp value to avoid overflow
                        avg_sample = max(-32768, min(32767, avg_sample))
                        avg_sample_r = max(-32768, min(32767, avg_sample_r))

                        # Check peak
                        if avg_sample > max_peak:
                            max_peak = avg_sample 
                        if avg_sample_r > max_peak_r:
                            max_peak_r = avg_sample_r  

                        # Lock only during shared variable writes
                        with lock:
                            shared_buffer[write_index.value] = avg_sample
                            shared_buffer_r[write_index.value] = avg_sample_r
                            write_index.value = (write_index.value + 1) % BUFFER_SIZE

                            # Update peak once per buffer cycle
                            if write_index.value == 0:
                                peak.value = max_peak
                                peak_r.value = max_peak_r
                                max_peak = 0  # Reset after committing
                                max_peak_r = 0  # Reset after committing


    finally:
        pcm.close()


