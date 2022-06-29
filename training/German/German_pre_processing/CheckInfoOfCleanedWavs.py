# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Ali Nadian)s
"""


import pickle 
import matplotlib.pyplot as plt

with open('d:\saved_dictionary.pkl', 'rb') as f:
    info = pickle.load(f)
    
with open('d:\saved_dictionary.pkl', 'rb') as f1:
    info1 = pickle.load(f1)
    
    
# #we want to see how much we have affected the dataset 
# X = []
# for p in range(100):
#     filtered_info = {k:v for (k,v) in info.items() if (v['trimed_percentage']>p)}
#     X.append(len(list(filtered_info)))
    
# plt.plot(X)
# plt.ylabel('frequency')
# plt.xlabel('precentage of wav removed by trimming')

X = []
for p in range(100):
    filtered_info1 = {k:v for (k,v) in info1.items() if (v['split_percentaeg']>p)}
    X.append(len(list(filtered_info1)))
    
plt.plot(X)
plt.ylabel('frequency')
plt.xlabel('precentage of wav removed by splitting')
