# 自动化进化引擎

文章发布后，系统自动从内容中提取新知识，反哺 `assets/`、`memory/` 与 `analytics/`，形成学习闭环。

## 自动资产提取

**发布后自动执行**：

### Step 1: 扫描文稿

识别以下内容：

1. **新定义/概念**：
   - 模式：「XXX 是一种...」「XXX 指的是...」
   - 示例：「思维链提示是一种通过分步推理提升 LLM 输出质量的提示技术」

2. **高质量表达/金句**：
   - 模式：短句、对仗、反问、比喻
   - 示例：「AI 不会取代你，但会 AI 的人会」

3. **个人案例**：
   - 模式：第一人称 + 具体数据
   - 示例：「我用这个方法，3个月粉丝从800涨到2万」

### Step 2: 写入资产库

**概念提取示例**：
```json
// assets/concepts/prompting.json
{
  "concept": "思维链提示",
  "definition": "通过分步推理提升 LLM 输出质量的提示技术",
  "source": "2026-02-06_ai_agent.md",
  "created_at": "2026-02-06",
  "category": "AI提示工程"
}
```

**金句提取示例**：
```json
// assets/quotes/ai_quotes.json
{
  "quote": "AI 不会取代你，但会 AI 的人会",
  "source": "2026-02-06_ai_agent.md",
  "created_at": "2026-02-06",
  "tags": ["AI", "职场竞争", "技能提升"]
}
```

**案例提取示例**：
```json
// assets/cases/personal_cases.json
{
  "case": "用AI工具提升公众号涨粉效率",
  "description": "3个月粉丝从800涨到2万",
  "method": "专注做公众号 + AI工具分享",
  "source": "2026-02-06_ai_agent.md",
  "metrics": {
    "timespan": "3 months",
    "growth": "800 -> 20000",
    "multiplier": "25x"
  }
}
```

### Step 3: 更新索引

生成快速检索索引：

```json
// assets/index.json
{
  "concepts": {
    "思维链提示": "concepts/prompting.json#思维链提示",
    "AI Agent": "concepts/ai_agent.json#AI_Agent"
  },
  "quotes": {
    "AI不会取代你": "quotes/ai_quotes.json#0",
    "专注是唯一的护城河": "quotes/business.json#3"
  },
  "tags": {
    "AI": ["concepts/prompting.json", "quotes/ai_quotes.json"],
    "效率": ["cases/personal_cases.json"]
  }
}
```

---

## 反馈微调

**用户提出修改意见时**：

### 场景 1：修改平台规则

**用户反馈**："小红书标题太夸张，改得低调点"

**执行步骤**：

1. 分析反馈内容
2. 自动拟定 JSON 修改建议：

```json
// platform_rules/xiaohongshu.json
{
  "title_style": {
    "tone": "低调务实",  // 原值："热情夸张"
    "emoji_usage": "适度"  // 原值："高频"
  }
}
```

3. 展示修改建议：
```
📝 根据你的反馈，建议更新小红书规则：

【修改内容】
- 标题语气：从"热情夸张"改为"低调务实"
- Emoji 使用：从"高频"改为"适度"

【影响范围】
- 未来小红书标题将更加克制
- Emoji 频率降低（从每 50 字改为每 100 字）

是否确认更新？（是/否）
```

4. 用户确认后执行 Edit 工具更新 JSON

### 场景 2：修改风格档案

**用户反馈**："我现在不太喜欢用'你想想看'了，换成'想一下'吧"

**执行步骤**：

1. 识别为风格偏好变更
2. 更新 `system/profile.json`：

```json
{
  "learned_from_edits": {
    "vocabulary_corrections": [
      {"avoid": "你想想看", "prefer": "想一下", "updated_at": "2026-02-06"}
    ]
  }
}
```

3. 提示用户：
```
✅ 风格偏好已更新！
- 从现在开始，系统会用"想一下"替代"你想想看"
- 这个变化会应用到未来所有写作中
```

---

## 学习闭环总结

```
首次使用
   ↓
Step 0.5: 风格学习（建立 profile.json）
   ↓
平台写作（应用风格）
   ↓
Pass 3: 展示修改（用户看到风格克隆过程）
   ↓
用户修改文章
   ↓
模式 F: 实时学习（更新 learned_from_edits）
   ↓
发布文章
   ↓
进化引擎（提取新资产）
   ↓
下次写作更精准（复用资产库）
   ↓
循环...
```

**核心价值**：
- 每篇文章都在训练系统
- 用户每次修改都在教系统
- 系统越用越懂用户
- 知识资产不断积累
