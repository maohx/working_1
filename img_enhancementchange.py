# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 14:26:42 2018

@author: Administrator
"""

import numpy as np
import cv2
import math
from skimage.transform import rotate
import os
from multiprocessing.dummy import Pool as ThreadPool 
import shutil

def facial_lum(image):    
    exposure=1.2
    r2=np.random.rand()
    r3=np.random.rand()
    exposure = r2*(exposure - 1) + 1
    if(r3 > 0.5):
        exposure=1.0/exposure;
    img_hsv=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
    img_hsv[:,:,2]=cv2.multiply(img_hsv[:,:,2],exposure)
    img_rgb=cv2.cvtColor(img_hsv,cv2.COLOR_HSV2RGB)
   # H,S,V=cv2.split(img_hsv)
    return cv2.cvtColor(img_rgb,cv2.COLOR_RGB2GRAY)

def coordinate_rotation(coordinates,center,angle):
    homogeneous_coordinates=np.concatenate([coordinates,np.ones((coordinates.shape[0],1))],axis=1)
    transtion_matrix1=np.matrix([[1,0,0],
                                [0,1,0],
                                [-center[0],-center[1],1]])
    rotation_matrix=np.matrix([[np.cos(angle),np.sin(angle),0],
                                [-np.sin(angle),np.cos(angle),0],
                                [0,0,1]])
    transtion_matrix2=np.matrix([[1,0,0],
                                [0,1,0],
                                [+center[0],+center[1],1]])
    new_coordinates=homogeneous_coordinates*transtion_matrix1*rotation_matrix*transtion_matrix2
    return new_coordinates[:,0:2]

def rotation_correction83(im,landmarks83):
    left_eye=np.mean(landmarks83[[26,19],:],axis=0)
    right_eye=np.mean(landmarks83[[72,65],:],axis=0)
    nose=landmarks83[64,:]
    left_mouth=landmarks83[37,:]
    right_mouth=landmarks83[46,:]
    eye_center=np.floor(1.0/2*(left_eye+right_eye));
    mouth_center=np.floor(1.0/2*(left_mouth+right_mouth));
    distance=lambda x,y:np.sqrt(np.sum(np.power(x-y,2)))
    eye_distance=distance(left_eye,right_eye)
    eye_mouth_distance=distance(eye_center,mouth_center)
    eye_nose_distance=distance(eye_center,nose);
    mouth_distance=distance(left_mouth,right_mouth);
    eye_alignment_vector=right_eye-left_eye
    angle_between_alignment_horizon=np.arctan(-1.0*eye_alignment_vector[1]/eye_alignment_vector[0])
    im=rotate(im,-angle_between_alignment_horizon/math.pi*180,center=eye_center)
    landmarks83_new=coordinate_rotation(landmarks83,eye_center,angle_between_alignment_horizon)
    return im,np.array(landmarks83_new)

def random_rotation(im,landmark83):
    left_eye=np.mean(landmark83[[26,19],:],axis=0)
    right_eye=np.mean(landmark83[[72,65],:],axis=0)
    eye_center=np.floor(1.0/2*(left_eye+right_eye));
    angle=np.random.randint(-20,21)
    im=rotate(im,angle,center=eye_center)
    degree=-angle*math.pi/180
    landmark=coordinate_rotation(landmark83,eye_center,degree)
    return im,np.array(landmark)

def landmark_reader(file_path):
    landmark=np.fromfile(file_path,sep=' ')[:-5]
    return landmark.reshape((-1,2))

def bbox_from_points(points):
#    mid_point=np.mean(points,axis=0)
    max_=np.max(points,axis=0)
    min_=np.min(points,axis=0)
#    r=np.max(max_-min_)/2
    return [min_[0],min_[1],max_[0],max_[1]]

def bbox_enlarging(bbox,img_shape,alpha):

    bbox_=[0,0,0,0]
    width=bbox[2]-bbox[0]
    height=bbox[3]-bbox[1]   
    bbox_[0]=max(0,bbox[0]-alpha*width*10)
    bbox_[1]=max(0,bbox[1]-alpha*height)
    bbox_[2]=min(img_shape[1],bbox[2]-alpha*width*0.6)
    bbox_[3]=min(img_shape[0],bbox[3]+alpha*height)
    return bbox_

def random_eye_left_cropping(im,landmarks83):
    
#    lm67=landmarks67[:-5].reshape(-1,2)
    left_index=[9,8,7,6,5,4,3,2,1]
  #  right_index=[28,29,30,31,32,33,34,35]
    leftpoints=landmarks83[left_index,:]
  #  rightpoitns=lm67[right_index,:]
    left_eye_bbox=bbox_from_points(leftpoints)
  #  right_eye_bbox=bbox_from_points(rightpoitns)
    if np.random.rand()>0.5:
        alpha=np.random.rand()*0.1+0.1
    else:
        alpha=0.1

    left_eye_bbox=bbox_enlarging(left_eye_bbox,im.shape,alpha)
#    left_eye=im[left_eye_bbox[1]:left_eye_bbox[3],left_eye_bbox[0]:left_eye_bbox[2]]
    eye_left=cv2.flip(im[int(left_eye_bbox[1]):int(left_eye_bbox[3]),int(left_eye_bbox[0]): int(left_eye_bbox[2])],1)
    
   # right_eye_bbox=bbox_enlarging(right_eye_bbox,im.shape,alpha)
  #  right_eye=im[int(right_eye_bbox[1]):int(right_eye_bbox[3]),int(right_eye_bbox[0]): int(right_eye_bbox[2])]
    
    return  eye_left

'''def random_right_eye_cropping(im,landmarks83):
    
#    lm67=landmarks67[:-5].reshape(-1,2)
  #  left_index=[37,38,39,40,41,42,43,44]
    right_index=[18,17,16,15,14,13,12,11,10]
  #  leftpoints=lm67[left_index,:]
    rightpoitns=landmarks83[right_index,:]
  #  left_eye_bbox=bbox_from_points(leftpoints)
    right_eye_bbox=bbox_from_points(rightpoitns)
    if np.random.rand()>0.5:
        alpha=np.random.rand()*0.8+0.8
    else:
        alpha=0.8
    alpha=0
   # left_eye_bbox=bbox_enlarging(left_eye_bbox,im.shape,alpha)
#    left_eye=im[left_eye_bbox[1]:left_eye_bbox[3],left_eye_bbox[0]:left_eye_bbox[2]]
  #  eye_left=cv2.flip(im[int(left_eye_bbox[1]):int(left_eye_bbox[3]),int(left_eye_bbox[0]): int(left_eye_bbox[2])],1)
    
    right_eye_bbox=bbox_enlarging(right_eye_bbox,im.shape,alpha)
    right_eye=im[int(right_eye_bbox[1]):int(right_eye_bbox[3]),int(right_eye_bbox[0]): int(right_eye_bbox[2])]
    
    return right_eye'''


def save_crop_img(img_path):
    try:
        img=cv2.imread(img_path)
        lm83_path=img_path.replace('.jpg','_83pts.txt')
        lm83=landmark_reader(lm83_path)
        img_aligned,lm83_aligned=rotation_correction83(img,lm83)
        fname=os.path.basename(img_path)
        for i in range(1):
            try:
                img_rotated,lm83_rotated=random_rotation(img_aligned,lm83_aligned)
                eye_left=(random_eye_left_cropping(img_rotated,lm83_rotated)*255).astype('uint8')  
#                right_eye=(random_right_eye_cropping(img_rotated,lm83_rotated)*255).astype('uint8')
                part_left=facial_lum(eye_left)
#               part_right=facial_lum(right_eye)
#                part_left_resize=cv2.resize(part_left, (48, 48))
                cv2.imwrite(os.path.join(save_path,fname.replace('.jpg','_left_'+str(i)+'.jpg')),part_left)
#                cv2.imwrite(os.path.join(save_path,fname.replace('.jpg','_right_'+str(i)+'.jpg')),part_right)               
            except Exception as e:
                print e
                continue
        print img_path,':finished'
        shutil.move(img_path,os.path.join(finished_path,fname))
        shutil.move(img_path.replace('.jpg','_83pts.txt'),os.path.join(finished_path,fname.replace('.jpg','_83pts.txt')))
    except Exception as e:
        print e

path='G:\\Calling_Dataset\\train\\calling\\left'
save_path='G:\\Calling_Dataset\\train\\calling\\left_save' 
finished_path=path+'_finished'
if not os.path.exists(finished_path):
    os.mkdir(finished_path)

'''path='D:\\Smoking_Calling_LM_Eye_Dataset\\val\\yj_finished'
save_path='D:\\sunglass_detection_dataset\\val\\glasses'
finished_path=path+'_finished
if not os.path.exists(finished_path):
    os.mkdir(finished_path)'''

img_paths=map(lambda x:os.path.join(path,x),filter(lambda x:'.jpg' in x,os.listdir(path)))
#pool = ThreadPool(5)
#pool.map(save_crop_img, img_paths)
#pool.close() 
#pool.join()
map(save_crop_img, img_paths)


