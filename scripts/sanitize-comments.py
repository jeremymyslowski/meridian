#!/usr/bin/env python3
"""Remove evaluator spoiler comments from a blind-repo tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

LINE_PATTERNS = [
    re.compile(r"^\s*#?\s*BUG \(scenario/.*", re.I),
    re.compile(r"^\s*//?\s*BUG \(scenario/.*", re.I),
    re.compile(r"^\s*#\s*TARGET FUNCTION.*", re.I),
    re.compile(r"^\s*#\s*intentional trap.*", re.I),
    re.compile(r"^\s*#\s*BUG in test:.*", re.I),
    re.compile(r"^\s*NOTE: qa-fixtures/.*", re.I),
]

REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r'"""DECOY —[^"]*"""'), '"""Legacy user service stub."""'),
    (re.compile(r"/\*\*\s*DECOY —[^*]*\*/"), "/** Legacy user service stub. */"),
    (re.compile(r"// DECOY —[^\n]*"), "// Legacy prototype — not used in production"),
    (re.compile(r'"""Task registry fixture — intentionally large file for agent navigation tests\."""'),
     '"""Task registry — handler registration and title utilities."""'),
    (re.compile(r'"""Paginator with intentional off-by-one bug\."""'),
     '"""Paginator utilities."""'),
    (re.compile(r'"""Meridian CLI — partial implementation for scenario/10-cli-export\."""'),
     '"""Meridian CLI — admin and developer tooling."""'),
    (re.compile(r"Not implemented — complete this command for scenario 10"),
     "Not implemented"),
    (re.compile(r"raise NotImplementedError\(\"This is a qa-fixtures decoy\"\)"),
     'raise NotImplementedError("Not implemented")'),
    (re.compile(r'fmt\.Errorf\("qa-fixtures decoy: use apps/api meridian_api/services/user_service\.py"\)'),
     'fmt.Errorf("not implemented")'),
    (re.compile(r"console\.warn\('UserService\.ts is a QA fixture decoy — not wired to the API'\)"),
     "console.warn('Legacy UserService stub')"),
]

SESSION_BUG_BLOCK = re.compile(
    r"/\*\*\s*\n \* Client session configuration\.\s*\n \*\s*\n \* BUG \(scenario/01-jwt-expiry\):[^\n]*\n \*/",
    re.MULTILINE,
)


def sanitize_file(path: Path) -> bool:
    text = path.read_text()
    original = text

    if path.name == "session.ts":
        text = SESSION_BUG_BLOCK.sub(
            "/**\n * Client session configuration.\n */",
            text,
        )

    lines = text.splitlines(keepends=True)
    filtered: list[str] = []
    for line in lines:
        if any(pat.search(line) for pat in LINE_PATTERNS):
            continue
        filtered.append(line)
    text = "".join(filtered)

    for pattern, replacement in REPLACEMENTS:
        text = pattern.sub(replacement, text)

    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> int:
    if not ROOT.is_dir():
        print(f"Not a directory: {ROOT}", file=sys.stderr)
        return 1

    extensions = {".py", ".ts", ".tsx", ".go", ".js", ".md"}
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in extensions:
            continue
        if any(part in {".git", "node_modules", "__pycache__"} for part in path.parts):
            continue
        if sanitize_file(path):
            changed += 1
            print(f"  sanitized: {path.relative_to(ROOT)}")

    print(f"Sanitized {changed} file(s) under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
