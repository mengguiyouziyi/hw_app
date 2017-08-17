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
	red = QueueRedis()
	chis = [chr(ch) for ch in range(0x4e00, 0x9fa6)]
	nums = range(10)
	abc = [chr(i) for i in range(97,123)]
	chis.extend(nums)
	chis.extend(abc)

	for i in chis:
		red.send_to_queue(key, i)

	print('done')


if __name__ == '__main__':
	send_key(key='zh_word')
















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