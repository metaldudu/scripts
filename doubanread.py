##coding=utf-8
# 抓取豆瓣已读书数量

import urllib.request
import json

USERNAME = 'metaldudu'
YEAR = '2017'
# 用户名和年份

#html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=2017-03-01T00:00:00+08:00&to=2017-04-01T00:00:00+08:00'
# 标准地址

print ('-------')
m = 1
while m <= 12:
	try:
		if m < 10:
			thismonth = YEAR + '-' + str('%.2d' % m) + '-01'
			nextmonth = YEAR + '-' + str('%.2d' % (m+1)) + '-01'
			# 构造月份
		else:
			thismonth = YEAR + '-' + str(m) + '-01'
			nextmonth = YEAR + '-' + str(m+1) + '-01'

		html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + thismonth + 'T00:00:00+08:00&to=' + nextmonth + 'T00:00:00+08:00'
		# 构造api地址
		#print (html)

		hjson = json.loads(urllib.request.urlopen(html.format()).read())
		print (thismonth[:-3] + ':' + str(hjson['total']))
	except Exception as e:
		print (e)

	m = m+1

# 输出年度数量
html2 = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + YEAR + '-01-01T00:00:00+08:00&to=' + str(int(YEAR)+1) + '-01-01T00:00:00+08:00'
hjson = json.loads(urllib.request.urlopen(html2.format()).read())
print ('-------')
print ('total :' + str(hjson['total']))


