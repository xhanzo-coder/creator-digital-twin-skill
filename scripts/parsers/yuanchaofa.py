#!/usr/bin/env python3
"""
袁超发技术博客解析器
RSS feed: https://yuanchaofa.com/rss.xml
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: 袁超发 - LLM/AI 技术深度博客
# ========================================

def parse_yuanchaofa(source):
    """
    解析袁超发博客的 RSS feed

    内容特点：
    - 深度技术文章（LLM、AI、工程实践）
    - 月度总结与思考
    - 高质量中文技术内容
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问袁超发博客 RSS...", file=sys.stderr)
        xml_content = fetch_html("https://yuanchaofa.com/rss.xml")

        if not xml_content:
            print(f"  ⚠️  袁超发博客 RSS 获取失败", file=sys.stderr)
            return articles

        # 验证 XML 格式
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  返回了非XML内容", file=sys.stderr)
            return articles

        # ========================================
        # 解析 RSS 2.0
        # ========================================

        # <item><title>...</title><link>...</link><description>...</description></item>
        item_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        items = re.findall(item_pattern, xml_content, re.DOTALL)

        limit = source.get("limit", 10)

        for title, link, description in items[:limit]:
            # 清理 HTML 和实体
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
            link = link.strip()

            # 提取摘要
            if description:
                summary = re.sub(r'<[^>]+>', '', description).strip()[:200]
            else:
                summary = "袁超发 - LLM/AI 技术深度文章"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ 袁超发博客发现 {len(articles)} 篇文章", file=sys.stderr)
        else:
            print(f"  ⚠️  袁超发博客解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ 袁超发博客抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
