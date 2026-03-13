#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻抓取器
从配置的多个AI新闻源抓取最新内容

v2 更新：
- 区分 seen_urls（抓取去重）和 read_urls（用户已阅读）
- 保存新闻时保留 published_at 字段
- 支持按发布日期组织数据
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
import hashlib
from collections import defaultdict

# Windows编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加parsers目录到路径
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR / "parsers"))

# 导入所有parsers
from bensbites import parse_bensbites
from tldrai import parse_tldrai
from importai import parse_importai
from huggingface import parse_huggingface
from hackernews import parse_hackernews
from producthunt import parse_producthunt
from beehiiv_generic import parse_therundown, parse_theneuron
from oneusefulthing import parse_oneusefulthing
from kdnuggets import parse_kdnuggets
from juya import parse_juya

# 解析器映射
PARSERS = {
    "bensbites": parse_bensbites,
    "tldrai": parse_tldrai,
    "importai": parse_importai,
    "huggingface": parse_huggingface,
    "hackernews": parse_hackernews,
    "producthunt": parse_producthunt,
    "therundown": parse_therundown,
    "theneuron": parse_theneuron,
    "oneusefulthing": parse_oneusefulthing,
    "kdnuggets": parse_kdnuggets,
    "juya": parse_juya,
}


def resolve_data_root() -> Path:
    """定位项目级 .creator-space 目录，优先当前工作目录及其父级"""
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        data_dir = candidate / ".creator-space"
        if data_dir.exists():
            return data_dir
    return current / ".creator-space"


DATA_ROOT = resolve_data_root()

