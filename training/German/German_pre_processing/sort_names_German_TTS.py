# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 10:11:25 2022

@author: Me
"""

# read data file / wave names and chnage the names

# lets give the following names

# Ger_TH_TSS_wavenumber


# a = ['1' , '101', '1002', '10003']

# b = [item.zfill(5) for item in a]


import os
import shutil
from os import listdir
from os.path import isfile, join

wav_path = 'D:\Datasets\German_Male_TTS\wavs'
wav_names = [f for f in listdir(wav_path) if isfile(join(wav_path, f))]
wav_only_name = [wav.split('.')[0] for wav in wav_names]


with open('D:\Datasets\German_Male_TTS\metadata.csv', 'r') as file:
    transcripts = file.readlines()


# we need two files :
    # new transcripts
    # new wave file

    # we want to all that from the transcripts file formatted as

    # wave_name , sentence


# read transcripts and
root = 'D:\Datasets\German_Male_TTS\sorted_german_tts'
current_wave_path = 'D:\Datasets\German_Male_TTS\wavs'
path_to_write_to =  'D:\Datasets\German_Male_TTS\sorted_german_tts\wavs'


with open(os.path.join(root,"sorted_metadata.csv"), 'w') as file:

    for idx, item in enumerate(transcripts):
   
        wav_name = item.split('|')[0]+'.wav'
        
        text = item.split('|')[1]
        new_wav_name_no_wav = 'German_TTS_'+str(idx).zfill(6)
        new_wav_name = 'German_TTS_'+str(idx).zfill(6)+'.wav'

        source_desitnation_wav = os.path.join(current_wave_path, wav_name)
        destiantion_wav = os.path.join(path_to_write_to, new_wav_name)
        #os.rename(src, dst)
        # print('destiantion_wav           ', destiantion_wav)
        # print('source_desitnation_wav    ', source_desitnation_wav)
        # os.rename(source_desitnation_wav,destiantion_wav)
        # shutil.copy(src,dst)
        shutil.copy(source_desitnation_wav, destiantion_wav)

        string = new_wav_name_no_wav +'|' + text
        file.writelines(string)
        
        if (idx%100==0):
            print('{}% of the files are processed'.format(100*idx/len(transcripts)))