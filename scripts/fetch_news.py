#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻抓取器
从配置的多个AI新闻源抓取最新内容
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
import hashlib

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
}


def resolve_data_root() -> Path:
    """定位项目级 .writing-style 目录，优先当前工作目录及其父级"""
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        data_dir = candidate / ".writing-style"
        if data_dir.exists():
            return data_dir
    return current / ".writing-style"


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
    """加载URL去重状态"""
    state_dir = DATA_ROOT / "news_sources"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "state.json"
    
    if not state_file.exists():
        return {"seen_urls": {}}
    
    with open(state_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_state(state):
    """保存URL去重状态"""
    state_dir = DATA_ROOT / "news_sources"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "state.json"
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

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
        
        return items
    except Exception as e:
        print(f"❌ {source['name']} 抓取失败: {e}")
        return []

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📰 AI新闻抓取器")
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
        
        # URL去重
        new_items = []
        for item in items:
            if item['url_hash'] not in state['seen_urls']:
                new_items.append(item)
                state['seen_urls'][item['url_hash']] = {
                    'url': item['url'],
                    'title': item['title'],
                    'first_seen': datetime.now(timezone.utc).isoformat()
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
    
    # 保存
    if filtered_items:
        # 保存到daily目录
        output_dir = DATA_ROOT / "news_sources" / "daily"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = output_dir / f"{today}.json"
        
        output_data = {
            "date": today,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "total_items": len(filtered_items),
            "items": filtered_items
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 保存到：{output_file}")
    
    # 保存state
    save_state(state)
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 下一步：AI智能过滤")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print(f"📂 数据文件：{output_file}")
    print(f"📄 待处理：{len(filtered_items)} 篇文章")
    print()
    print("⚡ Claude 需要执行：")
    print("   1. 读取上述JSON文件")
    print("   2. 根据 config/user_interests.json 过滤无关内容")
    print("   3. 生成推荐列表（翻译标题 + 打分排序）")
    print()

if __name__ == "__main__":
    main()
