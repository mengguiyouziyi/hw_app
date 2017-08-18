# -*- coding: utf-8 -*-
import scrapy
import re
import math
from datetime import datetime
from app.settings import SQL_DATETIME_FORMAT
from app.items import AppItem
from app.utils.get import get_key


class AppsSpider(scrapy.Spider):
	name = 'apps'
	allowed_domains = ['appstore.huawei.com']
	start_url = 'http://appstore.huawei.com/search/{}/'
	# start_url = 'http://appstore.huawei.com/plugin/appstore/search?searchText={}'
	chis = [chr(ch) for ch in range(0x4e00, 0x9fa6)]

	def start_requests(self):
		urls = (self.start_url.format(c) for c in self.chis)
		for url in urls:
			yield scrapy.Request(url)
		# while True:
		# 	zh_word = get_key('zh_word')
		# 	if not zh_word:
		# 		continue
		# 	url = self.start_url.format(zh_word)
		# 	yield scrapy.Request(url)

	def parse(self, response):
		if '抱歉，找不到您要的页' in response.text:
			return
		print(response.url)
		num_word = response.xpath('//div[@class="dotline-btn list-game-app"]/p/span/text()').extract_first()
		num = re.search(r'\d+', num_word).group()
		if not int(num):
			return
		page_num1 = math.ceil(int(num) / 24)

		# cur_page_list = re.findall(r'/(\d+)$', response.url)
		# cur_page = int(cur_page_list[0]) if cur_page_list else 1

		item_url_list = response.xpath('//*[@class="game-info-ico"]/a/@href').extract()
		for item_url in item_url_list:
			yield scrapy.Request(item_url, callback=self.parse_item)

		if page_num1 > 1:
			urls = (self.start_url.format(c) for c in range(2, page_num1 + 1))
			for url in urls:
				yield scrapy.Request(url, callback=self.parse)

		# if cur_page < page_num:
		# 	if cur_page == 1:
		# 		yield scrapy.Request(response.url + str(cur_page + 1), callback=self.parse)
		# 	else:
		# 		# response.url + str(cur_page)
		# 		yield scrapy.Request(re.sub(r'/(\d+)$', str(cur_page + 1), response.url), callback=self.parse)

	def parse_item(self, response):
		if '抱歉，找不到您要的页' in response.text:
			return
		item = AppItem()
		x = re.search(r'/C(\d+)$', response.url)
		soft_id = int(x.group(1)) if x else -1
		logo_url = response.xpath('//img[@class="app-ico"]/@src').extract_first()
		soft_name = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first()
		dlurl = response.xpath('//a[@class="mkapp-btn mab-install"]/@dlurl').extract_first()
		pname = re.search(r'/([^/]+?)\.apk', dlurl).group(1) if dlurl else ''
		down_num = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[@class="grey sub"]/text()').extract_first()
		soft_score_un = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[starts-with(@class, "score")]/@class').extract_first()
		soft_score = soft_score_un.replace('score_', '') if soft_score_un else ''

		li = response.xpath('//li[@class="ul-li-detail"]/span/text()').extract()
		soft_size = li[0] if len(li) == 4 else ''
		create_date = li[1] if len(li) == 4 else ''
		l = response.xpath('//li[@class="ul-li-detail"]')
		auth = l[2].xpath('./span/@title').extract_first() if len(li) == 4 else ''
		version = li[3] if len(li) == 4 else ''

		pic_url = response.xpath('.//*[@id="contentImages"]/ul/li/a/img/@src').extract()
		des = response.xpath(".//*[@id='app_strdesc']/text()").extract_first()
		comm_word = response.xpath(".//*[@id='commentForm']/h4/span/text()").extract_first()
		s = re.search(r'\d+', comm_word) if comm_word else ''
		comm_num = s.group() if s else ''

		item['soft_id'] = soft_id
		item['logo_url'] = logo_url
		item['soft_name'] = soft_name
		item['pname'] = pname
		item['down_num'] = down_num
		item['soft_score'] = soft_score
		item['soft_size'] = soft_size
		item['create_date'] = create_date
		item['auth'] = auth
		item['version'] = version
		item['pic_url'] = str(pic_url) if pic_url else ''
		item['des'] = des
		item['comm_num'] = comm_num
		item['crawl_time'] = datetime.now().strftime(SQL_DATETIME_FORMAT)
		yield item
