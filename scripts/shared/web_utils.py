#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享的网页抓取工具

提供三层 Fallback 机制获取网页内容：
Layer 1: curl 直接获取
Layer 2: Jina AI Reader (https://r.jina.ai/)
Layer 3: 返回 None，由调用方处理
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


def fetch_with_jina(url):
    """
    使用 Jina AI Reader 获取网页内容
    将任意网页转换为干净的 Markdown 格式

    Jina AI Reader 是一个免费的网页内容提取服务，
    可以绕过常见的反爬机制，获取网页的纯文本内容。

    Args:
        url: 目标网页 URL

    Returns:
        str: Markdown 格式的内容，失败返回 None
    """
    jina_url = f"https://r.jina.ai/{url}"

    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", jina_url],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode == 0 and len(result.stdout) > 200:
            # 检查是否返回了有效内容（不是错误页面）
            content_lower = result.stdout.lower()[:200]
            if "error" not in content_lower and "not found" not in content_lower:
                return result.stdout
            else:
                print(f"  ⚠️  Jina Reader returned error", file=sys.stderr)
                return None
        else:
            print(f"  ⚠️  Jina Reader failed: content too short or curl error", file=sys.stderr)
            return None

    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Jina Reader timeout for {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ⚠️  Jina Reader error: {e}", file=sys.stderr)
        return None


def fetch_article_content(url):
    """
    获取文章内容的主入口函数
    实现三层 Fallback 机制：curl → Jina Reader → 返回 None

    Args:
        url: 目标文章 URL

    Returns:
        tuple: (content, source)
               - content: 文章内容字符串
               - source: 内容来源标识 ("curl" | "jina" | None)
    """
    # Layer 1: 尝试 curl
    print(f"  📄 尝试直接获取...", file=sys.stderr)
    content = fetch_html(url)
    if content and len(content) > 500:
        return content, "curl"

    # Layer 2: 尝试 Jina Reader
    print(f"  📄 尝试 Jina Reader...", file=sys.stderr)
    content = fetch_with_jina(url)
    if content and len(content) > 200:
        return content, "jina"

    # Layer 3: 失败
    print(f"  ⚠️  所有获取方式失败", file=sys.stderr)
    return None, None


def extract_links(html, pattern):
    """
    从HTML中提取匹配pattern的链接
    pattern: 正则表达式
    返回: 链接列表
    """
    import re
    return re.findall(pattern, html)
