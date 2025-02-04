from multiprocessing import Process, Array, Value
from ctypes import c_float
import alsaaudio
import struct
import pygame
import time

BUFFER_SIZE = 100  # Size of the circular buffer
max_peak = 0

def audio_processing(shared_buffer, write_index, atrig, gain, peak, lock):
    global max_peak
    
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

    try:
        while True:
            length, data = pcm.read()
            if length == 64:
                # Calculate the number of samples
                num_samples = length * bytes_per_sample

                # Unpack binary data into 16-bit signed integers
                samples = struct.unpack(f'<{num_samples}h', data)

                # Write samples to the circular buffer
                with lock:
                    for i in range(0, len(samples), 16):
                        if i + 16 <= len(samples):
                            avg_sample = sum(samples[i:i+16]) / 16

                            # apply gain
                            avg_sample *= gain.value

                            # check for trigger
                            atrig.value = 0
                            if avg_sample > 5000: atrig.value = 1

                            # check peak value
                            if avg_sample > max_peak: max_peak = avg_sample

                            # write to buffer and increment
                            shared_buffer[write_index.value] = avg_sample
                            write_index.value = (write_index.value + 1) % BUFFER_SIZE
                            
                            # update peak once per buffer
                            if write_index.value == 0:
                                peak.value = max_peak
                                max_peak = 0

    finally:
        pcm.close()


