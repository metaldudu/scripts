#coding=utf-8
#好奇心日报专栏 万物简史
# 20181017

import requests
import urllib.request
import re
import os
from bs4 import BeautifulSoup

# 生成文件函数
def get_mdfile(page_id):

    url = 'http://www.qdaily.com/articles/' + str(page_id) +'.html'
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'lxml')

    # 建立文件
    filename = 'tmp/' + str(page_id) +'.md'
    filepage = open(filename, 'w')

    # 标题,梗概
    title = soup.find("title")
    filepage.write(str(title) + '\n\n')

    title = title.string.replace('_文化_好奇心日报', '')
    title = title.replace('_商业_好奇心日报', '')
    title = title.replace('「万物简史」', '')
    filepage.write('# ' + title + '\n\n')

    excerpt = soup.find("p", class_='excerpt')
    filepage.write(str(excerpt) + '\n\n<hr/>')

    # 正文部分
    detail = soup.find("div", class_='detail')
    detailtxt = detail.find_all("p", style='')
    maintxt = ''

    for i in detailtxt:
        if i.string == '\n':
            pass
        elif i.contents == 'img':
            pass
        else:
            #print(i)
            maintxt = maintxt + str(i)

    maintxt = maintxt[0:maintxt.find('<p nocleanhtml="true">一个物品如何成为')]
    filepage.write(maintxt)

    filepage.close()

#函数：清理html标签
def clean_html(html):
    html = html.replace('\\n', '')#去掉换行符，两个斜线反义
    html = html.replace('data-src', 'src')#修改图片加载部分
    html = html.replace('\xa0', ' ')#替换空格
    html = html.replace(' </figure></div>', '')
    html = html.replace('<title>', '')
    html = html.replace('<p>', '')
    html = html.replace('<p class="">', '')
    html = html.replace('</p>', '\n\n')
    html = html.replace('<h3>', '### ')
    html = html.replace('</h3>', '\n\n')
    html = html.replace('<br>', '')
    html = html.replace('"></figcaption>', ')\n\n`')
    html = html.replace('<figcaption>', '\n\n')
    html = html.replace('</figcaption>', '\n\n')
    html = html.replace('<p><strong>', '**')
    html = html.replace('</strong></p>', '**')
    html = html.replace('<strong>', '')
    html = html.replace('</strong>', '')
    html = html.replace('<p class="excerpt">', '')
    html = html.replace('  <div class="detail">  <p finallycleanhtml="true" nocleanhtml="true">', '')
    html = html.replace('\n ', '\n')
    return html

#函数：抓取网页
def get_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            response.encoding="utf-8"
            response=response.text
            return response
        else:
            return None
    except RequestException:
        return None

# 通过json逐一抓取页面id，首页包含第一个值： 1524264433 ，最后： 1409394840
def get_list2(keynum):
     
    keyurl = 'http://www.qdaily.com/special_columns/show_more/15/' + str(keynum)
    page = get_page(keyurl)
    pages_id = re.findall(r'"id":\d{4,5},"genre"', page)
    for i in range(len(pages_id)):
        pages_id[i] = str(pages_id[i]).replace(',"genre"', '')
        pages_id[i] = str(pages_id[i]).replace('"id":', '')
        i = i +1
    #print(pages_id)
    
    # 匹配下一个json页面值，注意列表格式转换为str
    nextkey = re.findall(r'"last_key":\d*', page)
    nextkey = str(nextkey[0]).replace('"last_key":', '')

    return (pages_id, nextkey)

# 定义列表存储，第一个数字是html内包含的值
list_keys = ['1524264433']
list_pageid = []

# 通过循环获得所有的值，写入列表，目前10页
for i in range(12):
    out = get_list2(list_keys[i])
    list_pageid = list_pageid + out[0]

    if not out[1] == '':
        list_keys.append(out[1])   
        i = i+1
    else:
        break

#print(list_keys)
#print(list_pageid)

# 生成文件
for id in list_pageid:
    print(id)
    get_mdfile(id)

# 生成metadata信息
def make_metafile():
    m_file = open('tmp/metadata.xml',  'w')
    m_file.write('<dc:title>好奇心日报：万物简史</dc:title>\n' )
    m_file.write('<dc:language>zh-CN</dc:language>\n')
    m_file.write('<dc:creator opf:file-as="好奇心日报" opf:role="aut">好奇心日报</dc:creator>\n')
    m_file.write('<dc:date opf:event="publication">2018-09-17</dc:date>\n')
    m_file.close()

make_metafile()

#调用pandoc制作epub，toc指定在h1，设置title（否则报错），读入metadata.xml
cmd = 'pandoc tmp/*.md --toc-depth=2 --epub-metadata=tmp/metadata.xml --metadata title=《好奇心日报：万物简史》 --output 好奇心日报：万物简史.epub'
os.system(cmd)
#os.system('rm -rf tmp/*.md')
print('epub cteated!')