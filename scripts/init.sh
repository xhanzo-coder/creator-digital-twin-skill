#!/bin/bash

set -euo pipefail

BASE_DIR="./.creator-space"

echo "🚀 初始化 Creator Digital Twin v1.0 ..."

# Core layered directories
mkdir -p "$BASE_DIR/system"
mkdir -p "$BASE_DIR/memory"
mkdir -p "$BASE_DIR/persona"
mkdir -p "$BASE_DIR/content/drafts"
mkdir -p "$BASE_DIR/content/published"
mkdir -p "$BASE_DIR/content/repurpose"
mkdir -p "$BASE_DIR/content/calendar"
mkdir -p "$BASE_DIR/content/metadata"
mkdir -p "$BASE_DIR/assets/ideas"
mkdir -p "$BASE_DIR/assets/concepts"
mkdir -p "$BASE_DIR/assets/quotes"
mkdir -p "$BASE_DIR/assets/cases"
mkdir -p "$BASE_DIR/assets/strategies"
mkdir -p "$BASE_DIR/analytics/reviews"
mkdir -p "$BASE_DIR/news_sources/daily"
mkdir -p "$BASE_DIR/news_sources/recommendations"
mkdir -p "$BASE_DIR/platform_rules"

echo "✅ 目录结构创建完成"

if [ ! -f "$BASE_DIR/system/profile.json" ]; then
cat > "$BASE_DIR/system/profile.json" <<EOF
{
  "initialized": false,
  "mode": "default_humanizer",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "learning_count": 0,
  "note": "当前使用默认去AI化风格。建议提供历史文章以建立个人风格档案。",
  "reference": "references/default-humanizer-style.md"
}
EOF
  echo "📄 已创建 system/profile.json"
fi

if [ ! -f "$BASE_DIR/system/config.json" ]; then
cat > "$BASE_DIR/system/config.json" <<EOF
{
  "focus_tracks": ["ai", "content", "creator-business"],
  "primary_platforms": ["twitter", "wechat", "xiaohongshu"],
  "news_enabled": true
}
EOF
  echo "📄 已创建 system/config.json"
fi

if [ ! -f "$BASE_DIR/system/router_rules.json" ]; then
  echo "{}" > "$BASE_DIR/system/router_rules.json"
fi

if [ ! -f "$BASE_DIR/system/safety_policy.json" ]; then
cat > "$BASE_DIR/system/safety_policy.json" <<EOF
{
  "high_risk_topics": ["medical", "legal", "financial"],
  "require_user_confirmation": true
}
EOF
fi

if [ ! -f "$BASE_DIR/assets/ideas/ideas.json" ]; then
  echo "[]" > "$BASE_DIR/assets/ideas/ideas.json"
fi

if [ ! -f "$BASE_DIR/assets/index.json" ]; then
cat > "$BASE_DIR/assets/index.json" <<EOF
{
  "concepts": {},
  "quotes": {},
  "cases": {},
  "tags": {}
}
EOF
fi

if [ ! -f "$BASE_DIR/memory/beliefs.json" ]; then
  echo '{"beliefs":[]}' > "$BASE_DIR/memory/beliefs.json"
fi

if [ ! -f "$BASE_DIR/memory/preferences.json" ]; then
  echo '{"preferences":[]}' > "$BASE_DIR/memory/preferences.json"
fi

if [ ! -f "$BASE_DIR/memory/relationships.json" ]; then
  echo '{"people":[]}' > "$BASE_DIR/memory/relationships.json"
fi

touch "$BASE_DIR/memory/timeline.jsonl"
touch "$BASE_DIR/memory/stories.jsonl"

if [ ! -f "$BASE_DIR/persona/voice_style.json" ]; then
  echo '{"tone":"default","cadence":"mixed","filler_words":[]}' > "$BASE_DIR/persona/voice_style.json"
fi

if [ ! -f "$BASE_DIR/persona/tone_by_scene.json" ]; then
  echo '{"public":"neutral","private":"casual"}' > "$BASE_DIR/persona/tone_by_scene.json"
fi

if [ ! -f "$BASE_DIR/persona/do_dont_say.json" ]; then
  echo '{"do":[],"dont":[]}' > "$BASE_DIR/persona/do_dont_say.json"
fi

if [ ! -f "$BASE_DIR/persona/stance_topics.json" ]; then
  echo '{"topics":[]}' > "$BASE_DIR/persona/stance_topics.json"
fi

touch "$BASE_DIR/analytics/performance.jsonl"
touch "$BASE_DIR/analytics/experiments.jsonl"
touch "$BASE_DIR/analytics/reviews.jsonl"
touch "$BASE_DIR/analytics/strategy_updates.jsonl"

echo "🎉 初始化完成（v4）"
