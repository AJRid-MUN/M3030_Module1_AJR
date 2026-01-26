import numpy as np
from scipy.io.wavfile import write
from matplotlib import pyplot as plt
from pydub import AudioSegment 
from pathlib import Path
import FFT_funcs as FFT

array=np.random.uniform(-1, 1, 60000).astype(np.float32)

output=FFT.normalize(array)

write("Output.wav", 44100, output.astype(np.float32))

print("written noise to Output.wav.")
