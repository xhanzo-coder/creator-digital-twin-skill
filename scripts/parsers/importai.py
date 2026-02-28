#!/usr/bin/env python3
"""
Import AI Newsletter 解析器
使用 Substack RSS feed
"""

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_importai(source):
    """
    解析 Import AI 的 RSS feed
    """
    articles = []

    # Substack RSS feed URL
    rss_url = "https://importai.substack.com/feed"
    xml_content = fetch_html(rss_url)

    if not xml_content:
        return articles

    try:
        # 解析 XML
        root = ET.fromstring(xml_content)

        # RSS 格式: <rss><channel><item>...
        items = root.findall('.//item')

        for item in items[:10]:  # 取最新 10 篇
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')

            if title_elem is not None and link_elem is not None:
                title = title_elem.text.strip() if title_elem.text else "Import AI Article"
                url = link_elem.text.strip() if link_elem.text else ""

                # 提取摘要（去除 HTML 标签）
                summary = ""
                if desc_elem is not None and desc_elem.text:
                    # 简单去除 HTML 标签，取前 200 字符
                    summary = re.sub(r'<[^>]+>', '', desc_elem.text)[:200]

                if url:
                    articles.append({
                        "url": url,
                        "title": title,
                        "summary": summary if summary else "AI 政策、研究与应用的深度分析"
                    })

    except ET.ParseError as e:
        print(f"  ⚠️  XML 解析失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  Import AI 解析错误: {e}", file=sys.stderr)

    return articles
