#!/usr/bin/python
#coding=utf-8
#markdown格式生成epub脚本
# 20181020

################################################################
# 制作电子书需要准备：
# 1. txt文件，utf8格式：1.txt
# 2. 封面图片文件：cover.jpg
# 3. 编辑下面的书籍信息
################################################################
import re
import os
import datetime

# 电子书路径

FILENAME = '1.txt'

# 以下为电子书基本信息，需编辑！

BOOKTITLE = '俗丽之夜' #书名
BOOKSUBTITLE = '' #副标题
BOOKAUTHOR = '多萝西·L.塞耶斯' #作者
BOOKISBN = '9787513303880' #ISBN，13位
BOOKDOUBAN = '6833941' # 豆瓣id，配合calibre插件
BOOKPUB = '新星出版社 ' #出版社
BOOKCOVER = 'cover.jpg' #封面图片


# 函数：整理text文件，生成书名.md文件
def cleantxt(txtfile):
    f = open(txtfile, 'r') #读utf8文件
    mdfile = open(BOOKTITLE+'.md', 'wb') #建立md文件

    for line in f.readlines():
        line = line.replace('　', '') # 删除空格
        line = line.replace(' ', '')
        if len(line) != 0:
            line = line.strip() #清除段落前后的空白，包括多个空行    
            if re.match(r'序章|第.+章|尾声|后记', line):#匹配章节并修改
                line = '# ' + line
                print(line)

            mdfile.write(line.encode('utf-8'))#写入时需要转换成utf-8
            mdfile.write('\n\n'.encode('utf-8'))# 在段落后写入空行
    f.close()
    mdfile.close()

# 函数：生成metadata信息
def make_metafile():
    m_file = open('metadata.txt',  'w')

    m_file.write('---\n')
    m_file.write('title:\n')
    m_file.write('- type: main\n')
    m_file.write('  text: ' + BOOKTITLE + '\n')
    m_file.write('- type: subtitle\n')
    m_file.write('  text: ' + BOOKSUBTITLE + '\n')
    m_file.write('creator:\n')
    m_file.write('- role: author\n')
    m_file.write('  text: ' + BOOKAUTHOR + '\n')
    m_file.write('identifier:\n')
    m_file.write('- scheme: ISBN-13\n')
    m_file.write('  text: isbn:' + BOOKISBN + '\n')
    m_file.write('- scheme: DOUBAN\n')
    m_file.write('  text: douban:' + BOOKDOUBAN +'\n')
    m_file.write('publisher: ' + BOOKPUB + '\n')
    m_file.write('rights:\n')
    m_file.write('language: zh-CN\n')
    m_file.write('cover-image: ' + BOOKCOVER + '\n')

    m_file.write('\n...')
    m_file.close()

cleantxt(FILENAME) # 整理txt文件
make_metafile() # 建立metadata.txt



#调用pandoc制作epub，toc指定在h1，设置title（否则报错），md转换读入metadata.txt
cmd = 'pandoc --toc-depth=2  -o ' + BOOKTITLE + '.epub metadata.txt ' + BOOKTITLE + '.md --metadata title=' + BOOKTITLE + ''
os.system(cmd)
os.system('rm -rf metadata.txt') #删除metadata文件
os.system('rm -rf ' +  BOOKTITLE + '.md') #删除临时md文件
print( BOOKTITLE +'.epub cteated!')

# 转换一份mobi
cmd = 'ebook-convert "' + BOOKTITLE + '.epub" "' + BOOKTITLE + '.mobi"'
os.system(cmd)

# 文档：https://pandoc.org/MANUAL.html#epub-metadata
# 参考：https://medium.com/programmers-developers/building-books-with-markdown-using-pandoc-f0d19df7b2ca
