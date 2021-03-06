#!/usr/local/bin/python3
#coding=utf-8

import os
import requests
from lxml import etree

def downloadImages(url):
	#下载页面html内容
	data=requests.get(url).text
	dom=etree.HTML(data)
    
    #解析(定位)元素
	title_path = '//*[@id="photos"]/h1/text()'
    totalpage_path = '//*[@id="picnum"]/span[2]/text()'
    image_path = '//*[@id="big-pic"]/p/a/img'
    #获取元素内容

    title=dom.xpath(title_path)[0]
    total=dom.xpath(totalpage_path)[0]
    image_url=dom.xpath(image_path)[0]

    img_src=image_url.xpath('./@src')[0]
    img_alt=image_url.xpath('./@alt')[0]

    print(tital,total,image_src,img_alt)

    cwd=os.getcwd()
    save_path=os.path(cwd,'images/'+title)
    if not os.path.exists(save_path):
    	os.makedirs(save_path)

    print(u'保存图片的路径：',save_path)

    img_path=os.path.dirname(img_src)
    img_name=os.path.basename(img_src)
    img_format=img_name.split('.')[1]
    print(img_path,img_name)

    for i in range(1,int(total)+1):
    	new_img_url='%s/%02d.%s' % (img_path,i,img_format)
    	save_img_path='%s/%02d.%s' % (save_path,i,img_format)
    	#下载图片
    	image=requests.get(new_img_url)
    	#命名并保存图片
    	with open(save_img_path,'wb') as f:
    		f.write(image.content)

if __name__ =='__main__':
	url='https://www.aitaotu.com/'

	list=[]
	print(u'准备下载：%d套图'，len(list))

	for type in list:
		page=url+type
		downloadImages(page)
	print(u'下载完成啦！')