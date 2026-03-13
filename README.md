# Creator Digital Twin

> 个人创作数字分身系统 - 让每一篇创作都成为系统的燃料

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

Creator Digital Twin 是一个运行在 Claude Code / Codex / Gemini CLI 中的智能创作助手，帮助你：

- **追踪 AI 新闻** - 多源聚合、热度感知、智能推荐
- **学习你的风格** - 数据驱动、增量进化、偏好捕捉
- **策略化写作** - 小红书/公众号/X 平台适配、5-Pass 质量检查
- **闭环进化** - 发布复盘、爆款分析、策略迭代

## 核心功能

### 🧭 模式 A：新闻雷达 (Radar)
聚合 13+ AI 新闻源，智能去重、热度评分、三段式交互（简报→深度→创作）

### 💎 模式 B：资产捕捉与共创 (Asset)
灵感记录、实时修改捕捉、Diff 风格学习

### ✍️ 模式 C：平台策略写作 (Platform Writing)
小红书/公众号/X 三平台适配，5-Pass 质量检查，自动套用策略框架

### 🌊 模式 D：头脑风暴 (Brainstorming)
碎片整理、选题引导、灵魂随笔

### 📊 模式 E：风格学习 (Profiling)
数据加权风格建模、三层解析、去 AI 化改写验证

### 🔍 模式 G：对标拆解 (Benchmark)
逆向解剖外部内容、生成策略包、价值观冲突评分

### 🔄 模式 H：内容重塑 (Remodeling)
4:6 重构比、40% 个人资产强制注入、原创度预估

### 📈 模式 I：发布追踪与数据进化 (Analytics)
多平台 KPI 记录、爆款特征逆向、策略自动更新

## 快速开始

### 安装

```bash
# Claude Code
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git ~/.claude/skills/creator-digital-twin

# Codex
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git ~/.codex/skills/creator-digital-twin

# Gemini CLI
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git ~/.gemini/skills/creator-digital-twin
```

### 初始化

```bash
cd ~/.claude/skills/creator-digital-twin
python scripts/setup.py
```

或在 CLI 中：
```
/creator-digital-twin 初始化设置
```

## 目录结构

```
.creator-space/
├── system/               # 系统配置
│   ├── profile.json      # 核心人格档案
│   └── config.json       # 赛道偏好
├── persona/              # 人格档案
│   ├── voice_style.json  # 语气风格
│   └── do_dont_say.json  # 表达偏好
├── content/
│   ├── drafts/           # 草稿目录
│   └── published/        # 已发布
├── assets/
│   ├── ideas/            # 点子库
│   ├── concepts/         # 概念库
│   ├── quotes/           # 金句库
│   ├── cases/            # 案例库
│   └── strategies/       # 策略库
├── analytics/            # 数据分析
│   └── performance.jsonl # 发布表现
└── news_sources/         # 新闻数据
    └── daily/            # 每日情报
```

## 可选扩展

本 skill 核心功能独立运行，可与以下 skills 配合实现完整工作流：

### 核心功能（无需扩展）

所有 8 个模式均可独立使用，生成 Markdown 草稿后用户可手动发布：

| 模式 | 功能 | 输出 |
|------|------|------|
| A | AI 新闻雷达 | 新闻简报 |
| B | 资产捕捉 | 偏好更新 |
| C | 平台写作 | Markdown 草稿 |
| D | 头脑风暴 | 选题、灵感 |
| E | 风格学习 | 人格档案 |
| G | 对标拆解 | 策略文件 |
| H | 内容重塑 | 改写草稿 |
| I | 发布复盘 | 数据记录 |

### 扩展 Skills（自动化最后一步）

| Skill | 功能 | 安装后的增强 |
|-------|------|------------|
| `baoyu-xhs-images` | 小红书图片生成 | 自动生成图片提示词 |
| `xiaohongshu-publisher` | 小红书发布 | 一键发布到小红书 |
| `baoyu-cover-image` | 文章封面图 | 公众号/X 封面图 |
| `baoyu-post-to-wechat` | 公众号发布 | 一键发布到公众号 |

