#!/usr/local/bin/python
#coding=utf-8
# 抓取pm2.5
# ver 20160204

import urllib.request
import re
from bs4 import BeautifulSoup  
import time
import os
import sys
from threading import Timer

linkurl = 'http://www.pm25.in/shijiazhuang'

response = urllib.request.urlopen(linkurl)
soup = BeautifulSoup(response,"lxml")  


def PmOutput():
    #print ('------------------------------------------------')
    city = soup.find("div", class_="city_name")#以class搜索
    level = soup.find("div", class_="level")
    #print  ((city.h2.string + ':' + level.h4.string.replace('\n','').replace(' ','')), end='')
    results = soup.find_all("div", class_="caption")
    for result in results:
        r = result.string.replace('\n','').replace(' ','')
        if r == 'AQI':
            r_aqi = result.find_previous_sibling()
            print (('Air quality: ' + r_aqi.string.replace('\n','').replace(' ','') ), end='')
        elif r == 'PM2.5/1h':
            r_pm25 = result.find_previous_sibling()
            #print ('PM2.5:' + r_pm25.string.replace('\n','').replace(' ',''))
    #print ('------------------------------------------------')

PmOutput()


