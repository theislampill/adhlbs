#!/usr/bin/env python3
"""Offline-safety scanner for docs/index.html."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = ROOT / "docs" / "index.html"

FORBIDDEN_TEXT_PATTERNS = [
    ("script src", re.compile(r"<script\b[^>]*\bsrc\s*=", re.I)),
    ("stylesheet link", re.compile(r"<link\b[^>]*\brel\s*=\s*['\"]?stylesheet", re.I)),
    ("css import", re.compile(r"@import\b", re.I)),
    ("img tag", re.compile(r"<img\b", re.I)),
    ("iframe tag", re.compile(r"<iframe\b", re.I)),
    ("fetch", re.compile(r"\bfetch\s*\(", re.I)),
    ("XMLHttpRequest", re.compile(r"\bXMLHttpRequest\b")),
    ("WebSocket", re.compile(r"\bWebSocket\b")),
    ("EventSource", re.compile(r"\bEventSource\b")),
    ("sendBeacon", re.compile(r"\bsendBeacon\s*\(", re.I)),
    ("serviceWorker", re.compile(r"\bnavigator\.serviceWorker\b", re.I)),
    ("dynamic import", re.compile(r"\bimport\s*\(", re.I)),
]

NETWORK_ATTRS = {"href", "src", "action", "formaction", "poster", "data"}


class ActiveUrlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() in {"img", "iframe"}:
            self.errors.append(f"forbidden active tag <{tag}>")
        if tag.lower() == "script" and attr_map.get("src"):
            self.errors.append("forbidden external script src")
        if tag.lower() == "link" and attr_map.get("rel", "").lower() == "stylesheet":
            self.errors.append("forbidden external stylesheet link")
        for name, value in attr_map.items():
            if name not in NETWORK_ATTRS:
                continue
            parsed = urlparse(value)
            if parsed.scheme in {"http", "https"}:
                self.errors.append(f"active remote URL in {tag}[{name}]={value!r}")


def check_html_offline_safe(html_text: str) -> list[str]:
    errors: list[str] = []
    for label, pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(html_text):
            errors.append(f"forbidden token/pattern: {label}")
    parser = ActiveUrlParser()
    parser.feed(html_text)
    errors.extend(parser.errors)
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_HTML
    html_text = path.read_text(encoding="utf-8")
    errors = check_html_offline_safe(html_text)
    if errors:
        print(f"OFFLINE_CHECK_FAILED {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"OFFLINE_CHECK_OK {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
