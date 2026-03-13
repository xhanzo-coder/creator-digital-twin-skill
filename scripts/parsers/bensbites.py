#!/usr/bin/env python3
"""
Ben's Bites Newsletter 解析器
直接访问 RSS feed（无需 Playwright）
"""

import re
import sys
from pathlib import Path
from datetime import datetime

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

        # 尝试 RSS 2.0 格式: <item><title>...</title><link>...</link><pubDate>...</pubDate></item>
        rss_pattern = r'<item>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?(?:<pubDate>(.*?)</pubDate>)?.*?(?:<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>)?.*?</item>'
        rss_matches = re.findall(rss_pattern, xml_content, re.DOTALL)

        if rss_matches:
            # RSS 格式解析
            for title, link, pubdate, description in rss_matches[:10]:
                # 清理 HTML 标签和实体
                title = re.sub(r'<[^>]+>', '', title).strip()
                title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
                link = link.strip()

                # 提取摘要
                if description:
                    summary = re.sub(r'<[^>]+>', '', description).strip()[:200]
                else:
                    summary = "Ben's Bites - AI 行业动态与创业洞察"

                # 提取发布日期
                published_at = None
                if pubdate:
                    try:
                        # RSS pubDate 格式: Wed, 05 Mar 2026 09:00:00 GMT
                        pubdate = pubdate.strip()
                        # 尝试多种格式
                        for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]:
                            try:
                                pub_dt = datetime.strptime(pubdate, fmt)
                                published_at = pub_dt.strftime("%Y-%m-%d")
                                break
                            except:
                                continue
                    except:
                        pass

                article = {
                    "url": link,
                    "title": title,
                    "summary": summary
                }
                if published_at:
                    article["published_at"] = published_at
                articles.append(article)
        else:
            # 尝试 Atom 格式: <entry><title>...</title><link href="..."/><published>...</published></entry>
            atom_pattern = r'<entry>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link[^>]*href=["\']([^"\']+)["\'].*?(?:<published>(.*?)</published>)?.*?(?:<summary>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>)?.*?</entry>'
            atom_matches = re.findall(atom_pattern, xml_content, re.DOTALL)

            for title, link, published, summary_text in atom_matches[:10]:
                title = re.sub(r'<[^>]+>', '', title).strip()
                title = title.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"')
                link = link.strip()

                if summary_text:
                    summary = re.sub(r'<[^>]+>', '', summary_text).strip()[:200]
                else:
                    summary = "Ben's Bites - AI 行业动态与创业洞察"

                # 提取发布日期
                published_at = None
                if published:
                    try:
                        # ISO 8601 格式: 2026-03-05T09:00:00Z
                        published = published.strip()
                        pub_dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        published_at = pub_dt.strftime("%Y-%m-%d")
                    except:
                        pass

                article = {
                    "url": link,
                    "title": title,
                    "summary": summary
                }
                if published_at:
                    article["published_at"] = published_at
                articles.append(article)

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
