import requests
import json
import time
import re

# 日剧
# https://m.douban.com/rexxar/api/v2/tv/recommend?refresh=0&start={start}&count=20&selected_categories=%7B%22%E7%B1%BB%E5%9E%8B%22:%22%22,%22%E5%BD%A2%E5%BC%8F%22:%22%E7%94%B5%E8%A7%86%E5%89%A7%22%7D&uncollect=false&tags=%E6%97%A5%E6%9C%AC,%E7%94%B5%E8%A7%86%E5%89%A7&sort=S&ck=p09x
# 动画
# https://m.douban.com/rexxar/api/v2/tv/recommend?refresh=0&start={start}&count=20&selected_categories=%7B%22%E7%B1%BB%E5%9E%8B%22:%22%E5%8A%A8%E7%94%BB%22,%22%E5%BD%A2%E5%BC%8F%22:%22%E7%94%B5%E8%A7%86%E5%89%A7%22,%22%E5%9C%B0%E5%8C%BA%22:%22%E6%97%A5%E6%9C%AC%22%7D&uncollect=false&tags=%E6%97%A5%E6%9C%AC,%E5%8A%A8%E7%94%BB&sort=S&ck=p09x

headers = {
    "Referer": "https://m.douban.com/tv/american",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36"
}

with open('douban_tv_japan_top500.md', 'w', encoding='utf-8') as file:
    for i in range(25):
        
        # 构造页面地址
        start = i * 20
        
        url_tv = f"https://m.douban.com/rexxar/api/v2/tv/recommend?refresh=0&start={start}&count=20&selected_categories=%7B%22%E7%B1%BB%E5%9E%8B%22:%22%22,%22%E5%BD%A2%E5%BC%8F%22:%22%E7%94%B5%E8%A7%86%E5%89%A7%22%7D&uncollect=false&tags=%E6%97%A5%E6%9C%AC,%E7%94%B5%E8%A7%86%E5%89%A7&sort=S&ck=p09x"
        response = requests.get(url_tv, headers=headers)

        # 判断是否返回json    
        if response.status_code == 200:
            data = response.json()
        
            # 循环获取
            for index, item in enumerate(data['items'], 1):
                title = item['title']
                viewers = item['rating']['count']    
                rating = item['rating']['value']
                uri_number = re.search(r'\d+', item['uri']).group()
            
                file.write(f"{start + index}. {title}， 评分：{rating} ， {viewers} 人看过，[豆瓣页面](https://movie.douban.com/subject/{uri_number})\n")
                
            print(f"第 {i + 1} 次请求完成")
        else:
            print(f"第 {i + 1} 次请求失败，状态码：{response.status_code}")
        # 休息
        time.sleep(3)
        
print("所有请求完成，结果已写入文件：douban_tv_japan_top500.md")
