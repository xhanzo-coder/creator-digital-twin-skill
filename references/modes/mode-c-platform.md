# 模式 C：平台写作 (Strategy-Driven Platform Writing)

**定位**：数字分身的主输出引擎。基于“策略对标”与“深度痛点挖掘”的高质量内容工厂。

## Step 1: 深度情报与策略锚点 (Intelligence & Strategy)

在动笔前，系统不直接生成文稿，而是先执行**背景侦察**：

1. **策略对标 (Strategy Anchoring)**：
   - 检索 `assets/strategies/`（如 `dontbesilent` 框架）和 `analytics/performance.jsonl`。
   - **逻辑**：寻找最适合当前主题的“爆款框架”，严禁从零开始盲目创作。

2. **全网痛点挖掘 (Pain-point Research)**：
   - 使用 WebSearch 搜索：`关于 [主题] 的 3 个最常见误区`、`新手学习 [主题] 时遇到的最大困难`、`关于 [主题] 的争议点`。
   - **逻辑**：寻找能引发共鸣或争议的“情绪钩子”，而非陈述事实。

3. **资产调用 (Asset Injection)**：
   - 自动检索 `assets/quotes`、`assets/cases`、`assets/concepts`。

---

## Step 2: 创作方案选择 (Creation Roadmap)

系统提供 3 个带“情报支持”的创作角度供用户选择：

- **角度展示格式**：
  - **[建议角度]**：如“反直觉干货”、“情绪共鸣短评”。
  - **[建议框架]**：如“dontbesilent 钩子-内容-反转”。
  - **[注入素材]**：列出 1-2 条建议加入的金句或全网痛点。
  - **[推荐平台]**：根据内容属性推荐。

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
  - *AI 原文*：“我觉得人工智能会改变我们的未来。”
  - *分身改写*：“别再把 AI 当工具了，它正在重塑我们的饭碗。”
  - *修改理由*：匹配你常用的情绪化动词和短促句式。

### Pass 5: 平台视觉规范 (Platform Visuals)
- 优化 Emoji 分布、Hashtags、及 3 个爆款标题/封面图文字建议。
