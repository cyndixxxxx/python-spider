import scrapy

class DoubanItem(scrapy.Item):
	title=scrapy.Field()
	link=scrapy.Field()

import scrapy
from scrapy.http import Request
for ...items import DoubanItem 
class DoubanSpider(scrapy.spider):
	name="douban"
	allowed_domains=["douban.com"]
	start_urls=[
		'http://'
	]

	def parse(self,response):
		item=DoubanItem()
		for sel in response.css():
			item['title']=sel.css().extract_first()
			yield item
		%获取下一页
		nextpage=response.css()
		url=base_url+nextpage.css().extract_first()
		yield Request(url,callback=self.parse)

%存储到json文件中去
import json
import codecs
class DoubanPipeline(object):
	def __init__(self):
		self.file=codecs.open('douban_movie.json','wb',encoding='utf-8')
	def process_item(self,item,spider):
		line=json.dumps(dict(item))+'\n'
		self.file.write(line.decode("unicode_escape"))
		return item
