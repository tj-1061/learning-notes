#!/usr/bin/env python3
"""Parse LeetCode submission dump into JSON + summary stats."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

RAW = Path(__file__).with_name("leetcode-submissions.raw.txt")
OUT = Path(__file__).with_name("leetcode-submissions.json")

DIFF = {"简单": "easy", "中等": "medium", "困难": "hard"}
RESULT = {
    "通过": "pass",
    "超出时间限制": "tle",
    "解答错误": "wa",
}

SQL_IDS = {
    175, 176, 177, 178, 180, 181, 182, 183, 184, 185, 196, 197, 262,
    511, 512, 534, 550, 569, 570, 571, 574, 577, 578, 579, 580, 584, 585,
    586, 595, 596, 597, 601, 602, 603, 607, 608, 610, 612, 613, 614, 615,
    618, 619, 620, 626, 627, 1045, 1050, 1068, 1069, 1070, 1075, 1076, 1077,
    1082, 1083, 1084, 1098, 1112, 1113, 1126, 1141, 1142, 1148, 1158, 1164,
    1173, 1174, 1179, 1193, 1204, 1211, 1212, 1225, 1241, 1251, 1264, 1270,
    1280, 1285, 1294, 1303, 1308, 1321, 1322, 1327, 1341, 1350, 1369, 1378,
    1384, 1393, 1398, 1407, 1412, 1421, 1435, 1440, 1445, 1454, 1459, 1484,
    1495, 1501, 1511, 1517, 1527, 1532, 1543, 1549, 1565, 1571, 1581, 1587,
    1596, 1607, 1613, 1633, 1661, 1667, 1677, 1683, 1693, 1709, 1715, 1729,
    1731, 1741, 1747, 1757, 1767, 1777, 1783, 1789, 1795, 1821, 1831, 1867,
    1873, 1890, 1907, 1934, 1949, 1951, 1965, 1972, 1978, 1988, 2010, 2026,
    2329, 2339, 2356, 2377, 2687,
}

# Interview-pattern tags for algorithm problems (id -> pattern). Unlisted = other.
PATTERN = {
    1: "hash", 3: "sliding-window", 5: "dp-string", 11: "two-pointers",
    15: "two-pointers", 20: "stack", 21: "linked-list", 23: "heap",
    25: "linked-list", 26: "two-pointers", 27: "two-pointers", 33: "binary-search",
    34: "binary-search", 35: "binary-search", 42: "stack", 48: "array",
    49: "hash", 53: "dp", 56: "intervals", 70: "dp", 73: "array",
    75: "two-pointers", 76: "sliding-window", 78: "backtracking", 88: "two-pointers",
    94: "tree", 98: "tree", 100: "tree", 101: "tree", 102: "tree",
    104: "tree", 105: "tree", 106: "tree", 108: "tree", 112: "tree",
    121: "array", 122: "greedy", 123: "dp", 125: "two-pointers", 128: "union-find",
    133: "graph", 134: "greedy", 136: "bit", 138: "linked-list", 139: "dp",
    141: "linked-list", 142: "linked-list", 146: "design", 150: "stack",
    152: "dp", 153: "binary-search", 155: "stack", 160: "linked-list",
    167: "two-pointers", 169: "array", 198: "dp", 199: "tree", 200: "graph",
    206: "linked-list", 207: "graph", 208: "trie", 210: "graph", 215: "heap",
    217: "hash", 226: "tree", 230: "tree", 235: "tree", 236: "tree",
    238: "array", 239: "sliding-window", 242: "hash", 297: "tree",
    300: "dp", 322: "dp", 347: "heap", 380: "design", 416: "dp",
    417: "graph", 424: "sliding-window", 435: "intervals", 438: "sliding-window",
    460: "design", 543: "tree", 560: "prefix", 572: "tree", 621: "heap",
    704: "binary-search", 739: "stack", 763: "greedy", 875: "binary-search",
    981: "binary-search", 994: "graph", 1143: "dp",
}

BLIND_75 = {
    1, 3, 5, 11, 15, 20, 21, 23, 33, 39, 42, 48, 49, 53, 54, 56, 57, 70,
    73, 76, 79, 98, 100, 102, 104, 105, 121, 124, 125, 127, 128, 133, 139,
    141, 143, 152, 153, 190, 191, 198, 200, 206, 207, 208, 211, 212, 213,
    217, 226, 230, 238, 242, 252, 253, 261, 268, 269, 271, 295, 297, 300,
    322, 323, 338, 347, 371, 417, 424, 435, 572, 647, 973,
}

NEETCODE_150 = BLIND_75 | {
    2, 4, 7, 8, 13, 14, 19, 22, 24, 25, 26, 27, 28, 35, 36, 46, 50, 55,
    62, 66, 74, 75, 78, 84, 90, 91, 94, 101, 110, 124, 131, 134, 136, 138,
    143, 146, 150, 155, 167, 169, 189, 199, 202, 210, 215, 230, 235, 236,
    239, 287, 310, 355, 416, 543, 567, 621, 703, 704, 739, 743, 746, 763,
    778, 846, 853, 875, 973, 981, 994, 1046, 1143, 1448, 1584, 1851, 1899,
}


def parse_date(token: str) -> str:
    if token.endswith("月") is False and "月" in token and token.endswith("日"):
        # 7月5日 → assume 2026 (most recent dump before Aug 2026)
        m = re.match(r"(\d+)月(\d+)日", token)
        if m:
            return f"2026-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    m = re.match(r"(\d{4})\.(\d{2})\.(\d{2})", token)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    raise ValueError(token)


def parse_id_title(line: str) -> tuple[str, str]:
    line = line.strip()
    m = re.match(r"^(LCR\s+\d+)\.\s*(.+)$", line)
    if m:
        return m.group(1).replace(" ", ""), m.group(2).strip()
    m = re.match(r"^(面试题\s+[\d.]+)\s+(.+)$", line)
    if m:
        return m.group(1), m.group(2).strip()
    m = re.match(r"^(\d+)\.\s*(.+)$", line)
    if m:
        return m.group(1), m.group(2).strip()
    raise ValueError(line)


def track(pid: str) -> str:
    if pid.startswith("LCR") or pid.startswith("面试题"):
        return "lccn"
    try:
        n = int(pid)
    except ValueError:
        return "other"
    if n in SQL_IDS:
        return "sql"
    return "algorithm"


def main() -> None:
    text = RAW.read_text()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # drop header lines
    start = 0
    for i, ln in enumerate(lines):
        if ln.endswith("日") or re.match(r"\d{4}\.\d{2}\.\d{2}", ln):
            start = i
            break
    lines = lines[start:]

    rows = []
    i = 0
    while i < len(lines):
        date_s = parse_date(lines[i])
        pid, title = parse_id_title(lines[i + 1])
        diff = DIFF[lines[i + 2]]
        result = RESULT[lines[i + 3]]
        nsub = int(lines[i + 4])
        kind = track(pid)
        rec = {
            "date": date_s,
            "id": pid,
            "title": title,
            "difficulty": diff,
            "result": result,
            "submissions": nsub,
            "track": kind,
        }
        try:
            n = int(pid)
            rec["pattern"] = PATTERN.get(n, "")
            rec["blind75"] = n in BLIND_75
            rec["neetcode150"] = n in NEETCODE_150
        except ValueError:
            rec["pattern"] = ""
            rec["blind75"] = False
            rec["neetcode150"] = False
        rows.append(rec)
        i += 5

    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")

    alg = [r for r in rows if r["track"] == "algorithm"]
    sql = [r for r in rows if r["track"] == "sql"]
    failed = [r for r in rows if r["result"] != "pass"]
    print(f"parsed={len(rows)} algorithm={len(alg)} sql={len(sql)} other={len(rows)-len(alg)-len(sql)}")
    print("algo difficulty", Counter(r["difficulty"] for r in alg))
    print("sql difficulty", Counter(r["difficulty"] for r in sql))
    print("failed", [(r["id"], r["title"], r["result"], r["submissions"]) for r in failed])
    print("blind75 in dump", sum(1 for r in rows if r["blind75"]))
    print("neetcode150 in dump", sum(1 for r in rows if r["neetcode150"]))


if __name__ == "__main__":
    main()
