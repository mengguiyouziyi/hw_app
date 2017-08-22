# coding:utf-8

import os
import sys
import pymysql
import time
from os.path import dirname

from my_redis import QueueRedis

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key(key):
	"""
		本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""
	# red = QueueRedis()
	# chis = [chr(ch) for ch in range(0x4e00, 0x9fa6)]
	# nums = range(10)
	# abc = [chr(i) for i in range(97,123)]
	# chis.extend(nums)
	# chis.extend(abc)
	#
	# for i in chis:
	# 	red.send_to_queue(key, i)
	# 	print(i)
	#
	# print('done')
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select soft_id, soft_name from hw_app ORDER BY soft_id"""
			cursor.execute(sql)
			results = cursor.fetchall()
			values = [i['soft_name'].strip() for i in results if i['soft_name']]
	finally:
		mysql.close()

	red = QueueRedis()

	if values:
		for value in values:
			red.send_to_queue(key, value)
			print(value)
	print('done')


if __name__ == '__main__':
	send_key(key='hw_zh')
















# """
# 本机 localhost；服务器 a027.hb2.innotree.org
# """
# red = QueueRedis()
# def send_id():
# 	for id in range(1, 14300000):
# 	# for id in range(1, 10000):
# 		red.send_to_queue('ids', id)
# 		print(id)


# if __name__ == '__main__':
# 	send_id()