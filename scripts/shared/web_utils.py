#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享的网页抓取工具
"""

import subprocess
import sys

def fetch_html(url):
    """
    使用curl获取HTML内容
    返回HTML字符串，失败返回None
    """
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='ignore'  # Windows编码修复：忽略无法解码的字符
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"  ⚠️  curl failed: {result.stderr}", file=sys.stderr)
            return None

    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Timeout fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ⚠️  Error fetching {url}: {e}", file=sys.stderr)
        return None

def extract_links(html, pattern):
    """
    从HTML中提取匹配pattern的链接
    pattern: 正则表达式
    返回: 链接列表
    """
    import re
    return re.findall(pattern, html)
