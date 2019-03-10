from scrapy.item import Item,Field

class DoubanItem(Item):
	name=Field()
	description=Field()
	url=Field()

 #!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
一个简单的Python 爬虫, 用于抓取豆瓣电影Top前250的电影的名称描述等
"""

form scrapy.contrib.spiders import CrawlSpider,Rule
form scrapy.selector import Selector
from douban.items import DoubanItem
from scrapy.contrib.linkextractors.sgml import SgmllLinkExtractor

class DoubanSpider(CrawlSpider):

	name="douban"
	allowed_domains={""}
	start_urls=[""]
	rules=(  #将所有符合正则表达式的url加入到抓取列表中
        Rule(SgmlLinkExtractor(allow = (r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=',))),
        #将所有符合正则表达式的url请求后下载网页代码, 形成response后调用自定义回调函数
        #如果你想让Rule跟随外链，你应该从callback方法return/yield，或设定Rule()的follow参数为True。当你的列表页既有Items又有其它有用的导航链接时非常有用。
        Rule(SgmlLinkExtractor(allow = (r'http://movie\.douban\.com/subject/\d+', )), callback = 'parse_page', follow = True),)

	def parse_page(self. response):
		sel=Selector(response)
		item=DoubanItem()
		item['name']=sel.xpath()
		item['description']=sel.xpath()
		item['url']=response.url
		return item
