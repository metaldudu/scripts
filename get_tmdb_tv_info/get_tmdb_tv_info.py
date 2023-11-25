import requests
from bs4 import BeautifulSoup
import subprocess
# 获取TMDB多集剧集信息，输出为 markdown 格式，并放到剪切板
# 2023-11

# 电视剧ID号和网址,修改ID获取对应网址
tv_id = 3476
url = f"https://www.themoviedb.org/tv/{tv_id}/seasons"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

# 发送HTTP请求获取页面内容
response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(response.text, 'html.parser')

# 创建一个空字符串，用于存储所有输出内容
output_text = ""


# 找到具有特定类名的元素
single_column_wrapper_elements = soup.select(".single_column_wrapper")

# 循环处理每个具有特定类名的元素
for single_column_wrapper_element in single_column_wrapper_elements:
    # 在该元素下找到<h2>标签
    h2_element = single_column_wrapper_element.find("h2")

    # 输出<h2>标签的内容
    if h2_element:
        h2_content = h2_element.text.replace('\n', ' ').strip()
        output_text += f"## TV name: {h2_content}\n"

# 增加TMDB地址
url_main = url.replace('/seasons', '')
output_text += f"\n[TMDB PAGE]({url_main})\n\n"

# 找到具有特定类名的元素
season_wrapper_elements = soup.select(".season_wrapper")

# 循环处理每个具有特定类名的元素
for season_wrapper_element in season_wrapper_elements:
    # 在该元素下找到所有具有特定类名的子元素
    content_elements = season_wrapper_element.select(".content")

    # 循环处理每个具有特定类名的子元素
    for content_element in content_elements:
        # 在该子元素下找到<h2>标签
        h2_element = content_element.find("h2")

        # 输出<h2>标签的内容
        if h2_element:
            h2_content = h2_element.text.strip()
            output_text += f"- [ ] {h2_content}"

        # 在该子元素下找到<h4>标签
        h4_element = content_element.find("h4")

        # 输出<h4>标签的内容
        if h4_element:
            # 提取评分和年份等信息
            rating_element = h4_element.find("div", class_="rating season_rating")
            rating = rating_element.text.strip() if rating_element else "N/A"

            year_and_episodes = h4_element.contents[-1].strip()

            output_text += f" - {year_and_episodes}\n"

print(output_text)

# 将所有输出内容放入剪贴板
subprocess.run(["xclip", "-selection", "clipboard"], input=output_text.encode("utf-8"), check=True)
