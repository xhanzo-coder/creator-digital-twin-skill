# 模式 C：平台写作 (Strategy-Driven Platform Writing)

**定位**：数字分身的主输出引擎。基于"策略对标"与"深度痛点挖掘"的高质量内容工厂。

---

## ⛔ 执行前强制检查 (Pre-flight Checklist)

**在执行任何生成动作前，必须逐项确认以下检查点。如果跳过任何 REQUIRED 步骤，视为违规操作。**

```
模式 C 执行检查清单：
□ Step 0: 平台规则检查 ⛔ REQUIRED - 必须读取规则文件
  □ 确认目标平台（小红书/公众号/X）
  □ 读取 .creator-space/platform_rules/{platform}.json
  □ 读取 persona/do_dont_say.json（用户偏好）
  □ 展示关键规则摘要：标题公式、内容结构、禁用词
  □ 如信息缺失，先询问用户

□ Step 1: 情报与策略锚点
  □ 已检索 assets/strategies/ 或 performance.jsonl
  □ 已执行全网痛点挖掘 (WebSearch)
  □ 已检索 assets/ 中的可用素材

□ Step 2: 创作方案选择 ⛔ REQUIRED - 三问必答
  □ 已展示 3 个创作角度（角度名称 + 框架 + 素材 + 推荐平台）
  □ 已询问创作角度
  □ 已询问目标平台（可多选）⛔ 禁止跳过
  □ 已询问内容风格偏好 ⛔ 禁止跳过
  □ 已调用 AskUserQuestion 工具一次性收集三个参数
  □ 用户选择已记录：角度=[A/B/C]，平台=[...]，风格=[...]

□ Step 3: 五遍检查写作流
  □ Pass 1: 策略蓝图 ✓
  □ Pass 2: 逻辑初稿 ✓
  □ Pass 3: 事实与伦理核查 ✓
  □ Pass 4: 风格克隆与差异展示（展示 Diff）✓
  □ Pass 5.1: 标题生成与选择 ⛔ REQUIRED - 必须让用户选择
      □ 已生成 5-8 个标题选项
      □ 已展示推荐理由
      □ 已用 AskUserQuestion 让用户选择
  □ Pass 5.2: 内容生成 ✓
  □ Pass 5.3: 内容预览与确认 ⛔ REQUIRED - 必须让用户确认
      □ 已展示完整正文
      □ 已用 AskUserQuestion 询问确认
      □ 用户已选择"满意，保存"
  □ Pass 5.4: 保存文件 ✓
  □ Pass 6: 平台规则合规检查 ⛔ REQUIRED - 必须全部通过

□ Step 6: 图片提示词（可选）
  □ 用户已确认是否生成

□ Step 7: 后续操作询问 ⛔ REQUIRED - 必须使用 AskUserQuestion
  □ 已显示内容保存路径
  □ 已根据平台推荐相关 Skills
  □ 已调用 AskUserQuestion 询问后续操作
  □ 用户已选择后续操作（或选择结束）
```

**⚠️ 强制规则**：
- 如果 Step 0 未读取平台规则和用户偏好，**禁止进入 Step 1**
- 如果 Step 2 未同时询问三个问题（角度、平台、风格），**禁止进入 Step 3**
- 如果 Pass 5.1 未让用户选择标题，**禁止生成内容**
- 如果 Pass 5.3 未让用户确认内容，**禁止保存文件**
- 如果 Step 7 未询问后续操作，**视为流程不完整**
- 如果直接生成内容而跳过用户选择，视为**流程违规**

---

## Step 0: 平台规则检查 (Platform Rules Check) ⛔ REQUIRED

**在动笔前，必须读取目标平台的规则文件。**

### 平台规则文件路径

```
.creator-space/platform_rules/
├── xiaohongshu.json    # 小红书规则
├── wechat.json         # 公众号规则
└── twitter.json        # X/Twitter 规则
```

### 执行流程

**Step 0.1: 确认目标平台**

如果用户未明确指定平台，询问：

