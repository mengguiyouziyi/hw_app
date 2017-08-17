# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):

	soft_id = scrapy.Field()
	logo_url = scrapy.Field()
	soft_name = scrapy.Field()
	pname = scrapy.Field()
	down_num = scrapy.Field()
	soft_score = scrapy.Field()
	soft_size = scrapy.Field()
	create_date = scrapy.Field()
	auth = scrapy.Field()
	version = scrapy.Field()
	pic_url = scrapy.Field()
	des = scrapy.Field()
	comm_num = scrapy.Field()
	crawl_time = scrapy.Field()
