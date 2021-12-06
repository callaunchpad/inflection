from torch.utils.data import Dataset, DataLoader, random_split
from nnmnkwii.preprocessing.alignment import DTWAligner
import librosa
from scipy.io import wavfile
import os
from nnmnkwii.metrics import melcd
import numpy as np
import pyworld
import pysptk
import torch

class AudioData(Dataset): 
    #Input and output directories (should change to joanna when done)
    DATASET_INP = "../../../../datasets/inflection/inflection_data" + "/joanna"
    DATASET_OUT = "../../../../datasets/inflection/inflection_data" + "/human"
    
    def __init__(self, n_mfcc = 40, win_length = 400, hop_length = 160):
        fs = 22050
        self.data_dir = AudioData.DATASET_INP # Joanna
        self.recording_dir = AudioData.DATASET_OUT  # random voices
        self.sampling_frequency = fs
        self.n_mfcc = n_mfcc
        self.win_length = win_length
        self.hop_length = hop_length
        self.files = [file for file in os.listdir(self.data_dir) if file[-4:] == '.wav']
        self.fftlen = pyworld.get_cheaptrick_fft_size(fs)
        self.alpha = pysptk.util.mcepalpha(fs)
        self.aligner = DTWAligner(verbose=0, dist=melcd)

    def __len__(self):
        return len(self.files)
    
    def preprocess(self,data):
        fs = self.sampling_frequency
        data = data.astype(np.float64)
        f0, sp, ap = pyworld.wav2world(data, fs)
        mcc = pysptk.sp2mc(sp, order= self.n_mfcc, alpha = self.alpha)
        return mcc, f0, ap
    
    def align(self, X, Y):
        X, Y = self.aligner.transform((np.array([X]), np.array([Y])))
        return X[0], Y[0]

    def __getitem__(self, idx):
        fs_X, X = wavfile.read(os.path.join(self.data_dir, self.files[idx]))
        fs_Y, Y = wavfile.read(os.path.join(self.recording_dir, self.files[idx]))
        X = self.preprocess(X)
        Y = self.preprocess(Y)
        aligned_input, aligned_output = self.align(X[0],Y[0])
        aux = (X,Y)
        return aligned_input, aligned_output, aux
    
    def decode(self, data):
        mcc, f0, ap = data
        mcc = torch.squeeze(mcc).cpu().detach().numpy()
        f0 = torch.squeeze(f0).cpu().detach().numpy()
        ap = torch.squeeze(ap).cpu().detach().numpy()
        fs = self.sampling_frequency
        sp = pysptk.mc2sp(
                mcc.astype(np.float64), alpha=self.alpha, fftlen=self.fftlen)
        waveform = pyworld.synthesize(
                f0, sp, ap, fs)
        return waveform

def get_dataloaders(ad):
    val_size = len(ad)//5 
    sizes = [len(ad) - val_size, val_size]
    train_data, val_data = random_split(ad, sizes)
    train_dataloader = DataLoader(train_data, batch_size=1, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size = 1, shuffle=True)
    return train_dataloader, val_dataloader