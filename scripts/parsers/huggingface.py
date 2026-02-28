#!/usr/bin/env python3
"""
Hugging Face Daily Papers 解析器
使用官方API获取论文列表和votes信息
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from web_utils import fetch_html

def parse_huggingface(source):
    """
    解析 Hugging Face Daily Papers

    使用API: https://huggingface.co/api/daily_papers
    包含完整的论文信息和upvotes数据
    """
    articles = []
    min_votes = source.get("min_votes", 0)
    limit = source.get("limit", 15)

    # 使用API而不是HTML
    api_url = "https://huggingface.co/api/daily_papers"

    try:
        # fetch_html也可以用来获取JSON
        response = fetch_html(api_url)
        if not response:
            print(f"  ⚠️  无法获取Hugging Face API响应", file=sys.stderr)
            return articles

        papers = json.loads(response)

        for item in papers:
            if not isinstance(item, dict):
                continue

            paper = item.get('paper', {})
            if not paper:
                continue

            paper_id = paper.get('id', '')
            title = paper.get('title', 'Untitled')
            upvotes = paper.get('upvotes', 0) or 0

            # 根据 min_votes 过滤
            if upvotes < min_votes:
                continue

            url = f"https://huggingface.co/papers/{paper_id}" if paper_id else ""
            if not url:
                continue

            articles.append({
                "url": url,
                "title": title,
                "summary": f"Hugging Face 社区热门论文 ({upvotes} votes)"
            })

            # 达到limit数量后停止
            if len(articles) >= limit:
                break

        # 如果设置了min_votes但没有找到符合条件的论文，输出提示
        if min_votes > 0 and len(articles) == 0:
            print(f"  ℹ️  未找到{min_votes}+ votes的论文，可能今天的论文都比较新", file=sys.stderr)

    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON 解析失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  Hugging Face API 错误: {e}", file=sys.stderr)

    return articles
