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
import sys

# 先用 txt2md.py 整理txt文件
#FILENAME = sys.argv[1]
FILENAME = '1.txt.md'

# 以下为电子书基本信息，需编辑！
BOOKTITLE = '野丫头凯蒂' #书名
BOOKSUBTITLE = '' #副标题
BOOKAUTHOR = '卡罗尔·拉瑞·布林克' #作者
BOOKISBN = '9787534266034' #ISBN，13位
BOOKDOUBAN = '6560634' # 豆瓣id，配合calibre插件
BOOKPUB = '浙江少年儿童出版社' #出版社
BOOKCOVER = 'cover.jpg' #封面图片

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

make_metafile() # 建立metadata.txt

#调用pandoc制作epub，toc指定在h1，设置title（否则报错），md转换读入metadata.txt
# 指定了epub.css，中文缩进两个字
cmd = 'pandoc --toc-depth=1  -o ' + BOOKTITLE + '.epub metadata.txt ' + FILENAME + ' --metadata title=' + BOOKTITLE + ' -c epub.css'
os.system(cmd)

os.system('rm -rf metadata.txt') #删除metadata文件
print( BOOKTITLE +'.epub cteated!')

# 转换一份mobi
cmd = 'ebook-convert "' + BOOKTITLE + '.epub" "' + BOOKTITLE + '.mobi"'
os.system(cmd)

# 文档：https://pandoc.org/MANUAL.html#epub-metadata
# 参考：https://medium.com/programmers-developers/building-books-with-markdown-using-pandoc-f0d19df7b2ca
