#!/usr/bin/env python3
"""
分析用户文章并提取写作风格
用法: python analyze_style.py [数据目录]
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

def read_articles(articles_dir):
    """读取所有文章"""
    articles_dir = Path(articles_dir)
    articles = []
    
    for pattern in ['*.md', '*.txt']:
        articles.extend(list(articles_dir.glob(pattern)))
    
    if not articles:
        return []
    
    contents = []
    for article_path in articles:
        with open(article_path, 'r', encoding='utf-8') as f:
            contents.append(f.read())
    
    return contents

def analyze_vocabulary(articles):
    """分析用词习惯"""
    all_text = ' '.join(articles)
    
    # 简单的分词（中文）
    words = re.findall(r'[\u4e00-\u9fff]+', all_text)
    
    # 停用词列表（简化版）
    stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
    
    # 过滤停用词
    filtered_words = [w for w in words if w not in stop_words and len(w) > 1]
    
    # 词频统计
    word_freq = Counter(filtered_words)
    high_freq_words = [word for word, count in word_freq.most_common(20)]
    
    # 检测AI词汇
    ai_words = ['标志着', '象征着', '深刻影响', '里程碑', '此外', '然而', '与此同时']
    avoided_words = [word for word in ai_words if word not in all_text]
    
    return {
        'high_frequency_words': high_freq_words[:10],
        'avoided_words': avoided_words
    }

def analyze_sentences(articles):
    """分析句式结构"""
    all_sentences = []
    for article in articles:
        # 简单的句子分割
        sentences = re.split(r'[。！？\n]', article)
        sentences = [s.strip() for s in sentences if s.strip()]
        all_sentences.extend(sentences)
    
    if not all_sentences:
        return {}
    
    # 句子长度分析
    lengths = [len(s) for s in all_sentences]
    avg_length = sum(lengths) / len(lengths)
    short_ratio = len([l for l in lengths if l < 20]) / len(lengths)
    
    # 疑问句检测
    questions = [s for s in all_sentences if '?' in s or '？' in s or s.endswith('吗')]
    question_freq = 'high' if len(questions) / len(all_sentences) > 0.1 else 'low'
    
    return {
        'avg_sentence_length': int(avg_length),
        'short_sentence_ratio': round(short_ratio, 2),
        'question_frequency': question_freq
    }

def analyze_paragraphs(articles):
    """分析段落节奏"""
    all_paragraphs = []
    for article in articles:
        paragraphs = article.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        all_paragraphs.extend(paragraphs)
    
    if not all_paragraphs:
        return {}
    
    # 段落长度分析（以句子数计）
    paragraph_lengths = []
    for para in all_paragraphs:
        sentences = re.split(r'[。！？]', para)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraph_lengths.append(len(sentences))
    
    avg_para_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
    single_sentence_ratio = len([l for l in paragraph_lengths if l == 1]) / len(paragraph_lengths) if paragraph_lengths else 0
    
    single_sentence_usage = 'common' if single_sentence_ratio > 0.2 else 'rare'
    
    return {
        'avg_paragraph_length': int(avg_para_length),
        'single_sentence_paragraph': single_sentence_usage
    }

def analyze_style(data_dir):
    """完整的风格分析"""
    data_dir = Path(data_dir)
    articles_dir = data_dir / 'articles'
    
    print(f"📚 正在分析: {articles_dir}")
    
    # 读取文章
    articles = read_articles(articles_dir)
    
    if not articles:
        print("⚠️  未找到文章文件 (.md 或 .txt)")
        return None
    
    print(f"✅ 找到 {len(articles)} 篇文章")
    print("🔍 分析中...")
    
    # 各维度分析
    vocabulary = analyze_vocabulary(articles)
    sentences = analyze_sentences(articles)
    paragraphs = analyze_paragraphs(articles)
    
    # 生成风格库
    profile = {
        "initialized": True,
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "basic_info": {
            "writing_field": "",
            "target_audience": "",
            "writing_purpose": ""
        },
        "writing_style": {
            "vocabulary": vocabulary,
            "sentence_patterns": sentences,
            "paragraph_rhythm": paragraphs,
            "thinking_mode": {
                "note": "需要人工分析补充"
            },
            "expression_preference": {
                "note": "需要人工分析补充"
            },
            "opening_closing": {
                "note": "需要人工分析补充"
            }
        },
        "external_knowledge": {},
        "statistics": {
            "articles_analyzed": len(articles),
            "total_chars": sum(len(a) for a in articles),
            "learning_sessions": 1
        }
    }
    
    return profile

def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / '.writing-style')
    data_dir = Path(data_dir).expanduser()
    
    print("================================")
    print("写作风格分析工具")
    print("================================")
    print()
    
    if not (data_dir / 'articles').exists():
        print(f"❌ 错误: {data_dir / 'articles'} 目录不存在")
        print(f"请先运行: bash scripts/init.sh")
        sys.exit(1)
    
    # 分析风格
    profile = analyze_style(data_dir)
    
    if not profile:
        sys.exit(1)
    
    # 保存 profile.json
    profile_path = data_dir / 'profile.json'
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ 风格分析完成！")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📄 风格库已生成: {profile_path}")
    print()
    print("📊 分析结果摘要：")
    print(f"  - 分析文章数: {profile['statistics']['articles_analyzed']}")
    print(f"  - 总字数: {profile['statistics']['total_chars']}")
    print(f"  - 高频词: {', '.join(profile['writing_style']['vocabulary']['high_frequency_words'][:5])}")
    print(f"  - 平均句长: {profile['writing_style']['sentence_patterns'].get('avg_sentence_length', 'N/A')} 字")
    print()
    print("💡 提示：你现在可以在 AI 对话中说：")
    print("   '按我的风格写一篇关于XXX的文章'")
    print()

if __name__ == '__main__':
    main()
