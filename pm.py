#!/usr/local/bin/python
#coding=utf-8
# 抓取 iqair.cn 空气质量和天气
# ver 2022-11-25

import urllib.request
import re
from bs4 import BeautifulSoup  
import os
import sys


linkurl = 'https://www.iqair.cn/cn/china/hebei/shijiazhuang/shijiazhuang-staff-hospital' #url对应空气监测站点
air_site = linkurl.split('/')[-1] #获取唯一的站点名称

response = urllib.request.urlopen(linkurl)
soup = BeautifulSoup(response,"lxml")  


def PmOutput(): 
    air_aqi = soup.find("p", class_="aqi-value__value").string #aqi数值
    
    air_all = soup.find("table", class_="aqi-overview-detail__other-pollution-table") #空气质量table

    pm25 = air_all.find_all('tr')[1]  # 第二个tr
    pm25_num = pm25.find_all('td')[2].select('span')[0].string

    pm10 = air_all.find_all('tr')[2]
    pm10_num = pm10.find_all('td')[2].select('span')[0].string

    weather = soup.find("div", class_="weather") #天气部分
    temperature = weather.table.find_all('tr')[1].find_all('td')[1].string
    humidity = weather.table.find_all('tr')[2].find_all('td')[1].string

    air_output = '\033[32;40m[' + air_site + '] ' + temperature + ' / '+ humidity + ' / AQI: ' + str(air_aqi) + ' / pm2.5: ' + str(pm25_num) + ' / pm10: ' + str(pm10_num) +'\033[0m'
    #  给输出命令行加颜色，\033[32;40m为黑底绿字

    print(air_output)
    

PmOutput()


