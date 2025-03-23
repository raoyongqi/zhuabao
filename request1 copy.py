from seleniumwire2 import webdriver  # 注意这里是 seleniumwire 而不是 selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

import time

# 设置本地 Chrome 浏览器路径
chrome_path = r'C:\Users\r\Desktop\zhuabao\chrome-headless-shell-win64\chrome-headless-shell-win64\chrome-headless-shell.exe'  # 根据实际路径设置

# Chrome 的选项配置
chrome_options = Options()

# 如果你不想看到浏览器界面，可以添加以下选项来启用无头模式（即不显示浏览器窗口）
chrome_options.headless = False  # 设置为 False 以便看到浏览器界面

# 设置 Chrome 浏览器的二进制位置
chrome_options.binary_location = chrome_path
chromedriver_path = 'chromedriver.exe'  # 这里设置 chromedriver 路径

# 创建 Chrome 的服务对象，指定浏览器路径
service = Service(executable_path=chromedriver_path, log_path='chromedriver.log')



# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

# 目标网页URL
url = 'https://www.computer.org/csdl/proceedings-article/sc/2015/2807623/12OmNBf94Xq'

max_retries = 3
retries = 0

# 尝试访问网页，直到成功或超过最大重试次数
while retries < max_retries:
    try:
        driver.get(url)
        print(f"成功加载页面: {url}")
        break  # 如果成功加载页面，跳出循环
    except Exception as e:
        print(Exception)
        retries += 1
        print(f"第 {retries} 次尝试加载页面失败: {e}")
        if retries < max_retries:
            print("等待 3 秒后重试...")
            time.sleep(3)  # 等待 3 秒后重试
        else:
            print(f"超过最大重试次数 ({max_retries} 次)，无法加载页面。")

# 用一个集合来保存所有不重复的host
hosts = set()

# 假设 driver 是一个已经初始化的浏览器驱动，并且抓取了所有请求
for request in driver.requests:
    if request.response:
        # 解析请求的URL，提取host部分
        parsed_url = urlparse(request.url)
        if parsed_url.netloc:  # 如果URL中有有效的host部分
            hosts.add(parsed_url.netloc)

# 将不同的host保存为JavaScript数组格式到.js文件
with open('hosts.js', 'w', encoding='utf-8') as file:
    file.write('const hosts = [\n')
    for host in hosts:
        file.write(f'    "{host}",\n')  # 将每个host作为字符串写入数组
    file.write('];\n')

print("所有不同的host已成功保存到 hosts.js")

# 关闭浏览器
driver.quit()
