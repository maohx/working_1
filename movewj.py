# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:13:42 2018

@author: Administrator
"""

import os
import shutil
path='H:\\c4_unsifted_profile'
move_path='H:\\c4_landmark'
save_path= 'H:\\c4_calling_landmark'
#if not os.path.exists(save_path):
#    os.mkdir(save_path)
for temp in os.listdir(path):
     if temp.replace('_right.jpg','.jpg') in os.listdir(move_path):
            shutil.move(os.path.join(move_path,temp.replace('_right.jpg','.jpg')),os.path.join(save_path,temp.replace('_right.jpg','.jpg')))
            shutil.move(os.path.join(move_path,temp.replace('_right.jpg','_83pts.txt')),os.path.join(save_path,temp.replace('_right.jpg','_83pts.txt')))

'''import os
import shutil
path='G:\\Calling_Dataset\\train\\calling\\right\\rightcrop_30_training'
#move_path='G:\\Calling_Dataset\\train\\calling\\left\\left_finished'
save_path='G:\\Calling_Dataset\\train\\calling\\calling'
for temp in os.listdir(path):
            shutil.move(os.path.join(path,temp),os.path.join(save_path,temp))'''
        
