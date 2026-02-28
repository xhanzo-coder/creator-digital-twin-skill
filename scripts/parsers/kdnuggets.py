#!/usr/bin/env python3
"""
KDnuggets 标签页文章解析器
支持 AI、机器学习等标签页面
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_kdnuggets(source):
    """
    解析 KDnuggets 标签页面，提取最新文章

    支持的URL格式：
    - https://www.kdnuggets.com/tag/artificial-intelligence
    - https://www.kdnuggets.com/tag/machine-learning
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # KDnuggets 页面结构：
    # <li> 包含文章链接和标题
    # 文章URL格式: /年/月/文章名.html 或 /文章名

    # 匹配文章链接 - KDnuggets 文章URL通常包含年份或直接是文章slug
    # 格式: <a href="/2026/01/article-name.html">标题</a>
    # 或: <a href="/article-name">标题</a>
    pattern = r'<a[^>]+href="(https://www\.kdnuggets\.com/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html, re.IGNORECASE)

    # 备用模式：相对路径
    if not matches:
        pattern = r'<a[^>]+href="(/\d{4}/\d{2}/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html, re.IGNORECASE)
        matches = [(f"https://www.kdnuggets.com{url}", title) for url, title in matches]

    # 再次备用：匹配任何内部文章链接
    if not matches:
        pattern = r'<a[^>]+href="(/[a-z0-9-]+(?:\.html)?)"[^>]*>([^<]{15,})</a>'
        matches = re.findall(pattern, html, re.IGNORECASE)
        matches = [(f"https://www.kdnuggets.com{url}", title) for url, title in matches]

    # 去重和过滤
    seen_urls = set()
    limit = source.get("limit", 10)

    for url, title in matches:
        # 跳过非文章链接
        if any(x in url.lower() for x in ['/tag/', '/tags/', '/author/', '/about', '/contact', '/newsletter', '/advertise', 'privacy', 'terms', '/recommends', '/kdnuggets-']):
            continue

        # 跳过太短的标题（可能是导航链接）
        title = title.strip()
        if len(title) < 20:
            continue

        # 跳过纯导航词
        nav_words = ['data engineering', 'machine learning', 'recommendations', 'artificial intelligence', 'deep learning', 'python', 'r programming']
        if title.lower() in nav_words:
            continue

        # 确保是完整URL
        if not url.startswith('http'):
            url = f"https://www.kdnuggets.com{url}"

        if url not in seen_urls:
            seen_urls.add(url)
            articles.append({
                "url": url,
                "title": title,
                "summary": "KDnuggets AI"
            })

            if len(articles) >= limit:
                break

    return articles
