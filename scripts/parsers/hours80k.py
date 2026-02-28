#!/usr/bin/env python3
"""
80,000 Hours Podcast 解析器
RSS feed: https://feeds.transistor.fm/80000-hours-podcast
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: 80,000 Hours - 有效利他主义与职业选择
# ========================================

def parse_hours80k(source):
    """
    解析 80,000 Hours Podcast RSS feed

    内容特点：
    - 有效利他主义（Effective Altruism）
    - 职业选择与社会影响
    - AI 安全、全球优先事项
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 80,000 Hours Podcast RSS...", file=sys.stderr)
        xml_content = fetch_html("https://feeds.transistor.fm/80000-hours-podcast")

        if not xml_content:
            print(f"  ⚠️  80,000 Hours RSS 获取失败", file=sys.stderr)
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
                summary = "80,000 Hours - 有效利他主义与职业影响力"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ 80,000 Hours 发现 {len(articles)} 期节目", file=sys.stderr)
        else:
            print(f"  ⚠️  80,000 Hours 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ 80,000 Hours 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
