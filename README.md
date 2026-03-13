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

## 触发词

| 模式 | 触发词示例 |
|------|-----------|
| A - 新闻雷达 | "今天有什么AI新闻"、"最近新闻"、"今天写什么" |
| B - 资产捕捉 | "记个点子"、"这是我改后的版本"、"这不对"、"我改一下" |
| C - 平台写作 | "写小红书"、"发公众号"、"写一篇"、"选X"（选择选题后） |
| D - 头脑风暴 | "理一下"、"头脑风暴"、"帮我整理想法" |
| E - 风格学习 | "学习我的风格"、"分析我的爆款" |
| G - 对标拆解 | "拆解这个博主"、"学习方法论"、"分析这篇文章" |
| H - 内容重塑 | "改写这篇文章"、"重塑这个内容" |
| I - 发布复盘 | "记录数据"、"复盘表现"、"更新发布数据" |

## 使用示例

### 示例 1：追踪 AI 新闻并创作

```
用户：今天有什么AI新闻？

分身：[运行新闻抓取脚本...]

     📰 今日AI新闻精选（2026-03-13）

     🔥 重磅新闻：
     1. 英伟达开源混合架构大模型 Nemotron 3 Super
     2. xAI 发布 Grok 4.20，支持 200 万 token 上下文
     ...

     你想深入了解哪条？或者选择一条进行创作？

用户：选2，写小红书

分身：好的，选择 Grok 4.20 进行创作。

     请选择创作角度：
     [A] 认知冲击型：200万token意味着什么？
     [B] 实用干货型：普通人如何利用长上下文
     [C] 行业观察型：xAI vs OpenAI 的新战场

     请选择目标平台：
     [ ] 小红书
     [ ] 公众号
     [ ] X/Twitter

     请选择内容风格：
     [A] 干货硬核
     [B] 轻松口语
     [C] 情绪表达

用户：[选择角度A，平台小红书，风格B]

分身：[生成 5-8 个标题供选择]

     请选择标题：
     1. Grok 4.20 发布：200万token意味着什么？ - 推荐 ✨
     2. 一次能读一本书？Grok 4.20 的 200 万 token 实测
     3. ...

用户：选1

分身：[生成内容并展示预览]

     标题：Grok 4.20 发布：200万token意味着什么？

     正文：
     ...

     内容是否满意？
     [满意，保存] [需要修改] [重新生成]

用户：满意，保存

分身：✅ 内容已保存
     草稿位置：.creator-space/content/drafts/2026-03-13-grok-420/

     下一步？
     [生成图片] [发布到小红书] [查看更多新闻]
```

### 示例 2：学习写作风格

```
用户：学习我的风格，这是我写的文章

用户：[粘贴文章内容]

分身：正在分析你的写作风格...

     📊 风格分析报告

     词汇偏好：
     - 高频使用："这个"、"其实"、"另外"
     - 避免使用："此外"、"综上所述"

     句式特点：
     - 短句为主（平均 15 字/句）
     - 喜欢用反问句开头

     情绪曲线：
     - 开头：轻快引入
     - 中段：逐步升温
     - 结尾：情绪高点 + 行动号召

     是否确认学习这些偏好？

用户：确认

分身：✅ 风格档案已更新
     已写入：.creator-space/persona/voice_style.json
     已更新：.creator-space/persona/do_dont_say.json
```

### 示例 3：纠正学习

```
分身：[生成的内容...]
     AI技术正在深刻地改变我们的生活方式...

用户：这不对，我不用"深刻地"这种词，太书面了

分身：收到纠正！正在学习...

     📝 偏好学习报告

     发现问题：
     - 原文："AI技术正在深刻地改变我们的生活方式"
     - 问题：使用书面化副词"深刻地"

     学习到的偏好：
     - ✅ 避免"深刻地"、"极大地"等书面副词
     - ✅ 偏好口语化表达："正在改变"、"彻底改变"

     是否更新偏好档案？

用户：是的

分身：✅ 已更新 .creator-space/persona/do_dont_say.json
     添加到 dont 列表：["深刻地", "极大地", "显著地"]
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

| Skill | 功能 | 安装方式 |
|-------|------|----------|
| `baoyu-xhs-images` | 小红书图片生成 | 见下方安装说明 |
| `xiaohongshu-publisher` | 小红书发布 | 独立仓库 |
| `baoyu-cover-image` | 文章封面图 | 见下方安装说明 |
| `baoyu-post-to-wechat` | 公众号发布 | 见下方安装说明 |

### 安装扩展 Skills

**baoyu-skills 仓库**（包含 baoyu-xhs-images、baoyu-cover-image、baoyu-post-to-wechat）：

```bash
cd ~/.claude/skills/
git clone https://github.com/JimLiu/baoyu-skills.git

# 包含的 Skills：
# - baoyu-xhs-images       (小红书图片生成)
# - baoyu-cover-image      (封面图生成)
# - baoyu-post-to-wechat   (公众号发布)
# - baoyu-image-gen        (通用图片生成)
# - baoyu-danger-gemini-web (Gemini 图片生成)
```

**xiaohongshu-publisher**（小红书发布，独立仓库）：

```bash
cd ~/.claude/skills/
# 请参考该 skill 的官方仓库获取安装方式
```

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
  ⚪ xiaohongshu-publisher → 小红书发布（未安装）
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

## 常见问题

### Q: 新闻抓取失败怎么办？

A: 检查以下几点：
1. 确保网络可以访问新闻源（部分源可能需要代理）
2. 运行 `python scripts/setup.py --upgrade` 更新配置
3. 查看 `news_sources/state.json` 中的 `last_fetch_time` 确认抓取状态

### Q: 如何添加新的新闻源？

A: 编辑 `config/sources.json`，添加新源配置：

```json
{
  "id": "my-new-source",
  "name": "我的新闻源",
  "url": "https://example.com/rss",
  "parser": "rss_generic",
  "enabled": true
}
```

### Q: 风格学习需要多少文章？

A:
- 最少 1 篇即可开始学习
- 推荐 3-5 篇获得较准确的风格画像
- 10 篇以上可以获得成熟的个人风格

### Q: 为什么模式 C 没有让我选择平台？

A: 模式 C 的正确流程是：
1. 选择创作角度
2. **选择目标平台**（必问）
3. 选择内容风格
4. 选择标题
5. 确认内容

如果跳过了平台选择，可能是模型没有正确遵循流程。请重新触发或明确说"我要写小红书"。

### Q: 如何备份数据？

A: 备份 `.creator-space/` 目录即可：

```bash
# 备份
cp -r ~/.creator-space ~/creator-space-backup-$(date +%Y%m%d)

# 恢复
cp -r ~/creator-space-backup-YYYYMMDD ~/.creator-space
```

## 文档

- [安装指南](INSTALLATION.md)
- [模式详细文档](references/modes/)
- [质量检查规范](references/quality-control.md)
- [进化引擎原理](references/evolution-engine.md)

## 更新日志

### v1.0 (2026-03)
- 8 个核心模式完整实现
- 新闻数据 v2 架构（seen_urls/read_urls 分离）
- 模式 C 流程强化（三问必答、标题选择、内容确认）
- 扩展 Skills 集成支持

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

本项目灵感来源于对内容创作流程的深度思考，感谢所有开源社区的贡献者。
