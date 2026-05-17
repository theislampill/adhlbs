#!/usr/bin/env python3
"""Check source freshness metadata and review-age policy."""

from __future__ import annotations

import sys
from datetime import date

from check_adhlbs_atomics import ALLOWED_SOURCE_TYPES, ALLOWED_STABILITY, load_atomics, norm, valid_date_error


MAX_AGE_DAYS = {
    "stable": 730,
    "volatile": 180,
    "candidate": 120,
}


def check_sources() -> list[str]:
    data = load_atomics()
    errors: list[str] = []
    today = date.today()
    for record in data["sources"]:
        rid = norm(record.get("id"))
        if norm(record.get("source_type")) not in ALLOWED_SOURCE_TYPES:
            errors.append(f"sources:{rid}: invalid source_type {record.get('source_type')!r}")
        stability = norm(record.get("stability")).lower()
        if stability not in ALLOWED_STABILITY:
            errors.append(f"sources:{rid}: invalid stability {record.get('stability')!r}")
            continue
        date_error = valid_date_error("sources", rid, "last_checked", record.get("last_checked"))
        if date_error:
            errors.append(date_error)
            continue
        checked = date.fromisoformat(norm(record.get("last_checked")))
        age = (today - checked).days
        max_age = MAX_AGE_DAYS[stability]
        if age > max_age:
            errors.append(
                f"sources:{rid}: stale last_checked={checked.isoformat()} age_days={age} "
                f"max_age_days={max_age} stability={stability}"
            )
        if not record.get("supports"):
            errors.append(f"sources:{rid}: supports must name the covered directive/pack area")
    return errors


def main() -> int:
    errors = check_sources()
    if errors:
        print("SOURCE_FRESHNESS_FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    data = load_atomics()
    counts = {key: 0 for key in sorted(ALLOWED_STABILITY)}
    for record in data["sources"]:
        counts[norm(record.get("stability")).lower()] += 1
    print(
        "SOURCE_FRESHNESS_OK "
        f"sources={len(data['sources'])} "
        f"stable={counts['stable']} "
        f"volatile={counts['volatile']} "
        f"candidate={counts['candidate']} "
        f"policy_days={MAX_AGE_DAYS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
