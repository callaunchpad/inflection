from torch.utils.data import Dataset, DataLoader, random_split
from nnmnkwii.preprocessing.alignment import DTWAligner
import librosa
from scipy.io import wavfile
import os
from nnmnkwii.metrics import melcd
import numpy as np

class AudioData(Dataset): 
    #Input and output directories (should change to joanna when done)
    DATASET_INP = "../../../../datasets/cmu_artic" + "/cmu_us_clb_arctic/wav"
    DATASET_OUT = "../../../../datasets/cmu_artic" + "/cmu_us_rms_arctic/wav"
    
    def __init__(self, n_mfcc = 40, win_length = 400, hop_length = 160):
        self.data_dir = AudioData.DATASET_INP # Joanna
        self.recording_dir = AudioData.DATASET_OUT  # random voices
        self.sampling_frequency = 16000
        self.n_mfcc = n_mfcc
        self.win_length = win_length
        self.hop_length = hop_length
        self.files = [file for file in os.listdir(self.data_dir) if file[-4:] == '.wav']
        self.aligner = DTWAligner(verbose=0, dist=melcd)
        
    def align(self, X, Y):
        X, Y = self.aligner.transform((np.array([X]), np.array([Y])))
        return X[0], Y[0]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        fs_X, X = wavfile.read(os.path.join(self.data_dir, self.files[idx]))
        fs_Y, Y = wavfile.read(os.path.join(self.recording_dir, self.files[idx]))
        mfcc_X = librosa.feature.mfcc(np.array(X, dtype=np.float), self.sampling_frequency, n_mfcc=self.n_mfcc, win_length=self.win_length, hop_length=self.hop_length)
        mfcc_Y = librosa.feature.mfcc(np.array(Y, dtype=np.float), self.sampling_frequency, n_mfcc=self.n_mfcc, win_length=self.win_length, hop_length=self.hop_length)
        X, Y = self.align(mfcc_X.T,mfcc_Y.T)
        return X,Y

    def decode(data):
        inverted_audio = librosa.feature.inverse.mfcc_to_audio(mfcc, sr=self.sampling_frequency, win_length=self.win_length, hop_length=self.hop_length)

def get_dataloaders(ad):
    val_size = len(ad)//5 
    sizes = [len(ad) - val_size, val_size]
    train_data, val_data = random_split(ad, sizes)
    train_dataloader = DataLoader(train_data, batch_size=1, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size = 1, shuffle=True)
    return train_dataloader, val_dataloader

