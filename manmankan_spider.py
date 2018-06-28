# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 21:20:51 2018

@author: Administrator
"""

import re
import os
import requests
from multiprocessing.dummy import Pool as ThreadPool
#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码  



def get_Html(url):#获取人名和对应链接
    response = requests.get(url)
    html = response.content
    #<a href="/dy2013/mingxing/201307/2649.shtml" title="安悦溪" target="_blank">安悦溪</a>
    #<a href="(.*)" title="(.*)" target="_blank">
    pattern = re.compile(r'<div class="i_cont">[\s\S]*</div>')
    pattern2 = re.compile(r'<a href="(.*)" title="(.*)" target="_blank">.*</a>')
    url_list=pattern2.findall(pattern.findall(html.decode('gb2312','ignore'))[0])
    print(url_list)
    return url_list



def get_stars_urls(url):#获取明星全部图片链接
    star_urls=[]
    base_url='http://www.manmankan.com'
    stars_infs=get_Html(url)
    for star_infs in stars_infs:
        star_url=star_infs[0]
      #  print(star_url)
        star_image_url=base_url+star_url.replace('/dy2013/mingxing','/dy2013/mingxing/tupian')
        star_urls.append((star_image_url,star_infs[1])) 
   # print(star_urls)
    return  star_urls


def get_images_urls(stars_url):
    imgurl_list=[]
    url=stars_url[0] 
    response = requests.get(url)
    html = response.text
    pattern = re.compile(r'<a class=".*" href=".*" title=".*"><img src=".*" data-original="(.*)" alt=".*"></a>')
    imgurl=pattern.findall(html)
    for imgurl_ in imgurl:
        imgurl_list.append((imgurl_,stars_url[1]))
 #       print(imgurl_list)
    return imgurl_list

def down_images(stars_url):
    dirpath='D:\\mamakan_stars'
    imgUrl_list=get_images_urls(stars_url)
    index=0
    if not imgUrl_list==[]:
        for imgUrl in imgUrl_list:
            imgName=imgUrl[1]
            file_new_path=os.path.join(dirpath,imgName)
            if not os.path.exists(file_new_path):    
                os.mkdir(file_new_path)
            
            
        
            try:
                res = requests.get(imgUrl[0], timeout=15)
                if str(res.status_code)[0] == "4":
                    print(str(res.status_code), ":" , imgUrl)
                    return False
            except Exception as e:
                print("抛出异常：", imgUrl)
                print(e)
                return False
            filename = os.path.join(file_new_path, imgName+"_"+str(index)+".jpg")
            index+=1
            with open(filename, "wb") as f:
                f.write(res.content)
    return True

urls=['http://www.manmankan.com/dy2013/mingxing/A/',
      'http://www.manmankan.com/dy2013/mingxing/B/',
      'http://www.manmankan.com/dy2013/mingxing/C/',
      'http://www.manmankan.com/dy2013/mingxing/D/',
      'http://www.manmankan.com/dy2013/mingxing/E/',
      'http://www.manmankan.com/dy2013/mingxing/F/',
      'http://www.manmankan.com/dy2013/mingxing/G/',
      'http://www.manmankan.com/dy2013/mingxing/H/',
      'http://www.manmankan.com/dy2013/mingxing/I/',
      'http://www.manmankan.com/dy2013/mingxing/J/',
      'http://www.manmankan.com/dy2013/mingxing/K/',
      'http://www.manmankan.com/dy2013/mingxing/L/',
      'http://www.manmankan.com/dy2013/mingxing/M/',
      'http://www.manmankan.com/dy2013/mingxing/N/',
      'http://www.manmankan.com/dy2013/mingxing/O/',
      'http://www.manmankan.com/dy2013/mingxing/P/',
      'http://www.manmankan.com/dy2013/mingxing/Q/',
      'http://www.manmankan.com/dy2013/mingxing/R/',
      'http://www.manmankan.com/dy2013/mingxing/S/',
      'http://www.manmankan.com/dy2013/mingxing/T/',
      'http://www.manmankan.com/dy2013/mingxing/U/',
      'http://www.manmankan.com/dy2013/mingxing/V/',
      'http://www.manmankan.com/dy2013/mingxing/W/',
      'http://www.manmankan.com/dy2013/mingxing/X/',
      'http://www.manmankan.com/dy2013/mingxing/Y/',
      'http://www.manmankan.com/dy2013/mingxing/Z/',
]  
for url in urls:
    stars_urls=get_stars_urls(url)
    for star_url in stars_urls:
        print(down_images(star_url))