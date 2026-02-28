#!/usr/bin/env python3
"""
Paul Graham Essays 解析器
HTML 列表: https://paulgraham.com/articles.html
"""

import re
import sys
from pathlib import Path

# ========================================
# ASCII: Paul Graham - 创业与黑客文化
# ========================================

def parse_paulgraham(source):
    """
    解析 Paul Graham 的文章列表页

    内容特点：
    - 创业哲学与黑客文化
    - Y Combinator 创始人
    - 经典长文（How to Do Great Work等）
    - 简单HTML结构，无RSS
    """
    articles = []

    try:
        SCRIPT_DIR = Path(__file__).parent.parent
        sys.path.insert(0, str(SCRIPT_DIR / "shared"))
        from web_utils import fetch_html

        print("  访问 Paul Graham 文章列表...", file=sys.stderr)
        html = fetch_html("https://paulgraham.com/articles.html")

        if not html:
            print(f"  ⚠️  Paul Graham 页面获取失败", file=sys.stderr)
            return articles

        # ========================================
        # 解析 HTML 链接
        # 模式: <a href="filename.html">Title</a>
        # ========================================

        # 提取所有文章链接
        link_pattern = r'<a\s+href=["\']([^"\']+\.html)["\'][^>]*>([^<]+)</a>'
        matches = re.findall(link_pattern, html, re.IGNORECASE)

        # 过滤掉导航链接（index.html 等）
        excluded = {'index.html', 'articles.html', 'bio.html', 'faq.html'}

        limit = source.get("limit", 15)
        count = 0

        for filename, title in matches:
            # 跳过导航链接和图片
            if filename.lower() in excluded or filename.startswith('http'):
                continue

            # 清理标题
            title = title.strip()
            if not title or len(title) < 3:  # 过滤太短的标题
                continue

            # 构造完整URL
            url = f"https://paulgraham.com/{filename}"

            articles.append({
                "url": url,
                "title": title,
                "summary": "Paul Graham - 创业哲学与黑客文化"
            })

            count += 1
            if count >= limit:
                break

        if articles:
            print(f"  ✅ Paul Graham 发现 {len(articles)} 篇文章", file=sys.stderr)
        else:
            print(f"  ⚠️  Paul Graham 解析失败", file=sys.stderr)
            # 调试：打印前500字符
            print(f"  调试：HTML 前500字符：{html[:500]}", file=sys.stderr)

    except Exception as e:
        print(f"  ❌ Paul Graham 抓取失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

    return articles
