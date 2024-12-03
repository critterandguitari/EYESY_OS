from multiprocessing import Process, Array, Value
from ctypes import c_float
import alsaaudio
import struct
import pygame
import time

BUFFER_SIZE = 100  # Size of the circular buffer

def audio_processing(shared_buffer, write_index, lock):
    """Audio processing function running in a separate process."""
    card_index = 1
    channels = 1
    format = alsaaudio.PCM_FORMAT_S16_LE
    period_size = 32
    rate = 32000  # Adjust as needed
    bytes_per_sample = 2  # S16_LE = 2 bytes per sample

    # Open PCM device for capture in blocking mode
    pcm = alsaaudio.PCM(
        type=alsaaudio.PCM_CAPTURE,
        mode=alsaaudio.PCM_NORMAL,
        cardindex=card_index,
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
                    for i in range(0, len(samples), 4):
                        if i + 4 <= len(samples):
                            avg_sample = sum(samples[i:i+4]) / 4
                            shared_buffer[write_index.value] = avg_sample
                            write_index.value = (write_index.value + 1) % BUFFER_SIZE

    finally:
        pcm.close()