```
请选择目标平台：
- [A] 小红书 - 图文为主，重视视觉和标题
- [B] 公众号 - 长文为主，重视深度和排版
- [C] X/Twitter - 短文为主，重视观点和传播
- [D] 多平台适配 - 根据内容自动调整
```

**Step 0.2: 读取并展示平台规则**

根据用户选择的平台，读取对应的规则文件并展示关键规则：

```markdown
## 📋 小红书平台规则速查

### 标题规则
- 长度：不超过20字符
- 公式：
  - 成果公式：[时间][成果], [工具]做[事]
  - 痛点公式：为什么你的[X]总是[问题]？
  - 认知冲击：[数字]%的人都理解错了[X]
- 示例："30行代码搞定AI客服，附源码"

### 内容规则
- 最优长度：不超过1000字符
- 段落风格：每段不超过2行，段间必须空行
- Emoji使用：密度15-25%，强化关键信息而非装饰
- 语气：专业但不装逼，深度但不晦涩

### 开篇技巧
- 具体场景 + 痛点/惊喜
- ❌ 禁止："随着AI发展..."、"近年来..."等套话

### 禁用内容（来自 do_dont_say.json）
- [ ] 检查用户不喜欢的表达
- [ ] 确认事实准确性
```

**Step 0.3: 检查用户偏好**

同时读取 `persona/do_dont_say.json`，展示用户的表达禁忌：

```markdown
## 🎯 你的偏好

### ✅ 喜欢的表达
- （从 do_dont_say.json 读取）

### ❌ 避免的表达
- （从 do_dont_say.json 读取）

### 你的背景
- AI工具使用水平：[advanced/beginner]
- 专业领域：[从 profile.json 读取]
```

**⚠️ 如果规则文件不存在或偏好文件为空**：

```
检测到以下信息缺失：
- [ ] 小红书规则文件未找到
- [ ] 你的偏好档案为空（建议运行模式 E 学习你的风格）

是否继续使用默认规则？或者先补充这些信息？
```

---

## 输出目录结构

模式 C 输出到 `.creator-space/content/drafts/` 目录：

```
.creator-space/content/drafts/{YYYY-MM-DD}-{topic-slug}/
├── meta.json                       # 元信息
├── platforms/                      # 各平台内容
│   ├── xiaohongshu.md              # 小红书正文（供 baoyu-xhs-images 读取）
│   ├── xiaohongshu.json            # 小红书元数据（标题、tag）
│   ├── wechat.md                   # 公众号正文
│   └── x.md                        # X/Twitter 内容
├── prompts/                        # 图片提示词（由 baoyu-xhs-images 生成）
│   ├── _index.md                   # 索引 + 使用说明
│   ├── cover.md                    # 封面图提示词
│   ├── 01-content.md               # 内容图提示词
│   └── ...
└── images/                         # 最终图片（手动放入）
    ├── cover.png
    └── ...
```

**命名规则**：
- 目录名：`{YYYY-MM-DD}-{topic-slug}`，如 `2026-03-06-ai-boundary`
- slug：2-4 个英文单词，kebab-case

---

## Step 1: 深度情报与策略锚点 (Intelligence & Strategy)

在动笔前，系统不直接生成文稿，而是先执行**背景侦察**：

1. **策略对标 (Strategy Anchoring)**：
   - 检索 `assets/strategies/`（如 `dontbesilent` 框架）和 `analytics/performance.jsonl`。
   - **逻辑**：寻找最适合当前主题的"爆款框架"，严禁从零开始盲目创作。

2. **全网痛点挖掘 (Pain-point Research)**：
   - 使用 WebSearch 搜索：`关于 [主题] 的 3 个最常见误区`、`新手学习 [主题] 时遇到的最大困难`、`关于 [主题] 的争议点`。
   - **逻辑**：寻找能引发共鸣或争议的"情绪钩子"，而非陈述事实。

3. **资产调用 (Asset Injection)**：
   - 自动检索 `assets/quotes`、`assets/cases`、`assets/concepts`。

---

## Step 2: 创作方案选择 (Creation Roadmap) ⚠️ REQUIRED

