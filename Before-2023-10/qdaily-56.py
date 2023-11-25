#coding=utf-8
#好奇心日报专栏

import requests
import re
import os

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

#函数：清理html标签
def clean_html(html):
    html = html.replace('\\n', '')#去掉换行符，两个斜线反义
    html = html.replace('data-src', 'src')#修改图片加载部分
    html = html.replace('\xa0', ' ')#替换空格
    html = html.replace(' </figure></div>', '')
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

# 清理广告部分
def clean_ad(html):

    # 建立列表
    list1 = html.split("\n\n")
    list2 =[]

    # 建立正则匹配模式
    match = re.compile(r'lazy\D*lazyload')
    for i in list1:
        if match.search(i):
            pass   
        else:
            list2.append(i)   
    html = "\n\n".join(list2)  
    return(html)
    

#函数：写入单个网页
def html_page(page_id):
    filename = 'tmp/' + str(page_id) +'.md'
    print('get file . . . ' + filename)
    filepage = open(filename, 'w')
    #建立文件

    page_url = 'http://www.qdaily.com/articles/' + str(page_id) + '.html'
    page = get_page(page_url)
    title = re.findall('<title>.*</title>', page, re.S)
    title = str(title).replace(' ', '')
    title = '# ' + str(title)[-28:-19] + '\n\n## ' + str(title)[9:-30] + '\n\n'
    filepage.write(title)
    #写入文章标题

    page = re.findall('<p class="excerpt">.* <div class="embed-mask">', page, re.S)
    page = str(page)[2:-31]#截取去掉头尾的括号和多余部分
    #获取正文部分

    page = str(clean_html(page))
    #清理html

    page = clean_ad(page)
    #清理广告

    filepage.write(page)
    #写入正文

    filepage.close()

#函数：抓取网页id到列表
def get_list(column_id):
    column_url = 'http://www.qdaily.com/special_columns/' + str(column_id)
    page = get_page(column_url)
    pages_id = re.findall(r'articles/\d+', page)
    return pages_id


   
############################## 主程序部分开始
# 指定专栏
columns = 56
os.system('mkdir tmp')

#开始输出md文件
ids = get_list(columns)
for i in ids:
    #print(i)
    i = i[9:]#获得pageid
    html_page(i)

def make_metafile():
    m_file = open('tmp/metadata.xml',  'w')
    m_file.write('<dc:title>房子和我们的生活</dc:title>\n' )
    m_file.write('<dc:language>zh-CN</dc:language>\n')
    m_file.write('<dc:creator opf:file-as="好奇心日报" opf:role="aut">好奇心日报</dc:creator>\n')
    m_file.write('<dc:date opf:event="publication">2018-09-17</dc:date>\n')
    m_file.close()

make_metafile()

#调用pandoc制作epub，toc指定在h1，设置title（否则报错），读入metadata.xml
cmd = 'pandoc tmp/*.md --toc-depth=1 --epub-metadata=tmp/metadata.xml --metadata title=好奇心日报：房子和我们的生活 --output 56.epub'
os.system(cmd)
#os.system('rm -rf tmp')
print('epub cteated!')