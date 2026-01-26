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

def DFT(a):
    if isinstance(a, np.ndarray):
        N=len(a)
        k=np.arange(N)
        fd=np.zeros(N, dtype=complex)

        for n in range(N):
            fd[n]=np.sum(a*np.exp((-2*np.pi*1j*k*n)/N))
            ##opted not to precompute the twiddles at a performance
            ##loss. i found handling them a bit tricky! might mess 
            ##with it later but for now im too stuck in one place.

        return fd

def iDFT(a):
    if isinstance(a, np.ndarray):
        N=len(a)
        k=np.arange(N)
        fd=np.zeros(N, dtype=complex)

        for n in range(N):
            fd[n]=np.sum(a*np.exp((2*np.pi*1j*k*n)/N))

        return fd/N
    
def FFT_Cooley_Tukey(a):
    if isinstance(a, np.ndarray):
        N=len(a)
        if N<= 2:
            return DFT(a)
        evens=a[::2]
        odds=a[1::2]
        FFT_evens=FFT_Cooley_Tukey(evens)
        FFT_odds=FFT_Cooley_Tukey(odds)
        fd=np.zeros(N, dtype=complex)

        for n in range(N//2):
            twiddle=np.exp((-2*np.pi*1j*n)/N)
            fd[n]=FFT_evens[n]+twiddle*FFT_odds[n]
            fd[n+N//2]=FFT_evens[n]-twiddle*FFT_odds[n]
        return fd

def get_freq_bins(sample_rate, N):
    return np.arange(0, N)*(sample_rate/N)

def iFFT_Cooley_Tukey(a):
    if isinstance(a, np.ndarray):
        N=len(a)
        if N<= 2:
            return iDFT(a)
        evens=a[::2]
        odds=a[1::2]
        FFT_evens=iFFT_Cooley_Tukey(evens)
        FFT_odds=iFFT_Cooley_Tukey(odds)
        fd=np.zeros(N, dtype=complex)

        for n in range(N//2):
            twiddle=np.exp((2*np.pi*1j*n)/N)
            fd[n]=FFT_evens[n]+twiddle*FFT_odds[n]
            fd[n+N//2]=FFT_evens[n]-twiddle*FFT_odds[n]
        return fd

def lowpass_flat_cutoff(a, cutoff): ##note that cutoff is on bins!! not frequencies.
    if isinstance(a, np.ndarray):
        N=len(a)
        if cutoff<N//2: ##cutoff>N//2 dont do anything by nyquist theorem
            a[cutoff:N-cutoff]=0 ##ensure to maintain symmetry across
            return a

def hipass_flat_cutoff(a, cutoff): 
    if isinstance(a, np.ndarray):
        N=len(a)
        if cutoff<N//2:
            a[:cutoff]=0 ##complement operation!!
            a[N-cutoff:]=0
            return a

def normalize(a):
    if isinstance(a, np.ndarray):
        max=np.max(np.abs(a))
        if max>0:
            a=a/max
        return a
