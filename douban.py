##coding=utf-8
# 20181203 豆瓣阅读数量柱状图显示

import urllib.request
import json

USERNAME = 'metaldudu'
YEAR = '2018'

readlist = []
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

		# 构造api地址
		html = 'https://api.douban.com/v2/book/user/' + USERNAME + '/collections?status=read&from=' + thismonth + 'T00:00:00+08:00&to=' + nextmonth + 'T00:00:00+08:00'

		hjson = json.loads(urllib.request.urlopen(html.format()).read())
		readlist.append(hjson['total'])
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
print(USERNAME +' in ' + YEAR + ' total: ' +str(sum(readlist)) )