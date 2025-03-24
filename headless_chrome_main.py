import json
import os
import re
import csv
from urllib.parse import urlparse



with open('newbackground.js','r', encoding='utf-8') as file:
    js_content = file.read()

# 使用正则表达式匹配 'const allowedUrls = [' 后的数组内容
match = re.search(r'const\s+allowedUrls\s*=\s*\[([^\]]*)\];', js_content)

if match:
    # 提取数组中的 URL 并按 URL 长度排序
    urls = re.findall(r'"([^"]+)"', match.group(1))
    sorted_urls = sorted(urls, key=len)
    filtered_urls = [
        url for url in sorted_urls 
        if not url.startswith('*.') and url not in ['ws', 'www']
    ]


import os
import json
import re
import time
from seleniumwire2 import webdriver  # 注意这里是 seleniumwire 而不是 selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

# 记录开始时间
start_time = time.time()

# 设置本地 Chrome 浏览器路径
chrome_path = r'C:\Users\r\Desktop\zhuabao\chrome-headless-shell-win64\chrome-headless-shell-win64\chrome-headless-shell.exe'  # 根据实际路径设置

# Chrome 的选项配置
chrome_options = Options()
chrome_options.headless = False  # 设置为 False 以便看到浏览器界面
chrome_options.binary_location = chrome_path
chromedriver_path = 'chromedriver.exe'  # 这里设置 chromedriver 路径

# 创建 Chrome 的服务对象，指定浏览器路径
service = Service(executable_path=chromedriver_path, log_path='chromedriver.log')

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

def sanitize_url(url):
    # 去掉 URL 中的协议部分（http:// 或 https://）
    url = re.sub(r'^https?://', '', url)
    
    # 将下划线 _ 替换为空字符串
    url = url.replace('_', '')
    
    # 替换 URL 中的特殊字符为合法的文件名字符
    # 可以替换为其他字符，比如下划线，空格等
    url = re.sub(r'[^\w\s.-]', '', url)
    
    # 将多个连续的点（.）替换为一个点
    url = re.sub(r'\.{2,}', '.', url)
    
    return url


# 存储所有唯一的 hosts URL
# 获取目录中所有的文件
folder_path = 'data'  # 替换为您文件夹的路径
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 '{folder_path}' 已创建。")
else:
    print(f"文件夹 '{folder_path}' 已存在。")
total_files = len(sorted_urls)

# 定义计数器
counter = 0

# 创建错误日志文件
error_log_path = 'error_log.txt'


keep_urls = filtered_urls
keep_urls.append('ws')
# 定义函数记录错误日志
def log_error(message):
    with open(error_log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')
for line in filtered_urls:
    try:
        print('https://'+line)

        file_path = 'data/' + sanitize_url(line) + '.js'

        if os.path.exists(file_path):
            print(f"文件 {file_path} 已存在，跳过处理.")


        else:
            hosts = set()  # Assuming this is declared outside the loop
            driver.get('https://'+line)
            for request in driver.requests:
                if request.response:
                    parsed_url = urlparse(request.url)
                    if parsed_url.netloc:  # 如果 URL 中有有效的 host 部分
                        hosts.add(parsed_url.netloc)

            # Avoid cumulative data
            del driver.requests

            # Write to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('const hosts = [\n')
                for host in hosts:
                    file.write(f'    "{host}",\n')  # 将每个 host 作为字符串写入数组
                file.write('];\n')

            print(f"已处理 {line}")
        
        # 每处理10个文件输出一次时间
        counter += 1
        if counter % 100 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"已处理 {counter} 个文件，总耗时: {elapsed_time:.2f} 秒")
    
    except Exception as e:
        error_message = f"处理 URL {line} 时出错: {e}"
        print(error_message)
        log_error(error_message)

        with open("error_urls.txt", "a") as error_file:
            error_file.write(f"{line}\n")
        keep_urls.remove(line)
        js_content_new = f"""
        const allowedUrls = {json.dumps(keep_urls, ensure_ascii=False, indent=4)};
        const blockedUrls = [
        "*://www.google.com/search*",
        ".*firefox.*",
        ".*firefox",
        "*://camo.githubusercontent.com/*" // 用于阻止包含“firefox”的 URL 的正则表达式
        ];

        const onBeforeRequest = (details) => {{
        const url = new URL(details.url);
        const host = url.hostname;

        // 检查是否在被阻止的 URL 列表中
        const isBlocked = blockedUrls.some(pattern => {{
            const regex = new RegExp(pattern.replace(/\*/g, '.*'));
            return regex.test(details.url); // 检查整个 URL
        }});

        if (isBlocked) {{
            console.log(`Blocked URL: ${{details.url}}`);
            return {{ cancel: true }}; // 拦截请求
        }}

        // 检查是否在允许的 URL 列表中
        const isAllowed = allowedUrls.some(pattern => {{
            // 处理通配符
            if (pattern.startsWith("*.") && host.endsWith(pattern.slice(2))) {{
            return true;
            }}
            return host === pattern || host === 'www.' + pattern; // 检查主机名
        }});

        if (!isAllowed) {{
            console.log(`Blocked URL: ${{details.url}}`);
            return {{ cancel: true }}; // 拦截请求
        }}

        return {{ cancel: false }}; // 允许请求
        }};

        // 监听所有请求
        browser.webRequest.onBeforeRequest.addListener(
        onBeforeRequest,
        {{ urls: ["<all_urls>"] }},
        ["blocking"]
        );
        """

        # 将生成的新内容写入到文件中
        with open('newbackground1.js', 'w', encoding='utf-8') as js_file:
            js_file.write(js_content_new)

        print("Combined and de-duplicated hosts saved to newbackground.js")

def save_hosts_to_js(hosts, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('const hosts = [\n')
        for host in hosts:
            file.write(f'    "{host}",\n')  # 将每个 host 作为字符串写入数组
        file.write('];\n')

# 记录结束时间
end_time = time.time()

# 计算并输出操作耗时
elapsed_time = end_time - start_time
print(f"操作完成，总耗时: {elapsed_time:.2f} 秒")

# 关闭浏览器
driver.quit()
