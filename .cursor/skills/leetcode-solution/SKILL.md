---
name: leetcode-solution
description: Scaffolds and formats LeetCode algorithm solutions in this repo as markdown notes plus runnable Python, and appends attempts to algorithm/PROGRESS.md. Use when adding a LeetCode problem, formatting a solution, logging an attempt, creating a problem file, or when the user mentions LeetCode, Blind 75, NeetCode, or interview prep in learning-notes.
---

# LeetCode solution format

New algorithm work uses **markdown + Python**, not Jupyter. Existing `.ipynb` files stay as an archive; do not convert them unless the user asks. SQL stays in `database/*.md`.

## When this applies

- User asks to add, format, redo, or log a LeetCode (or NeetCode / Blind 75) problem
- User pastes a problem or a `Solution` class and wants it filed in this repo
- User asks to record time, pass/fail, or a retry

## File layout

```
algorithm/<topic>/NNN-difficulty-slug.md
algorithm/<topic>/NNN-difficulty-slug.py
algorithm/PROGRESS.md
```

- `NNN` is the LeetCode id, zero-padded to 3 digits when id < 1000, otherwise the full id (`1` → `001`, `1143` → `1143`)
- `difficulty` is `easy`, `medium`, or `hard`
- `slug` is the LeetCode title slug in kebab-case
- Do not put spaces in new filenames

### Topic folders

Reuse an existing folder when the pattern matches. Create a new folder only for a missing pattern.

| Pattern | Folder |
| --- | --- |
| Arrays, strings, two pointers, sliding window, prefix | `array and string` |
| Hash map / set | `hash map and hash set` |
| Stack / queue / monotonic stack | `stack and queue` |
| Linked list | `linked list` |
| Binary tree / BST | `binary tree` |
| 1D / 2D DP | `dynamic programming` |
| Binary search (index or answer) | `binary search` |
| Heap / Top-K | `heap` |
| Graph, BFS, DFS, topo sort | `graph` |
| Backtracking | `backtracking` |
| Intervals | `intervals` |
| Trie | `trie` |
| Union-Find | `union-find` |
| Greedy (when that is the point) | `greedy` |
| Design / parsers | `system design` |

If a problem spans topics, pick the **interview pattern** (e.g. Course Schedule → `graph`, not array).

## Workflow

1. If the files do not exist, run the scaffold (agent executes it):

```bash
python .cursor/skills/leetcode-solution/scripts/scaffold.py \
  --id 200 --title "Number of Islands" --difficulty medium --topic graph
```

2. Fill the markdown from [template.md](template.md). Keep the user's own words for approach when they provide them.
3. Put the **interview solution** in the `.py` file from [template.py](template.py): `Solution` class, type hints, `if __name__ == "__main__"` asserts. No notebook cells, no `print` of every case as the only test.
4. Append one row to `algorithm/PROGRESS.md` for this attempt. Never rewrite history of older rows.
5. Do not paste the full LeetCode statement if it is long; 2–4 sentence restatement + one example is enough. Link the official problem.

## Markdown sections (required)

Use this heading set, in this order:

```markdown
# NNN Title

difficulty · topic · [LeetCode](url) · [Doocs](url)

## Meta
## Problem
## Approach
## Complexity
## Attempts
## Notes
```

- **Meta**: pattern name, related problems (ids), date created
- **Approach**: brute force in one sentence, then the chosen idea. No tutorial filler.
- **Complexity**: time and space with the parameters named (`n` = length of `nums`)
- **Attempts**: newest first. `pass` (unaided in time), `soft` (one hint, then redo in 3 days), `fail` (editorial; redo in 7 and 21 days)
- **Notes**: what was missed vs an old notebook, or nothing if clean

## Python rules

- Match LeetCode's method name and types
- Prefer `list`, `dict`, `set`, `collections.deque`, `heapq`, `bisect`
- One primary solution. A second function is OK if labeled `brute_force_` or a named variant
- Tests are asserts on representative cases, including an edge case
- Do not import `pytest` unless the user asks

## Progress log

`algorithm/PROGRESS.md` is the source of truth for the 8-month plan. Append a markdown table row:

`| YYYY-MM-DD | id | title | topic | difficulty | attempt # | minutes | result | pattern | note |`

- `result` is exactly `pass`, `soft`, or `fail`
- `minutes` is an integer
- If the user omits time, ask once; if they still skip it, use `?`

## What not to do

- Do not create new `.ipynb` files
- Do not dump editorial text or a second copy of the solution into the markdown
- Do not solve the problem for the user on a first attempt if they asked to try it timed; scaffold the files and wait
- Do not mass-migrate old notebooks

## Redo of an old notebook

When the user redos a problem that already has a `.ipynb`:

1. Create the new `.md` + `.py` beside it (same folder if the topic still fits)
2. Leave the notebook in place
3. In **Notes**, compare to the old solution in one or two lines
4. Log the redo in `PROGRESS.md`
