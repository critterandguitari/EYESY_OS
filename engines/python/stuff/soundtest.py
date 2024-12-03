import alsaaudio
import audioop
import time


# Open PCM device for capture with non-blocking mode
pcm = alsaaudio.PCM(
    type=alsaaudio.PCM_CAPTURE,
    mode=alsaaudio.PCM_NONBLOCK,
    cardindex=1,
    channels=1,
    rate=16000,
    format = alsaaudio.PCM_FORMAT_S16_LE,
    periodsize=1024,
    periods=4
)

pcm.dumpinfo()

# Capture loop
try:
    while True:
        time.sleep(.05)
        length, data = pcm.read()
        if length < 0:
            length, data = pcm.read()
        print(str(length)) 
        if length > 0:
           #print(audioop.getsample(data, 2, 0))
           print(str(length)) 
            
except KeyboardInterrupt:
    print("Capture stopped.")
finally:
    pcm.close()

