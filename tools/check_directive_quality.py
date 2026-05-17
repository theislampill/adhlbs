#!/usr/bin/env python3
"""Validate directive/stacks/prompt-pack quality audit coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from check_adhlbs_atomics import load_atomics, norm


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "docs" / "audits" / "adhlbs-directive-quality-audit-2026-05-17.json"
REPORT_MD = ROOT / "docs" / "audits" / "adhlbs-directive-quality-audit-2026-05-17.md"
ALLOWED_STATUSES = {"keep", "merge", "split", "strengthen", "deprecate"}


def expected_ids() -> dict[str, str]:
    data = load_atomics()
    expected: dict[str, str] = {}
    for label in ["directives", "stacks", "prompt_packs"]:
        record_type = {"directives": "directive", "stacks": "stack", "prompt_packs": "prompt_pack"}[label]
        for record in data[label]:
            expected[norm(record.get("id"))] = record_type
    return expected


def validate_report() -> list[str]:
    errors: list[str] = []
    if not REPORT_MD.exists():
        errors.append(f"quality audit markdown missing: {REPORT_MD}")
    if not REPORT_JSON.exists():
        return errors + [f"quality audit JSON missing: {REPORT_JSON}"]
    try:
        payload = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return errors + [f"quality audit JSON parse failed: {exc}"]
    records = payload.get("records")
    if not isinstance(records, list):
        return errors + ["quality audit JSON records must be a list"]
    expected = expected_ids()
    seen: dict[str, str] = {}
    for idx, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"records[{idx}] must be an object")
            continue
        rid = norm(record.get("id"))
        status = norm(record.get("status"))
        record_type = norm(record.get("type"))
        if rid in seen:
            errors.append(f"quality audit duplicate id {rid!r}")
        seen[rid] = record_type
        if rid not in expected:
            errors.append(f"quality audit unknown id {rid!r}")
        elif expected[rid] != record_type:
            errors.append(f"quality audit {rid}: expected type {expected[rid]!r}, got {record_type!r}")
        if status not in ALLOWED_STATUSES:
            errors.append(f"quality audit {rid}: invalid status {status!r}")
        for field in ["concrete_action", "when_to_use", "blocks", "negative_example", "source_refs", "verification_hook", "overlap"]:
            if field not in record:
                errors.append(f"quality audit {rid}: missing {field}")
    missing = sorted(set(expected) - set(seen))
    if missing:
        errors.append(f"quality audit missing id(s): {missing[:20]}")
    patched = payload.get("patched_high_impact_ids", [])
    if not isinstance(patched, list) or len(patched) < 5:
        errors.append("quality audit must record at least five patched_high_impact_ids")
    else:
        unknown_patched = sorted(set(norm(item) for item in patched) - set(expected))
        if unknown_patched:
            errors.append(f"quality audit patched_high_impact_ids include unknown id(s): {unknown_patched}")
    backlog = payload.get("remaining_backlog_ids", [])
    if not isinstance(backlog, list):
        errors.append("quality audit remaining_backlog_ids must be a list")
    else:
        expected_backlog = sorted(
            norm(record.get("id"))
            for record in records
            if isinstance(record, dict) and norm(record.get("status")) != "keep"
        )
        actual_backlog = sorted(norm(item) for item in backlog)
        if actual_backlog != expected_backlog:
            errors.append("quality audit remaining_backlog_ids must exactly match non-keep record ids")
    return errors


def main() -> int:
    errors = validate_report()
    if errors:
        print("DIRECTIVE_QUALITY_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    payload = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for record in payload["records"]:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    print(
        "DIRECTIVE_QUALITY_OK "
        f"records={len(payload['records'])} "
        f"patched_high_impact={len(payload['patched_high_impact_ids'])} "
        f"statuses={counts}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
