import requests
import json
import pymysql
import time


class A:
	def __init__(self):

		"""
		本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
		"""
		self.mysql = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.mysql.cursor()
		self.session = requests.session()

		self.url = "http://a.vmall.com/index/indexmoreaction.action"

		self.payloads = ["reqPageNum=%s" % num for num in range(1, 100)]

		self.headers = {
			'host': "a.vmall.com",
			'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
			'accept': "application/json, text/javascript, */*; q=0.01",
			'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			'accept-encoding': "gzip, deflate",
			'content-type': "application/x-www-form-urlencoded",
			'x-requested-with': "XMLHttpRequest",
			'referer': "http://a.vmall.com/",
			'content-length': "12",
			'connection': "keep-alive",
			'cache-control': "no-cache",
			'postman-token': "d5b7be85-594d-1c49-7db8-c428c5224133"
		}

	def get_insert(self, payload):
		response = self.session.request("POST", self.url, data=payload, headers=self.headers)

		j = json.loads(response.text)
		moreFineList = j.get('moreFineList', {})
		status = moreFineList.get('status', 0)
		if status == 200:
			li = moreFineList.get('list', [])
			for l in li:
				keys = list(l.keys())
				sql = "replace into hw_app ({}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
					str(keys).replace("'", '').replace('[', '').replace(']', ''))
				args = tuple(str(x) for x in l.values())
				self.cursor.execute(sql, args)
				self.mysql.commit()

	def main(self):
		for i, payload in enumerate(self.payloads):
			print(i)
			self.get_insert(payload)
			time.sleep(3)

		self.mysql.close()


if __name__ == '__main__':
	a = A()
	a.main()
