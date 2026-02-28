#!/usr/bin/env python3
"""
Farnam Street Brain Food 解析器
RSS feed: https://fs.blog/feed/
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Brain Food - 认知与决策思维
# ========================================

def parse_brainfood(source):
    """
    解析 Farnam Street Brain Food newsletter

    内容特点：
    - 认知科学、心理学、决策理论
    - 周更 newsletter（225+ 期）
    - 深度思考与智慧洞察
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Brain Food RSS...", file=sys.stderr)
        xml_content = fetch_html("https://fs.blog/feed/")

        if not xml_content:
            print(f"  ⚠️  Brain Food RSS 获取失败", file=sys.stderr)
            return articles

        # 验证 XML 格式
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  返回了非XML内容", file=sys.stderr)
            return articles

        # ========================================
        # 解析 RSS 2.0 / WordPress feed
        # ========================================

        # WordPress通常用 CDATA 包裹内容
        item_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        items = re.findall(item_pattern, xml_content, re.DOTALL)

        limit = source.get("limit", 10)

        for title, link, description in items[:limit]:
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')

            # 提取期数（如果有）
            edition_match = re.search(r'Brain Food #(\d+)', title)
            if edition_match:
                edition = edition_match.group(1)
                # 保留期数信息
                if not title.startswith('Brain Food'):
                    title = f"Brain Food #{edition}: {title}"

            link = link.strip()

            # 提取摘要
            if description:
                summary = re.sub(r'<[^>]+>', '', description).strip()[:200]
            else:
                summary = "Farnam Street - 认知决策与智慧洞察"

            articles.append({
                "url": link,
                "title": title,
                "summary": summary
            })

        if articles:
            print(f"  ✅ Brain Food 发现 {len(articles)} 篇文章", file=sys.stderr)
        else:
            print(f"  ⚠️  Brain Food 解析失败", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Brain Food 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
