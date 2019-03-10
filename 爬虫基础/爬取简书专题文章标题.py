#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a crawler'

import requests
from bs4 import BeautifulSoup

base_url='http://www.jianshu.com/collections/16/notes?order_by=added_at&page=%d' #page=0
add_url=1#page数
num=0#文章标题计数

while(True):
	try:
		page=requests.request('get', base_url% add_url).content
		# 将基础网址和页数拼接得到实际网址，使用request的get方法获取响应，再用content方法得到内容
		soup=BeautifulSoup(page)
		# 使用BeautifulSoup分析页面，这里并没有指定解析器，会自动选取可获得的最优解析器
        # BeautifulSoup会报一个warning要你选择解析器，可以忽略

        article_list=[i.get_text() for i in soup.select(".title a")]
        # 这里使用了BeautifulSoup的选择器soup.select，它会返回一个被选取的对象列表，我们使用列表推导，对每个对象获取其中的文字再组成列表。
        # 选择器使用见下文

        for i in article_list:
        	num+=1
        	print(num,' ',i)
        add_url+=1
    except exception as e:
    	print(e)
    	break

