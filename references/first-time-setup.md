# 首次使用设置指南（v4）

## Step 0: 环境检查与初始化

每次触发技能时，先检查 v4 结构是否存在：

```bash
if [ ! -d ./.creator-space ] || [ ! -f ./.creator-space/system/profile.json ]; then
    echo "❌ 系统未初始化，先运行初始化脚本"
    echo "🔧 python scripts/setup.py"
    exit 1
fi
```

## Step 0.1: 检查可选扩展 Skills

本 Skill 核心功能完全独立，以下为可选扩展：

```bash
# 检测扩展 Skills 是否安装
ls ~/.claude/skills/ 2>/dev/null | grep -E "baoyu-xhs-images|xiaohongshu-publisher|baoyu-cover-image|baoyu-post-to-wechat" || echo ""
```

| 扩展 Skill | 功能 | 必需 | 未安装时的替代方案 |
|-----------|------|:----:|-------------------|
| baoyu-xhs-images | 小红书图片生成 | 否 | 手动复制草稿到小红书 |
| xiaohongshu-publisher | 小红书自动发布 | 否 | 手动发布 |
| baoyu-cover-image | 封面图生成 | 否 | 其他图片工具 |
| baoyu-post-to-wechat | 公众号发布 | 否 | 手动复制到公众号后台 |

## 首次初始化步骤

**触发条件**：`.creator-space/` 不存在，或 `system/profile.json` 缺失。

**执行命令**：

```bash
python scripts/setup.py
```

初始化脚本必须完成：

1. 创建 v4 分层目录（`system/ memory/ persona/ content/ assets/ analytics/`）
2. 创建基础资产文件（`assets/ideas/ideas.json`、`assets/index.json`）
3. 创建策略库目录（`assets/strategies/`）
4. 创建默认平台规则目录（`platform_rules/`）
5. 创建默认配置（`system/config.json`）
6. 创建默认人格档案（`system/profile.json`，`initialized=false`）

## v3 数据迁移（旧项目升级时）

如果历史项目还在 v3 结构（`.writing-style/`），可以手动迁移：

迁移规则：

1. `profile.json -> system/profile.json`
2. `config.json -> system/config.json`
3. `idea_bank/ -> assets/ideas/`
4. `knowledge_base/{concepts,quotes} -> assets/{concepts,quotes}`
5. `drafts/ -> content/drafts/`
6. `articles/ -> content/published/`
7. `learning_history/ -> analytics/reviews/legacy/`
8. `platform_rules/` 与 `news_sources/` 保留原位

## Step 0.5: 首次风格学习

**触发条件**：`system/profile.json.initialized == false`

执行流程：

1. 采集写作目标、受众、语气、思维方式
2. 分析 3-5 篇历史文章（推荐）
3. 生成并写入 `system/profile.json`
4. 用户确认后设为 `initialized=true`

## 人格状态与风格成熟度检查

```bash
# 读取风格数据
profile_initialized=$(cat ./.creator-space/system/profile.json | jq -r '.initialized')
articles_analyzed=$(cat ./.creator-space/system/profile.json | jq -r '.statistics.articles_analyzed // 0')
do_dont_say_count=$(cat ./.creator-space/persona/do_dont_say.json | jq -r '[.do // [], .dont // []] | add | length')
voice_style_tone=$(cat ./.creator-space/persona/voice_style.json | jq -r '.tone // "default"')
```

**风格成熟度判断**：

| 状态 | initialized | 成熟度条件 | 风格来源 |
|------|-------------|-----------|----------|
| 未初始化 | false | - | `references/default-humanizer-style.md`（全量） |
| 风格未成熟 | true | articles < 3 或 do_dont < 5 或 tone=default | 个人风格 + 核心AI痕迹检查 |
| 风格成熟 | true | articles ≥ 3 且 do_dont ≥ 5 且 tone≠default | 个人风格优先（仅提醒硬伤） |

**三种模式的行为差异**：

| 检查项 | 未初始化 | 风格未成熟 | 风格成熟 |
|-------|---------|-----------|---------|
| 个人风格应用 | ❌ 不应用 | ⚠️ 部分应用 | ✅ 全量应用 |
| 去AI化规则 | ✅ 全量24条 | ⚠️ 硬伤级5条 | ⚠️ 仅提醒 |
| 模糊归因检查 | ✅ 强制修改 | ✅ 强制修改 | ⚠️ 提醒 |
| 宣传性语言检查 | ✅ 强制修改 | ✅ 强制修改 | ⚠️ 提醒 |
| 空洞开头检查 | ✅ 强制删除 | ✅ 强制删除 | ✅ 强制删除 |

## 核心功能与扩展功能

### 核心功能（无需扩展 Skills）

| 模式 | 功能 | 输出 |
|------|------|------|
| A | AI 新闻雷达 | 新闻简报、热度分析 |
| B | 资产捕捉与纠正学习 | 偏好更新、点子记录 |
| C | 平台策略写作 | Markdown 草稿 |
| D | 头脑风暴 | 选题、灵感整理 |
| E | 风格学习 | 人格档案更新 |
| G | 对标拆解 | 策略文件 .md |
| H | 内容重塑 | 改写后的 Markdown |
| I | 发布复盘 | 数据记录、爆款分析 |

### 扩展功能（需要安装扩展 Skills）

| 扩展 Skill | 增强功能 |
|-----------|---------|
| baoyu-xhs-images | 模式 C 后自动生成图片提示词 |
| xiaohongshu-publisher | 一键发布到小红书 |
| baoyu-cover-image | 公众号/X 平台封面图 |
| baoyu-post-to-wechat | 一键发布到公众号 |
