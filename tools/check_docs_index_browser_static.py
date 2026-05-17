#!/usr/bin/env python3
"""Deterministic static UI parity smoke for docs/index.html.

This is not a live browser run. It verifies that the generated single-file DOM
contains the controls, data attributes, inert source URLs, CSP, and no-JS
fallback content needed by the rich UI.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from build_docs_index import DOCS_INDEX, extract_manifest
from check_adhlbs_atomics import load_atomics
from check_docs_index_offline import check_html_offline_safe


class StaticDomParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.remote_active_urls: list[str] = []
        self.data_copy_values: list[str] = []
        self.option_text: list[str] = []
        self._in_option = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        self.tags.append((tag.lower(), attr))
        if "id" in attr:
            self.ids.add(attr["id"])
        if "data-copy" in attr:
            self.data_copy_values.append(attr["data-copy"])
        if tag.lower() == "option":
            self._in_option = True
        for name in ["href", "src", "action", "formaction", "poster", "data"]:
            value = attr.get(name, "")
            if urlparse(value).scheme in {"http", "https"}:
                self.remote_active_urls.append(f"{tag}[{name}]={value}")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "option":
            self._in_option = False

    def handle_data(self, data: str) -> None:
        if self._in_option:
            text = data.strip()
            if text:
                self.option_text.append(text)


def count_attr(parser: StaticDomParser, attr_name: str) -> int:
    return sum(1 for _, attrs in parser.tags if attr_name in attrs)


def tags_with(parser: StaticDomParser, tag: str, **attrs: str) -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    for current, current_attrs in parser.tags:
        if current != tag:
            continue
        if all(current_attrs.get(key) == value for key, value in attrs.items()):
            matches.append(current_attrs)
    return matches


def check_static_dom(path: Path = DOCS_INDEX) -> list[str]:
    html_text = path.read_text(encoding="utf-8")
    data = load_atomics()
    parser = StaticDomParser()
    parser.feed(html_text)
    errors: list[str] = []

    errors.extend(check_html_offline_safe(html_text))
    if parser.remote_active_urls:
        errors.append(f"active remote URL(s) found: {parser.remote_active_urls[:5]}")
    if "<noscript" in html_text.lower():
        errors.append("unexpected noscript island; no-JS fallback should be the static rendered DOM")
    if not re.search(r'http-equiv="Content-Security-Policy"', html_text):
        errors.append("CSP meta tag missing")
    if "connect-src 'none'" not in html_text or "default-src 'none'" not in html_text:
        errors.append("offline CSP directives missing")
    if extract_manifest(html_text) is None:
        errors.append("build manifest missing")

    expected_ids = {
        "search",
        "kind",
        "stackTag",
        "toggleDensity",
        "resetBtn",
        "printBtn",
        "resultSummary",
        "stacksTable",
        "sortRisk",
        "sortStackId",
        "copyVisibleStacks",
        "collapseStackDetails",
        "copyVisibleCards",
        "expandAll",
        "collapseAll",
        "copyAllPacks",
        "copyVisiblePacks",
        "collapsePackDetails",
        "sourcesTable",
        "copyVisibleSources",
        "copySourceKeys",
        "common-tasks",
        "prompt-guidance-not-enforcement",
    }
    missing_ids = sorted(expected_ids - parser.ids)
    if missing_ids:
        errors.append(f"required UI id(s) missing: {missing_ids}")

    expected_counts = {
        "data-card-id": len(data["directives"]),
        "data-stack-id": len(data["stacks"]),
        "data-pack-id": len(data["prompt_packs"]),
        "data-source-id": len(data["sources"]),
        "data-common-task-id": len(data["sections"].get("common_tasks", [])),
    }
    for attr, expected in expected_counts.items():
        actual = count_attr(parser, attr)
        if actual != expected:
            errors.append(f"{attr} count mismatch: expected {expected}, got {actual}")

    for category in data["sections"].get("categories", []):
        if category["name"] not in parser.option_text:
            errors.append(f"category option missing: {category['name']}")
    for tag in data["sections"].get("stack_tags", []):
        if not tags_with(parser, "option", value=tag["value"]):
            errors.append(f"stack workstream option missing: {tag['value']}")

    if len([value for value in parser.data_copy_values if value.strip()]) < 50:
        errors.append("too few non-empty data-copy controls")
    if 'id="copyAllPacks"' not in html_text or 'id="copyVisiblePacks"' not in html_text:
        errors.append("prompt pack copy controls missing")
    if html_text.count('data-copy-kind="terse"') != len(data["directives"]):
        errors.append("terse copy button count does not match directives")
    if html_text.count("<details") < len(data["directives"]) + len(data["prompt_packs"]):
        errors.append("details expand/collapse coverage appears too low")
    if "<main" not in html_text or html_text.find('data-card-id=') > html_text.find("<script>\n(function"):
        errors.append("no-JS fallback content is not statically rendered before active script")
    if "function updateFilter()" not in html_text or "stackTag?.addEventListener('change'" not in html_text:
        errors.append("filtering script hooks missing")
    if "window.print()" not in html_text:
        errors.append("print control hook missing")
    if "navigator.clipboard.writeText" not in html_text or "document.execCommand('copy')" not in html_text:
        errors.append("copy behavior hooks missing")
    if "source URLs are inert" not in html_text and "URLs are inert" not in html_text:
        errors.append("source table inert-link copy missing")
    if 'data-boundary-topic="prompt-guidance"' not in html_text:
        errors.append("prompt guidance enforcement-boundary row missing")

    return errors


def main() -> int:
    errors = check_static_dom()
    if errors:
        print("BROWSER_STATIC_CHECK_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    data = load_atomics()
    print(
        "BROWSER_STATIC_CHECK_OK "
        f"directives={len(data['directives'])} "
        f"stacks={len(data['stacks'])} "
        f"prompt_packs={len(data['prompt_packs'])} "
        f"sources={len(data['sources'])} "
        f"common_tasks={len(data['sections'].get('common_tasks', []))} "
        "mode=static-dom"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
