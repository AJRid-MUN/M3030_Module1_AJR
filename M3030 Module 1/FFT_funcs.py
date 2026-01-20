import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from pydub import AudioSegment 
from pathlib import Path

#pads our function with zeroes to do cooley-tukey!!
#not that we can't use a similar algorithm, but I
#would like to stick to the definition i got from
#that paper.
def pad_zeroes(a):
    if isinstance(a, np.ndarray):
        length=len(a)
        if (length & (length-1)) == 0:
            return a
        else:
            i=1
            while 2**i < length:
                i+=1
            return np.pad(a, (0,2**i-length), mode='constant')
    else:
        print("pad_zeroes expects a numpy array argument.")
        return None
#might later want to also return the amount padded so if we modulate on
#frequency domain, we can remove our appended silence in output audio

def compute_twiddles(N):
    n=np.arange(N)
    twiddles=np.exp((-2j*np.pi*n)/N)
    return twiddles
    
def Cooley_Tukey(a):
    if isinstance(a, np.ndarray):
        N=len(a)
        twiddles=compute_twiddles(N)
        return 0
    else:
        print("Cooley_Tukey expects a numpy array argument.")
        return None
#seems a good place to stop... haha