**⛔ 阻塞步骤：必须使用 AskUserQuestion 工具让用户选择，不得跳过**

**⛔ 三问必答：必须同时询问以下三个问题，缺一不可！**

在完成 Step 1 的情报收集后，**必须暂停**，使用 AskUserQuestion 工具一次性询问用户以下三个问题：

### ⚠️ 强制要求：一次性收集所有创作参数

**必须在一个 AskUserQuestion 调用中同时包含以下三个问题：**

1. **创作角度**（必问）
2. **目标平台**（必问，可多选）
3. **内容风格**（必问）

**禁止行为**：
- ❌ 只问创作角度就进入写作
- ❌ 默认选择某个平台
- ❌ 跳过任何问题

### ⚠️ 选项展示规范（强制要求）

**每个创作角度必须包含以下完整信息**：

```markdown
### 角度 A：[角度名称]（例如：反直觉干货型）

**核心切入点**：一句话说明这个角度的独特之处
**为什么选这个**：结合热点/用户痛点/数据说明选择理由

**内容框架**：
- 钩子（Hook）：[具体的开头设计]
- 核心论点 1：[论点 + 支撑素材]
- 核心论点 2：[论点 + 支撑素材]
- 核心论点 3：[论点 + 支撑素材]
- 结尾/CTA：[具体的设计]

**注入素材**：
- 金句："[可用的金句]"
- 案例："[可用的案例/数据]"
- 痛点："[挖到的用户痛点]"

**推荐平台**：小红书 / 公众号 / X（并说明理由）
**预期效果**：收藏型 / 转发型 / 评论型
**风险提示**：可能的敏感点或需要注意的地方
```

### 必须展示的三个差异化角度

| 角度 | 特点 | 适合场景 |
|------|------|---------|
| **A: 干货型** | 信息密集、实用性强 | 知识分享、教程类 |
| **B: 情感型** | 引发共鸣、情绪导向 | 个人经历、观点表达 |
| **C: 争议型** | 制造话题、引发讨论 | 行业观察、热点评论 |

### AskUserQuestion 配置示例

```json
{
  "questions": [
    {
      "question": "请选择创作角度（每个角度都已基于情报分析设计）：",
      "header": "创作角度",
      "multiSelect": false,
      "options": [
        {
          "label": "角度A：反直觉干货型",
          "description": "用打破常识的视角切入，预期效果：高收藏。框架：Hook → 3个反直觉观点 → 实操建议。注入素材：[具体金句]"
        },
        {
          "label": "角度B：情绪共鸣型",
          "description": "从用户痛点切入，预期效果：高转发。框架：痛点场景 → 共鸣点 → 解决方案。注入素材：[具体案例]"
        },
        {
          "label": "角度C：争议讨论型",
          "description": "抛出争议观点引发讨论，预期效果：高评论。框架：争议点 → 正反分析 → 开放式结尾。风险：[具体风险]"
        }
      ]
    },
    {
      "question": "目标发布平台（可多选）：",
      "header": "平台选择",
      "multiSelect": true,
      "options": [
        {
          "label": "小红书",
          "description": "适合图文卡片形式，需要生成图片提示词"
        },
        {
          "label": "公众号",
          "description": "长文形式，可使用 Markdown 格式"
        },
        {
          "label": "X/Twitter",
          "description": "短文形式，控制在 280 字以内"
        }
      ]
    },
    {
      "question": "内容风格偏好：",
      "header": "风格选择",
      "multiSelect": false,
      "options": [
        {
          "label": "干货硬核",
          "description": "信息密集、逻辑清晰、专业术语多"
        },
        {
          "label": "轻松口语",
          "description": "口语化、轻松、有段子"
        },
        {
          "label": "情绪表达",
          "description": "有情绪起伏、个人色彩强"
        }
      ]
    }
  ]
}
```

**只有用户明确选择后，才能进入 Step 3**。

---

## Step 3: 五遍检查写作流 (5-Pass Quality Control)

用户选定角度后，严格执行以下五遍生成与检查逻辑：

