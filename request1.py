from seleniumwire2 import webdriver  # 注意这里是 seleniumwire 而不是 selenium
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlparse

import time

# 设置本地 Firefox 浏览器路径
firefox_path = r'C:\Users\r\Desktop\firefox\firefox.exe'

# Firefox 的选项配置
firefox_options = Options()

# 如果你不想看到浏览器界面，可以添加以下选项来启用无头模式（即不显示浏览器窗口）
firefox_options.headless = False
firefox_options.set_preference('security.ssl.enable_ocsp_stapling', False)
firefox_options.set_preference('security.ssl.errorReporting.automatic', False)
firefox_options.set_preference('security.ssl.treat_unsafe_negotiation_as_broken', False)

firefox_options.binary_location = firefox_path
geckodriver_path = 'geckodriver.exe'  # 这里设置 geckodriver 路径
# 创建 Firefox 的服务对象，指定浏览器路径

#https://leetcode.com/

service = Service(executable_path=geckodriver_path, log_path='geckodriver.log')
# 禁用代理
import psutil
import os
import signal

# 查找并强制终止 Tor 相关进程
import psutil

# 查找包含 "tor" 的进程，并获取进程路径
for proc in psutil.process_iter(attrs=['pid', 'name', 'exe']):
    if 'tor' in proc.info['name'].lower():  # 过滤出 Tor 进程
        try:
            # 输出进程路径（exe 属性）
            print(f"进程 {proc.info['name']} ({proc.info['pid']}) 路径: {proc.info['exe']}")
        except psutil.AccessDenied:
            print(f"拒绝访问进程 {proc.info['pid']}，无法获取路径")
        except psutil.NoSuchProcess:
            print(f"进程 {proc.info['pid']} 已经不存在")

# seleniumwire_options = {
#     'disable_encoding': True,  # 确保没有代理
#     'proxy': None  # 禁用代理
# }

# # 启动 Firefox 浏览器并确保不使用代理
driver = webdriver.Firefox(service=service, options=firefox_options)
# print(f"服务运行在端口： {driver.process.pid}")
# # 启动 Firefox 浏览器



# with open('geckodriver.log', 'r') as log_file:
#     print(log_file.read())

# # 打开网页
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
            time.sleep(300)  # 等待 3 秒后重试
        else:
            print(f"超过最大重试次数 ({max_retries} 次)，无法加载页面。")

# # 等待网页加载完成，或者可以在这里设置一些逻辑来确保页面完全加载
# # 例如：time.sleep(5) 等待5秒

# # 用一个集合来保存所有不重复的host
hosts = set()

# # 遍历所有的请求（抓包请求）
for request in driver.requests:
    if request.response:
        # 解析请求的URL，提取host部分
        parsed_url = urlparse(request.url)
        if parsed_url.netloc:  # 如果URL中有有效的host部分
            hosts.add(parsed_url.netloc)

# # # 将不同的host保存到txt文件
with open('hosts.txt', 'w', encoding='utf-8') as file:
    for host in hosts:
        file.write(host + '\n')

print("所有不同的host已成功保存到 hosts.txt")

# # 关闭浏览器
# driver.quit()
