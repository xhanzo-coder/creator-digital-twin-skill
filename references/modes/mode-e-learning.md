# 模式 E：风格学习 (Data-Driven Style Learning)

**定位**：数字分身系统的”基因工程中心”。通过分析历史文章，提取并加权你的语气、策略与价值观。

## ⛔ 执行前强制检查 (Pre-flight Checklist)

**在执行任何生成动作前，必须逐项确认以下检查点。如果跳过任何 REQUIRED 步骤，视为违规操作。**

```
模式 E 执行检查清单：
□ Step 1: 数据对齐与加权
  □ 已扫描 performance.jsonl（如存在）
  □ 已对文章进行分组（爆款/基准/低分）
  □ 如无 performance.jsonl，已按默认权重处理

□ Step 2: 三层解析架构
  □ 已完成语言层分析（语气节奏、词汇偏好）
  □ 已完成策略层分析（标题逻辑、Hooks、内容框架）
  □ 已完成灵魂层分析（立场、禁忌）

□ Step 3: 对标验证与风格演示 ⚠️ REQUIRED
  □ 已展示 AI 原句 vs 分身改写
  □ 已展示风格说明
  □ 已收到用户确认

□ Step 4: 档案更新 ⚠️ REQUIRED
  □ 已更新 system/profile.json
  □ 已更新 persona/ 相关文件
  □ 已更新 assets/strategies/

□ Step 5: 后续操作询问 ⚠️ REQUIRED - 必须使用 AskUserQuestion
  □ 已显示学习结果摘要
  □ 已推荐后续操作
  □ 已调用 AskUserQuestion 询问后续操作
```

---

## Step 1: 数据对齐与加权 (Data-Driven Weighting)

在读取文章目录前，系统优先扫描 `./analytics/performance.jsonl`：

1. **爆款组 (Top 10%)**：表现最优秀的文章。系统将对其进行**”金牌拆解”**，重点提取标题逻辑、钩子、结构框架。
2. **基准组 (Average)**：表现稳健的文章。提取核心语气、常用词汇、句式节奏。
3. **低分组 (Poor/Outdated)**：表现平平或已过时的文章。分析其”低效模式”，将其中的雷区存入 `persona/do_dont_say.json`。

**⚠️ 如果 `performance.jsonl` 不存在或为空**：
- 提示用户：”未找到发布数据，将按默认权重分析所有文章”
- 继续执行三层解析，但不进行数据加权

---

## Step 2: 三层解析架构 (Triple-Layer Parsing)

系统对每一组文章进行深度扫描，构建完整的人格模型：

### L1 语言层 (Language)
- **语气节奏**：短促有力、温润如水、还是冷峻专业？
- **词汇偏好**：提取高频专业词、口头禅、特定的转折连词。

### L2 策略层 (Strategy) - **关键进化**
- **标题逻辑**：识别你是”数字派”、”悬念派”还是”反直觉派”。
- **首句钩子 (Hooks)**：分析前 3 句如何留住读者，并将其模板化存入 `assets/strategies/`。
- **内容框架 (Structure)**：自动识别常用的 3-5 种叙事逻辑（如：总分总、故事化、对比论证）。

### L3 灵魂层 (Values)
- **立场与立场边界 (Stance)**：自动识别你对争议话题（如 AI 伦理、职场竞争）的一贯态度。
- **禁忌 (Do-Don'ts)**：识别你绝对不会用的表达方式或敏感词。

---

## Step 3: 对标验证与风格演示 (Contrastive Verification) ⚠️ REQUIRED

学习完成后，系统必须现场”交作业”供用户确认：

- **展示格式**：
  - **[AI 原句]**：一段中性的、教科书式的 AI 表达。
  - **[分身改写]**：基于刚学习到的风格档案进行的去 AI 化改写。
  - **[风格说明]**：解释为什么这样改（例如：*”融入了你常用的反问句式和辛辣的词汇习惯”*）。

**⚠️ 必须等待用户确认**：用户回复”对”、”是的”、”确认”后才可进入 Step 4。

---

## Step 4: 档案更新 (Evolution Tracking) ⚠️ REQUIRED

**必须使用 Write 工具更新以下文件**：

1. **首次建档**：生成主档案 `system/profile.json`。
2. **更新人格档案**：
   - `persona/voice_style.json` - 语气节奏、词汇偏好
   - `persona/do_dont_say.json` - 表达禁忌与偏好
   - `persona/stance_topics.json` - 立场声明
3. **更新策略库**：
   - `assets/strategies/` - 提取的成功框架
4. **增量学习/风格漂移**：若新输入的文章与旧档案有明显偏移（如：语气变严肃了），AI 主动询问：”我发现你最近的风格更偏向专业化，是否需要更新你的主风格档案？”

---

## Step 5: 后续操作询问 ⚠️ REQUIRED

**完成后，必须使用 AskUserQuestion 询问后续操作**：

```markdown
✅ 风格学习完成

📊 本次学习概览：
- 分析文章数：[X] 篇
- 提取词汇偏好：[X] 个
- 识别标题逻辑：[类型]
- 提取框架模板：[X] 个
- 更新立场声明：[X] 条

📁 更新的文件：
- system/profile.json
- persona/voice_style.json
- persona/do_dont_say.json
- assets/strategies/learned_framework.md

🔄 接下来你可以：

- [A] 测试学习效果 → 用新风格写一段示例
- [B] 拆解爆款博主的方法论 → 切换到模式 G
- [C] 开始创作 → 切换到模式 C
- [D] 查看完整风格档案 → 显示所有 persona 文件
- [E] 结束，稍后处理

请选择后续操作：
```

### 模式跳转映射表

| 用户选择 | 跳转模式 | 执行动作 |
|---------|---------|---------|
| A | - | 现场演示风格改写效果 |
| B | 模式 G | 进入对标拆解，学习外部博主 |
| C | 模式 C | 进入平台写作，应用新风格 |
| D | - | 显示 persona/ 目录下所有文件 |
| E | 结束 | 保存后退出 |

### AskUserQuestion 配置示例

```json
{
  “questions”: [
    {
      “question”: “风格学习已完成，接下来你想做什么？”,
      “header”: “后续操作”,
      “multiSelect”: false,
      “options”: [
        {
          “label”: “测试学习效果”,
          “description”: “让系统用新风格改写一段示例内容”
        },
        {
          “label”: “拆解爆款博主”,
          “description”: “进入模式 G，学习外部博主的方法论”
        },
        {
          “label”: “开始创作”,
          “description”: “进入模式 C，应用新风格进行平台写作”
        },
        {
          “label”: “查看完整风格档案”,
          “description”: “显示 persona/ 目录下所有文件内容”
        }
      ]
    }
  ]
}
```
