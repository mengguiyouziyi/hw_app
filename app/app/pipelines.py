# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		sql = """replace into hw_app(soft_id, logo_url, soft_name, pname, down_num, soft_score, soft_size, create_date, auth, version, pic_url, des, comm_num, crawl_time) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
		args = (
			item['soft_id'], item['logo_url'], item['soft_name'], item['pname'], item['down_num'], item['soft_score'],
			item['soft_size'],
			item['create_date'], item['auth'], item['version'], item['pic_url'], item['des'], item['comm_num'],
			item['crawl_time']
		)
		self.cursor.execute(sql, args=args)
		self.conn.commit()
		print(str(item['soft_id']))

	# print(str(item['app_id']))
