# code=utf-8
# 人民美术出版社 连环画出版社 数字图书馆
# 清晰版本
# http://223.100.155.234:8013/index.php?r=collection/index
# 201890729

import os
import urllib.request
from bs4 import BeautifulSoup
import time

# 麻城奇案
book_url = 'http://223.100.155.234:8013/index.php?r=reader&itemid=897&type=1'

response = urllib.request.urlopen(book_url)
soup = BeautifulSoup(response, 'lxml')
contents = soup.find_all('div', class_='content')

# print(contents)

for i in contents:
    imgurl = 'http://223.100.155.234:8013/' + i.a.get('href') #获取图片地址
    imgname = i.img.get('title') #获取图片名称
    imgname = imgname.replace('第', '')
    imgname = imgname.replace('页麻城奇案', '')
    imgname = imgname.zfill(3) #格式化文件名
    # print(imgurl)
    print(imgname)
    
    urllib.request.urlretrieve(imgurl, imgname) #直接下载文件
    time.sleep(3) #测试不休息会卡死


print('done!')