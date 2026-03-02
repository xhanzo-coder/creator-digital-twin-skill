# 模式 B：资产与记忆管理 (Asset & Memory Co-creation)

**定位**：数字分身的“外挂大脑”。不再是被动记录，而是通过“灵感对撞”将碎片点子转化为结构化资产。

## Step 1: 灵感接收与全库扫描 (Multi-dimensional Scanning)

当你提供一个想法、点子、金句或一段经历时，系统立即启动**背景关联检查**：

### 1. 维度 A：历史内容关联 (Contextual Search)
- **扫描路径**：`./.writing-style/content/published/`
- **逻辑**：寻找相似的主题或观点，提醒你：“你曾在 [日期] 写过类似内容，是延续还是更新？”

### 2. 维度 B：冷启动策略关联 (Cold Start Strategy)
- **扫描路径**：`./.writing-style/assets/strategies/` 或 `./.writing-style/system/profile.json`
- **逻辑**：若无历史文章，则调用你学习过的方法论（如 `dontbesilent` 框架）或你的人设边界（`stance_topics.json`）。
- **反馈示例**： “这个想法非常符合你主张的‘AI 提效’人设。按照你存过的‘爆款文稿库’结构，这个点子可以作为‘反直觉切入点’。”

### 3. 维度 C：实时情报对冲 (News Pulse)
- **扫描路径**：`./.writing-style/news_sources/`
- **逻辑**：检索最近 7 天的爆款新闻。
- **反馈示例**： “你这个关于‘数字员工’的想法，正好呼应了昨天那条关于 GPT-5 Agent 能力的新闻，建议结合起来做一次‘深度点评’。”

---

## Step 2: 探讨式共创 (Co-creation Dialogue)

系统不应只回复“已记录”，而应提供 **2-3 个深化建议**：
1. **角度拆解**：这个点子可以发小红书（教程向）还是 X（观点向）？
2. **素材补全**：询问用户是否需要调用已有的“金句库”或“案例库”来填充这个点子。
3. **任务转化**：询问“是否直接生成初步大纲？”

---

## Step 3: 隐式记录与资产固化 (Implicit Capture)

在探讨过程中，系统自动识别并格式化以下资产：

| 资产类型 | 存放路径 | 判定标准 |
| :--- | :--- | :--- |
| **点子 (Ideas)** | `assets/ideas/` | 尚未成熟的选题、灵感片段、未来计划 |
| **概念 (Concepts)** | `assets/concepts/` | 你独特的定义、方法论名词（如“生产型兴趣”） |
| **金句 (Quotes)** | `assets/quotes/` | 具有穿透力的短句、对话中蹦出的精彩表达 |
| **案例 (Cases)** | `assets/cases/` | 具体的例子、调研数据、成功/失败的事实 |
| **经历 (Stories)** | `memory/stories.jsonl` | 你的个人故事、情绪、具体发生的事件 |
| **观点 (Beliefs)** | `memory/beliefs.json` | 价值观的声明、对某事的深度看法 |

**👉 确认逻辑**：对话结束前，系统汇总准备记录的项目，用户回复“确认”或“好”后正式写入 JSONL。

---

## Step 4: 更新索引与关联 (Indexing)

写入后，自动更新 `assets/index.json`。
如果该点子关联了某条新闻，在 `metadata` 中记录 `news_hash`，实现“情报与灵感”的强绑定。
