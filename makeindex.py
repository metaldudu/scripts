#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# 读取文档目录，生成适合mdwiki格式的首页

import os
import sys
import platform


# print (platform.system())

if platform.system() == 'Windows':
    path = "d:/jianguoyun/mynotes"
else:
    path = "/home/laodu/jianguoyun/mynotes/"
# 定义主目录
dirlist = []
indexfile = open('index2.md','w',encoding='utf-8')
#注意编码！

files = os.listdir(path)
files.sort()
for f in files:
    fpath = os.path.join(path,f)
    if (f[0] == '.'):
        pass
    elif os.path.isdir(fpath):
        #print ('## ' + f + '\n\n')
        indexfile.write('\n\n## ' + f + '\n\n')
        for l in os.listdir(fpath):
            filename = '[' + l.replace('.md', '') +'](' + f +'/' + l + ') 　'
            indexfile.write(filename)
    elif os.path.isfile(fpath):
        print ('ok')


#print (dirlist)

indexfile.close()