import os

import re



url_result = set()  # 使用集合来去重

with open('newbackground.js','r', encoding='utf-8') as file:
    js_content = file.read()

# 使用正则表达式匹配 'const allowedUrls = [' 后的数组内容
match = re.search(r'const\s+allowedUrls\s*=\s*\[([^\]]*)\];', js_content)

if match:
    # 提取数组中的 URL 并按 URL 长度排序
    url_result = set(re.findall(r'"([^"]+)"', match.group(1)))
    


error_set = set()
with open('error_urls.txt', 'r') as file:
    for line in file:
        # 去掉行末的换行符并将每行添加到集合中
        error_set.add(line.strip())

# 打开文件并逐行读取
overlap = url_result.intersection(error_set)

if overlap:
    print("重叠元素:", overlap)
else:
    print("没有重叠元素")



url_result = url_result-overlap 

sorted_urls = sorted(url_result, key=len)
import json
js_content_new = f"""
const allowedUrls = {json.dumps(sorted_urls, ensure_ascii=False, indent=4)};
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
with open('newbackground_m.js', 'w', encoding='utf-8') as js_file:
    js_file.write(js_content_new)

print("Combined and de-duplicated hosts saved to newbackground_m.js")

