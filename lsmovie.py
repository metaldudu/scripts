# coding=utf-8
# 输出电影硬盘文件夹名，并拼音排序
# 2022.11.6

import os
import time
from pypinyin import pinyin

moviedir = '/media/MOV-4T/电影已削刮/'
files = os.listdir(moviedir)
files_dir = [f for f in files if os.path.isdir(os.path.join(moviedir, f))]
files_dir.sort(key=pinyin) #按拼音排序便于查找

list_file_name = '/home/laodu/notes/archives/movielist-' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.md'
f = open(list_file_name,'w')
f.write('total movies: ' + str(len(files_dir)-1) + '\n\n')
for i in files_dir:
    f.write('>> '+str(i)+'\n')
f.close()
