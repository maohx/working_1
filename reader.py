# -*- coding: utf-8 -*-
"""
Created on Fri May 04 11:04:15 2018

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt

path='C:\\Users\\Administrator\\Desktop\\test\\test_2\\5748213-6_0_0_m0_l0_r0_e3.jpg'
txt_path=path.replace('.jpg','_83pts.txt')

def landmark_reader(file_path):
    landmark=np.fromfile(file_path,sep=' ')[:-5]
    return landmark.reshape((-1,2))
    
#lm83=landmark_reader(txt_path)
##img=plt.imread(path)
##plt.imshow(img)
#
#plt.scatter(lm83[:,0],lm83[:,1])
#for i in range(83):
#    plt.text(lm83[i,0],lm83[i,1],str(i),fontsize=8)
#plt.show 

def bbox_from_points(points):
#    mid_point=np.mean(points,axis=0)
    max_=np.max(points,axis=0)
    min_=np.min(points,axis=0)
    print points
#    r=np.max(max_-min_)/2
    print min_
#    print [min_[0],min_[1],max_[0],max_[1]]
    
point = landmark_reader(txt_path)
print point
bbox_from_points(point)