def url_hash(url: str) -> str:
    """生成URL的短hash用于快速查重"""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def load_sources_config():
    """加载新闻源配置"""
    config_file = SKILL_DIR / "config" / "sources.json"
    if not config_file.exists():
        return {"sources": []}

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_filters():
    """加载过滤配置"""
    filters_file = SKILL_DIR / "config" / "filters.json"
    if not filters_file.exists():
        return {"blacklist": {"keywords": []}, "whitelist": {"keywords": []}}

    with open(filters_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_state():
    """加载状态（包含抓取去重和阅读记录）"""
    state_dir = DATA_ROOT / "news_sources"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "state.json"

    if not state_file.exists():
        return {
            "seen_urls": {},      # 抓取去重：url_hash -> {url, title, first_seen, published_at}
            "read_urls": {}       # 阅读记录：url_hash -> {url, title, read_at, published_at}
        }

    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
        # 兼容旧版本
        if "seen_urls" not in state:
            state["seen_urls"] = {}
        if "read_urls" not in state:
            state["read_urls"] = {}
        # 迁移旧版本的 shown_news_hashes
        if "shown_news_hashes" in state and "seen_urls" not in state:
            state["seen_urls"] = {h: {"url": "", "title": "", "first_seen": "", "published_at": ""} for h in state["shown_news_hashes"]}
            del state["shown_news_hashes"]
        return state

def save_state(state):
    """保存状态"""
    state_dir = DATA_ROOT / "news_sources"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "state.json"

    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_daily_news(date_str):
    """加载指定日期的新闻数据"""
    daily_dir = DATA_ROOT / "news_sources" / "daily"
    daily_file = daily_dir / f"{date_str}.json"
    if daily_file.exists():
        with open(daily_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_news_by_publish_date(items, state):
    """按发布日期保存新闻（而不是抓取日期）"""
    if not items:
        return {}

    daily_dir = DATA_ROOT / "news_sources" / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)

    # 按发布日期分组
    by_date = defaultdict(list)
    today = datetime.now().strftime("%Y-%m-%d")

    for item in items:
        # 优先使用 published_at，其次使用 fetched_at 的日期，最后用今天
        pub_date = item.get('published_at')
        if not pub_date:
            fetched = item.get('fetched_at', '')
            if fetched:
                pub_date = fetched[:10]  # 取日期部分
            else:
                pub_date = today

        by_date[pub_date].append(item)

    saved_files = {}
    for date_str, date_items in by_date.items():
        # 加载已有数据（追加模式）
        output_file = daily_dir / f"{date_str}.json"
        existing_items = []

        if output_file.exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_items = existing_data.get('items', [])
            except:
                pass

        # 合并并去重
        existing_urls = {item.get('url_hash') for item in existing_items}
        new_items = [item for item in date_items if item.get('url_hash') not in existing_urls]

        if new_items or existing_items:
            all_items = existing_items + new_items
            output_data = {
                "date": date_str,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "total_items": len(all_items),
                "items": all_items
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            saved_files[date_str] = len(new_items)
            print(f"  📅 {date_str}: {len(new_items)} 篇新文章")

    return saved_files

def apply_keyword_filter(items, filters):
    """应用关键词黑白名单过滤"""
    blacklist = [kw.lower() for kw in filters.get("blacklist", {}).get("keywords", [])]
    whitelist = [kw.lower() for kw in filters.get("whitelist", {}).get("keywords", [])]

    filtered = []
    for item in items:
        title_lower = item['title'].lower()

        # 检查黑名单
        if any(kw in title_lower for kw in blacklist):
            continue

        # 检查白名单（如果有白名单）
        if whitelist:
            if not any(kw in title_lower for kw in whitelist):
                continue

        filtered.append(item)

    return filtered

def fetch_from_source(source):
    """从单个源抓取内容"""
    parser_name = source.get('parser')
    if not parser_name or parser_name not in PARSERS:
        print(f"⚠️  未找到 {source['name']} 的解析器")
        return []

    try:
        parser = PARSERS[parser_name]
        items = parser(source)

        # 添加元数据
        for item in items:
            item['source_name'] = source['name']
            item['source_id'] = source['id']
            item['url_hash'] = url_hash(item['url'])
            item['fetched_at'] = datetime.now(timezone.utc).isoformat()
            # published_at 已由 parser 提供，保留

        return items
    except Exception as e:
        print(f"❌ {source['name']} 抓取失败: {e}")
        return []

def get_unread_stats(state):
    """获取未读新闻统计"""
    seen = set(state.get('seen_urls', {}).keys())
    read = set(state.get('read_urls', {}).keys())
    unread_count = len(seen - read)
    return unread_count

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📰 AI新闻抓取器 v2")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    # 加载配置
    sources_config = load_sources_config()
    filters = load_filters()
    state = load_state()

    # 抓取所有enabled的源
    all_items = []
    enabled_sources = [s for s in sources_config['sources'] if s.get('enabled', False)]

    print(f"🔍 开始抓取 {len(enabled_sources)} 个新闻源...")
    print()

    for source in enabled_sources:
        print(f"  抓取 {source['name']}...", end=" ")
        items = fetch_from_source(source)

        # URL去重（只检查是否已抓取过，不检查是否已阅读）
        new_items = []
        for item in items:
            url_h = item['url_hash']
            if url_h not in state['seen_urls']:
                new_items.append(item)
                state['seen_urls'][url_h] = {
                    'url': item['url'],
                    'title': item['title'],
                    'first_seen': datetime.now(timezone.utc).isoformat(),
                    'published_at': item.get('published_at', '')
                }

        all_items.extend(new_items)
        print(f"✅ {len(new_items)} 篇新文章")

    print()
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 抓取统计")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"总计抓取：{len(all_items)} 篇新文章")

    # 关键词过滤
    filtered_items = apply_keyword_filter(all_items, filters)
    print(f"关键词过滤后：{len(filtered_items)} 篇")

    # 按发布日期保存
    if filtered_items:
        print()
        print("📅 按发布日期保存：")
        saved_files = save_news_by_publish_date(filtered_items, state)
        print()
        print(f"✅ 已保存到 {len(saved_files)} 个日期文件")
    else:
        # 即使没有新内容也要更新时间戳
        pass

    # 保存state（更新时间戳）
    state['last_fetch_time'] = datetime.now(timezone.utc).isoformat()
    state['last_check_time'] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    # 显示未读统计
    unread_count = get_unread_stats(state)
    total_seen = len(state.get('seen_urls', {}))
    total_read = len(state.get('read_urls', {}))

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📈 数据统计")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"已抓取新闻：{total_seen} 篇")
    print(f"已阅读新闻：{total_read} 篇")
    print(f"未读新闻：{unread_count} 篇")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 下一步：AI智能过滤")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("⚡ Claude 需要执行：")
    print("   1. 读取 daily/YYYY-MM-DD.json（根据用户请求的日期范围）")
    print("   2. 过滤掉 read_urls 中已阅读的新闻")
    print("   3. 根据 config/user_interests.json 过滤无关内容")
    print("   4. 生成推荐列表（翻译标题 + 打分排序）")
    print()

if __name__ == "__main__":
    main()
