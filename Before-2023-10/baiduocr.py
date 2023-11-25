#coding=utf-8  
# 百度ocrapi，读取本地图片并识别

from aip import AipOcr


# 百度AI部分
APP_ID = '15529244'
API_KEY = 'TgXpSb1tWliUDeqrYLh722i7'
SECRET_KEY = 'K19qjQ2An9LSEDwd143vCxpXU3whwOsz'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('111.png')
results = client.general(image)["words_result"]

outputtxt = []
for r in results:
    text = r["words"]
    outputtxt.append(text)

#print(outputtxt)
f = open('111.md','w',encoding='utf-8')
for i in outputtxt:
    f.write(i + '\n')
f.close()
