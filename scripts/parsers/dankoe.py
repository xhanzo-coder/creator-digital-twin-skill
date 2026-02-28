#!/usr/bin/env python3
"""
Dan Koe Letters 解析器
从归档页面提取最新的文章链接
https://thedankoe.com/letters/
"""

import re
import sys
from pathlib import Path

# 添加shared目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_dankoe(source):
    """
    解析Dan Koe的letters归档页
    返回格式: [{"url": str, "title": str, "summary": str}]
    """
    articles = []

    # 获取页面HTML
    html = fetch_html(source["url"])
    if not html:
        return articles

    # Dan Koe的归档页结构：
    # <h4><a href="https://thedankoe.com/letters/xxx">Title</a></h4>
    # 提取所有文章链接和标题
    pattern = r'<h4[^>]*>\s*<a\s+href="(https://thedankoe\.com/letters/[^"]+)"[^>]*>([^<]+)</a>\s*</h4>'
    matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)

    # 限制数量
    limit = source.get("limit", 10)
    seen = set()

    for url, title in matches:
        if url in seen:
            continue
        seen.add(url)

        # 清理标题
        title = title.strip()
        title = re.sub(r'\s+', ' ', title)  # 合并多余空格
        # 处理HTML实体
        title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
        title = title.replace('&#8217;', "'").replace('&#8216;', "'")
        title = title.replace('&#8220;', '"').replace('&#8221;', '"')

        articles.append({
            "url": url,
            "title": title,
            "summary": "Dan Koe - 个人成长与创业智慧"
        })

        if len(articles) >= limit:
            break

    return articles
