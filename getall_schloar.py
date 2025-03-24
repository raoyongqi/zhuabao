import os
import json

# 指定文件夹路径
folder_path = 'folder'  # 替换为你的文件夹路径

# 存储不重复的 href 值
unique_hrefs = set()

# 获取文件夹中的所有 JSON 文件
json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

# 遍历所有 JSON 文件并读取它们
for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)  # 获取文件的完整路径
    try:
        # 打开并读取每个 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 解析 JSON 数据为 Python 对象
            print(f"Contents of {json_file}:")

            # 遍历 JSON 数据并提取 href 值
            for item in data:
                if 'href' in item:  # 确保有 href 字段
                    unique_hrefs.add(item['href'])  # 将 href 加入 set 中，自动去重

    except Exception as e:
        print(f"无法读取文件 {json_file}，错误：{e}")

# 将不重复的 href 值保存到 txt 文件
with open('unique_hrefs.txt', 'w', encoding='utf-8') as output_file:
    for href in unique_hrefs:
        output_file.write(href + '\n')  # 将每个 href 值写入文件，换行分隔

print("所有不重复的 href 已成功保存到 unique_hrefs.txt")