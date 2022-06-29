# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 06:13:52 2022

@author: Me
"""
import os
import ffmpeg
from os import listdir
from os.path import isfile, join

          # D:\Datasets\Geramn_Male_TTS\Geramn_Male_TTS\thorsten-de\wavs
# mypath = 'D:\Datasets\Geramn_Male_TTS\Geramn_Male_TTS\thorsten-de\wavs'
# output_dir_audio = 'D:/Datasets/Geramn_Male_TTS/Geramn_Male_TTS/thorsten-de'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# wav= join(mypath,onlyfiles[0])

# (ffmpeg
#       .input(wav)
#       .output(os.path.join(output_dir_audio, os.path.basename(wav)), acodec='pcm_s16le', ac=1, ar=22050, loglevel='error')
#       .overwrite_output()
#       .run(capture_stdout=True)
#     )
#, acodec='pcm_s16le', ac=1, ar=22050, loglevel='info')
(ffmpeg
  .input('A.wav')
  .output('b.wav', acodec='pcm_s16le', ac=1, ar=22050, loglevel='error')
  .overwrite_output()
  .run(capture_stdout=True)
)
