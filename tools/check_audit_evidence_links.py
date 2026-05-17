#!/usr/bin/env python3
"""Check committed docs do not use local absolute paths as evidence links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "CHANGELOG.md",
    ROOT / "README.md",
    ROOT / "docs" / "audits",
]
LOCAL_PATH_RE = re.compile(r"C:(?:\\\\|/)+adhlbs", re.IGNORECASE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-16")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in SCAN_PATHS:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
            files.extend(sorted(path.rglob("*.json")))
        elif path.exists():
            files.append(path)
    return files


def validate_links() -> list[str]:
    errors: list[str] = []
    for path in iter_markdown_files():
        text = read_text(path)
        for idx, line in enumerate(text.splitlines(), start=1):
            if LOCAL_PATH_RE.search(line):
                rel = path.relative_to(ROOT).as_posix()
                errors.append(f"{rel}:{idx}: local absolute path found")
    return errors


def main() -> int:
    errors = validate_links()
    if errors:
        print("AUDIT_EVIDENCE_LINKS_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"AUDIT_EVIDENCE_LINKS_OK files={len(iter_markdown_files())} mode=repo-relative")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
