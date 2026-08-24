#!/usr/bin/env python3
"""Create algorithm/<topic>/NNN-difficulty-slug.md and .py from templates."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_MD = SKILL_DIR / "template.md"
TEMPLATE_PY = SKILL_DIR / "template.py"
PROGRESS = REPO_ROOT / "algorithm" / "PROGRESS.md"

TOPICS = {
    "array and string",
    "hash map and hash set",
    "stack and queue",
    "linked list",
    "binary tree",
    "dynamic programming",
    "binary search",
    "heap",
    "graph",
    "backtracking",
    "intervals",
    "trie",
    "union-find",
    "greedy",
    "system design",
    "math and bitwise",
}


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def problem_id(raw: str) -> str:
    n = int(raw)
    return f"{n:03d}" if n < 1000 else str(n)


def leetcode_slug(title: str) -> str:
    return slugify(title)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--difficulty", required=True, choices=["easy", "medium", "hard"])
    parser.add_argument("--topic", required=True)
    parser.add_argument("--pattern", default="")
    args = parser.parse_args()

    topic = args.topic.strip()
    if topic not in TOPICS:
        raise SystemExit(
            f"Unknown topic {topic!r}. Use one of: {', '.join(sorted(TOPICS))}"
        )

    pid = problem_id(args.id)
    file_slug = slugify(args.title)
    stem = f"{pid}-{args.difficulty}-{file_slug}"
    folder = REPO_ROOT / "algorithm" / topic
    folder.mkdir(parents=True, exist_ok=True)

    md_path = folder / f"{stem}.md"
    py_path = folder / f"{stem}.py"
    if md_path.exists() or py_path.exists():
        raise SystemExit(f"Already exists: {md_path.relative_to(REPO_ROOT)} or .py")

    url = f"https://leetcode.com/problems/{leetcode_slug(args.title)}/"
    today = date.today().isoformat()

    md = TEMPLATE_MD.read_text()
    md = md.replace("# NNN Title", f"# {pid} {args.title}")
    md = md.replace("medium · graph ·", f"{args.difficulty} · {topic} ·")
    md = md.replace("https://leetcode.com/problems/slug/", url)
    md = md.replace("- Pattern:", f"- Pattern: {args.pattern}".rstrip())
    md = md.replace("Created: YYYY-MM-DD", f"Created: {today}")
    md = md.replace("| YYYY-MM-DD | 1 |  | pass / soft / fail |  |", f"| {today} | 1 |  |  |  |")
    md_path.write_text(md)

    py = TEMPLATE_PY.read_text()
    py_path.write_text(py)

    if not PROGRESS.exists():
        raise SystemExit(f"Missing {PROGRESS}")

    title_link = f"[{args.title}]({topic}/{stem}.md)"
    row = (
        f"| {today} | {pid} | {title_link} | {topic} | {args.difficulty} "
        f"| 1 |  |  | {args.pattern} | scaffolded |\n"
    )
    text = PROGRESS.read_text()
    if not text.endswith("\n"):
        text += "\n"
    PROGRESS.write_text(text + row)

    print(md_path.relative_to(REPO_ROOT))
    print(py_path.relative_to(REPO_ROOT))
    print("appended algorithm/PROGRESS.md")


if __name__ == "__main__":
    main()
