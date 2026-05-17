#!/usr/bin/env python3
"""Check that docs/index.html matches a fresh atomics build."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from build_docs_index import ROOT, DOCS_INDEX, build_manifest, extract_manifest, render_html, validate_generated_html
from check_adhlbs_atomics import load_atomics, validate_atomics


def main() -> int:
    data = load_atomics(ROOT)
    errors = validate_atomics(data, root=ROOT, check_generated_presence=False)
    if errors:
        print("FRESHNESS_ABORTED_ATOMICS_INVALID", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    html_text = render_html(data)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".html") as handle:
        temp_path = Path(handle.name)
        handle.write(html_text)
    tmp_errors = validate_generated_html(temp_path.read_text(encoding="utf-8"), data)
    if tmp_errors:
        print(f"FRESHNESS_ABORTED_TMP_INVALID tmp={temp_path}", file=sys.stderr)
        for error in tmp_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    current = DOCS_INDEX.read_text(encoding="utf-8") if DOCS_INDEX.exists() else ""
    if current != html_text:
        print("DOCS_INDEX_STALE", file=sys.stderr)
        print("Regenerate with: python tools/build_docs_index.py", file=sys.stderr)
        print(f"Fresh temp output: {temp_path}", file=sys.stderr)
        return 1
    manifest = extract_manifest(current)
    expected_manifest = build_manifest(data)
    if manifest != expected_manifest:
        print("DOCS_INDEX_MANIFEST_STALE", file=sys.stderr)
        print("Regenerate with: python tools/build_docs_index.py", file=sys.stderr)
        print(f"Fresh temp output: {temp_path}", file=sys.stderr)
        return 1
    temp_path.unlink(missing_ok=True)
    counts = expected_manifest["counts"]
    print(
        "FRESHNESS_OK docs/index.html matches atomics build "
        f"directives={counts['directives']} "
        f"stacks={counts['stacks']} "
        f"prompt_packs={counts['prompt_packs']} "
        f"sources={counts['sources']} "
        f"common_tasks={counts['common_tasks']} "
        f"schema_version={expected_manifest['schema_version']} "
        f"generator_hash={expected_manifest['generator_hash'][:16]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
