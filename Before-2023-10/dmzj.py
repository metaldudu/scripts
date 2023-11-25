# -*- coding:utf-8 -*-
# 批量下载dmzj的漫画，因为异步加载无法直接下载，利用chrome控制台，copy as curl
# 找到初始的漫画地址就可以
# 需要 BeautifulSoup 和 curl
# 2020.10.09


import re
import os
import sys
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}



# 获取漫画名称和id
def get_comic_id(comic_url):
    res = requests.get(comic_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser') 

    global comic_name # 定义漫画书名字为全局变量
    comic_name = soup.h1.string
    print('【漫画名称】' + comic_name)  # 获得名称

    comic_id = soup.find('span', id='comic_id').get_text() #抓取漫画id
    print('【漫画ID】' + str(comic_id))
    return comic_id
    

# 抓取漫画包含书的id
def get_book_list(comic_url):
    res = requests.get(comic_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    book_list = [] #定义漫画书列表

    soup_booklist = soup.find('div', class_='cartoon_online_border')
    book_li = soup_booklist.find_all('li')#找到列表链接部分

    short_name = comic_url.replace('http://manhua.dmzj1.com/', '')   # 漫画名称url字符串
    short_name = short_name.replace('/', '')
    print('【漫画简称】' + short_name)

    for i in book_li:
        try:
            # print(i)
            book_id = i.a.get('href').replace(short_name, '').replace('.shtml', '')#取出漫画书的id号
            book_id = book_id.replace('/', '')
            book_list.append(book_id)#加入列表
            # print(book_id)          
        except AttributeError:
            pass
    
    print('【漫画数量】 ' + str(len(book_list)) )
    return book_list

# 构造移动版网址并获取图片路径

def get_image(book_url):
    res = requests.get(book_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    strs = str(soup.find_all('script'))
    # print(strs)
    pattern = re.compile(r'(https:\\u002F\\u002Fimages.*?jpg)')
    img_urls = re.findall(pattern, strs)
    # print(img_urls)
    return(img_urls)

# 修正图片地址错误
def fix_img(img_url):
    fixed_url = img_url.replace('\\u002F', '\\')
    fixed_url = fixed_url.replace(' ', '%20')
    fixed_url = fixed_url.replace('\\', '/')
    return(fixed_url)


def down_comic(comic_url):
    newid = get_comic_id(comic_url) #漫画id
    newlist = get_book_list(comic_url) # 书列表
    folder_num = 1 # 下载子目录序号
    
    filepath = os.getcwd()  + '/' + comic_name # 当前下载目录
    os.mkdir(filepath) # 创建漫画目录

    for i in newlist:
        newbookurl = 'http://m.dmzj1.com/view/' + newid + '/' + str(i) + '.html' # 每本漫画的首页
        print(newbookurl)
        # curl 的参数
        imghead = ' -H \'Referer: ' + newbookurl + '\' -H \'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.106 Safari/537.36\' -H \"DNT: 1\"  --compressed  -#' 
        
        # 创建和切换子目录
        try:
            subpath = filepath + '/' + str(folder_num) # 建立子目录
            os.mkdir(subpath) #创建书目录
            os.chdir(subpath) # 切换目录
            print(os.getcwd())
        except Exception as e:
            print(e)

        imglist = get_image(newbookurl) # 取得图片地址列表
        # print(imglist)
        for j in imglist:
            j = fix_img(j)
            # print(j)
            cmd = 'curl -O ' + j +  imghead
            os.system(cmd) # 执行下载命令
            # print(cmd)
        print('------------')

        folder_num = folder_num + 1 #子目录序号加一


# 改这里就可以下载了
down_comic('http://manhua.dmzj1.com/szg/')
