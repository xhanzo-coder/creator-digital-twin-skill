#!/usr/bin/env python3
"""
Hacker News 首页热门文章解析器
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_hackernews(source):
    """
    解析Hacker News首页，提取前N条热门文章
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # HN的HTML结构：
    # <tr class="athing" id="...">
    #   <td class="title">
    #     <span class="titleline">
    #       <a href="...">标题</a>

    # 提取所有文章链接和标题
    # 使用正则匹配 titleline 中的链接
    pattern = r'<span class="titleline"><a href="([^"]+)">([^<]+)</a>'
    matches = re.findall(pattern, html)

    limit = source.get("limit", 30)

    for i, (url, title) in enumerate(matches[:limit]):
        # HN的链接可能是相对路径，需要处理
        if url.startswith("item?id="):
            url = f"https://news.ycombinator.com/{url}"
        elif not url.startswith("http"):
            url = f"https://news.ycombinator.com/{url}"

        articles.append({
            "url": url,
            "title": title.strip(),
            "summary": f"HN排名#{i+1}"
        })

    return articles
