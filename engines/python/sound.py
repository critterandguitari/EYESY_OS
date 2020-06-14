import alsaaudio, audioop
import time
import math

inp = None
etc = None
trig_this_time = 0
trig_last_time = 0
sin = [0] * 100

def init (etc_object) :
    global inp, etc, trig_this_time, trig_last_time, sin
    etc = etc_object
    #setup alsa for sound in
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
    inp.setchannels(1)
    inp.setrate(11025)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(300)
    trig_last_time = time.time()
    trig_this_time = time.time()
    
    for i in range(0,100) :
        sin[i] = int(math.sin(2 * 3.1459 * i / 100) * 32700)

def recv() :
    global inp, etc, trig_this_time, trig_last_time, sin
    # get audio
    l,data = inp.read()
    peak = 0
    while l:
        for i in range(0,100) :
            try :
                avg = audioop.getsample(data, 2, i * 3)
                avg += audioop.getsample(data, 2, (i * 3) + 1)
                avg += audioop.getsample(data, 2, (i * 3) + 2)
                avg = avg / 3
                # scale it
                avg = int(avg * etc.audio_scale)
                if (avg > 20000) :
                    trig_this_time = time.time()
                    if (trig_this_time - trig_last_time) > .05:
                        if etc.audio_trig_enable: etc.audio_trig = True
                        trig_last_time = trig_this_time
                if avg > peak :
                    etc.audio_peak = avg
                    peak = avg
                # if the trigger button is held
                if (etc.trig_button) :
                    etc.audio_in[i] = sin[i] 
                else :
                    etc.audio_in[i] = avg

            except :
                pass
        l,data = inp.read()