### 安装扩展 Skills

所有扩展 Skills 都在同一个仓库中：

```bash
# 克隆 baoyu-skills 仓库
cd ~/.claude/skills/
git clone https://github.com/JimLiu/baoyu-skills.git

# 安装后会包含以下 Skills：
# - baoyu-xhs-images      (小红书图片生成)
# - xiaohongshu-publisher (小红书发布)
# - baoyu-cover-image     (封面图生成)
# - baoyu-post-to-wechat  (公众号发布)
# - baoyu-image-gen       (通用图片生成)
# - baoyu-danger-gemini-web (Gemini 图片生成)
# - ... 等
```

或者单独安装需要的 Skill：

```bash
# 进入 skills 目录
cd ~/.claude/skills/

# 克隆仓库到临时目录
git clone https://github.com/JimLiu/baoyu-skills.git /tmp/baoyu-skills

# 只复制需要的 Skill
cp -r /tmp/baoyu-skills/baoyu-xhs-images ./
cp -r /tmp/baoyu-skills/xiaohongshu-publisher ./

# 清理
rm -rf /tmp/baoyu-skills
```

### 扩展 Skills 版本要求

扩展 Skills 需要修改以支持 `.creator-space/` 目录结构。

**安装后需要修改以下文件**（将 `.writing-style` 替换为 `.creator-space`）：

| Skill | 需修改的路径示例 |
|-------|----------------|
| baoyu-xhs-images | `--from-draft .creator-space/content/drafts/...` |
| xiaohongshu-publisher | `.creator-space/content/drafts/...` |
| baoyu-cover-image | `--from-draft .creator-space/content/drafts/...` |

**快速修改方法**：

```bash
# 进入扩展 Skills 目录
cd ~/.claude/skills/baoyu-skills

# 批量替换路径
sed -i 's/\.writing-style\/content\/drafts/\.creator-space\/content\/drafts/g' \
  baoyu-xhs-images/SKILL.md \
  xiaohongshu-publisher/SKILL.md \
  baoyu-cover-image/SKILL.md
```

或手动编辑三个 `SKILL.md` 文件，将所有 `.writing-style/content/drafts` 替换为 `.creator-space/content/drafts`。

### 工作流对比

**无扩展 Skills**：
```
模式 C 写作 → Markdown 草稿 → 用户手动复制发布 → 模式 I 手动记录数据
```

**有扩展 Skills**：
```
模式 C 写作 → 自动生成图片 → 一键发布 → 自动记录数据 → 模式 I 分析爆款
```

### 验证安装

在 Claude Code 中触发 Skill，查看环境检查结果：

```
/creator-digital-twin
```

输出示例：
```
✅ 环境检查通过

核心功能：全部可用
  ✅ 模式 A：AI 新闻雷达
  ✅ 模式 B：资产捕捉与纠正学习
  ...

可选扩展 Skills：
  ✅ baoyu-xhs-images      → 小红书图片生成（已安装）
  ✅ xiaohongshu-publisher → 小红书发布（已安装）
  ⚪ baoyu-cover-image     → 封面图生成（未安装）
  ⚪ baoyu-post-to-wechat  → 公众号发布（未安装）
```

## 新闻源配置

默认支持 13+ AI 新闻源，可在 `config/sources.json` 中自定义：

- TLDR AI
- Ben's Bites
- The Rundown AI
- The Neuron Daily
- One Useful Thing
- KDnuggets AI
- Hugging Face Papers
- 橘鸦AI早报
- ...

## 文档

- [安装指南](INSTALLATION.md)
- [模式详细文档](references/modes/)
- [质量检查规范](references/quality-control.md)
- [进化引擎原理](references/evolution-engine.md)

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

本项目灵感来源于对内容创作流程的深度思考，感谢所有开源社区的贡献者。
