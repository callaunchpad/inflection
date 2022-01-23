from scipy.io import wavfile
import pyworld
import pysptk
import torch

import torch.nn as nn
import numpy as np
import os

n_mfcc = 40

fs = 22050
fftlen = pyworld.get_cheaptrick_fft_size(fs)
alpha = pysptk.util.mcepalpha(fs)

torch.cuda.empty_cache()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

inp = 'response2.wav'

def preprocess(data):
    data = data.astype(np.float64)
    f0, sp, ap = pyworld.wav2world(data, fs)
    mcc = pysptk.sp2mc(sp, order=n_mfcc, alpha = alpha)
    return mcc, f0, ap

def decode(mcc, f0, ap):
    sp = pysptk.mc2sp(
            mcc.astype(np.float64), alpha=alpha, fftlen=fftlen)
    waveform = pyworld.synthesize(
            f0, sp, ap, fs)
    return waveform

def predict(mcc):
    ...

def convert():
    fs, data_inp = wavfile.read(inp)

    mcc, f0, ap = preprocess(data_inp)

    predicted_mcc = mcc.copy()
    predicted_mcc[:,1:] = predict(mcc[:,1:])

    prediction = decode(predicted_mcc, f0 * 1.15, ap)

    data=np.int16(prediction/np.max(np.abs(prediction)) * 32767)
    wavfile.write('output.wav', 22050, data)




