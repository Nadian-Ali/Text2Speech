# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 07:10:06 2022

@author: Ali Nadain
"""
import os
from os import listdir
from os.path import isfile, join
import logging
import shutil


"""    Variable decelarations """
speaker = 'thorstenMueller'
first_time_train = True
first_time_test  = True
first_time_val   = True
not_found  =[]



root_path        = "D:\Datasets\German_Male_TTS\sorted_german_tts"
wav_folder       = "wavs"
transcript_file  = "sorted_metadata.csv"
data_folder      = 'data'
final_wav_folder = "wavs"
final_wav_path   = os.path.join(root_path,final_wav_folder)
data_path        = os.path.join(root_path,data_folder)
log_filename     = os.path.join(root_path,'logs.txt')
path_to_waves    = os.path.join(root_path,wav_folder)
transcript_path  = os.path.join(root_path,transcript_file)

""" Variable deceleration finished  """


"""    setup_logger     """
log = logging.getLogger()
log.setLevel(logging.INFO)
fh = logging.FileHandler(filename=log_filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
                fmt='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )
fh.setFormatter(formatter)
log.addHandler(fh)
"""  setup logging finished   """
log.info('--------------------this is a new session-----------------------')



def create_folders(data_path):
    log =logging.getLogger()
    if (os.path.isdir(data_path)):
        log.info('data folder was available / it was deleted and new folder was created')
        shutil.rmtree(data_path)
    log.info('data folder created')
    os.makedirs(os.path.join(data_path,"train"))
    os.makedirs(os.path.join(data_path,"valid"))
    os.makedirs(os.path.join(data_path,"test"))
    log.info("subfloders created")
    



def get_split_counts(samples,tr_portion = .89, val_portion = .10, test_portion = .01):
    log =logging.getLogger()
    if (tr_portion + val_portion + test_portion != 1):
        
        raise Exception(' the split protions should add up to 1')
        
    test_size  = round(samples*test_portion)
    val_size   = round(samples*val_portion)
    train_size = samples -test_size - val_size
    log.info('a total of {} train, {} validation, {} test samples are set'.format(train_size,val_size,test_size))
    return {'trn_smpls':train_size,'val_smpls':val_size,'tst_smpls':test_size}

        



"""  Create  train / test / validation folders  - Kadli style              """
create_folders(data_path)

# """        read data including a text file and the wave names              """
file_names = [f for f in listdir(path_to_waves) if isfile(join(path_to_waves, f))]
log.info('filenames extract')

# get the numebr of wave_files 
num_samples = len(file_names)
log.info('number of samples is {}'.format(num_samples))


#get splits 
splits = get_split_counts(num_samples)
log.info('samples should be divided into,\n\
                                          {} samples for train,\n,\
                                          {} samples for validation,\n,\
                                          {}samples for test,\n'.format
                                          (
                                          splits['trn_smpls'],
                                          splits['val_smpls'],
                                          splits['tst_smpls']
                                          )
                                        )

# read the transcripts

with open(transcript_path,'r') as file:
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

min_train = 0
max_train = splits['trn_smpls']
min_valid = splits['trn_smpls'] + 1
max_valid = min_valid + splits['val_smpls']
min_test  = max_valid + 1 
max_test  = max_valid + splits['tst_smpls'] - 1
folder = ['train','valid','test']
file = ['text','wav.scp','utt2spk','spk2utt']



match = 0

with open(os.path.join(data_path,"train","text"),'w')     as train_text,\
     open(os.path.join(data_path,"train","wav.scp"),'w')  as train_wav,\
     open(os.path.join(data_path,"train","utt2spk"),'w')  as train_utt2spk,\
     open(os.path.join(data_path,"train","spk2utt"),'w')  as train_spk2utt,\
     open(os.path.join(data_path,"valid","text"),'w')     as val_text,\
     open(os.path.join(data_path,"valid","wav.scp"),'w')  as val_wav,\
     open(os.path.join(data_path,"valid","utt2spk"),'w')  as val_utt2spk,\
     open(os.path.join(data_path,"valid","spk2utt"),'w')  as val_spk2utt,\
     open(os.path.join(data_path,"test","text"),'w')      as test_text,\
     open(os.path.join(data_path,"test","wav.scp"),'w')   as test_wav,\
     open(os.path.join(data_path,"test","utt2spk"),'w')   as test_utt2spk,\
     open(os.path.join(data_path,"test","spk2utt"),'w')   as test_spk2utt:        
       
     for idx,Sentence in enumerate(transcripts):
        not_assigned = True
        if ((min_train <= idx <= max_train) and not_assigned):
            not_assigned = False
            text = Sentence.split('|')[1]
            wav_name = Sentence.split('|')[0]
            wav_file = wav_name+'.wav'
            if ( wav_file in file_names):
                match += 1
                
                write_to_text   = wav_name + ' ' +text
                write_to_wavscp = wav_name + ' ' +'wavs/'+wav_file+'\n'
                write_to_utt2spk = Sentence.split('|')[0]+ '  ' + speaker+'\n'
                
                if first_time_train:
                    train_spk2utt.writelines(speaker)
                    train_spk2utt.writelines(' ')
                    first_time_train = False 
                write_to_spk2utt = Sentence.split('|')[0]+' '
                
                
                train_text.writelines(write_to_text)
                train_wav.writelines(write_to_wavscp)    
                train_utt2spk.writelines(write_to_utt2spk)
                train_spk2utt.writelines(write_to_spk2utt)
                
                
                # src = os.path.join(path_to_waves,wav_file)
                # dst = os.path.join(final_wav_path,wav_file)
                # shutil.copy(src,dst)
                
                if (idx%100==0):
                    print('preparing training files .... {}% done'.format(100*idx/(num_samples)))
            else:
                    not_found.append(wav_file)           

        if( (min_valid <= idx <= max_valid) and not_assigned):
            not_assigned = False            
            text = Sentence.split('|')[1]
            wav_name = Sentence.split('|')[0]
            wav_file = wav_name+'.wav'
            if ( wav_file in file_names):
                match += 1
                
                write_to_text   = wav_name + ' ' +text
                write_to_wavscp = wav_name + ' ' +'wavs/'+wav_file+'\n'
                write_to_utt2spk = Sentence.split('|')[0]+ '  ' + speaker+'\n'
                
                if first_time_val:
                    val_spk2utt.writelines(speaker)
                    val_spk2utt.writelines(' ')
                    print('dummay  added')
                    first_time_val = False 
                write_to_spk2utt = Sentence.split('|')[0]+' '
                
                
                val_text.writelines(write_to_text)
                val_wav.writelines(write_to_wavscp)    
                val_utt2spk.writelines(write_to_utt2spk)
                val_spk2utt.writelines(write_to_spk2utt)
                
                # src = os.path.join(path_to_waves,wav_file)
                # dst = os.path.join(final_wav_path,wav_file)
                # shutil.copy(src,dst)
                
                if (idx%100==0):
                    print('preparing validation files .... {}% done'.format(100*idx/(num_samples)))
            else:
                not_found.append(wav_file)
                
        if ((min_test <= idx <= max_test) and not_assigned):
            not_assigned = False        
            text = Sentence.split('|')[1]
            wav_name = Sentence.split('|')[0]
            wav_file = wav_name+'.wav'
            if ( wav_file in file_names):
                match += 1
                
                write_to_text   = wav_name + ' ' +text
                write_to_wavscp = wav_name + ' ' +'wavs/'+wav_file+'\n'
                write_to_utt2spk = Sentence.split('|')[0]+ ' ' + speaker+'\n'
                
                if first_time_test:
                    test_spk2utt.writelines(speaker)
                    test_spk2utt.writelines(' ')
                    first_time_test = False 
                write_to_spk2utt = Sentence.split('|')[0]+' '
                
                test_text.writelines(write_to_text)
                test_wav.writelines(write_to_wavscp)    
                test_utt2spk.writelines(write_to_utt2spk)
                test_spk2utt.writelines(write_to_spk2utt)
            
                # src = os.path.join(path_to_waves,wav_file)
                # dst = os.path.join(final_wav_path,wav_file)
                # shutil.copy(src,dst)
                
                if (idx%100==0):
                    print('preparing test files .... {}% done'.format(100*idx/(num_samples)))    
            else:
                not_found.append(wav_file)
                
                
print(not_found)                
log.info('printing the name of the files that where not found in the procesed wave files')                
for  item in not_found:
    log.info(item)
    
    
                
                
                
                
                
                
                
                
log.removeHandler(fh)
del log,fh




