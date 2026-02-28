#!/usr/bin/env python3
"""
通用 Substack 解析器
支持所有 Substack 博客的 RSS 订阅
"""

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

# ========================================
# ASCII: Generic Substack RSS Parser
# ========================================

def parse_substack_rss(source):
    """
    通用 Substack RSS 解析器

    使用方法：
    - 在 sources.json 中配置 url 为 substack 地址
    - 自动转换为 RSS feed URL
    """
    articles = []

    # 获取配置
    base_url = source.get("url", "")
    source_name = source.get("name", "Substack")
    limit = source.get("limit", 10)

    # 构建 RSS URL
    # https://xxx.substack.com/ -> https://xxx.substack.com/feed
    if base_url.endswith('/'):
        rss_url = base_url + "feed"
    else:
        rss_url = base_url + "/feed"

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

            if title_elem is not None and link_elem is not None:
                title = title_elem.text.strip() if title_elem.text else f"{source_name} Article"
                url = link_elem.text.strip() if link_elem.text else ""

                # 提取摘要（去除 HTML 标签）
                summary = ""
                if desc_elem is not None and desc_elem.text:
                    summary = re.sub(r'<[^>]+>', '', desc_elem.text)[:200]

                if url:
                    articles.append({
                        "url": url,
                        "title": title,
                        "summary": summary if summary else f"{source_name} 文章"
                    })

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
# 特定 Substack 解析器工厂
# ========================================

def parse_dcthemedian(source):
    """DC The Median - 数据科学与AI应用"""
    return parse_substack_rss(source)

def parse_markmcneilly(source):
    """Mark McNeilly - 战略与领导力"""
    return parse_substack_rss(source)

def parse_businessanalytics(source):
    """Business Analytics - 商业分析与数据驱动"""
    return parse_substack_rss(source)

def parse_aileadershipedge(source):
    """AI Leadership Edge - AI领导力洞察"""
    return parse_substack_rss(source)

def parse_chinai(source):
    """ChinAI - 中国AI发展追踪"""
    return parse_substack_rss(source)

def parse_memia(source):
    """Memia (Ben Reid) - AI与商业创新"""
    return parse_substack_rss(source)

def parse_ai2roi(source):
    """AI to ROI - AI落地与商业回报"""
    return parse_substack_rss(source)

def parse_natesnewsletter(source):
    """Nate's Newsletter - AI技术与趋势"""
    return parse_substack_rss(source)

def parse_aichangeseverything(source):
    """AI Changes Everything - AI变革洞察"""
    return parse_substack_rss(source)
