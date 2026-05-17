#!/usr/bin/env python3
"""Validate second-pass release/publication gate evidence.

This is a local gate checker, not proof of a pushed/deployed public artifact.
It ensures the audit record explicitly keeps live/public trust-boundary items
as NOT RUN until a commit, CI run, Pages URL, and live artifact comparison have
actually been verified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_docs_index import DOCS_INDEX, extract_manifest


ROOT = Path(__file__).resolve().parents[1]
GATE_JSON = ROOT / "docs" / "audits" / "adhlbs-publication-gate-2026-05-17.json"
GATE_MD = ROOT / "docs" / "audits" / "adhlbs-publication-gate-2026-05-17.md"
REQUIRED_ITEMS = {
    "commit-hash-or-source-marker",
    "actions-pass-after-push",
    "live-pages-url-checked",
    "live-html-manifest-matches-repo",
    "live-source-copy-surfaces-match-generated",
}
ALLOWED_STATUSES = {"DONE", "PARTIAL", "NOT RUN", "BLOCKED", "OWNER DECISION REQUIRED"}


def validate_gate() -> list[str]:
    errors: list[str] = []
    if not GATE_MD.exists():
        errors.append(f"publication gate markdown missing: {GATE_MD}")
    if not GATE_JSON.exists():
        return errors + [f"publication gate JSON missing: {GATE_JSON}"]
    try:
        payload = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return errors + [f"publication gate JSON parse failed: {exc}"]
    items = payload.get("items")
    if not isinstance(items, list):
        return errors + ["publication gate items must be a list"]
    seen: set[str] = set()
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"items[{idx}] must be an object")
            continue
        iid = str(item.get("id", "")).strip()
        status = str(item.get("status", "")).strip()
        seen.add(iid)
        if status not in ALLOWED_STATUSES:
            errors.append(f"{iid or idx}: invalid status {status!r}")
        for field in ["gate", "evidence", "next_action"]:
            if not str(item.get(field, "")).strip():
                errors.append(f"{iid or idx}: missing/empty {field}")
    missing = REQUIRED_ITEMS - seen
    if missing:
        errors.append(f"publication gate missing item(s): {sorted(missing)}")

    live_items = {
        "actions-pass-after-push",
        "live-pages-url-checked",
        "live-html-manifest-matches-repo",
        "live-source-copy-surfaces-match-generated",
    }
    live_statuses = {item.get("id"): item.get("status") for item in items if isinstance(item, dict)}
    for item_id in live_items:
        if live_statuses.get(item_id) != "NOT RUN":
            errors.append(f"{item_id}: must remain NOT RUN until pushed/deployed/live-checked")

    manifest = extract_manifest(DOCS_INDEX.read_text(encoding="utf-8"))
    if not manifest:
        errors.append("local docs/index.html manifest missing")
    else:
        source_tree = manifest.get("source_tree", {})
        if not isinstance(source_tree, dict) or source_tree.get("mode") != "deterministic-source-content":
            errors.append("manifest source_tree marker is not deterministic-source-content")
        marker_status = live_statuses.get("commit-hash-or-source-marker")
        if marker_status not in {"DONE", "PARTIAL"}:
            errors.append("commit/source marker gate must be DONE or PARTIAL for local artifact")
    return errors


def main() -> int:
    errors = validate_gate()
    if errors:
        print("PUBLICATION_GATE_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    payload = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    not_run = sum(1 for item in payload["items"] if item["status"] == "NOT RUN")
    print(f"PUBLICATION_GATE_PARTIAL checked={len(payload['items'])} not_run={not_run} mode=local-gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
