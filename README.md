# creator-digital-twin

个人创作数字分身技能（v1.0），用于构建“像你写、懂你想、会复盘”的长期创作系统。

## 这个 Skill 能做什么

- 学习你的写作风格与表达习惯（模式 E/F）
- 进行多平台创作（X/Twitter、公众号、小红书，模式 C/D）
- 沉淀长期记忆与内容资产（模式 B）
- 从新闻和外部材料提炼选题与方法（模式 A/G）
- 对外部内容进行改写包装并做版权风险控制（模式 H）

## 安装方式

### 从 GitHub 安装

```bash
npx skills add <your-org-or-name>/<repo>@creator-digital-twin -g -y
```

### 项目级安装（不全局）

在项目目录执行：

```bash
npx skills add <your-org-or-name>/<repo>@creator-digital-twin -y
```

## 首次使用（最短路径）

1. 先让助手初始化目录：`bash scripts/init.sh`
2. 如果你是旧版数据：`python scripts/migrate_v3_to_v4.py`
3. 先做一次风格学习：给 3-5 篇历史文章，触发模式 E
4. 开始日常创作：直接说你要发哪个平台和主题

## 你可以直接这样对话（示例）

| 你对助手说 | 触发模式 | 结果 |
|---|---|---|
| 学习我的风格，文章在 `E:\\xxx\\my_articles` | E 风格学习 | 提取风格并更新 `system/profile.json` |
| 今天有什么 AI 新闻，给我 3 个可写选题 | A 新闻雷达 | 输出可创作选题包（角度+平台建议） |
| 记个点子：AI Agent 在客服中的 3 个坑 | B 资产管理 | 写入 `assets/ideas/ideas.json` |
| 发一篇小红书，主题是 AI 自动化入门 | C 平台写作 | 按平台规则生成稿件并进行质检 |
| 我改完这篇了，学习一下我的修改 | F 实时学习 | 从差异中更新你的表达偏好 |
| 学习这篇外部文章的方法论：`https://...` | G 外部学习 | 提炼技巧并做兼容性评分 |
| 把这篇文章改成我的风格，发公众号 | H 改写包装 | 生成改写稿并做版权核查 |

## 数据目录（运行后）

技能会在项目内维护 `./.writing-style/`：

- `system/`：配置、路由、安全策略、主档案
- `memory/`：长期记忆（事件/观点/故事）
- `persona/`：说话方式与边界
- `content/`：草稿、发布稿、二创稿
- `assets/`：点子、概念、金句、案例
- `analytics/`：发布表现与策略迭代
- `news_sources/`：新闻抓取数据

## 发布前检查（GitHub）

1. 确认 `SKILL.md` frontmatter 只有 `name` 和 `description`
2. 清理缓存文件（`__pycache__/`, `*.pyc`）
3. 验证脚本可解析（至少做一次语法检查）
4. 确认 `references/` 路径都可访问且没有断链
5. 在干净环境做一次安装与最小对话验证

## 建议的发布流程

```bash
git add .
git commit -m "release: creator-digital-twin v1.0"
git push origin <branch>
```

发布后即可用上面的 `npx skills add ...` 安装。
