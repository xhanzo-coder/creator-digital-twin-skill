#!/usr/bin/env python3
"""
Wait But Why 博客解析器
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_waitbutwhy(source):
    """
    解析Wait But Why博客首页
    """
    articles = []

    html = fetch_html(source["url"])
    if not html:
        return articles

    # Wait But Why的文章链接通常是 /yyyy/mm/article-title 格式
    pattern = r'href="(https://waitbutwhy\.com/\d{4}/\d{2}/[^"]+)"'
    matches = re.findall(pattern, html)

    seen = set()
    for url in matches[:15]:
        if url in seen:
            continue
        seen.add(url)

        # 从URL提取标题
        title_match = re.search(r'/([^/]+)$', url)
        if title_match:
            title = title_match.group(1).replace('-', ' ').title()
        else:
            title = "Wait But Why Article"

        articles.append({
            "url": url,
            "title": title,
            "summary": "深度长文，探讨科技、人生、社会等话题"
        })

        if len(articles) >= 5:  # WBW更新较慢，只取最近5篇
            break

    return articles
