# 判断阿里云盘链接是否失效
# 20240107 with ChatGPT

import re
import time
import requests
import json
from datetime import datetime

class AliResponse:
    def __init__(self, code):
        self.code = code
        # Add other fields if needed

def aliYunCheck(url):
    share_id = url[25:]
    api_url = f"https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id={share_id}"

    # Define constants
    user_agent = "Mozilla/5.0 (Linux; Android 11; SM-G9880) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.37 Mobile Safari/537.36"
    referer = "https://www.alipan.com/"

    # Prepare parameters and headers
    params = {"share_id": share_id}
    headers = {"User-Agent": user_agent, "Referer": referer}
    data = json.dumps(params)

    try:
        # Send HTTP POST request
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse JSON response
        ali_response = AliResponse(response.json().get('code', ''))
        return ali_response.code == ""
    except requests.exceptions.RequestException as e:
        #print(f"Error sending HTTP request: {e}")
        return False

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 去除每行末尾的 'ok' 或 'no'
    lines = [re.sub(r'\s*( ✅| ❌)$', '', line) for line in lines]

    modified_lines = []
    for line in lines:
        # 使用正则表达式查找链接
        match = re.search(r'https://www.alipan.com/s/(\w+)', line)
        if match:
            url = match.group(0)
            result = aliYunCheck(url)
            
            # 打印URL和检查结果
            print(f"Checking URL: {url}, Result: {result}")

            # 在检查后休息1秒，否则查询几次就会全部返回错误
            time.sleep(1)

            # 更新行内容
            line = line.rstrip('\n') + ' ✅\n' if result else line.rstrip('\n') + ' ❌\n'
        modified_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)
        
def add_date(file_path):
    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 删除末尾的一行
    if lines:
        lines.pop()

    # 添加空行和包含当前日期的新行
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #lines.append('\n')
    lines.append(f"Checked Date: {current_date}\n")

    # 将更新后的内容写回文件
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    file_path = "links-file.md"
    process_file(file_path)
    add_date(file_path)
