#!/usr/bin/env python3
"""
Readwise Wise Newsletter 解析器
精选阅读推荐
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_readwise(source):
    """
    解析 Readwise Wise Newsletter 列表页面

    URL格式: https://wise.readwise.io/
    文章URL: https://wise.readwise.io/issues/wisereads-vol-###/
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # 匹配 newsletter 链接
    # 格式: <a href="https://wise.readwise.io/issues/wisereads-vol-123/">标题</a>
    # 或相对路径: <a href="/issues/wisereads-vol-123/">标题</a>
    pattern = r'<a[^>]+href="((?:https://wise\.readwise\.io)?/issues/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html, re.IGNORECASE)

    # 去重
    seen_urls = set()
    limit = source.get("limit", 10)

    for url, title in matches:
        title = title.strip()

        # 跳过太短的标题
        if len(title) < 10:
            continue

        # 确保完整URL
        if not url.startswith('http'):
            url = f"https://wise.readwise.io{url}"

        if url not in seen_urls:
            seen_urls.add(url)
            articles.append({
                "url": url,
                "title": title,
                "summary": "Readwise Wise - 精选阅读"
            })

            if len(articles) >= limit:
                break

    return articles
