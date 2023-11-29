import requests
import json
import time
import re

headers = {
    "Referer": "https://m.douban.com/tv/american",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36"
}

movies = []

for i in range(20):
    # 构造页面地址
    start = i * 20
    
    # 电影
    url_tv = f"https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start={start}&count=20&selected_categories=%7B%22%E5%9C%B0%E5%8C%BA%22:%22%E5%8D%8E%E8%AF%AD%22%7D&uncollect=false&tags=%E5%8D%8E%E8%AF%AD&sort=S&ck=p09x"
    response = requests.get(url_tv, headers=headers)

    # 判断是否返回json    
    if response.status_code == 200:
        data = response.json()
    
        # 循环获取
        for item in data['items']:
            title = item['title']
            viewers = item['rating']['count']    
            rating = item['rating']['value']
            uri_number = re.search(r'\d+', item['uri']).group()
            
            if '演唱会' not in title and '音乐会' not in title:
                if viewers > 5000:
                    movies.append({"title": title, "rating": rating, "viewers": viewers, "uri_number": uri_number})
            else:
                print(f"跳过标题包含演唱会或音乐会的电影：{title}")
        
        print(f"第 {i + 1} 次请求完成")
    else:
        print(f"第 {i + 1} 次请求失败，状态码：{response.status_code}")
    # 休息
    time.sleep(2)

# 写入文件
with open('douban_movie_cn_top100.md', 'w', encoding='utf-8') as file:
    for index, movie in enumerate(movies, 1):
        file.write(f"{index}. {movie['title']}， 评分：{movie['rating']} ， {movie['viewers']} 人看过，[豆瓣页面](https://movie.douban.com/subject/{movie['uri_number']})\n")

print("所有请求完成，结果已写入文件：douban_movie_cn_top100.md")
