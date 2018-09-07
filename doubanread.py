##coding=utf-8
# 抓取豆瓣已读书数量
# 20180907 增加柱状图显示

import urllib.request
import json

USERNAME = 'metaldudu'
YEAR = '2018'
# 用户名和年份

readlist = []

#html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=2017-03-01T00:00:00+08:00&to=2017-04-01T00:00:00+08:00'
# 标准地址

print ('------------------------------------')
m = 1
while m <= 12:
	try:
		if m < 11:
			thismonth = YEAR + '-' + str('%.2d' % m) + '-01'
			nextmonth = YEAR + '-' + str('%.2d' % (m+1)) + '-01'
			# 构造月份
		elif m == 11:
			thismonth = YEAR + '-11-01'
			nextmonth = YEAR + '-12-01'
		else:
			thismonth = YEAR + '-12-01'
			nextmonth = str(int(YEAR)+1) + '-01-01'

		html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + thismonth + 'T00:00:00+08:00&to=' + nextmonth + 'T00:00:00+08:00'
		# 构造api地址

		hjson = json.loads(urllib.request.urlopen(html.format()).read())
		readlist.append(hjson['total'])
		#print (thismonth[:-3] + ':' + str(hjson['total']))
	except Exception as e:
		print (e)
	m = m+1

# 年度最大值
maxread = max(readlist)

# 纵向显示
for i in range(0,maxread+1):
  for j in range(0, 12):
    
	# 输出间隔空格
    if len(str(readlist[j])) == 2 and readlist[j] == (maxread-i):
      print(' ', end='')
    else:
      print('  ', end='')

    if readlist[j] < (maxread-i):
      print(' ', end='')
    elif readlist[j] == (maxread-i):
      print(readlist[j], end='')
    else:
      print('█', end='') 
  print('')

# 输出总数
for i in range(1,13):
  print(' ' + str('%.2d' % (i)), end='')
print('\n' + '------------------------------------')
print(YEAR + ' total read : ' + str(sum(readlist)))