# -*- coding:utf-8 -*-
# 批量下载dmzj的漫画，因为异步加载无法直接下载，利用chrome控制台，copy as curl
# 进行拼接命令行，然后输出
# 访问 m.dmzj.com 找到对应的漫画
# img = 'https://images.dmzj.com/j/精灵鼠小兵 1152之冬/第2卷/001.jpg' 
# 图片格式例子，注意有空格替换成%20
# 2020.9.27


import re
import os
import sys

# 【需修改的内容】
albumurl = 'https://m.dmzj.com/view/7194/14853.html' # 注意需要引用章节地址，curl 才能正确下载，通常只要改 14634 这里
imgurl = 'https://images.dmzj.com/j/精灵鼠小兵%201152之冬/第6卷/' # 复制图片地址的前部
imgnum = 27 #图片总数

# 循环下载到当前目录，剪切走，懒得再构造下载目录了
k = 1
imghead = ' -H \'Referer: ' + albumurl + '\' -H \'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.106 Safari/537.36\' -H \"DNT: 1\"  --compressed  -#' 
for i in range(1, imgnum+1):
    tmpurl = imgurl +  str('%.3d' % k) +'.jpg' #构造图片地址
    k = k+1
    cmd = 'curl -O ' + tmpurl +  imghead
    #print(cmd)
    os.system(cmd)
 


