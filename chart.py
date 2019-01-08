##coding=utf-8
# 柱状图

#monthcount = range(1,13)

readlist = [12,16,14,8,10,7,14,14,20,10,5,14]
maxread = max(readlist)

print(sum(readlist))

# 横向显示
for i in range(0,12):
  print(str('%.2d' % (i+1)) + ' : ' + readlist[i]*'█' + ' ' + str(readlist[i]))

print('------------------------------------')

# 纵向显示
for i in range(0,maxread+1):
  for j in range(0, 12):
    
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
print(' total read : ' + str(sum(readlist)))