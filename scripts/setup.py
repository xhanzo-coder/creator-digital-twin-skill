#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creator Digital Twin 初始化脚本

功能：
1. 创建数据目录结构
2. 初始化配置文件
3. 首次运行引导

使用方法：
  python scripts/setup.py              # 完整初始化
  python scripts/setup.py --init       # 仅初始化目录
  python scripts/setup.py --upgrade    # 升级（保留现有数据）
"""

import os
import json
import sys

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path

# ============================================================
# 目录结构配置
# ============================================================

STRUCTURE = [
    ".creator-space/system",
    ".creator-space/memory",
    ".creator-space/persona",
    ".creator-space/content/drafts",
    ".creator-space/content/published",
    ".creator-space/content/repurpose",
    ".creator-space/content/calendar",
    ".creator-space/content/metadata",
    ".creator-space/assets/ideas",
    ".creator-space/assets/concepts",
    ".creator-space/assets/quotes",
    ".creator-space/assets/cases",
    ".creator-space/assets/strategies",
    ".creator-space/analytics/reviews",
    ".creator-space/news_sources/daily",
    ".creator-space/news_sources/archive",
    ".creator-space/platform_rules"
]

# ============================================================
# 默认配置文件
# ============================================================

DEFAULT_FILES = {
    ".creator-space/system/profile.json": {
        "initialized": False,
        "version": "1.0",
        "created_at": "",
        "last_updated": "",
        "basic_info": {
            "user_id": "",
            "writing_field": "",
            "target_audience_profile": []
        },
        "writing_style": {
            "tone": "",
            "vocabulary": {
                "preferred_words": [],
                "avoided_words": []
            }
        },
        "statistics": {
            "articles_analyzed": 0,
            "learning_sessions": 0
        }
    },
    ".creator-space/system/config.json": {
        "priorities": [],
        "interests": [],
        "platforms": ["xiaohongshu", "wechat", "x"],
        "keywords": []
    },
    ".creator-space/persona/voice_style.json": {
        "tone": "default",
        "cadence": "mixed",
        "filler_words": []
    },
    ".creator-space/persona/do_dont_say.json": {
        "do": [],
        "dont": []
    },
    ".creator-space/persona/stance_topics.json": {
        "topics": []
    },
    ".creator-space/persona/tone_by_scene.json": {
        "scenes": {}
    },
    ".creator-space/memory/beliefs.json": {
        "beliefs": []
    },
    ".creator-space/memory/stories.jsonl": "",
    ".creator-space/memory/timeline.jsonl": "",
    ".creator-space/news_sources/state.json": {
        "seen_urls": {},
        "read_urls": {},
        "last_check_time": "",
        "last_fetch_time": ""
    },
    ".creator-space/analytics/performance.jsonl": "",
    ".creator-space/analytics/reviews.jsonl": "",
    ".creator-space/assets/strategies/README.md": """# 策略库

存放从爆款内容中提取的写作框架。

## 如何使用

模式 C（平台写作）会自动读取此目录下的策略文件。

## 如何添加新策略

1. 使用模式 G（对标拆解）分析外部内容
2. 系统会自动生成策略文件存入此目录
3. 或手动创建策略文件

## 策略文件格式

参见 `dontbesilent.md` 示例。
""",
    ".creator-space/platform_rules/xiaohongshu.json": {
        "platform": "Xiaohongshu",
        "rules": {
            "title": {
                "length": "不超过20字符",
                "style": [
                    "成果公式：[时间][成果], [工具]做[事]",
                    "痛点公式：为什么你的[X]总是[问题]？",
                    "认知冲击：[数字]%的人都理解错了[X]"
                ]
            },
            "content": {
                "max_length": 1000,
                "paragraph_style": "每段不超过2行，段间空行",
                "emoji_usage": "15-25%，强化关键信息"
            }
        }
    }
}

# ============================================================
# 初始化函数
# ============================================================

def init_directories():
    """创建目录结构"""
    print("\n📁 创建目录结构...")
    for folder in STRUCTURE:
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}")

def init_files():
    """初始化配置文件"""
    print("\n📝 初始化配置文件...")
    for file_path, content in DEFAULT_FILES.items():
        path = Path(file_path)
        if path.exists():
            print(f"  ⏭️  已存在: {file_path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                if isinstance(content, dict):
                    json.dump(content, f, indent=2, ensure_ascii=False)
                else:
                    f.write(content)
            print(f"  ✅ 已创建: {file_path}")

def upgrade_files():
    """升级配置文件（保留现有数据）"""
    print("\n🔄 升级配置文件...")
    for file_path, default_content in DEFAULT_FILES.items():
        path = Path(file_path)
        if not path.exists():
            # 文件不存在，创建新文件
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                if isinstance(default_content, dict):
                    json.dump(default_content, f, indent=2, ensure_ascii=False)
                else:
                    f.write(default_content)
            print(f"  ✅ 新建: {file_path}")
        else:
            # 文件存在，检查是否需要合并新字段
            if isinstance(default_content, dict):
                with open(path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)

                # 合并缺失的字段
                updated = False
                for key, value in default_content.items():
                    if key not in existing:
                        existing[key] = value
                        updated = True

                if updated:
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(existing, f, indent=2, ensure_ascii=False)
                    print(f"  ✅ 升级: {file_path}")
                else:
                    print(f"  ⏭️  无需更新: {file_path}")

def check_initialization():
    """检查是否已初始化"""
    profile_path = Path(".creator-space/system/profile.json")
    if profile_path.exists():
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)
            return profile.get("initialized", False)
    return False

def set_initialized():
    """标记为已初始化"""
    from datetime import datetime
    profile_path = Path(".creator-space/system/profile.json")
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    profile["initialized"] = True
    profile["last_updated"] = datetime.now().isoformat()
    if not profile.get("created_at"):
        profile["created_at"] = datetime.now().isoformat()

    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print("\n✅ 已标记为已初始化")

# ============================================================
# 主函数
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Creator Digital Twin 初始化脚本")
    parser.add_argument("--init", action="store_true", help="仅初始化目录")
    parser.add_argument("--upgrade", action="store_true", help="升级（保留现有数据）")
    args = parser.parse_args()

    print("=" * 60)
    print("🚀 Creator Digital Twin 初始化脚本")
    print("=" * 60)

    # 初始化模式
    if args.init:
        init_directories()
        init_files()
        print("\n✨ 目录初始化完成！")
        return

    # 升级模式
    if args.upgrade:
        init_directories()
        upgrade_files()
        print("\n✨ 升级完成！")
        return

    # 完整初始化
    init_directories()
    init_files()

    # 检查初始化状态
    is_initialized = check_initialization()

    print("\n" + "=" * 60)
    print("✨ 初始化完成！")
    print("=" * 60)

    if not is_initialized:
        print("""
🎯 下一步：

1. 首次运行引导（推荐）：
   在 Claude Code 中输入：/creator-digital-twin 初始化设置

2. 或手动编辑配置文件：
   - .creator-space/system/profile.json（基本信息）
   - .creator-space/persona/do_dont_say.json（表达偏好）
   - .creator-space/platform_rules/xiaohongshu.json（平台规则）

3. 运行模式 E 学习你的写作风格：
   /creator-digital-twin 学习我的风格
""")
    else:
        print("\n✅ 系统已初始化，可以直接使用")

if __name__ == "__main__":
    main()
