# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:03:09 2018

@author: Administrator
"""

import urllib
import requests
import os
import re


cookie_str='cna=nS82E9hlQkoCARsT4dFoz8K5; x=__ll%3D-1%26_ato%3D0; _m_h5_tk=e4bd8a8aa9ae4387cdeaf1cf8b6dbbd3_1521543821544; _m_h5_tk_enc=fbb21ca1f3ddfb8cdde9e3e1d7e10549; hng=CN%7Czh-CN%7CCNY%7C156; t=7fe913f3f86c540b8371d15e803f0445; tracknick=%5Cu9B4F%5Cu4E39%5Cu5A77124; lgc=%5Cu9B4F%5Cu4E39%5Cu5A77124; _tb_token_=55587bfedf363; cookie2=283bca02060afbdfc8493c08ab5b3aed; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; JSESSIONID=3C96CD768E30A3CDEDD22E5ECC6EAEFE; isg=BCoqlvCGBF1QJogmpeqGXYP1bpAMM6x2Xe2RT7TlpH2T58ehnCgNB0R5cxN7DCaN'
cookie=dict(map(lambda x:map(lambda x: x.strip(),x.split('=')),cookie_str.split(';')))
cookie['uc3:nk2']='rSM5RFTfNlaC&id2=UonZBGCbwcj%2BSQ%3D%3D&vt3=F8dBz4KDAPNxTlbo3xc%3D&lg2=UtASsssmOIJ0bQ%3D%3D'

def build_urls(word):
    word = urllib.parse.quote(word)
    url = r"https://s.taobao.com/search?q={word}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180327&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s={image_number}"
    urls = (url.format(word=word, image_number=x) for x in range(0,220,44))
#     print urls
    return urls

def get_item_ids(html):
    re_url = re.compile(r'"nid":"(.*?)"')
    item_ids =re_url.findall(html)
    return item_ids

def get_img_urls(item_id):
    url=r'http://rate.tmall.com//list_detail_rate.htm?itemId='+item_id+'&spuId=0&sellerId=3044123044&order=3&&currentPage={page}&append=0'
    response=requests.post(url,cookies=cookie)
    try:
        req_con = response.content.decode('gbk')
        pattern = re.compile('"pics":\[(.+?)\],')
        items = re.findall(pattern,req_con)     
        img_urls=[]
        for item in items:
            for temp in item .split(','):
                img_urls.append("http:"+temp.strip('"')+'_400x400.jpg')
    except Exception as e:
        print(e)
        img_urls=[]
    return img_urls

def down_img(imgUrl, dirpath):
    filename = os.path.join(dirpath, os.path.basename(imgUrl).replace('_!!0-rate.jpg_400x400.jpg','.jpg'))
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


if __name__ == '__main__':
    print("欢迎使用淘宝买家秀下载脚本！")
    print("=" * 50)
    word = input("请输入你要下载的图片关键词：\n")

    dirpath ="D:\\Smoking_Calling_LM_Eye_Dataset\\taobao\\taobao_yj"#储存地址

    urls = build_urls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)
        html = requests.get(url,verify=False,timeout=10).content.decode('utf-8')
        requests.packages.urllib3.disable_warnings()
        item_ids = get_item_ids(html)
        for item_id in item_ids:
            if len(item_id) == 0:  # 没有宝贝
                continue
            img_urls=get_img_urls(item_id)
            if img_urls!=[]:
                for img_url in img_urls:
                    down_img(img_url, dirpath)
                    index += 1                
                    print("已下载 %s 张" % index)
                
                
                
                
                
                
                
