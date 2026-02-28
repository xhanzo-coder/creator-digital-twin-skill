#!/usr/bin/env python3
"""
One Useful Thing 解析器 (Ethan Mollick's Substack)
关于 AI 在工作、教育和生活中的应用
"""

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_oneusefulthing(source):
    """
    解析 One Useful Thing 的 RSS feed
    """
    articles = []

    # Substack RSS feed URL
    rss_url = source.get("url", "https://www.oneusefulthing.org/feed")
    xml_content = fetch_html(rss_url)

    if not xml_content:
        return articles

    try:
        # 解析 XML
        root = ET.fromstring(xml_content)

        # RSS 格式: <rss><channel><item>...
        items = root.findall('.//item')
        limit = source.get("limit", 10)

        for item in items[:limit]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')

            if title_elem is not None and link_elem is not None:
                title = title_elem.text.strip() if title_elem.text else "One Useful Thing Article"
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
                        "summary": summary if summary else "Ethan Mollick 关于 AI 应用的深度思考"
                    })

    except ET.ParseError as e:
        print(f"  ⚠️  XML 解析失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  One Useful Thing 解析错误: {e}", file=sys.stderr)

    return articles
