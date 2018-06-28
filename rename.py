# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 19:00:20 2018

@author: Administrator
"""

#import os
#path='G:\\Calling_Dataset2\\Calling_Dataset_All_rubbish'
#for temp in os.listdir(path):
#    os.rename(os.path.join(path,temp),os.path.join(path,temp.replace('.jpg','_lm0.jpg')))
#    os.rename(os.path.join(path,temp.replace('.jpg','_83pts.txt')),os.path.join(path,temp.replace('_83pts.txt','_lm0_83pts.txt')))

import os
import shutil
path='G:\\Calling_Dataset2\\Calling_Dataset_All_sifted'
save_path=path +'_finished'
if not os.path.exists(save_path):
        os.mkdir(save_path)
for temp in os.listdir(path):
    try:
        shutil.move(os.path.join(path,temp),os.path.join(save_path,temp.replace('.jpg','_lm1.jpg')))
        shutil.move(os.path.join(path,temp.replace('.jpg','_83pts.txt')),os.path.join(save_path,temp.replace('.jpg','_lm1_83pts.txt')))
            #shutil.move(os.path.join(move_path,temp.replace('_0_left.jpg','_face.json')),os.path.join(save_path,temp.replace('_0_left.jpg','_face.json')))
    except Exception as e:
        print(e)
#import os
#path='H:\\c4_unsifted_profile'
#save_path='H:\\c4_calling_landmark'
#try: 
#    for temp in os.listdir(save_path):
#        #if temp.replace('.jpg','_right.jpg') in os.listdir(path):
#            #os.rename(os.path.join(save_path,temp),os.path.join(save_path,temp.replace('.jpg','_m0_l0_r1_e3.jpg')))
#            os.rename(os.path.join(save_path,temp),os.path.join(save_path,temp.replace('_83pts.txt','_m0_l0_r1_e3_83pts.txt')))  
#       # if temp.replace('.jpg','_m0_l0_r1_e3_right.jpg') in os.listdir(path):
#except Exception as e:
#     print(e)        