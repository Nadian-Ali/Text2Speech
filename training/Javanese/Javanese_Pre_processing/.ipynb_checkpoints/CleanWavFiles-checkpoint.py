# -*- coding: utf-8 -*-
"""
Created on Mon May  9 05:08:44 2022

@author: Ali Nadian 
"""



import os
import wave
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import librosa.display
import json
import pprint
import IPython
import matplotlib.pyplot as plt
import IPython.display as ipd
import soundfile as sf

def clean_wav(wav,trim_db=25,split_db=30):
    
    # significantly_trimed = False
    significantly_split = False
    clips = []
    # trim start end
    clip,indexs = librosa.effects.trim(wav, top_db= trim_db) 
    # print(indexs,indexs[1],indexs[0],len(indexs))
    
     
    #split silence in the middle 
    clips = librosa.effects.split(clip, top_db=split_db)
    wave_extended = []
    for c in clips:
        # print(c)
        data = clip[c[0]: c[1]]
        wave_extended.extend(data)
    # sf.write('5s.wav', wav_data, sr)
    wave_extended = np.array(wave_extended)
    
    #trim percentage
    #work out significant difference and save record if it too much is cut
    #lets say too much is .01% of the the signal 
    signal_length = np.shape(wav)[0]
    trimed_lenght = indexs[1]-indexs[0]
    trimed_percentage = 100 * (signal_length-trimed_lenght)/signal_length

        
    #split precentage
    #process wav to see what is how much we cut from it 
    #see if the amount we cut is significant 
    split_length = sum([x[1]-x[0] for x in clips])
    split_percentage = 100 * (signal_length-split_length)/signal_length
    
    #info 
        #did we split siginicantly? 
        #did we trim sginificantly?
        #where did we split? 

    
    info = {
    
        'trimed_percentage': trimed_percentage,
        'split_percentaeg':split_percentage,
    
        'split_index':[list(c) for c in clips],
        'trimmed_index':list(indexs),
        'wav_length':signal_length,
        'split_length' : split_length,
        }
    return clip,wave_extended,info


# root_german = 'D:\Datasets\German_Male_TTS\sorted_german_tts'
root_Javanese = 'D:\Datasets\jv_id_female'

root = root_Javanese
folder = 'wavs_original'
folder_trimed = 'wavs_trimed'
folder_split = 'wavs_split'
path_to_waves = os.path.join(root,folder)
pre_processed_info = {}


file_names = [f for f in os.listdir(path_to_waves) if os.path.isfile(os.path.join(path_to_waves, f))]



for idx,file_name in enumerate(file_names):
    
    if (idx%10==0):
        print('{} % done'.format(100 * idx/len(file_names)))
        
    file_path = os.path.join(path_to_waves,file_name)
    wav, sr = librosa.load(file_path)
    trimed,split,info = clean_wav(wav,trim_db=25,split_db=30)
    info['file_name']=file_name
    pre_processed_info[file_name] = info
    
    # save trimed file
    trimed_path = os.path.join(root,folder_trimed,file_name)
    sf.write(trimed_path, trimed, sr)
    # save split file 
    split_path = os.path.join(root,folder_split,file_name)
    sf.write(split_path, split, sr)

import pickle
with open('d:\saved_dictionary.pkl', 'wb') as f:
    pickle.dump(pre_processed_info, f)








