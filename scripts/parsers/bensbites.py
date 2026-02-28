#!/usr/bin/env python3
"""
Ben's Bites Newsletter 解析器
直接访问 RSS feed（无需 Playwright）
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Simple is better than complex
# ========================================

def parse_bensbites(source):
    """
    解析 Ben's Bites 的 RSS feed

    设计哲学：
    - RSS feed 本身可以直接访问，无需浏览器模拟
    - 简单的 curl 请求足以获取内容
    - 过度工程化（Playwright）是复杂度的源泉
    """
    articles = []

    try:
        # 导入 web_utils（已有的 curl 封装）
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        # 直接访问 RSS feed（简单有效）
        print("  访问 Ben's Bites RSS feed...", file=sys.stderr)
        xml_content = fetch_html("https://www.bensbites.com/feed")

        if not xml_content:
            print(f"  ⚠️  Ben's Bites feed 获取失败", file=sys.stderr)
            return articles

        # 验证是否为有效 XML
        if not xml_content.strip().startswith('<?xml'):
            print(f"  ⚠️  Ben's Bites 返回了非XML内容", file=sys.stderr)
            print(f"  调试：前100字符：{xml_content[:100]}", file=sys.stderr)
            return articles

        # ========================================
        # 解析 RSS/Atom feed
        # ========================================

        # 尝试 RSS 2.0 格式: <item><title>...</title><link>...</link></item>
        rss_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        rss_matches = re.findall(rss_pattern, xml_content, re.DOTALL)

        if rss_matches:
            # RSS 格式解析
            for title, link, description in rss_matches[:10]:
                # 清理 HTML 标签和实体
                title = re.sub(r'<[^>]+>', '', title).strip()
                title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
                link = link.strip()

                # 提取摘要
                if description:
                    summary = re.sub(r'<[^>]+>', '', description).strip()[:200]
                else:
                    summary = "Ben's Bites - AI 行业动态与创业洞察"

                articles.append({
                    "url": link,
                    "title": title,
                    "summary": summary
                })
        else:
            # 尝试 Atom 格式: <entry><title>...</title><link href="..."/></entry>
            atom_pattern = r'<entry>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link[^>]*href=["\']([^"\']+)["\'].*?(?:<summary>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>)?.*?</entry>'
            atom_matches = re.findall(atom_pattern, xml_content, re.DOTALL)

            for title, link, summary_text in atom_matches[:10]:
                title = re.sub(r'<[^>]+>', '', title).strip()
                title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
                link = link.strip()

                if summary_text:
                    summary = re.sub(r'<[^>]+>', '', summary_text).strip()[:200]
                else:
                    summary = "Ben's Bites - AI 行业动态与创业洞察"

                articles.append({
                    "url": link,
                    "title": title,
                    "summary": summary
                })

        if not articles:
            print(f"  ⚠️  Ben's Bites feed 解析失败，未找到文章", file=sys.stderr)
            print(f"  调试：feed 前500字符：{xml_content[:500]}", file=sys.stderr)
        else:
            print(f"  ✅ Ben's Bites 发现 {len(articles)} 篇文章", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Ben's Bites 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return articles

    return articles
