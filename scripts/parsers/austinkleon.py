#!/usr/bin/env python3
"""
Austin Kleon Substack 解析器
RSS feed: https://austinkleon.substack.com/feed
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Austin Kleon - 创意与艺术实践
# ========================================

def parse_austinkleon(source):
    """
    解析 Austin Kleon 的 Substack newsletter

    内容特点：
    - 创意写作与艺术实践
    - "Steal Like an Artist" 作者
    - 创作过程与生活洞察
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Austin Kleon Substack RSS...", file=sys.stderr)
        xml_content = fetch_html("https://austinkleon.substack.com/feed")

        if not xml_content:
            print(f"  ⚠️  Austin Kleon RSS 获取失败", file=sys.stderr)
            return articles

        # 验证 XML 格式
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  返回了非XML内容", file=sys.stderr)
            return articles

        # ========================================
        # 解析 RSS/Atom (Substack 使用 Atom)
        # ========================================

        # 先尝试 Atom 格式
        atom_pattern = r'<entry>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link[^>]*href=["\']([^"\']+)["\'].*?(?:<summary>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>)?.*?</entry>'
        items = re.findall(atom_pattern, xml_content, re.DOTALL)

        if not items:
            # 回退到 RSS 2.0
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
                summary = "Austin Kleon - 创意实践与艺术洞察"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ Austin Kleon 发现 {len(articles)} 篇文章", file=sys.stderr)
        else:
            print(f"  ⚠️  Austin Kleon 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Austin Kleon 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
