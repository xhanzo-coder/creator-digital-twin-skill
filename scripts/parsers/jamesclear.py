#!/usr/bin/env python3
"""
James Clear 3-2-1 Newsletter 解析器
从归档页面提取最新的newsletter链接
"""

import re
import sys
from pathlib import Path

# 添加shared目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html, extract_links

def parse_jamesclear(source):
    """
    解析James Clear的newsletter归档页
    返回格式: [{"url": str, "title": str, "summary": str}]
    """
    articles = []

    # 获取页面HTML
    html = fetch_html(source["url"])
    if not html:
        return articles

    # James Clear的归档页结构：
    # - 每个newsletter是一个链接，格式为 /3-2-1/month-day-year
    # - 标题通常在链接文本或附近的文本中

    # 提取所有 /3-2-1/ 开头的链接
    pattern = r'href="(/3-2-1/[^"]+)"'
    matches = re.findall(pattern, html)

    # 去重并限制数量（最近10期）
    seen = set()
    for match in matches[:20]:  # 多抓一些，后面会去重
        if match in seen:
            continue
        seen.add(match)

        full_url = f"https://jamesclear.com{match}"

        # 从URL中提取日期作为标题的一部分
        date_match = re.search(r'/3-2-1/([^/]+)$', match)
        if date_match:
            date_str = date_match.group(1)
            title = f"3-2-1: {date_str}"
        else:
            title = f"3-2-1 Newsletter"

        articles.append({
            "url": full_url,
            "title": title,
            "summary": "James Clear每周newsletter：3个想法，2句引用，1个问题"
        })

        if len(articles) >= 10:
            break

    return articles
