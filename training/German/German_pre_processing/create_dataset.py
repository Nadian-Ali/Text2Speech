# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:17:57 2022

@author: Ali Nadian
"""


# read avialable data and store in lists

from os import listdir
from os.path import isfile, join
import logging


speaker = 'DUMMY'
first_time = True

"""    setup_logger     """
log = logging.getLogger()
log.setLevel(logging.INFO)
fh = logging.FileHandler(filename='D:/Datasets/jv_id_female/log_file.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
                fmt='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )
fh.setFormatter(formatter)
log.addHandler(fh)
"""  setup logging finished   """
log.info('--------------------this is a new session-----------------------')

 
"""        read data including a text file and the wave names              """
#get the name of the wave files 
path_to_waves = 'D:\Datasets\jv_id_female\wavs'
file_names = [f for f in listdir(path_to_waves) if isfile(join(path_to_waves, f))]
log.info('filenames extract')

# get the numebr of wave_files 
num_samples = len(file_names)
log.info('number of samples is {}'.format(num_samples))

#read the transcripts
path_to_tsv = 'D:\Datasets\jv_id_female\line_index.tsv'
with open('D:\Datasets\jv_id_female\line_index.tsv','r') as file:
    transcripts = file.readlines()
log.info('the transcript file was read')
"""                             finished reading the data                  """




"""                         create Kaldi data style                        """
"""
for files have to be created : text utt2spk  spk2utt wav.csp

each file is formatted as below :
                text        <utt> <transcript>
                wav.csp     <utt> <path to wave>
                utt2spk     <utt> <speakr>  is it is a single speaker then speaker is dummy
                spk2utt     <speeker> <utt1> <utt2> ...
                for a sample file look into                 
"""



match = 0

with open('D:/Datasets/jv_id_female/text','w')     as texts,\
     open('D:/Datasets/jv_id_female/wavs.csp','w') as wavs,\
     open('D:/Datasets/jv_id_female/utt2spk','w')  as utt2spk,\
     open('D:/Datasets/jv_id_female/spk2utt','w')  as spk2utt:      
    for idx,Sentence in enumerate(transcripts):
        to_write = Sentence.split('\t')[0] + ' ' + Sentence.split('\t')[1]
        texts.writelines(to_write)
        
        wave_name = file_names[idx].split('.')[0]
        if Sentence.split('\t')[0] == wave_name:
            match+=1
            to_write_in_wav = Sentence.split('\t')[0]+ ' ' + 'wavs/'+file_names[idx]+'\n'
            wavs.writelines(to_write_in_wav)
            # if match == num_samples:
            #     log.info('number of matches and num_samples are equal')
            # else:
            #     log.info('Exiting : number of matches and num_samples are NOT equal')
    
        write_to_utt2spk = Sentence.split('\t')[0]+ ' ' + speaker+'\n'
        utt2spk.writelines(write_to_utt2spk)
        
        if first_time:
            spk2utt.writelines(speaker)
            spk2utt.writelines(' ')
            first_time = False
        
        spk2utt_to_write = Sentence.split('\t')[0]+ ' '
        spk2utt.writelines(spk2utt_to_write)
        
log.info('wavs.csp file and text files were created in {} and {}'.format(2,3))








log.removeHandler(fh)
del log,fh




