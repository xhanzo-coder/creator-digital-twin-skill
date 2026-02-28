#!/usr/bin/env python3
"""
Lex Fridman Podcast 解析器
RSS feed: https://lexfridman.com/feed/podcast/
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Lex Fridman - AI/科学/哲学深度对话
# ========================================

def parse_lexfridman(source):
    """
    解析 Lex Fridman Podcast RSS feed

    内容特点：
    - AI、科学、哲学、历史深度访谈
    - 嘉宾包括顶级研究者、创业者、思想家
    - 长篇对话（2-4小时）
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Lex Fridman Podcast RSS...", file=sys.stderr)
        xml_content = fetch_html("https://lexfridman.com/feed/podcast/")

        if not xml_content:
            print(f"  ⚠️  Lex Fridman RSS 获取失败", file=sys.stderr)
            return articles

        # 验证 XML
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  返回了非XML内容", file=sys.stderr)
            return articles

        # ========================================
        # 解析 Podcast RSS
        # ========================================

        # <item><title>...</title><link>...</link><description>...</description></item>
        item_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        items = re.findall(item_pattern, xml_content, re.DOTALL)

        limit = source.get("limit", 10)

        for title, link, description in items[:limit]:
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
            link = link.strip()

            # 提取嘉宾名字（通常格式："#123 – Guest Name: Topic"）
            guest_match = re.search(r'#\d+\s*[-–]\s*([^:]+)', title)
            if guest_match:
                guest = guest_match.group(1).strip()
                summary = f"Lex Fridman 对话 {guest}"
            else:
                summary = "Lex Fridman Podcast - AI/科学/哲学深度访谈"

            # 从描述中提取摘要（如果有）
            if description:
                desc_text = re.sub(r'<[^>]+>', '', description).strip()
                if len(desc_text) > 50:
                    summary = desc_text[:200]

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ Lex Fridman 发现 {len(articles)} 期节目", file=sys.stderr)
        else:
            print(f"  ⚠️  Lex Fridman 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Lex Fridman 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
