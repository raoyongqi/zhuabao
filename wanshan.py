import os
import re

# 存储所有唯一的 hosts URL
unique_hosts = set()

# 获取目录中所有的文件
folder_path = 'data'  # 替换为您文件夹的路径
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # 确保我们只处理 JS 文件
    if os.path.isfile(file_path) and file_path.endswith('.js'):
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            js_content = file.read()

        # 使用正则表达式匹配 'const hosts = [...]' 数组内容
        match = re.search(r'const\s+hosts\s*=\s*\[([^\]]*)\];', js_content)
        
        # 如果匹配成功
        if match:
            # 提取数组中的 URL
            urls = re.findall(r'"([^"]+)"', match.group(1))
            
            # 将 URL 添加到集合中，自动去重
            unique_hosts.update(urls)
unique_hosts
# 打印去重后并排序的 URL 列表
print(sorted_hosts)
