# -*- coding:utf-8 -*-
# 长文字转图片脚本 20190107
# https://pypi.org/project/pyperclip/
# 只支持linux 安装了 xclip

from PIL import Image, ImageDraw, ImageFont
import pyperclip
import os

#text = u"这是一段测试文本这是一段测试文本这是一段测试文本这是一段测试文本这是一段测试文本"
text = pyperclip.paste() #剪切板内容

#处理换行 每行17字
textout = []
j = 0
for i in text:
  textout.append(i)
  if i == '\n':
    j = 0
  else: 
    j = j +1
    if j % 17 == 0:
      textout.append('\n')
      j = 0

text = ''.join(textout)

# 行高计算
image_height = text.count('\n') * 33 + 40
if image_height < 700:
  image_height = 700

im = Image.new("RGB", (450, image_height), ("#E0E3DA"))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype('/usr/share/fonts/adobe-source-han-serif/SourceHanSerifCN-Regular.otf', 25)
dr.text((10, 5), text, font=font, fill="#383A3F")
 
im.show()
im.save("t.png")