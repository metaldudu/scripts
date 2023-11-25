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


url_list = 'https://www.51voa.com/Words_And_Their_Stories_16.html' #列表网址

response = urllib.request.urlopen(url_list)
soup = BeautifulSoup(response, 'lxml')
sub_urls = soup.find_all('a', href=re.compile("VOA_Special_English"))

fileurls = open('urls.txt', 'a')

for i in sub_urls:
    if not '_1.html' in str(i):
        page_url = 'https://www.51voa.com' + i.get('href') + '\n'     
        fileurls.write(page_url)
        
fileurls.close()





