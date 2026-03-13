# 模式 D：思维助产与灵魂随笔 (Brainstorming & Soul Flow)

**定位**：数字分身的”真我表达空间”。兼具**头脑风暴伙伴**与**情感随笔**双重功能。

## ⛔ 执行前强制检查 (Pre-flight Checklist)

**在执行任何生成动作前，必须逐项确认以下检查点。如果跳过任何 REQUIRED 步骤，视为违规操作。**

```
模式 D 执行检查清单：
□ Step 0: 头脑风暴与灵感整理
  □ 已识别并分类碎片元素（观点/痛点/素材/疑问）
  □ 已提供 2-3 个洞察建议
  □ 已引导用户确认选题方向

□ Step 1: 随笔选题确认 ⚠️ REQUIRED - 必须使用 AskUserQuestion
  □ 已展示可选的选题方向
  □ 已调用 AskUserQuestion 工具
  □ 已收到用户明确选择

□ Step 2: 随笔创作
  □ 已关联 memory/stories.jsonl 增加人味
  □ 已注入 assets/ 中的相关素材
  □ 已执行风格克隆

□ Step 3: 后续操作询问 ⚠️ REQUIRED - 必须使用 AskUserQuestion
  □ 已显示创作结果
  □ 已根据内容推荐后续操作
  □ 已调用 AskUserQuestion 询问后续操作
```

---

## Step 0: 头脑风暴与灵感整理 (Brainstorming Partner)

**触发场景**：用户说”理一下”、”整理一下”、”头脑风暴”、”帮我理理”、”帮我整理”。

**执行流程**：
1. **碎片捕捉与分类**：从混乱输入中快速识别出核心元素（如：观点、痛点、素材、疑问），并以结构化清单展示。
2. **深度建议与启发**：基于整理出的信息，主动提供 2-3 个独特的创作视角或洞察建议。
3. **选题方向引导 (The Hook)**：
   - **关键动作**：询问用户：”在这些整理出的逻辑中，你觉得哪个最有潜力做成选题？”
   - **互动**：提供 2-3 个初步的选题题目，引导用户锁定创作方向。
4. **决策流转**：
   - 用户若想继续聊 -> 保持 Step 0 循环。
   - 用户若选定方向 -> 询问是否进入 **Step 1 (随笔模式)** 或跳转 **模式 C (平台写作)**。

---

## Step 1: 随笔选题确认 ⚠️ REQUIRED

**⛔ 阻塞步骤：必须使用 AskUserQuestion 工具让用户选择，不得跳过**

```json
{
  “questions”: [
    {
      “question”: “基于整理的灵感，你想往哪个方向发展？”,
      “header”: “选题方向”,
      “multiSelect”: false,
      “options”: [
        {
          “label”: “方向A：[具体选题]”,
          “description”: “[选题描述 + 预期效果]”
        },
        {
          “label”: “方向B：[具体选题]”,
          “description”: “[选题描述 + 预期效果]”
        },
        {
          “label”: “方向C：[具体选题]”,
          “description”: “[选题描述 + 预期效果]”
        }
      ]
    },
    {
      “question”: “选择输出形式：”,
      “header”: “输出形式”,
      “multiSelect”: false,
      “options”: [
        {
          “label”: “随笔写作”,
          “description”: “个人化表达，保留情感色彩，适合公众号/个人博客”
        },
        {
          “label”: “平台内容”,
          “description”: “进入模式 C，进行策略化写作，适合小红书/X”
        },
        {
          “label”: “仅整理记录”,
          “description”: “存入资产库，不进行创作”
        }
      ]
    }
  ]
}
```

---

## Step 2: 随笔创作

用户选择”随笔写作”后执行：

1. **记忆唤醒**：强制检索 `memory/stories.jsonl`，寻找相关个人经历注入。
2. **资产注入**：从 `assets/quotes`、`assets/concepts` 检索相关金句和概念。
3. **风格保持**：遵循 `persona/voice_style.json` 的语气规范。
4. **输出格式**：
   - 标题
   - 正文（Markdown 格式）
   - 可选的 CTA 或金句结尾

---

## Step 3: 后续操作询问 ⚠️ REQUIRED

**完成后，必须使用 AskUserQuestion 询问后续操作**：

```markdown
✅ 随笔创作完成

📊 本次创作概览：
- 字数：[XXX] 字
- 核心主题：[主题]
- 注入资产：[使用的金句/故事]

🔄 接下来你可以：

- [A] 发布到公众号 → /baoyu-post-to-wechat
- [B] 转化为小红书内容 → 进入模式 C 进行平台适配
- [C] 转化为 X/Twitter 内容 → 进入模式 C 进行平台适配
- [D] 记录到资产库 → 存入 assets/ideas/ 或 assets/quotes/
- [E] 继续头脑风暴 → 返回 Step 0
- [F] 结束，稍后处理

请选择后续操作：
```

### 模式跳转映射表

| 用户选择 | 跳转模式/Skill | 执行动作 |
|---------|---------------|---------|
| A | baoyu-post-to-wechat | 发布到微信公众号 |
| B | 模式 C | 携带随笔内容进入平台写作 |
| C | 模式 C | 携带随笔内容进入平台写作 |
| D | 模式 B | 存入资产库 |
| E | 返回 Step 0 | 继续头脑风暴 |
| F | 结束 | 保存后退出 |

### AskUserQuestion 配置示例

```json
{
  “questions”: [
    {
      “question”: “随笔已完成，接下来你想做什么？”,
      “header”: “后续操作”,
      “multiSelect”: false,
      “options”: [
        {
          “label”: “发布到公众号”,
          “description”: “调用 baoyu-post-to-wechat 发布文章”
        },
        {
          “label”: “转化为小红书内容”,
          “description”: “进入模式 C，将随笔适配为小红书笔记”
        },
        {
          “label”: “记录到资产库”,
          “description”: “将金句/点子存入资产库供后续使用”
        },
        {
          “label”: “继续头脑风暴”,
          “description”: “返回 Step 0 继续整理灵感”
        }
      ]
    }
  ]
}
```
