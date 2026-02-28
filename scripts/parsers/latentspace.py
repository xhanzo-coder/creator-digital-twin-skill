#!/usr/bin/env python3
"""
Latent Space Podcast 解析器
RSS feed: https://rss.flightcast.com/vgnxzgiwwzwke85ym53fjnzu.xml
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Latent Space - AI工程师与创业者访谈
# ========================================

def parse_latentspace(source):
    """
    解析 Latent Space Podcast RSS feed

    内容特点：
    - AI 工程实践与产品开发
    - AI 创业公司故事
    - 技术栈选择与架构设计
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Latent Space Podcast RSS...", file=sys.stderr)
        xml_content = fetch_html("https://www.latent.space/feed")

        if not xml_content:
            print(f"  ⚠️  Latent Space RSS 获取失败", file=sys.stderr)
            return articles

        # 验证 XML
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  返回了非XML内容", file=sys.stderr)
            return articles

        # ========================================
        # 解析 Podcast RSS
        # ========================================

        item_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        items = re.findall(item_pattern, xml_content, re.DOTALL)

        limit = source.get("limit", 10)

        for title, link, description in items[:limit]:
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
            link = link.strip()

            # 提取摘要
            if description:
                summary = re.sub(r'<[^>]+>', '', description).strip()[:200]
            else:
                summary = "Latent Space - AI 工程实践与创业洞察"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ Latent Space 发现 {len(articles)} 期节目", file=sys.stderr)
        else:
            print(f"  ⚠️  Latent Space 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Latent Space 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
