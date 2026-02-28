#!/usr/bin/env python3
"""
Scott H Young 博客文章解析器
学习方法论、个人成长类内容
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_scotthyoung(source):
    """
    解析 Scott H Young 博客文章列表页面

    URL格式: https://www.scotthyoung.com/blog/articles/
    文章URL: https://www.scotthyoung.com/blog/YYYY/MM/DD/article-slug/
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # 匹配文章链接
    # 格式: <a href="https://www.scotthyoung.com/blog/2026/01/05/article-slug/">标题</a>
    pattern = r'<a[^>]+href="(https://www\.scotthyoung\.com/blog/\d{4}/\d{2}/\d{2}/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html, re.IGNORECASE)

    # 去重
    seen_urls = set()
    limit = source.get("limit", 10)

    for url, title in matches:
        title = title.strip()

        # 跳过太短的标题
        if len(title) < 5:
            continue

        if url not in seen_urls:
            seen_urls.add(url)
            articles.append({
                "url": url,
                "title": title,
                "summary": "Scott H Young - 学习方法论"
            })

            if len(articles) >= limit:
                break

    return articles
