import numpy as np
from scipy.io.wavfile import write
from matplotlib import pyplot as plt
from pydub import AudioSegment 
from pathlib import Path
import FFT_funcs as FFT

currentpath = Path(__file__).resolve()
currentdir = currentpath.parent

inputpath = currentdir/"Input"/"Input.wav"

audio = AudioSegment.from_file(inputpath)

samplerate = audio.frame_rate
print("Input.wav has sample rate:", samplerate,"Hz.")

if audio.channels == 1:
    print("working with mono...")
elif audio.channels == 2:
    print("working with stereo, converting to mono...")
    audio = audio.set_channels(1)
    print("converted to mono.")

array_raw = audio.get_array_of_samples()
array = np.array(array_raw)
print("converted to array for modification and analysis.")
N=len(array)
print("Input.wav contains ",N," samples!")

padded_array=FFT.pad_zeroes(array)
DFT_array=FFT.FFT_Cooley_Tukey(padded_array)
print("fourier transform obtained.")

outputarray=FFT.iFFT_Cooley_Tukey(DFT_array)
print("inverse fourier transform complete.")
output_real = np.real(outputarray) ##turns out ive been outputting complex values
output_real/=np.max(np.abs(output_real)) ##normalize it!! (this could be done within the FFT function, probably with better respect to the original audio volume, but whatever!!

write("Output.wav", samplerate, output_real.astype(np.float32))
print("written to Output.wav!")
