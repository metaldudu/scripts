# coding=utf-8
# 51voa慢速英语
# 2021.10.19

import os
import re
import wget
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}


# 获取单个页面的内容，时间格式转换
def get_mp3(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
    mp3_url = soup.find('a', id='mp3').get('href') #音频地址
    content_str = soup.find('div', class_='content')
    title = soup.find('title').text.replace('VOA Special English - ', '')#名字

    day_str = content_str.find('span', class_='datetime').text
    day_str = day_str.replace(',', '')
    # day_str = datetime.strptime(day_str, '%d %B %Y')
    # day_str = day_str.strftime('%Y-%m-%d')
    
    save_name = day_str + '-' + title #以日期开头的文件名
    print(save_name)

    filepage = open(save_name + '.html', 'w')
    filepage.write(str(content_str))
    filepage.close()#保存文本

    wget.download(str(mp3_url), (save_name + '.mp3')) #保存音频

# 从文件读取并下载
fileurls = open('urls.txt', 'r')
for line in fileurls:
    print(line)
    get_mp3(line)
    time.sleep(14)

fileurls.close()
