import json
import os
import re
from urllib.parse import urlparse
import time
from seleniumwire2 import webdriver  # 注意这里是 seleniumwire 而不是 selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

with open('newbackground.js','r', encoding='utf-8') as file:
    js_content = file.read()

# 使用正则表达式匹配 'const allowedUrls = [' 后的数组内容
def extract_and_sort_urls(js_content, variable_name):
    """
    提取并过滤特定 JS 内容中的 URL 列表。
    
    :param js_content: JS 内容的字符串
    :param variable_name: 变量名（如 'beginWithStar' 或 'beginWithoutStar'
    :return: 排序并过滤后的 URL 列表
    """
    match = re.search(rf'const\s+{variable_name}\s*=\s*\[([^\]]*)\];', js_content)
    
    if match:
        urls = re.findall(r'"([^"]+)"', match.group(1))
        sorted_urls = sorted(urls, key=len)
        filtered_urls = [url for url in sorted_urls if url not in ['ws', 'www']]
        return filtered_urls
    return []

with open('newbackground.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

begin_with_star_urls = extract_and_sort_urls(js_content, 'beginWithStar')
begin_without_star_urls = extract_and_sort_urls(js_content, 'beginWithoutStar')

start_time = time.time()

# 设置本地 Chrome 浏览器路径
chrome_path = r'C:\Users\r\Desktop\zhuabao\chrome-headless-shell-win64\chrome-headless-shell-win64\chrome-headless-shell.exe'  # 根据实际路径设置

chrome_options = Options()
chrome_options.headless = False  # 设置为 False 以便看到浏览器界面
chrome_options.binary_location = chrome_path
chromedriver_path = 'chromedriver.exe'  # 这里设置 chromedriver 路径

# 创建 Chrome 的服务对象，指定浏览器路径
service = Service(executable_path=chromedriver_path, log_path='chromedriver.log')

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

def sanitize_url(url):

    url = re.sub(r'^https?://', '', url)
    
    url = url.replace('_', '')
    
    url = re.sub(r'[^\w\s.-]', '', url)
    
    url = re.sub(r'\.{2,}', '.', url)
    
    return url


folder_path = 'data'  # 替换为您文件夹的路径
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 '{folder_path}' 已创建。")

else:
    print(f"文件夹 '{folder_path}' 已存在。")
total_files = len(begin_without_star_urls)

# 定义计数器
counter = 0

# 创建错误日志文件
error_log_path = 'error_log.txt'


keep_urls = begin_without_star_urls

keep_urls.append('ws')

def log_error(message):

    with open(error_log_path, 'a', encoding='utf-8') as log_file:

        log_file.write(message + '\n')

for line in begin_without_star_urls:
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
        
        counter += 1
        if counter % 100 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"已处理 {counter} 个文件，总耗时: {elapsed_time:.2f} 秒")
    
    except Exception as e:
        error_message = f"处理 URL {line} 时出错: {e}"
        print(f"An error occurred: {e}")
        
        if "disconnected: not connected to DevTools" in str(e):
            print("Connection to DevTools was lost.")
            raise



        print(error_message)
        log_error(error_message)

        with open("error_urls.txt", "a") as error_file:
            error_file.write(f"{line}\n")
        keep_urls.remove(line)
        
        js_content_new = f"""
        const beginWithStar = {json.dumps(begin_with_star_urls, ensure_ascii=False, indent=4)};
        const beginWithoutStar = {json.dumps(keep_urls, ensure_ascii=False, indent=4)};

        const allowedUrls = beginWithStar.concat(beginWithoutStar);  // concat 方法 gpt认为效率更高
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



# 记录结束时间
end_time = time.time()

# 计算并输出操作耗时
elapsed_time = end_time - start_time
print(f"操作完成，总耗时: {elapsed_time:.2f} 秒")

# 关闭浏览器
driver.quit()
