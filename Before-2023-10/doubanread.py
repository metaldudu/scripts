##coding=utf-8
# 抓取豆瓣已读书数量
# 修改用户名和年度，生成markdown文件
# 20190216

import urllib.request
import json
import time

USERNAME = 'metaldudu'
YEAR = '2019'
# 用户名和年份

#html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=2017-03-01T00:00:00+08:00&to=2017-04-01T00:00:00+08:00'
# 标准地址

print ('start job! ',end='')
fname = 'douban' + YEAR + '.md'
f1 = open(fname, 'w')
f1.write('# '+ USERNAME + YEAR +'\n\n')
# 创建文件

m = 1
while m <= 12:
	try:
		if m < 10:
			thismonth = YEAR + '-' + str('%.2d' % m) + '-01'
			nextmonth = YEAR + '-' + str('%.2d' % (m+1)) + '-01'
		elif m < 12:
			thismonth = YEAR + '-' + str(m) + '-01'
			nextmonth = YEAR + '-' + str(m+1) + '-01'
		else:
			thismonth = YEAR + '-12-01'
			nextmonth = str(int(YEAR) +1) + '-01-01'
		# 构造月份

		html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + thismonth + 'T00:00:00+08:00&to=' + nextmonth + 'T00:00:00+08:00'
		# 构造api地址
		
		hjson = json.loads(urllib.request.urlopen(html.format()).read().decode())

		
		month_num = '## ' + thismonth[:-3] + ' : ' + str(hjson['total'])
		f1.write(month_num + '\n\n')
		# 写入月份

		for i in hjson['collections']:

			if ('comment' in i):
				book_comment = i['comment']
			else:
				book_comment = ' '
			# 判断是否加入短评

			book_log = '- 《' + i['book']['title'] + '》: '  + book_comment + ' `' + i['updated'] + '`'
			f1.write(book_log + '\n')			
			# 输出书名、短评、时间
						
			print ('.',end='')
			# 命令行效果

			time.sleep(2)
			# 休息，豆瓣API限制每分钟40次
		
	except Exception as e:
		print (e)

	f1.write('\n')
	m = m+1

# 输出年度数量
html2 = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + YEAR + '-01-01T00:00:00+08:00&to=' + str(int(YEAR)+1) + '-01-01T00:00:00+08:00'
hjson = json.loads(urllib.request.urlopen(html2.format()).read().decode())

year_totalread =  ('---\n### ' +  YEAR + '\ntotal readed:' + str(hjson['total']))
f1.write(year_totalread)
# 写入年度数量

f1.close()
print ('\nfinish!')


# TODO:@comment 为空的需要排除