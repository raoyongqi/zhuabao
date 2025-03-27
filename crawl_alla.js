const links = document.querySelectorAll('a');

const hrefs = Array.from(links).map(link => link.href);

const hosts = new Set();
hrefs.forEach(href => {
    try {
   const url = new URL(href);
        hosts.add(url.host);
    } catch (error) {
        // 忽略无法解析的 href
    }
});

const hostArray = Array.from(hosts);

// 将 JSON 数据格式化为一行一个，并包含双引号
const jsonData = JSON.stringify(hostArray, null, 2);

const blob = new Blob([`const hosts = ${jsonData};`], { type: 'application/javascript' });

const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'hosts.js';
document.body.appendChild(a);
a.click(); // 模拟点击下载链接
document.body.removeChild(a);
URL.revokeObjectURL(url); 