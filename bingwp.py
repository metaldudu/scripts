#coding=utf-8
# 抓取下载当天的bing壁纸
# 最后部分设置xfce壁纸

import urllib.request
import re
from bs4 import BeautifulSoup
import time
import os
import sys


rssurl = 'http://www.bing.com/HPImageArchive.aspx?format=rss&idx=0&n=1&mkt=en-US'
# 官方rss源


response = urllib.request.urlopen(rssurl)
soup = BeautifulSoup(response,"lxml")
wpurl = soup.find("item")

wpurl = str(wpurl)
ps1 = wpurl.index('<link/>') + 7
ps2 = wpurl.index('<pubdate>')

wpurl = wpurl[ps1:ps2]
wpurl = 'http://bing.com' + wpurl
print (wpurl)

day = time.strftime('%Y-%m-%d',time.localtime(time.time()))

cmd = 'wget -O "' + day +'.jpg" ' + wpurl
os.system(cmd)

cmd1 = 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s /home/laodu/doc/python/' + day + '.jpg'
os.system(cmd1)

cmd2 = 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s /home/laodu/doc/python/' + day + '.jpg'
os.system(cmd2)

