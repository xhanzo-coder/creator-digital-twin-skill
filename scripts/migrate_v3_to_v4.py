#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate writing-style data directory from v3 layout to v4 layered layout.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def resolve_data_root() -> Path:
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        data_dir = candidate / ".writing-style"
        if data_dir.exists():
            return data_dir
    return current / ".writing-style"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def move_if_exists(src: Path, dst: Path, moved: list[str]) -> None:
    if not src.exists():
        return
    ensure_dir(dst.parent)
    if dst.exists():
        return
    shutil.move(str(src), str(dst))
    moved.append(f"{src} -> {dst}")


def copytree_if_exists(src: Path, dst: Path, moved: list[str]) -> None:
    if not src.exists():
        return
    ensure_dir(dst.parent)
    if dst.exists():
        return
    shutil.copytree(src, dst)
    moved.append(f"{src} -> {dst} (copy)")


def main() -> int:
    root = resolve_data_root()
    ensure_dir(root)

    moved: list[str] = []
    created: list[str] = []

    # v4 directories
    for rel in [
        "system",
        "memory",
        "persona",
        "content/drafts",
        "content/published",
        "content/repurpose",
        "content/calendar",
        "content/metadata",
        "assets/ideas",
        "assets/concepts",
        "assets/quotes",
        "assets/cases",
        "analytics/reviews",
        "news_sources/daily",
        "news_sources/recommendations",
        "platform_rules",
    ]:
        path = root / rel
        if not path.exists():
            created.append(str(path))
        ensure_dir(path)

    # File migrations
    move_if_exists(root / "profile.json", root / "system" / "profile.json", moved)
    move_if_exists(root / "config.json", root / "system" / "config.json", moved)

    # Directory migrations
    move_if_exists(root / "idea_bank", root / "assets" / "ideas", moved)
    move_if_exists(root / "knowledge_base" / "concepts", root / "assets" / "concepts", moved)
    move_if_exists(root / "knowledge_base" / "quotes", root / "assets" / "quotes", moved)
    move_if_exists(root / "drafts", root / "content" / "drafts", moved)
    move_if_exists(root / "articles", root / "content" / "published", moved)
    move_if_exists(root / "external_knowledge", root / "memory" / "external_knowledge", moved)
    move_if_exists(root / "learning_history", root / "analytics" / "reviews" / "legacy", moved)

    # Keep backward compatible copies if only old folders exist and new is empty
    copytree_if_exists(root / "knowledge_base", root / "assets" / "_legacy_knowledge_base", moved)

    # Required defaults
    defaults = {
        root / "system" / "router_rules.json": {},
        root / "system" / "safety_policy.json": {
            "high_risk_topics": ["medical", "legal", "financial"],
            "require_user_confirmation": True,
        },
        root / "assets" / "index.json": {"concepts": {}, "quotes": {}, "cases": {}, "tags": {}},
        root / "memory" / "beliefs.json": {"beliefs": []},
        root / "memory" / "preferences.json": {"preferences": []},
        root / "memory" / "relationships.json": {"people": []},
        root / "persona" / "voice_style.json": {
            "tone": "default",
            "cadence": "mixed",
            "filler_words": [],
        },
        root / "persona" / "tone_by_scene.json": {"public": "neutral", "private": "casual"},
        root / "persona" / "do_dont_say.json": {"do": [], "dont": []},
        root / "persona" / "stance_topics.json": {"topics": []},
    }

    for path, payload in defaults.items():
        if not path.exists():
            ensure_dir(path.parent)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            created.append(str(path))

    for rel in [
        "memory/timeline.jsonl",
        "memory/stories.jsonl",
        "analytics/performance.jsonl",
        "analytics/experiments.jsonl",
        "analytics/reviews.jsonl",
        "analytics/strategy_updates.jsonl",
        "content/metadata/content_map.jsonl",
    ]:
        path = root / rel
        if not path.exists():
            ensure_dir(path.parent)
            path.touch()
            created.append(str(path))

    # Ensure profile minimal fields exist
    profile_path = root / "system" / "profile.json"
    if not profile_path.exists():
        profile = {
            "initialized": False,
            "mode": "default_humanizer",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "learning_count": 0,
            "reference": "references/default-humanizer-style.md",
        }
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        created.append(str(profile_path))

    report = {
        "migrated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "moved": moved,
        "created": created,
    }
    report_path = root / "system" / "migration_report_v3_to_v4.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("v3 -> v4 migration completed")
    print(f"root: {root}")
    print(f"moved: {len(moved)}")
    print(f"created: {len(created)}")
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
