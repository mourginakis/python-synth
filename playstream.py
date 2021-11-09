import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
# import time
import matplotlib.pyplot as plot
from itertools import count
from random import seed, random


sps = 44100     # Samples per second
tau = 2*np.pi   # Because i'm a Tau purist
                # https://tauday.com/tau-manifesto

# For debugging                
#seed(2)


#############
## Sample Sounds

def organ(t, f=400):
    """Example Organ Modifier Function.
    To be used with generator core, in seconds.
    -- Input: time, frequency."""
    return np.sin(tau*2*f*t)+np.sin(tau*f*t)


def clarinet(t, f=229):
    """Example Clarinet Modifier Function.
    To be used with generator core, in seconds.
    -- Input: time, frequency."""
    return 0.4*(1 * np.sin(tau*1*t*f)
                + 0.7 * np.sin(tau*2*t*f)
                + 0.5 * np.sin(tau*3*t*f)
                + 0.4 * np.sin(tau*4*t*f)
                + 0.3 * np.sin(tau*5*t*f)
                + 0.3 * np.sin(tau*6*t*f)
                + 0.2 * np.sin(tau*7*t*f)
                + 0.1 * np.sin(tau*8*t*f))


def random_klangfarbe(t, f=122):
    """Example Klangfarbe Modifier Function.
    To be used with generator core, in seconds.
    -- Input: time, frequency."""
    return 0.2*(random() * np.sin(tau*1*t*f)
                + random() * np.sin(tau*1*t*f)
                + random() * np.sin(tau*2*t*f)
                + random() * np.sin(tau*3*t*f)
                + random() * np.sin(tau*4*t*f)
                + random() * np.sin(tau*5*t*f)
                + random() * np.sin(tau*6*t*f)
                + random() * np.sin(tau*7*t*f))


def white_noise(t):
    """Example White Noise Modifier Function.
    To be used with generator core, in seconds.
    -- Input: time.
    -- Returns: Random from (-1, 1)"""
    return 2*(random()-0.5)


def adsr(t):
    """Example ADSR envelope Modifier Function.
    To be used with generator core, in seconds.
    -- Input: time."""
    return abs(np.sin(20*t))




#############
## Main program functions begin

def core(sps = 44100):
    """Elegant Generator function using count, returns time in s"""
    # y = t = sample/sps
    return map(lambda x: x/sps, count())


def playstream(generator):
        """
        Play the waveform from generator with a callback stream
        -- Input: A generator function that represents a sound stream.
        -- Returns: nothing
        """
        blocksize = 4410
        try:
            def callback(outdata, frames, time, status):
                if status:
                    print(status) #file=sys.stderr
                outdata[:, 0] = np.fromiter(generator,
                                            float,
                                            count=blocksize) 
        
            with sd.OutputStream(channels=1,
                                 callback=callback,
                                 samplerate=sps,
                                 blocksize=blocksize):
                print('#' * 80)
                print('press Return to quit')
                print('#' * 80)
                input()
          
        except KeyboardInterrupt:
           parser.exit('')


def outport(generator, filename, seconds):
    """
    Write to wav file.
    -- Input: generator object, filename, number of seconds
    """
    waveform = np.fromiter(generator, float, count=seconds*sps)
    waveform_integers = np.int16(waveform * 32767)
    write(filename, sps, waveform_integers)


if __name__ == "__main__":
    """Example!
    playstream takes a generator as a function, use map to apply a
    modifier function to the generator core"""
    playstream(map(lambda x: adsr(x) * clarinet(x), core()))
    outport(map(lambda x: adsr(x) * clarinet(x), core()), 'out.wav', 2)


