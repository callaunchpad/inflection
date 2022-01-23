import pyworld
from scipy.io import wavfile

import IPython
from IPython.display import Audio

import matplotlib.pyplot as plt
import numpy as np
import pysptk
import sys
from pydub import AudioSegment
import math

NAME = sys.argv[1]
INPUT_FILE = f"{NAME}.mp3"

sampling_frequency, data = wavfile.read(INPUT_FILE)
IPython.display.display(Audio(data.T, rate = sampling_frequency))
plt.plot(data)
print("Sampling Frequency: ", sampling_frequency)

class SplitWavAudioMubin():
    def __init__(self, filename):
        self.filename = filename
        self.filepath = filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 1000
        t2 = to_min * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(split_filename, format="wav")
        
    def multiple_split(self, secs_per_split):
        total_secs = math.ceil(self.get_duration())
        for i in range(0, total_secs, secs_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+secs_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_secs - secs_per_split:
                print('All splited successfully')

split_wav = SplitWavAudioMubin(INPUT_FILE)
split_wav.multiple_split(secs_per_split=15)