import requests

# 目标URL
url = 'https://chromedriver.chromium.org/'

# 发送GET请求获取页面内容
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    # 将网页内容保存到 HTML 文件
    with open('chromedriver_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("页面已成功保存为 chromedriver_page.html")
else:
    print(f"请求失败，状态码：{response.status_code}")
