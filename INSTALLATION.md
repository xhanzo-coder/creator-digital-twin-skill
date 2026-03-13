# Creator Digital Twin 安装指南

## 概述

Creator Digital Twin 是一个个人创作数字分身系统，支持从小红书/公众号/X 的内容创作到发布的完整闭环。

---

## 安装方式

### 方式一：从 GitHub 克隆（推荐）

```bash
# Claude Code
cd ~/.claude/skills/
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git creator-digital-twin

# Codex
cd ~/.codex/skills/
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git creator-digital-twin

# Gemini CLI
cd ~/.gemini/skills/
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git creator-digital-twin
```

### 方式二：手动安装

1. 下载或克隆仓库到本地
2. 将 `creator-digital-twin` 文件夹放入对应 CLI 的 skills 目录：

```bash
# Claude Code
~/.claude/skills/creator-digital-twin

# Codex
~/.codex/skills/creator-digital-twin

# Gemini CLI
~/.gemini/skills/creator-digital-twin
```

### 方式三：项目级安装

如果只想在特定项目中使用，可以安装在项目目录下：

```bash
# 在项目根目录
cd your-project/
mkdir -p .claude/skills/
git clone https://github.com/xhanzo-coder/creator-digital-twin-skill.git .claude/skills/creator-digital-twin
```

---

## 初始化

安装后需要进行初始化，创建必要的数据目录：

### 方法一：运行初始化脚本

```bash
cd ~/.claude/skills/creator-digital-twin
python scripts/setup.py
```

### 方法二：在 CLI 中初始化

```
/creator-digital-twin 初始化设置
```

初始化会创建以下目录结构：

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

---

## 安装扩展 Skills（可选）

本 skill 核心功能可独立运行，安装扩展 Skills 可实现自动化发布：

### baoyu-skills（小红书图片、封面图、公众号发布）

```bash
cd ~/.claude/skills/
git clone https://github.com/JimLiu/baoyu-skills.git

# 包含：
# - baoyu-xhs-images       (小红书图片生成)
# - baoyu-cover-image      (封面图生成)
# - baoyu-post-to-wechat   (公众号发布)
# - baoyu-image-gen        (通用图片生成)
```

### xiaohongshu-publisher（小红书发布）

```bash
# 请参考该 skill 的官方仓库获取安装方式
```

---

## 验证安装

在 Claude Code 中输入：

```
/creator-digital-twin
```

如果安装成功，会显示环境检查结果：

```
✅ 环境检查通过

核心功能：全部可用
  ✅ 模式 A：AI 新闻雷达
  ✅ 模式 B：资产捕捉与纠正学习
  ...

可选扩展 Skills：
  ✅ baoyu-xhs-images      → 小红书图片生成（已安装）
  ⚪ xiaohongshu-publisher → 小红书发布（未安装）
```

---

## 与其他 Skills 联动

安装扩展 Skills 后，可实现完整工作流：

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

## 更新

```bash
cd ~/.claude/skills/creator-digital-twin
git pull

# 如有数据库结构变更，运行升级脚本
python scripts/setup.py --upgrade
```

---

## 常见问题

### Q: 初始化脚本报错怎么办？

A: 确保已安装 Python 3.7+，并检查是否有写入权限：

```bash
python --version
ls -la ~/.claude/skills/creator-digital-twin/scripts/
```

### Q: 新闻抓取失败？

A: 检查网络连接和新闻源配置：

```bash
# 查看抓取状态
cat .creator-space/news_sources/state.json

# 检查新闻源配置
cat ~/.claude/skills/creator-digital-twin/config/sources.json
```

### Q: 如何在不同项目间共享数据？

A: `.creator-space/` 目录默认在项目根目录。如需共享：

```bash
# 创建符号链接
ln -s ~/shared-creator-space .creator-space
```

---

## 下一步

安装完成后，可以：

1. 运行 `/creator-digital-twin` 开始使用
2. 查看触发词列表选择需要的功能
3. 编辑 `.creator-space/system/config.json` 配置你的兴趣领域
4. 运行模式 E 学习你的写作风格
