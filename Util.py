import audioop
import time
import wave
import pyaudio
from Constants import * 

def log(layer, content, severity):
    print(severity+'[{layer}] \t| {content}'.format(layer=type(layer).__name__, content=content) + ENDC)

def playBeep():
    wf = wave.open('beep.wav', 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)


    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
        # if data == b'':
        #     wf.rewind()
        #     data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()
    
    # close PyAudio (5)
    p.terminate()
    wf.rewind()

def split(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def timestamp():
    return int(round(time.time() * 1000))


def getVol(data):
    return audioop.rms(data,2)

