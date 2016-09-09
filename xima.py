#coding=utf-8
# 抓取喜马拉雅下载地址

import urllib.request
import re
from bs4 import BeautifulSoup
import time
import os
import sys

# 专辑地址，以 m.ximalaya.com 开头
albumurl = 'http://m.ximalaya.com/7712455/album/3408225'
#albumurl = 'http://m.ximalaya.com/25256063/album/2910554'
# albumurl = 'http://m.ximalaya.com/album/more_tracks?url=%2Falbum%2Fmore_tracks&aid=2910554&page=9'

# 取得专辑id
tmppos = albumurl.index('album/')
xalbumid = albumurl[tmppos + 6:]
#print (xalbumid)

# BS, 抓取专辑首页
response = urllib.request.urlopen(albumurl)
soup = BeautifulSoup(response,"lxml")

# 取出专辑内曲目总数
xcount = soup.find("a", class_='item active trackCount')
xcount = str(xcount.contents)[5:]
xcount = xcount.replace(')\']', '')
# print (xcount)

# 获得分页数量，整除20
xpages = int(xcount)//20 + 1
print ('The album has ' + str(xpages) + ' pages')
print ('--------------------------------------------')

# 生成url地址
strprifx = 'http://m.ximalaya.com/album/more_tracks?url=%2Falbum%2Fmore_tracks&aid='
strprifx = strprifx + xalbumid +'&page='

for i in range (1, xpages+1):
  pageurl = strprifx + str(i)
  # BS 抓取页面
  response = urllib.request.urlopen(pageurl)
  soup = BeautifulSoup(response,"lxml")
  xname = soup.find_all("h4")
  xlink = soup.find_all("a", class_ = 'col col-r j-ibtn btn-player')

  arrxname = []
  for i in xname:
      #print (i.string)
      arrxname.append(i.string)
  j = 0

  for i in xlink:
    #实际下载地址
    #print (i['sound_url'])
    #音频文件名称
    #print (arrxname[j])

    #print (i['sound_url'])
    cmd = 'wget -O ' + arrxname[j] + ' ' + i['sound_url']
    print (cmd)
    os.system(cmd)
    j = j+1
