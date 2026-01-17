import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from pydub import AudioSegment 
from pathlib import Path

#Setting up to read my Input sample!
currentpath = Path(__file__).resolve()
currentdir = currentpath.parent

inputpath = currentdir/"Input"/"Input.wav"

#Making it possible to work on the file by
#Making it a pydub AudioSegment, and then
#Converting to a numpy array.
audio = AudioSegment.from_file(inputpath)

#would be good to know the sample rate and bit rate.
samplerate = audio.frame_rate
print("Input.wav has sample rate:", samplerate,"Hz.")

if audio.channels == 1:
    print("working with mono...")
elif audio.channels == 2:
    print("working with stereo, converting to mono...")
    #for now, I want to operate on mono audio, so I'll convert it:
    audio = audio.set_channels(1)
    print("converted to mono.")

array_raw = audio.get_array_of_samples() #Getting array of raw audio data...
array = np.array(array_raw)
print("converted to array for modification and analysis.")

plt.plot(array)
plt.title("Input.wav Amplitude over Time")
plt.xlabel("Time (1/"+str(samplerate)+"s)")
plt.ylabel("Amplitude")
plt.show()

