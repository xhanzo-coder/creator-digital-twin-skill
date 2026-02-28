#!/usr/bin/env python3
"""
HackerNoon 频道文章解析器
支持 life-hacking, writing, product-management 等频道
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_hackernoon(source):
    """
    解析 HackerNoon 频道页面，提取最新文章

    支持的URL格式：
    - https://hackernoon.com/c/life-hacking
    - https://hackernoon.com/c/writing
    - https://hackernoon.com/c/product-management
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # HackerNoon 页面结构：
    # 文章链接格式: <a href="/article-slug">标题</a>
    # 文章URL模式: /xxx-xxx-xxx (不含 /c/ /u/ /company/ 等路径)

    # 提取所有文章链接 - 匹配 href 指向文章的链接
    # 文章链接特征：以 / 开头，不含特殊路径前缀，包含多个单词用连字符连接
    pattern = r'<a[^>]+href="(/[a-z0-9][a-z0-9-]+-[a-z0-9-]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html, re.IGNORECASE)

    # 去重（同一文章可能在页面上出现多次）
    seen_urls = set()
    limit = source.get("limit", 10)

    for url_path, title in matches:
        # 跳过非文章链接
        if any(x in url_path for x in ['/c/', '/u/', '/company/', '/tagged/', '/signup', '/login', '/feed']):
            continue

        # 跳过太短的标题（可能是按钮或导航）
        title = title.strip()
        if len(title) < 10:
            continue

        full_url = f"https://hackernoon.com{url_path}"

        if full_url not in seen_urls:
            seen_urls.add(full_url)
            articles.append({
                "url": full_url,
                "title": title,
                "summary": f"HackerNoon - {source.get('name', 'article')}"
            })

            if len(articles) >= limit:
                break

    return articles