### Pass 1: 策略蓝图 (Strategy Blueprint)
- 组装选定的框架、注入素材清单、设定首句钩子（Hook）。

### Pass 2: 逻辑初稿 (Logical Draft)
- 按照平台（小红书/公众号/X）的字数、语气、排版规范生成全文。

### Pass 3: 事实与伦理核查 (Fact & Ethics Check)
- 检查专业术语准确性、链接有效性、及是否存在版权引用风险。

### Pass 4: 风格克隆与差异展示 (Style Clone & Diff) - **核心步骤**
- 系统对比 `persona/voice_style.json` 进行去 AI 化。
- **强制展示修改过程**：
  - *AI 原文*："我觉得人工智能会改变我们的未来。"
  - *分身改写*："别再把 AI 当工具了，它正在重塑我们的饭碗。"
  - *修改理由*：匹配你常用的情绪化动词和短促句式。

### Pass 5: 平台视觉规范与输出 (Platform Visuals & Output)

**⛔ 强制流程：标题选择 → 内容生成 → 用户确认 → 保存文件**

#### Pass 5.1: 标题生成与选择 ⚠️ REQUIRED

**必须先生成标题让用户选择，不能自己决定！**

1. **读取平台规则**：读取 `.creator-space/platform_rules/{platform}.json` 获取标题规范
2. **读取用户偏好**：读取 `persona/do_dont_say.json` 和 `persona/voice_style.json`
3. **生成 5-8 个标题选项**：基于平台规则和个人风格生成多个候选标题
4. **展示推荐理由**：每个标题必须说明推荐理由
5. **使用 AskUserQuestion 让用户选择**

**标题选择输出格式**：

```markdown
## 📝 标题选择

基于你的写作风格和平台规则，我生成了以下标题选项：

**推荐标题**（符合你的风格偏好）：
1. **[标题1]** - 推荐 ✨
   理由：[具体理由，如"使用了你的常用句式"、"符合认知冲击公式"等]

**备选标题**：
2. **[标题2]**
   理由：[具体理由]
3. **[标题3]**
   理由：[具体理由]
4. **[标题4]**
   理由：[具体理由]
5. **[标题5]**
   理由：[具体理由]

**你也可以自定义标题**。
```

**AskUserQuestion 配置**：

```json
{
  "questions": [
    {
      "question": "请选择一个标题（或选择自定义）",
      "header": "标题选择",
      "multiSelect": false,
      "options": [
        { "label": "[标题1]", "description": "[推荐理由]" },
        { "label": "[标题2]", "description": "[推荐理由]" },
        { "label": "[标题3]", "description": "[推荐理由]" },
        { "label": "[标题4]", "description": "[推荐理由]" },
        { "label": "[标题5]", "description": "[推荐理由]" },
        { "label": "自定义标题", "description": "输入你自己的标题" }
      ]
    }
  ]
}
```

**⚠️ 禁止行为**：
- ❌ 直接选择标题而不让用户确认
- ❌ 只提供 3 个或更少的标题选项
- ❌ 不展示推荐理由

#### Pass 5.2: 内容生成

用户选择标题后，按照平台规范生成正文内容：

- 优化 Emoji 分布、Hashtags
- 确保内容符合平台字数要求
- 应用用户风格偏好

#### Pass 5.3: 内容预览与确认 ⚠️ REQUIRED

**⛔ 保存前必须让用户确认内容！**

**展示完整内容预览**：

```markdown
---
📝 内容已生成，请确认：

【标题】
{用户选择的标题}

【正文】
{完整正文内容}

【标签】
{标签列表}

【字数统计】
{字数}

---

⚠️ 请确认内容是否满意：
```

**使用 AskUserQuestion 询问确认**：

```json
{
  "questions": [
    {
      "question": "内容是否满意？",
      "header": "确认",
      "multiSelect": false,
      "options": [
        { "label": "满意，保存", "description": "保存内容到草稿目录" },
        { "label": "需要修改", "description": "告诉我需要修改的地方" },
        { "label": "重新生成", "description": "换个角度重新生成内容" }
      ]
    }
  ]
}
```

