#!/usr/bin/env python3
"""
Product Hunt 解析器
提取昨天的top产品
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_producthunt(source):
    """
    解析Product Hunt，获取昨天的top产品
    """
    articles = []

    # Product Hunt有按日期归档的页面
    # 格式: https://www.producthunt.com/leaderboard/daily/YYYY/MM/DD
    yesterday = datetime.now() - timedelta(days=1)
    date_url = yesterday.strftime("%Y/%m/%d")
    url = f"https://www.producthunt.com/leaderboard/daily/{date_url}"

    html = fetch_html(url)
    if not html:
        # 如果昨天的页面不存在，尝试首页
        html = fetch_html(source["url"])
        if not html:
            return articles

    # Product Hunt的产品链接格式：/posts/product-name
    pattern = r'href="(/posts/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)

    seen = set()
    limit = source.get("limit", 10)

    for i, (path, title) in enumerate(matches[:limit]):
        full_url = f"https://www.producthunt.com{path}"

        if full_url in seen:
            continue
        seen.add(full_url)

        articles.append({
            "url": full_url,
            "title": title.strip(),
            "summary": f"Product Hunt昨日#{i+1}"
        })

    return articles
