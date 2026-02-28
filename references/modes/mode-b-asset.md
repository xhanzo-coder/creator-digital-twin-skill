# 模式 B：资产管理模式 (Asset)

**触发条件**：
- 用户说"记个点子"、"存个金句"、"有个想法"

## v4 目标

模式 B 在 v4 不再只是“记点子”，而是统一管理三类沉淀：

1. **内容资产**：ideas / concepts / quotes / cases
2. **长期记忆**：timeline / stories / beliefs
3. **创作证据**：素材来源、验证状态、复用历史

## 用途 1：保存选题灵感（assets）

```bash
# 示例：用户说 "记个点子：GPT-5 对内容创作的影响"
```

**执行步骤**：
1. 提取灵感核心要点
2. 写入 `./.writing-style/assets/ideas/ideas.json`：

```json
{
  "id": "idea_001",
  "title": "GPT-5 对内容创作的影响",
  "source": "AI新闻推荐",
  "status": "待深化",
  "created_at": "2026-02-06"
}
```

## 用途 2：管理知识资产库（assets）

### 场景 1：手动添加概念

```bash
# 用户：存个概念 - "思维链提示：通过分步推理提升 LLM 输出质量"
```
- 写入 `assets/concepts/prompting.json`

### 场景 2：手动添加金句

```bash
# 用户：存个金句 - "AI 不会取代你，但会 AI 的人会"
```
- 写入 `assets/quotes/ai_quotes.json`

## 用途 3：沉淀个人记忆（memory）

### 场景 1：记录真实经历（stories）

```bash
# 用户：记一下，我 3 个月把公众号从 800 做到 2 万
```

- 以结构化条目写入 `memory/stories.jsonl`
- 记录字段：时间、场景、动作、结果、可复用教训

### 场景 2：记录观点变化（beliefs/timeline）

```bash
# 用户：我现在不再相信“多平台同时做”这件事
```

- 更新 `memory/beliefs.json`
- 追加到 `memory/timeline.jsonl`，保留“观点变化轨迹”

## 资产检索与复用

在平台写作模式（Mode C）中，系统会自动检索资产库：

```bash
# 示例：用户选题 "AI Agent 的应用场景"
# 检索操作
grep -r "AI Agent" .writing-style/assets/concepts/
grep -r "Agent" .writing-style/assets/quotes/
grep -r "Agent" .writing-style/memory/stories.jsonl
```

**若发现相关资产**：
- 主动提示："发现你之前定义过 'AI Agent' 概念，是否复用？"
- 展示既有定义/金句/个人故事，询问是否融入本次写作
