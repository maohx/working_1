# -*- coding: utf-8 -*-
"""
Created on Mon Jun 04 09:47:35 2018

@author: Administrator
"""
#import time
#import os
#import random
#start_time = time.time()
#path = 'C:\\Users\\Administrator\\Desktop\\test\\kb'
#imgs = os.listdir(path)
#imgs_1 = random.sample(imgs, 30)  
#print imgs_1
#end_time = time.time()
#print("elapsed: %f" % (end_time - start_time))
#print("complete!")
import random
import os
import shutil
import time
start_time = time.time()
def random_copyfile(srcPath,dstPath,numfiles):
    name_list=list(os.path.join(srcPath,name) for name in os.listdir(srcPath))
    random_name_list=list(random.sample(name_list,numfiles))
    if not os.path.exists(dstPath):
        os.mkdir(dstPath)
    for oldname in random_name_list:
        shutil.copyfile(oldname,oldname.replace(srcPath, dstPath))
srcPath='G:\\Calling_Dataset2\\Calling_Dataset\\train\\no_calling'         
dstPath = 'G:\\Calling_Dataset2\\Calling_Dataset\\train\\no_calling_random'
random_copyfile(srcPath,dstPath,337260)
end_time = time.time()
print("elapsed: %f" % (end_time - start_time))
print("complete!")
