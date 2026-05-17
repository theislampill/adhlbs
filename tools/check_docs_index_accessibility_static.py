#!/usr/bin/env python3
"""Static accessibility smoke for docs/index.html.

This check is intentionally dependency-free. It does not replace a screen
reader, contrast, or assistive-technology pass; it verifies that the generated
single-file artifact keeps the semantic controls and keyboard/fallback hooks
needed for a credible local accessibility smoke.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from build_docs_index import DOCS_INDEX


class A11yParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.ids: set[str] = set()
        self.labels_for: set[str] = set()
        self.buttons: list[dict[str, str]] = []
        self.controls: list[dict[str, str]] = []
        self.details_count = 0
        self.summary_count = 0
        self.positive_tabindex: list[str] = []
        self._button_stack: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {key.lower(): value or "" for key, value in attrs}
        self.tags.append((tag, attr))
        if "id" in attr:
            self.ids.add(attr["id"])
        if tag == "label" and attr.get("for"):
            self.labels_for.add(attr["for"])
        if tag == "button":
            current = dict(attr)
            current["_text"] = ""
            self._button_stack.append(current)
        if tag in {"input", "select", "textarea"}:
            self.controls.append(attr)
        if tag == "details":
            self.details_count += 1
        if tag == "summary":
            self.summary_count += 1
        tabindex = attr.get("tabindex")
        if tabindex and tabindex.lstrip("+").isdigit() and int(tabindex) > 0:
            self.positive_tabindex.append(f"{tag}#{attr.get('id', '')}[tabindex={tabindex}]")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "button" and self._button_stack:
            self.buttons.append(self._button_stack.pop())

    def handle_data(self, data: str) -> None:
        if self._button_stack:
            self._button_stack[-1]["_text"] += data


def has_label(control: dict[str, str], labels_for: set[str]) -> bool:
    cid = control.get("id", "")
    return bool(
        control.get("aria-label", "").strip()
        or control.get("aria-labelledby", "").strip()
        or (cid and cid in labels_for)
    )


def check_accessibility_static(path: Path = DOCS_INDEX) -> list[str]:
    html_text = path.read_text(encoding="utf-8")
    parser = A11yParser()
    parser.feed(html_text)
    errors: list[str] = []

    if not any(tag == "main" and attrs.get("id") == "main" and attrs.get("tabindex") == "-1" for tag, attrs in parser.tags):
        errors.append("main landmark with id=main and tabindex=-1 is missing")
    if not any(tag == "a" and attrs.get("class") == "skip-link" and attrs.get("href") == "#main" for tag, attrs in parser.tags):
        errors.append("skip link to #main is missing")
    if parser.positive_tabindex:
        errors.append(f"positive tabindex found: {parser.positive_tabindex[:5]}")

    unlabeled_controls = [
        control.get("id", "<unnamed>")
        for control in parser.controls
        if control.get("type") != "hidden" and not has_label(control, parser.labels_for)
    ]
    if unlabeled_controls:
        errors.append(f"form controls missing labels: {unlabeled_controls}")

    unlabeled_buttons = [
        button.get("id") or button.get("class", "<button>")
        for button in parser.buttons
        if not (button.get("aria-label", "").strip() or button.get("_text", "").strip())
    ]
    if unlabeled_buttons:
        errors.append(f"buttons missing accessible name: {unlabeled_buttons[:10]}")

    if parser.summary_count < parser.details_count:
        errors.append(f"details/summary mismatch: details={parser.details_count} summary={parser.summary_count}")
    if 'aria-live="polite"' not in html_text:
        errors.append("aria-live status region missing")
    if ":focus-visible" not in html_text or "outline:" not in html_text:
        errors.append("visible focus CSS missing")
    if "@media (prefers-reduced-motion: reduce)" not in html_text:
        errors.append("reduced-motion CSS hook missing")
    if "document.addEventListener('keydown'" not in html_text:
        errors.append("keyboard shortcut listener missing")
    for key in ["Escape", "search?.focus()", "window.print()", "resetBtn"]:
        if key not in html_text:
            errors.append(f"keyboard/print/reset hook missing: {key}")
    if "data-card-id=" not in html_text or html_text.find("data-card-id=") > html_text.find("<script>\n(function"):
        errors.append("no-JS fallback content is not statically rendered before script")
    if re.search(r"<a\s[^>]*href=[\"']https?://", html_text, flags=re.IGNORECASE):
        errors.append("active external link found; source URLs should remain inert text")

    return errors


def main() -> int:
    errors = check_accessibility_static()
    if errors:
        print("ACCESSIBILITY_STATIC_CHECK_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "ACCESSIBILITY_STATIC_CHECK_OK "
        "semantic_controls=checked labels=checked focusability=checked "
        "keyboard_hooks=checked no_keyboard_trap=static-only no_js_fallback=checked mode=static-only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
