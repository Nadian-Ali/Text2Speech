# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 05:39:37 2022

@author: Ali Nadian 
"""

import os
import wave
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import librosa.display

root_german = 'D:\Datasets\German_Male_TTS\sorted_german_tts'
root_Javanese = 'D:\Datasets\jv_id_female'
folder = 'wavs'
path_to_waves = os.path.join(root_Javanese,folder)
print(path_to_waves )


file_names = [f for f in os.listdir(path_to_waves) if os.path.isfile(os.path.join(path_to_waves, f))]




def get_signal_signiture(file_names,path_to_waves):
    file = np.random.randint(len(file_names))
    
    
    file_name = file_names[file]
    file_path = os.path.join(path_to_waves,file_name)
    
    print(file_name,'\n',file_path)
    
    y, sr = librosa.load(file_path)
    
    plt.title(str(file_name))
    plt.xlabel('Sample')
    plt.ylabel('value')
    plt.plot(y) 
    
    sr = 22050
    X = librosa.stft(y)
    Xdb = librosa.power_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    # plt.ylim([0,400])
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')

    return file_name 


get_signal_signiture(file_names,path_to_waves)


# 'German_TTS_011723.wav' for silence inbetween






