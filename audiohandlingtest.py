import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from pydub import AudioSegment 
from pathlib import Path
import FFT_funcs as FFT

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
N=len(array)
print("Input.wav contains ",N," samples!")

DC_offset=np.mean(array)

if DC_offset != 0:
    print("DC offset detected! Correcting...")
    array=array-DC_offset
    print("DC offset corrected.")

plt.plot(array)
plt.title("Input.wav Amplitude over Time")
plt.xlabel("Time (1/"+str(samplerate)+"s)")
plt.ylabel("Amplitude")
plt.show()

DFT_array=FFT.FFT_Cooley_Tukey(FFT.pad_zeroes(array))

N=len(FFT.pad_zeroes(array))

print("after padding, we have ",N," samples.") 

freqs=FFT.get_freq_bins(samplerate, N)

plt.plot(freqs[:N//2], np.abs(DFT_array)[:N//2]) ##I guess it's redundant to include values >N//2...
plt.title("Input.wav frequency distribution")
plt.xlabel("frequency (Hz.)")
plt.ylabel("Coefficient")
plt.show()



