import requests
from bs4 import BeautifulSoup
import time

# 基础URL
base_url = "https://book.douban.com/tag/%E6%8E%A8%E7%90%86"

# 添加头部信息，模拟正常浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 存储图书信息的列表
all_books = []

# 循环抓取10个页面
for page in range(0, 30):
    # 构造当前页的URL
    current_url = f"{base_url}?start={page * 20}&type=T"

    # 发送请求，包含头部信息
    response = requests.get(current_url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有符合条件的 li 标签
        subject_items = soup.find_all('li', class_='subject-item')

        # 遍历每个 li 标签，获取对应的标题、评分、评论和链接
        for item in subject_items:
            title_element = item.find('h2', class_='')
            book_title = title_element.find('a').text.strip().replace('\n', '').replace(' ', '')
            book_link = title_element.find('a').get('href')

            rating_element = item.find('div', class_='star clearfix')
            rating_nums_element = rating_element.find('span', class_='rating_nums')
            if rating_nums_element is None:
                # 如果无法获取评分，跳过当前循环
                print(f"第 {page + 1} 页的一本书无法获取评分，跳过当前循环")
                continue

            rating_nums = rating_nums_element.text.strip()

            pl_element = item.find('span', class_='pl')
            comment_count = pl_element.text.strip().replace('(', '').replace('人评价)', '')

            all_books.append((book_title, rating_nums, comment_count, book_link))

        # 输出当前页的结果
        print(f"第 {page + 1} 页抓取成功")

        # 休息6秒
        time.sleep(4)

    else:
        print(f"第 {page + 1} 页请求失败，状态码:{response.status_code}")

# 按照评分（第二个字段）大小进行排序
sorted_books_rating = sorted(all_books, key=lambda x: float(x[1]) if x[1] else 0, reverse=True)
sorted_books_people = sorted(all_books, key=lambda x: float(x[2]) if x[2] else 0, reverse=True)


# 写入到 output.md 文件
with open('douban_tuili_people.md', 'w', encoding='utf-8') as file:
    file.write("# 豆瓣推理小说排名：按人数\n\n")
    for book in sorted_books_people:
        file.write(f"- [《{book[0]}》]({book[3]})  {book[1]} （{book[2]}）\n")
        
        
with open('douban_tuili_rating.md', 'w', encoding='utf-8') as file:
    file.write("# 豆瓣推理小说排名：按评分\n\n")
    for book in sorted_books_rating:
        file.write(f"- [《{book[0]}》]({book[3]})  {book[1]} （{book[2]}）\n")
        
  