**如果选择"需要修改"**：
- 询问具体修改意见
- 修改后重新展示预览
- 再次确认

**如果选择"重新生成"**：
- 返回 Step 2 选择新的创作角度

**⚠️ 只有用户选择"满意，保存"后，才能执行 Pass 5.4 保存文件！**

#### Pass 5.4: 保存文件（用户确认后）

- **创建输出目录**：
  ```bash
  mkdir -p .creator-space/content/drafts/{YYYY-MM-DD}-{topic-slug}/platforms
  ```
- **保存文件**（按用户选择的平台）：
  - `platforms/xiaohongshu.md`：小红书正文（纯文本，供 baoyu-xhs-images 读取）
  - `platforms/xiaohongshu.json`：标题、tags、封面文字建议
  - `platforms/wechat.md`：公众号正文
  - `platforms/x.md`：X/Twitter 内容
- **保存元信息**：`meta.json`

### Pass 6: 平台规则合规检查 ⛔ REQUIRED

**在保存文件前，必须逐项检查以下合规项**：

#### 小红书合规检查清单

```markdown
## 📋 小红书规则合规检查

### 标题检查
□ 标题长度 ≤ 20 字符？
□ 标题符合公式（成果/痛点/认知冲击/认知颠覆）？
□ 标题避免泛化词（"打工人必备"等）？

### 内容检查
□ 正文长度 ≤ 1000 字符？
□ 每段 ≤ 2 行？
□ 段落间有空行？
□ Emoji 密度在 15-25%？

### 开篇检查
□ 开篇没有使用套话（"随着AI发展..."、"近年来..."）？
□ 开篇使用了具体场景 + 痛点/惊喜？

### 事实检查
□ 版本号/数据是否准确？（需标注来源）
□ 没有编造任何事实？

### 用户偏好检查
□ 是否遵守 `persona/do_dont_say.json` 中的 Do 项？
□ 是否避免 `persona/do_dont_say.json` 中的 Don't 项？
□ 语气是否符合 `persona/voice_style.json`？

### 立场检查
□ 是否符合 `persona/stance_topics.json` 中的立场？
```

#### 检查结果处理

| 检查结果 | 处理方式 |
|---------|---------|
| 全部通过 | 继续保存文件 |
| 有不通过项 | **必须修改后重新检查** |
| 涉及事实不确定 | **必须向用户确认** |

**⚠️ 合规检查不通过时，禁止保存文件**：

```
❌ 合规检查失败：

- 标题长度：23 字符（超过 20 字符限制）
- 正文长度：1250 字符（超过 1000 字符限制）
- 开篇使用套话："随着AI技术的发展..."

请修改后再保存。
```

#### 检查通过反馈

```
✅ 合规检查通过

- 标题："又是王炸——但我真的累了" (11字符) ✓
- 正文：892 字符 ✓
- 段落格式：每段 ≤ 2 行 ✓
- Emoji 密度：18% ✓
- 用户偏好：符合 ✓

文件已保存到：.creator-space/content/drafts/{date}-{slug}/
```

---

## Step 6: 图片提示词生成 (可选)

**⚠️ 强制前置检查**：

```bash
# 检测 baoyu-xhs-images skill 是否安装
installed_skills=$(ls ~/.claude/skills/ 2>/dev/null | grep -E "baoyu-xhs-images" || echo "")
project_skills=$(ls .claude/skills/ 2>/dev/null | grep -E "baoyu-xhs-images" || echo "")
has_xhs_skill=""
if [ -n "$installed_skills" ] || [ -n "$project_skills" ]; then
  has_xhs_skill="yes"
fi
```

### 情况 1：已安装 baoyu-xhs-images

询问用户是否生成图片提示词：

```json
{
  "questions": [
    {
      "question": "是否生成小红书图文卡片的图片提示词？",
      "header": "图片生成",
      "multiSelect": false,
      "options": [
        {
          "label": "是，生成提示词",
          "description": "调用 baoyu-xhs-images --prompt-only"
        },
        {
          "label": "否，稍后处理",
          "description": "内容已保存，可以稍后手动生成"
        }
      ]
    }
  ]
}
```

