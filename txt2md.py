# coding=utf-8


# 转换一般txt格式电子书，到markdown格式，
# 分章节以便进一步转换epub
# 20181020

import sys
import re


# txt文档路径

txtfile = '1.txt'

# 函数：清除多余空行
def cleantxt(txtfile):
    f = open(txtfile, 'r')#读utf8文件
    fnew = open('tmp.md', 'wb')#建立临时文件tmp.md

    for line in f.readlines():
        line = line.replace('　', '') # 删除空格
        line = line.replace(' ', '')
        if len(line) != 0:
            line = line.strip()     
            if re.match(r'序章|第.+章|尾声|后记', line):#匹配章节并修改
                line = '# ' + line
                print(line)

            fnew.write(line.encode('utf-8'))#写入时需要转换成utf-8
            fnew.write('\n\n'.encode('utf-8'))# 写入空行
    f.close()
    fnew.close()


# 函数：删除特定行
def dellines(txtfile):
    f = open(txtfile, 'r')#读utf8文件
    fnew = open('tmp2.md', 'wb')#建立临时文件tmp.md

    for line in f.readlines():
        if re.match(r'第.+部分', line):#匹配章节并修改
            print(line)
            line = ''
        line = line.strip()
        if len(line) != 0:          
            
            fnew.write(line.encode('utf-8'))#写入时需要转换成utf-8
            fnew.write('\n\n'.encode('utf-8'))#写入换行

    f.close()
    fnew.close()

dellines('1.txt')