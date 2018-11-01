# coding=utf-8

# 20181020

# todo：把功能做成可选菜单型
# 1. 修正全角数字 2. 删除特定行（如电子书网站分页）

import sys
import re
import os

# 用户输入处理的txt文档
text_file = sys.argv[1]
md_file = text_file + '.md'
os.system('cp ' + text_file + ' ' + md_file)
print('已保存.md副本')



# 函数01：清理缩进的空格
def cleanblank(textfile):
    f = open(textfile, 'r') #读txt文件
    tmplist = [] #建立临时list

    for line in f.readlines():
        line = line.strip() #清除头尾的空格
        line = line.strip('　')# 清除所有全角空格
        if len(line) > 0: #跳过空行
            tmplist.append(line+'\n\n') #每段加上空行
    f.close()

    fnew = open(textfile, 'w')
    for i in tmplist: #回写到文件
        fnew.write(i)
    fnew.close()
    print('已清除缩进的空格')

# 函数02：按章节分割文件
def addtoc(textfile):
    f = open(textfile, 'r')#读utf8文件
    tmplist = [] #建立临时list

    for line in f.readlines():
        line = line.strip()
        if len(line) != 0:           
            match1 = r'序章|第.+章|第.+乐章|尾声|后记|终章|[一二三四五六七八九十]、' # 各种奇葩分节方式
            match2 = r'[１２３４５６７８９０]+' #全角数字
            match4 = r'\d' #半角数字，一般为小节
            match5 = r'.+～' # 章节中含有某个字符
            match6 = r'.+月.+日' # 小节名称含有月和日

            if re.match(match1, line) and len(line) < 20:# 章节名不可能太长
                line = '# ' + line # 改为h1          
            if (re.match(match2, line)) and len(line) < 28:# 匹配可能的小节
                line = '## ' + line # 改为h2
                
            tmplist.append(line+'\n\n') #每段加上空行
    f.close()

    fnew = open(textfile, 'w')
    for i in tmplist: #回写到文件
        fnew.write(i)
    fnew.close()
    print('已安章节分割文件')

# 函数03：特定标题添加空格，例：第一章开始》第一章　开始
def addblank(txtfile):
    f = open(txtfile, 'r')#读utf8文件
    tmplist = [] #建立临时list

    for line in f.readlines():
        line = line.strip() #清除头尾的空格
        if re.match(r'第.+章', line):#匹配章节
            # print(line)
            posi = line.find('章') + 1 #章字的位置
            line = line[0:posi] + '　' + line[posi:]
        if len(line) > 0: #跳过空行
            tmplist.append(line+'\n\n') #每段加上空行
    f.close()

    fnew = open(txtfile, 'w')
    for i in tmplist: #回写到文件
        fnew.write(i)
    fnew.close()
    print('已在标题中添加空格')

######################################
print('-------------------------------')
print('1. 清除缩进的空格  2. 按章节分割文件 3. 章节部分添加空格')
print('-------------------------------')
keyinput = input('输入需要的操作： ')


if keyinput == '1':
    cleanblank(md_file)
elif keyinput == '2':
    addtoc(md_file)
elif keyinput == '3':
    addblank(md_file)


######################################


# 函数：删除特定行
def dellines(txtfile):
    f = open(txtfile, 'r')#读utf8文件
    fnew = open('tmp2.md', 'wb')#建立临时文件tmp.md

    for line in f.readlines():

        if re.match(r'第.+部分', line):#匹配章节并修改
            print(line)
            line = ''
        line = line.strip()
        if len(line) != 0:# 跳过空行           
            fnew.write(line.encode('utf-8'))#写入时需要转换成utf-8
            fnew.write('\n\n'.encode('utf-8'))#写入换行

    f.close()
    fnew.close()







# 下面两个函数转自：https://segmentfault.com/a/1190000012227758
# 处理全角数字，包括⑩ ⑽ ⒑ Ⅻ

def SBC2DBC(char):
    chr_code = ord(char)
    # 处理全角中数字大等于10的情况
    if chr_code in range(9312, 9332):
        return str(chr_code - 9311)
    elif chr_code in range(9332, 9352):
        return str(chr_code - 9331)
    elif chr_code in range(9352, 9372):
        return str(chr_code - 9351)
    elif chr_code in range(8544, 8556):
        return str(chr_code - 8543)

    else:
        if chr_code == 12288: # 全角空格，同0x3000
            chr_code = 32
        if chr_code == 8216 or chr_code == 8217:  # ‘’
            chr_code = 39 # '
        elif chr_code in range(65281, 65374):
            chr_code = chr_code - 65248
        return chr(chr_code)


def fixnumber(txtfile):
    f = open(txtfile, 'r')#读utf8文件
    fnew = open('tmp3.md', 'wb')#建立临时文件tmp.md

    for line in f.readlines():
        new_line = ''
        for char in line:
            new_line += SBC2DBC(char)
            
        fnew.write(new_line.encode('utf-8'))

    f.close()
    fnew.close()    

###############################
# 以下手工处理

#cmd = 'cp 1.txt 1.md'
#os.system(cmd) #复制一份

#cleantxt('1.md')

#dellines('1.md')
#fixnumber('1.txt')