# 模式 D：自由创作模式 (Free)

**触发条件**：
- 用户说"随便写点"、"自由发挥"
- 不指定特定平台

**适用场景**：用户不指定平台，随意发挥。

## 执行逻辑

**检查人格状态并加载对应风格**：

```bash
# 检查 profile.json 状态
profile_initialized=$(cat ./.writing-style/profile.json | jq -r '.initialized')

if [ "$profile_initialized" == "true" ]; then
    echo "✅ 使用个人风格档案"
    STYLE_SOURCE="./.writing-style/profile.json"
else
    echo "📢 使用默认去AI化风格"
    STYLE_SOURCE="references/default-humanizer-style.md"
fi
```

## 创作规则

1. **读取风格指导**：
   - 个人风格模式：读取 `profile.json` 中的用词习惯、句式偏好
   - 默认人格模式：读取 `default-humanizer-style.md` 中的去AI化规则

2. **不执行**：平台硬性规则（字数、标签、Emoji 等限制）

3. **允许**：自由选择主题、长度、结构

4. **必须执行人格边界检查（v4新增）**：
   - 读取 `./.writing-style/system/safety_policy.json`
   - 读取 `./.writing-style/persona/do_dont_say.json`
   - 若触发高风险话题（投资建议、法律结论、医疗断言、替用户做强表态），先提示并请求确认

## 质量控制

仅执行 **Pass 3（风格克隆）**，跳过平台规范检查。

**默认人格模式下的额外提示**：
```
💡 提示：当前使用默认去AI化风格，文章将自动：
   - 删除 AI 套话和填充短语
   - 变化句子节奏，避免机械重复
   - 注入真实感和个人观点

📌 建议：提供 3-5 篇历史文章，系统将提取你的个人风格，
   未来创作将更符合你的写作习惯。
```
