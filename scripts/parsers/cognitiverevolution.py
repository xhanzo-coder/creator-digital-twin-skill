#!/usr/bin/env python3
"""
Cognitive Revolution Podcast 解析器
RSS feed: https://feeds.megaphone.fm/RINTP3108857801
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Cognitive Revolution - AI前沿技术与应用
# ========================================

def parse_cognitiverevolution(source):
    """
    解析 Cognitive Revolution Podcast RSS feed

    内容特点：
    - AI 前沿技术深度解析
    - AI 应用案例与创业故事
    - 技术趋势与产业洞察
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Cognitive Revolution RSS...", file=sys.stderr)
        xml_content = fetch_html("https://feeds.megaphone.fm/RINTP3108857801")

        if not xml_content:
            print(f"  ⚠️  Cognitive Revolution RSS 获取失败", file=sys.stderr)
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
                summary = "Cognitive Revolution - AI 前沿技术与应用洞察"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ Cognitive Revolution 发现 {len(articles)} 期节目", file=sys.stderr)
        else:
            print(f"  ⚠️  Cognitive Revolution 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Cognitive Revolution 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
