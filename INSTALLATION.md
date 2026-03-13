# Creator Digital Twin 安装指南

## 概述

Creator Digital Twin 是一个个人创作数字分身系统，支持从小红书/公众号/X 的内容创作到发布的完整闭环。

---

## 快速开始

### 方式一：直接使用

将 skill 文件夹放入对应的 CLI skills 目录：

```bash
# Claude Code
~/.claude/skills/creator-digital-twin

# Codex
~/.codex/skills/creator-digital-twin

# Gemini CLI
~/.gemini/skills/creator-digital-twin
```

### 方式二：从 GitHub 克隆

```bash
cd ~/.claude/skills/
git clone https://github.com/<your-username>/creator-digital-twin.git
```

> 将 `<your-username>` 替换为你的 GitHub 用户名

---

## 初始化

```bash
cd creator-digital-twin
python scripts/setup.py
```

或在 CLI 中输入：
```
/creator-digital-twin 初始化设置
```

---

## 与其他 Skills 联动

本 skill 可与以下 skills 配合使用，实现完整工作流：

| Skill | 用途 | 调用命令 |
|-------|------|----------|
| `baoyu-xhs-images` | 小红书图片生成 | `/baoyu-xhs-images --from-draft {draft-path}` |
| `xiaohongshu-publisher` | 小红书发布 | `/xiaohongshu-publisher --from-draft {draft-path}` |
| `baoyu-cover-image` | 文章封面图 | `/baoyu-cover-image` |
| `baoyu-post-to-wechat` | 公众号发布 | `/baoyu-post-to-wechat` |

**完整工作流**：
```
模式 C 写作 → platforms/xiaohongshu.md
      ↓
/baoyu-xhs-images --from-draft {path} --prompt-only
      ↓
prompts/*.md → 手动生成图片 → images/*.png
      ↓
/xiaohongshu-publisher --from-draft {path}
```

---

## 目录结构

```
.creator-space/
├── system/               # 系统配置
│   ├── profile.json      # 核心人格档案
│   └── config.json       # 赛道偏好、关键词
├── persona/              # 人格档案
│   ├── voice_style.json  # 语气风格
│   └── do_dont_say.json  # 表达偏好
├── content/
│   ├── drafts/           # 草稿
│   └── published/        # 已发布
├── assets/
│   └── strategies/       # 策略库
└── analytics/            # 数据分析
```
