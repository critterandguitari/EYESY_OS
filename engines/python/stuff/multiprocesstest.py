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
    rate = 44100  # Adjust as needed
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

def main():
    """Main PyGame program."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption("Audio Visualization")
    clock = pygame.time.Clock()

    # Shared resources
    shared_buffer = Array(c_float, BUFFER_SIZE, lock=True)  # Circular buffer
    write_index = Value('i', 0)  # Write index for the buffer
    lock = shared_buffer.get_lock()  # Lock for thread-safe access

    # Start the audio processing in a separate process
    audio_process = Process(target=audio_processing, args=(shared_buffer, write_index, lock))
    audio_process.start()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Calculate the average of the buffer
            with lock:
                average_value = sum(abs(sample) for sample in shared_buffer) / BUFFER_SIZE

            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw a rectangle based on the average value
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                pygame.Rect(100, 300, 600, int(abs(average_value) / 10))
            )

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)
    finally:
        # Ensure the audio processing process is terminated
        audio_process.terminate()
        audio_process.join()

# Run the program
if __name__ == "__main__":
    main()