**如果选择"是"**：
1. 调用 baoyu-xhs-images skill
2. 参数：`--from-draft .creator-space/content/drafts/{date}-{slug} --prompt-only`
3. 该 skill 会读取内容并生成提示词

### 情况 2：未安装 baoyu-xhs-images

**禁止生成图片提示词文件！** 直接告知用户：

```markdown
---
✅ 内容已保存到 .creator-space/content/drafts/{date}-{slug}/

💡 提示：未检测到 baoyu-xhs-images skill，无法自动生成图片提示词。

如需生成图片，可以：
1. 安装 baoyu-xhs-images skill
2. 手动将内容复制到小红书，配合其他图片工具

---
```

**⚠️ 禁止行为**：
- 未安装 skill 时禁止生成 `prompts/` 目录
- 未安装 skill 时禁止调用 skill 相关功能
- 必须根据检测结果动态调整后续流程

---

## 输出文件格式

### meta.json
```json
{
  "id": "2026-03-06-ai-boundary",
  "date": "2026-03-06",
  "topic": "AI 公司边界感",
  "source": {
    "type": "news",
    "url": "https://..."
  },
  "status": "draft",
  "platforms": ["xiaohongshu", "wechat"],
  "workflow": {
    "content_created": true,
    "prompts_generated": false,
    "images_ready": false,
    "published": false
  },
  "created_at": "2026-03-06T10:00:00",
  "updated_at": "2026-03-06T11:30:00",
  "published_at": null,
  "xiaohongshu_note_id": null
}
```

**状态字段说明**：
- `status`: `draft` | `content_ready` | `prompts_ready` | `images_ready` | `published`
- `workflow.content_created`: 内容已创建
- `workflow.prompts_generated`: 图片提示词已生成（baoyu-xhs-images 执行后）
- `workflow.images_ready`: 图片已放入 images/ 目录
- `workflow.published`: 已发布到平台

### platforms/xiaohongshu.md
```markdown
# AI 圈大新闻：这次不是卷参数，是卷"边界感"

今天看到一条很关键的 AI 新闻：Anthropic 和五角大楼因为军事 AI 使用边界发生冲突。

我提炼成 3 句人话：
- 以后大模型公司不只卖能力，也卖立场
- B 端买 AI，不只看 demo，还要看风控与责任归属
- 创业团队最容易翻车的点：先上线，后补合规

给做 AI 项目的朋友一个 MVP 建议：
先做一页《使用边界清单》，把高风险场景提前划掉。

这一步看似慢，实际最省时间。
```

### platforms/xiaohongshu.json
```json
{
  "title": "AI 圈大新闻：这次不是卷参数，是卷"边界感"",
  "tags": ["#AI新闻", "#AIGC", "#AI创业", "#产品经理", "#合规"],
  "title_suggestions": [
    "Anthropic 硬刚五角大楼：AI 公司的边界在哪里？",
    "这次不是卷参数，是卷边界感"
  ],
  "cover_text_suggestions": [
    "AI 公司的新选择题",
    "边界感 = 竞争力"
  ]
}
```

---

## 与其他 Skills 的整合

