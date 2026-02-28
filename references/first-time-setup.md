# 首次使用设置指南（v4）

## Step 0: 环境检查与初始化

每次触发技能时，先检查 v4 结构是否存在：

```bash
if [ ! -d ./.writing-style ] || [ ! -f ./.writing-style/system/profile.json ]; then
    echo "❌ 系统未初始化，先运行初始化脚本"
    echo "🔧 bash scripts/init.sh"
    exit 1
fi
```

## 首次初始化步骤

**触发条件**：`.writing-style/` 不存在，或 `system/profile.json` 缺失。

**执行命令**：

```bash
bash scripts/init.sh
```

初始化脚本必须完成：

1. 创建 v4 分层目录（`system/ memory/ persona/ content/ assets/ analytics/`）
2. 创建基础资产文件（`assets/ideas/ideas.json`、`assets/index.json`）
3. 创建默认平台规则目录（`platform_rules/`）
4. 创建默认配置（`system/config.json`）
5. 创建默认人格档案（`system/profile.json`，`initialized=false`）

## v3 数据迁移（旧项目升级时）

如果历史项目还在 v3 结构，执行：

```bash
python scripts/migrate_v3_to_v4.py
```

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

## 人格状态检查

```bash
profile_status=$(cat ./.writing-style/system/profile.json | jq -r '.initialized')

if [ "$profile_status" == "false" ]; then
    STYLE_MODE="default_humanizer"
    STYLE_REFERENCE="references/default-humanizer-style.md"
else
    STYLE_MODE="personal"
    STYLE_REFERENCE="./.writing-style/system/profile.json"
fi
```

| 状态 | initialized 值 | 风格来源 |
|------|----------------|----------|
| 默认人格 | false | `references/default-humanizer-style.md` |
| 个人风格 | true | `./.writing-style/system/profile.json` |
