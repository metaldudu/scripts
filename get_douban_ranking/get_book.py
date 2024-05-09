import requests
import json
from datetime import datetime

# 抓取豆瓣图书热门榜数据，方便web展示
# ver 1.0
# 2024.5.9


headers = {
    "Referer": "https://m.douban.com/tv/american",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36"
}

type_dict = {
    "总榜": "EC645NBAI",
    "小说": "ECF45REBQ",
    "文学": "ECRM5OCGI",
    "历史文化": "ECIE5S2IQ",
    "社会纪实": "ECQU5U7HQ",
    "科学新知": "ECIM5L2YI",
    "艺术设计": "ECI45ZBNY",
    "影视戏剧": "ECWU5QFUI",
    "商业经管": "ECE45ORCA",
    "绘本漫画": "EC5U5NVYQ",
    "科幻奇幻": "ECEA5SP5A",
    "悬疑推理": "ECHU5PTUY"
}

with open('douban_book_hot_ranking.md', 'w', encoding='utf-8') as file:
    
    file.write(f"# 豆瓣一周热门图书榜\n\n")
    file.write(datetime.now().strftime('%Y-%m-%d') + "\n\n")
        
    url_head = "https://m.douban.com/rexxar/api/v2/subject_collection/"
    url_end = "/items?start=0&count=20&updated_at=&items_only=1&ck=Ho3x&for_mobile=1"
    
    for genre, identifier in type_dict.items():
        print(f"类型: {genre}, 标识符: {identifier}")
        file.write(f"## {genre}\n\n")
        url_full = url_head + str(identifier) + url_end
        #print(url_full)
        response = requests.get(url_full, headers=headers)

        # 判断是否返回json    
        index = 1
        if response.status_code == 200:
            data = response.json()
        
            for item in data['subject_collection_items']:
                title = item['title']
                rating_value = item['rating']['value']
                book_id = item['id']
                book_info = item['card_subtitle']
                
                #print(f"{index}. [《{title}》](https://book.douban.com/subject/{book_id}/), {book_info}, {rating_value}\n")
                file.write(f"{index}. [《{title}》](https://book.douban.com/subject/{book_id}/), {book_info}, {rating_value}\n")
                index += 1
            file.write(f"\n\n")
        
print("获取完成，结果已写入文件：douban_book_hot_ranking.md")
