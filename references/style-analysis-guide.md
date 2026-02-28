# 写作风格分析指南

本文档指导如何从用户的历史文章中提取写作风格特征（本地存储版）。

## 分析维度

### 1. 用词习惯
- 高频词汇（排除停用词）
- 专业术语使用程度
- 口语化程度
- 避免使用的词汇

### 2. 句式结构
- 平均句长
- 长短句比例
- 复杂从句使用频率
- 疑问句、感叹句使用

### 3. 段落节奏
- 平均段落长度
- 单句段落使用
- 段落过渡方式

### 4. 思维方式
- 论证逻辑（演绎/归纳/案例）
- 是否使用对比、类比
- 是否承认复杂性和不确定性

### 5. 表达偏好
- 第一人称使用频率
- 比喻和修辞使用
- 具体例子vs抽象概念
- 数据引用习惯

### 6. 开头结尾
- 开头惯用方式（提问/直入/场景）
- 结尾惯用方式（总结/提问/留白）
- 是否使用金句

## 输出格式

分析完成后，生成 `profile.json`：

```json
{
  "initialized": true,
  "created_at": "2026-02-01T10:30:00Z",
  "writing_style": {
    "vocabulary": {
      "high_frequency_words": ["其实", "挺", "你想想看"],
      "colloquial_level": "very_high",
      "avoided_words": ["标志着", "象征着"]
    },
    "sentence_patterns": {
      "avg_sentence_length": 16,
      "short_sentence_ratio": 0.7,
      "question_frequency": "high"
    },
    "paragraph_rhythm": {
      "avg_paragraph_length": 3,
      "single_sentence_paragraph": "common"
    },
    "thinking_mode": {
      "logic_type": "case_driven",
      "analogy_usage": "frequent"
    },
    "expression_preference": {
      "first_person_usage": "frequent",
      "concrete_examples": "always"
    },
    "opening_closing": {
      "opening_style": "question",
      "closing_style": "open_ended"
    }
  }
}
```

详细分析方法请参考 Python 实现。