| 后续 Skill | 触发命令 | 输入 | 输出 |
|-----------|---------|------|------|
| **baoyu-xhs-images** | `--from-draft {path} --prompt-only` | xiaohongshu.md | prompts/*.md |
| **xiaohongshu-publisher** | 读取 draft 目录 | xiaohongshu.md + images/*.png | 发布到小红书 |

**完整工作流**：
```
模式 C 写作 → xiaohongshu.md → baoyu-xhs-images --prompt-only
                                          ↓
                                     prompts/*.md
                                          ↓
                                    手动去 Gemini 生成图片
                                          ↓
                                     images/*.png
                                          ↓
                               xiaohongshu-publisher 发布
```

---

## 🔄 模式完成后的串联提醒 (Post-Mode Hook)

**⚠️ 强制要求：模式完成后必须询问后续操作**

### Step 7: 后续操作询问 ⛔ REQUIRED

**完成 Step 5/6 后，必须先检测 Skills 安装状态，再生成后续选项。**

#### Step 7.1: 检测 Skills 安装状态

```bash
# 检测扩展 Skills 安装状态
global_xhs_images=$(ls ~/.claude/skills/ 2>/dev/null | grep -E "baoyu-xhs-images" || echo "")
project_xhs_images=$(ls .claude/skills/ 2>/dev/null | grep -E "baoyu-xhs-images" || echo "")
global_xhs_publisher=$(ls ~/.claude/skills/ 2>/dev/null | grep -E "xiaohongshu-publisher" || echo "")
project_xhs_publisher=$(ls .claude/skills/ 2>/dev/null | grep -E "xiaohongshu-publisher" || echo "")

# 判断安装状态
has_xhs_images=""
has_xhs_publisher=""
if [ -n "$global_xhs_images" ] || [ -n "$project_xhs_images" ]; then
  has_xhs_images="yes"
fi
if [ -n "$global_xhs_publisher" ] || [ -n "$project_xhs_publisher" ]; then
  has_xhs_publisher="yes"
fi
```

#### Step 7.2: 根据安装状态生成 AskUserQuestion

**情况 1：已安装 baoyu-xhs-images**

```json
{
  "questions": [
    {
      "question": "内容已保存！接下来你想做什么？",
      "header": "后续操作",
      "multiSelect": false,
      "options": [
        {
          "label": "生成小红书图片",
          "description": "调用 baoyu-xhs-images 生成图文卡片提示词"
        },
        {
          "label": "修改内容",
          "description": "调整正文、标题或角度"
        },
        {
          "label": "结束本次",
          "description": "记录到资产库，稍后处理"
        },
        {
          "label": "继续创作",
          "description": "基于另一条新闻再创作一篇"
        }
      ]
    }
  ]
}
```

**情况 2：未安装 baoyu-xhs-images**

```json
{
  "questions": [
    {
      "question": "内容已保存！接下来你想做什么？",
      "header": "后续操作",
      "multiSelect": false,
      "options": [
        {
          "label": "手动发布",
          "description": "直接复制内容，手动发布到小红书"
        },
        {
          "label": "修改内容",
          "description": "调整正文、标题或角度"
        },
        {
          "label": "结束本次",
          "description": "记录到资产库，稍后处理"
        },
        {
          "label": "继续创作",
          "description": "基于另一条新闻再创作一篇"
        }
      ]
    }
  ]
}
```

**⚠️ 注意：选项必须根据 Skills 安装状态动态生成！**

- 已安装 `baoyu-xhs-images`：选项包含"生成小红书图片"
- 未安装：选项包含"手动发布"，并提示可安装 skill

#### Step 7.3: 根据用户选择执行

| 用户选择 | 执行动作 |
|---------|---------|
| 生成小红书图片 | 调用 `/baoyu-xhs-images --from-draft {path} --prompt-only` |
| 手动发布 | 显示内容路径，提示用户手动复制 |
| 修改内容 | 询问具体修改意见，返回 Step 3 |
| 结束本次 | 更新 meta.json 状态，结束流程 |
| 继续创作 | 返回模式 A 新闻列表 |

---

### 平台-Skill 映射表

| 平台 | 推荐 Skill | 用途 |
|------|-----------|------|
| 小红书 | `baoyu-xhs-images` | 生成图文卡片提示词 |
| 小红书 | `xiaohongshu-publisher` | 自动发布 |
| 公众号 | `baoyu-article-illustrator` | 生成文章插图 |
| 公众号 | `baoyu-post-to-wechat` | 发布到公众号 |
| X/Twitter | `baoyu-cover-image` | 生成封面图 |
| X/Twitter | `baoyu-post-to-x` | 发布到 X |
| 通用 | `baoyu-markdown-to-html` | Markdown 转 HTML |
