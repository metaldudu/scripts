#!/usr/local/bin/python
#coding=utf-8
# 抓取温度和空气质量
# ver 20210127

import urllib.request
from bs4 import BeautifulSoup

linkurl = 'https://www.weaoo.com/shijiazhuang-181427.html'
response = urllib.request.urlopen(linkurl)
soup = BeautifulSoup(response,"lxml")  


def PmOutput():
    print('----------------------------------------------------------------------'+ '\033[93m') # 加了一个颜色输出
    pm = soup.find("p", class_="mt1 mb2")
    print('|  '  +pm.span.string) # 空气指数
    
    temp = soup.find("span", class_="temp ml2")
    print('|  ' + '温度：' + temp.get_text()) # 当前温度

    forw = pm.previous_sibling.previous_sibling # 这里要用两次
    forw = forw.get_text().replace('石家庄天气', '') # 天气预报
    print('|  ' + forw)
    
    print('\033[0m' + '----------------------------------------------------------------------') # 颜色输出结束


PmOutput()


