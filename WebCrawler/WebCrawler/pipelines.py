# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WebcrawlerPipeline(object):
	def close_spider(self, spider):
		print("\n\n\n\n\n**********************FIM*************************\n\n\n\n")
		print(spider.propriedades)
		with open('output/'+spider.name+"/keys.json","w") as fileKeys:
			json.dump({'keys':spider.propriedades},fileKeys)

