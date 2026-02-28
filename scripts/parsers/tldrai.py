#!/usr/bin/env python3
"""
TLDR AI Newsletter 解析器
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_tldrai(source):
    """
    解析 TLDR AI 的最新一期 newsletter
    """
    articles = []

    # TLDR AI 有个 /api/latest/ai 端点返回最新一期
    html = fetch_html("https://tldr.tech/api/latest/ai")
    if not html:
        return articles

    try:
        # 提取文章标题和链接
        # 格式：<a class="font-bold" href="URL" target="_blank" rel="noopener noreferrer"><h3>TITLE</h3></a>

        # 方法1：提取 Headlines & Launches 部分
        headlines_match = re.search(r'Headlines &amp; Launches</h3></header>(.*?)</section>', html, re.DOTALL)
        if headlines_match:
            section = headlines_match.group(1)
            pattern = r'<a class="font-bold" href="([^"]+)"[^>]*><h3>([^<]+)</h3></a>'
            matches = re.findall(pattern, section)

            for url, title in matches[:5]:  # 取前5条头条
                # 清理 HTML 实体
                title = title.replace('&amp;', '&').replace('&#x27;', "'")
                articles.append({
                    "url": url,
                    "title": title,
                    "summary": "TLDR AI 每日速览"
                })

        # 方法2：提取 Engineering & Research 部分
        research_match = re.search(r'Engineering &amp; Research</h3></header>(.*?)</section>', html, re.DOTALL)
        if research_match:
            section = research_match.group(1)
            pattern = r'<a class="font-bold" href="([^"]+)"[^>]*><h3>([^<]+)</h3></a>'
            matches = re.findall(pattern, section)

            for url, title in matches[:3]:  # 取前3条研究
                title = title.replace('&amp;', '&').replace('&#x27;', "'")
                articles.append({
                    "url": url,
                    "title": title,
                    "summary": "AI 工程与研究"
                })

        # 如果上面两种方法都失败，用通用方法抓所有文章链接
        if not articles:
            pattern = r'<a class="font-bold" href="([^"]+?)"[^>]*?target="_blank"[^>]*?><h3>([^<]+)</h3></a>'
            all_matches = re.findall(pattern, html)

            for url, title in all_matches[:10]:
                # 过滤广告和赞助内容
                if 'utm_source=tldr' in url or 'Sponsor' in title:
                    continue

                title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
                articles.append({
                    "url": url,
                    "title": title,
                    "summary": "TLDR AI 文章"
                })

    except Exception as e:
        print(f"  ⚠️  TLDR AI 解析错误: {e}", file=sys.stderr)

    return articles
