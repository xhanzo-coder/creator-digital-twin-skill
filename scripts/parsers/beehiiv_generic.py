#!/usr/bin/env python3
"""
Beehiiv Newsletter 平台解析器
支持 The Rundown AI, The Neuron Daily 等
"""

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

# ========================================
# ASCII: Beehiiv RSS Parser
# ========================================

def parse_beehiiv_rss(source):
    """
    通用 Beehiiv RSS 解析器

    Beehiiv RSS 格式：
    - Feed URL: https://rss.beehiiv.com/feeds/XXXXX.xml
    """
    articles = []

    # 获取配置
    rss_url = source.get("url", "")
    source_name = source.get("name", "Beehiiv Newsletter")
    limit = source.get("limit", 10)

    print(f"  访问 {source_name} RSS...", file=sys.stderr)
    xml_content = fetch_html(rss_url)

    if not xml_content:
        print(f"  ⚠️  {source_name} RSS 获取失败", file=sys.stderr)
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
                title = title_elem.text.strip() if title_elem.text else f"{source_name} Article"
                url = link_elem.text.strip() if link_elem.text else ""

                # 去除标题中的 emoji 前缀（beehiiv 常见格式）
                title = re.sub(r'^[^\w\s]{1,3}\s*', '', title).strip()

                # 提取摘要（去除 HTML 标签）
                summary = ""
                if desc_elem is not None and desc_elem.text:
                    summary = re.sub(r'<[^>]+>', '', desc_elem.text)[:200]

                # 提取发布日期
                published_at = None
                if pubdate_elem is not None and pubdate_elem.text:
                    try:
                        # RSS pubDate 格式: Wed, 05 Mar 2026 09:00:00 GMT
                        pub_dt = datetime.strptime(pubdate_elem.text.strip(), "%a, %d %b %Y %H:%M:%S %Z")
                        published_at = pub_dt.strftime("%Y-%m-%d")
                    except:
                        # 尝试其他格式
                        try:
                            pub_dt = datetime.strptime(pubdate_elem.text.strip(), "%a, %d %b %Y %H:%M:%S %z")
                            published_at = pub_dt.strftime("%Y-%m-%d")
                        except:
                            pass

                if url:
                    article = {
                        "url": url,
                        "title": title,
                        "summary": summary if summary else f"{source_name} 文章"
                    }
                    if published_at:
                        article["published_at"] = published_at
                    articles.append(article)

        if articles:
            print(f"  ✅ {source_name} 发现 {len(articles)} 篇文章", file=sys.stderr)
        else:
            print(f"  ⚠️  {source_name} 未发现新文章", file=sys.stderr)

    except ET.ParseError as e:
        print(f"  ⚠️  {source_name} XML 解析失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  {source_name} 解析错误: {e}", file=sys.stderr)

    return articles


# ========================================
# 特定 Beehiiv 解析器
# ========================================

def parse_therundown(source):
    """The Rundown AI - 每日AI新闻速递"""
    return parse_beehiiv_rss(source)

def parse_theneuron(source):
    """The Neuron Daily - AI新闻与洞察"""
    return parse_beehiiv_rss(source)
