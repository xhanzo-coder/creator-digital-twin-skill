#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
橘鸦AI早报解析器
https://imjuya.github.io/juya-ai-daily/rss.xml
中文AI行业动态与开发者早报
"""

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html


def parse_juya(source):
    """
    解析橘鸦AI早报的RSS feed

    RSS格式特点：
    - 标题为日期格式：2026-03-05
    - 内容为当日AI新闻汇总，分类清晰（要闻、模型发布、开发生态等）
    - 中文内容，适合国内用户
    """
    articles = []

    rss_url = source.get("url", "https://imjuya.github.io/juya-ai-daily/rss.xml")
    limit = source.get("limit", 10)

    print(f"  访问橘鸦AI早报 RSS...", file=sys.stderr)
    xml_content = fetch_html(rss_url)

    if not xml_content:
        print(f"  ⚠️  橘鸦AI早报 RSS 获取失败", file=sys.stderr)
        return articles

    try:
        # 解析 XML
        root = ET.fromstring(xml_content)

        # RSS 格式: <rss><channel><item>...
        items = root.findall('.//item')

        for item in items[:limit]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')
            pubdate_elem = item.find('pubDate')

            if title_elem is not None and link_elem is not None:
                # 标题是日期格式，如 "2026-03-05"
                date_str = title_elem.text.strip() if title_elem.text else ""
                url = link_elem.text.strip() if link_elem.text else ""

                # 提取发布日期
                published_at = None
                if pubdate_elem is not None and pubdate_elem.text:
                    # RSS pubDate 格式: Thu, 05 Mar 2026 01:23:18 +0000
                    try:
                        pub_dt = datetime.strptime(pubdate_elem.text.strip(), "%a, %d %b %Y %H:%M:%S %z")
                        published_at = pub_dt.strftime("%Y-%m-%d")
                    except:
                        pass

                # 如果没有 pubDate，从标题提取日期
                if not published_at and date_str:
                    try:
                        # 标题格式: "2026-03-05"
                        datetime.strptime(date_str, "%Y-%m-%d")
                        published_at = date_str
                    except:
                        pass

                # 从 description 提取摘要
                summary = ""
                if desc_elem is not None and desc_elem.text:
                    desc_text = desc_elem.text

                    # 尝试提取"概览"后的要闻
                    overview_match = re.search(r'概览.*?要闻.*?(?:<li>|)(.*?)(?:</li>|$)', desc_text, re.DOTALL)
                    if overview_match:
                        summary = re.sub(r'<[^>]+>', '', overview_match.group(1))[:200]
                    else:
                        # 直接取前200字符
                        summary = re.sub(r'<[^>]+>', '', desc_text)[:200]

                    summary = summary.strip()

                # 构建完整标题
                full_title = f"橘鸦AI早报 {date_str}" if date_str else "橘鸦AI早报"

                if url:
                    article = {
                        "url": url,
                        "title": full_title,
                        "summary": summary if summary else "中文AI行业动态与开发者早报"
                    }
                    # 添加发布日期
                    if published_at:
                        article["published_at"] = published_at

                    articles.append(article)

        if articles:
            print(f"  ✅ 橘鸦AI早报发现 {len(articles)} 期", file=sys.stderr)
        else:
            print(f"  ⚠️  橘鸦AI早报未发现新内容", file=sys.stderr)

    except ET.ParseError as e:
        print(f"  ⚠️  橘鸦AI早报 XML 解析失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  橘鸦AI早报解析错误: {e}", file=sys.stderr)

    return articles
