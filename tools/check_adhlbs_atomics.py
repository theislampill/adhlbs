#!/usr/bin/env python3
"""Validate ADHLBS atomic records.

The checker is intentionally dependency-free. It validates the canonical JSON
records and, when docs/index.html already exists, checks that generated records
are represented in the public artifact.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ATOMICS = ROOT / "atomics"
GENERATED_BANNER = (
    "<!-- GENERATED FILE: do not hand-edit docs/index.html. "
    "Edit atomics/** and run tools/build_docs_index.py. -->"
)

ALLOWED_RISKS = {"Low", "Medium", "High", "Critical"}
ALLOWED_STABILITY = {"stable", "volatile", "candidate"}
REQUIRED = {
    "directives": [
        "id",
        "html_id",
        "kind",
        "name",
        "expansion",
        "why",
        "directive",
        "use",
        "blocks",
        "tags",
        "source_class",
        "related",
        "negative_example",
        "source_refs",
    ],
    "stacks": ["id", "html_id", "name", "risk", "tag", "stack", "use", "avoid", "stop"],
    "prompt_packs": ["id", "html_id", "title", "tag", "risk", "source_refs", "variants"],
    "sources": [
        "id",
        "title",
        "url",
        "source_type",
        "stability",
        "notes",
        "supports",
        "last_checked",
        "trust",
    ],
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - reported as validation error
        raise ValueError(f"{path}: JSON parse failed: {exc}") from exc


def records_file(name: str) -> Path:
    return ATOMICS / f"{name}.json"


def load_atomics(root: Path = ROOT) -> dict[str, object]:
    atomics = root / "atomics"
    data = {
        "directives": load_json(atomics / "directives.json")["records"],
        "stacks": load_json(atomics / "stacks.json")["records"],
        "prompt_packs": load_json(atomics / "prompt_packs.json")["records"],
        "sources": load_json(atomics / "sources.json")["records"],
        "sections": load_json(atomics / "sections.json"),
        "ui_copy": load_json(atomics / "ui_copy.json"),
        "schema": load_json(atomics / "adhlbs.schema.json"),
    }
    return data


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def search_text(*parts: object) -> str:
    flattened: list[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, dict):
            flattened.extend(search_text(v) for v in part.values())
        elif isinstance(part, (list, tuple, set)):
            flattened.extend(search_text(v) for v in part)
        else:
            flattened.append(norm(html.unescape(str(part))).lower())
    return norm(" ".join(flattened))


def directive_copy(record: dict[str, object]) -> str:
    name = norm(record.get("name"))
    expansion = norm(record.get("expansion"))
    directive = norm(record.get("directive"))
    if expansion:
        return f"{name} \u2014 {expansion}\n{directive}"
    return f"{name}\n{directive}"


def directive_terse_copy(record: dict[str, object]) -> str:
    return f"{norm(record.get('name'))}: {norm(record.get('directive'))}"


def stack_short_copy(record: dict[str, object]) -> str:
    return f"{norm(record.get('name'))}: {norm(record.get('stack'))}"


def stack_full_copy(record: dict[str, object]) -> str:
    return (
        f"{norm(record.get('id'))} \u2014 {norm(record.get('name'))}\n"
        f"Stack: {norm(record.get('stack'))}\n"
        f"Use: {norm(record.get('use'))}\n"
        f"Avoid: {norm(record.get('avoid'))}\n"
        f"Stop: {norm(record.get('stop'))}"
    )


def pack_copy(record: dict[str, object]) -> str:
    header = f"{norm(record.get('id'))} \u2014 {norm(record.get('title'))}"
    chunks = []
    for idx, variant in enumerate(record.get("variants", [])):
        label = norm(variant.get("label"))
        if idx > 0 and "variant" in label.lower():
            label = "Variants"
        body = norm(variant.get("body"))
        chunks.append(f"{label}:\n{body}")
    return header + "\n" + "\n\n".join(chunks)


def source_url_copy(record: dict[str, object]) -> str:
    return norm(record.get("url"))


def duplicate_errors(label: str, records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, int] = {}
    for idx, record in enumerate(records, start=1):
        rid = norm(record.get("id"))
        if rid in seen:
            errors.append(f"{label}: duplicate id {rid!r} at records {seen[rid]} and {idx}")
        seen[rid] = idx
    return errors


def required_errors(label: str, records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for idx, record in enumerate(records, start=1):
        rid = norm(record.get("id")) or f"record {idx}"
        for field in REQUIRED[label]:
            if field not in record:
                errors.append(f"{label}:{rid}: missing required field {field}")
                continue
            value = record[field]
            if isinstance(value, str) and not value.strip():
                errors.append(f"{label}:{rid}: empty required field {field}")
            elif isinstance(value, list) and not value and field in {"tags", "variants", "supports"}:
                errors.append(f"{label}:{rid}: empty required list {field}")
    return errors


def validate_url(source: dict[str, object]) -> str | None:
    url = norm(source.get("url"))
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return f"sources:{source.get('id')}: malformed URL field {url!r}"
    return None


def validate_atomics(
    data: dict[str, object],
    *,
    root: Path = ROOT,
    check_generated_presence: bool = True,
) -> list[str]:
    errors: list[str] = []
    directives = list(data["directives"])
    stacks = list(data["stacks"])
    packs = list(data["prompt_packs"])
    sources = list(data["sources"])
    sections = dict(data["sections"])

    for label, records in [
        ("directives", directives),
        ("stacks", stacks),
        ("prompt_packs", packs),
        ("sources", sources),
    ]:
        errors.extend(duplicate_errors(label, records))
        errors.extend(required_errors(label, records))

    directive_ids = {norm(r.get("id")) for r in directives}
    source_ids = {norm(r.get("id")) for r in sources}
    categories = {norm(c.get("name")) for c in sections.get("categories", [])}
    stack_tags = {norm(t.get("value")) for t in sections.get("stack_tags", [])}

    for record in directives:
        rid = norm(record.get("id"))
        if norm(record.get("kind")) not in categories:
            errors.append(f"directives:{rid}: unknown category/kind {record.get('kind')!r}")
        if not norm(record.get("directive")):
            errors.append(f"directives:{rid}: empty directive text")
        if any(len(norm(tag)) == 1 for tag in record.get("tags", [])):
            errors.append(f"directives:{rid}: probable split-character tag list {record.get('tags')!r}")
        for related in record.get("related", []):
            if norm(related) not in directive_ids:
                errors.append(f"directives:{rid}: broken related id {related!r}")
        for ref in record.get("source_refs", []):
            if norm(ref) not in source_ids:
                errors.append(f"directives:{rid}: unknown source ref {ref!r}")
        if "copy_text" in record and norm(record["copy_text"]) != directive_copy(record):
            errors.append(f"directives:{rid}: copy_text override does not match derived copy")
        if "terse_copy" in record and norm(record["terse_copy"]) != directive_terse_copy(record):
            errors.append(f"directives:{rid}: terse_copy override does not match derived copy")

    for record in stacks:
        rid = norm(record.get("id"))
        if "\u2605" in norm(record.get("name")):
            errors.append(f"stacks:{rid}: recommendation marker must not be part of canonical name")
        if norm(record.get("risk")) not in ALLOWED_RISKS:
            errors.append(f"stacks:{rid}: invalid risk {record.get('risk')!r}")
        if norm(record.get("tag")) not in stack_tags:
            errors.append(f"stacks:{rid}: unknown stack tag {record.get('tag')!r}")
        if "copy_text" in record and norm(record["copy_text"]) != stack_full_copy(record):
            errors.append(f"stacks:{rid}: copy_text override does not match derived copy")

    for record in packs:
        rid = norm(record.get("id"))
        if norm(record.get("risk")) not in ALLOWED_RISKS:
            errors.append(f"prompt_packs:{rid}: invalid risk {record.get('risk')!r}")
        for ref in record.get("source_refs", []):
            if norm(ref) not in source_ids:
                errors.append(f"prompt_packs:{rid}: unknown source ref {ref!r}")
        for idx, variant in enumerate(record.get("variants", []), start=1):
            if not norm(variant.get("label")):
                errors.append(f"prompt_packs:{rid}: variant {idx} missing label")
            if not norm(variant.get("body")):
                errors.append(f"prompt_packs:{rid}: variant {idx} missing body")
        labels = [norm(variant.get("label")) for variant in record.get("variants", [])]
        if labels != ["Normal", "Strict", "Exploratory"]:
            errors.append(f"prompt_packs:{rid}: expected Normal, Strict, Exploratory variants; got {labels!r}")
        if "copy_text" in record and norm(record["copy_text"]) != pack_copy(record):
            errors.append(f"prompt_packs:{rid}: copy_text override does not match derived copy")

    for record in sources:
        rid = norm(record.get("id"))
        if norm(record.get("stability")).lower() not in ALLOWED_STABILITY:
            errors.append(f"sources:{rid}: invalid stability {record.get('stability')!r}")
        url_error = validate_url(record)
        if url_error:
            errors.append(url_error)
        if "copy_text" in record and norm(record["copy_text"]) != source_url_copy(record):
            errors.append(f"sources:{rid}: copy_text override does not match derived URL copy")

    if categories:
        missing_categories = categories - {norm(r.get("kind")) for r in directives}
        if missing_categories:
            errors.append(f"sections: categories without directive records: {sorted(missing_categories)}")

    if check_generated_presence:
        html_path = root / "docs" / "index.html"
        if html_path.exists():
            page = html_path.read_text(encoding="utf-8")
            if GENERATED_BANNER in page:
                for record in directives:
                    rid = norm(record.get("id"))
                    if f'data-card-id="{html.escape(rid, quote=True)}"' not in page:
                        errors.append(f"generated html: directive {rid} is not represented")
                for record in stacks:
                    rid = norm(record.get("id"))
                    if f'data-stack-id="{html.escape(rid, quote=True)}"' not in page:
                        errors.append(f"generated html: stack {rid} is not represented")
                for record in packs:
                    rid = norm(record.get("id"))
                    if f'data-pack-id="{html.escape(rid, quote=True)}"' not in page:
                        errors.append(f"generated html: prompt pack {rid} is not represented")
                for record in sources:
                    rid = norm(record.get("id"))
                    if f'data-source-id="{html.escape(rid, quote=True)}"' not in page:
                        errors.append(f"generated html: source {rid} is not represented")

    return errors


def main() -> int:
    try:
        data = load_atomics(ROOT)
    except Exception as exc:
        print(f"ATOMICS_INVALID: {exc}", file=sys.stderr)
        return 1
    errors = validate_atomics(data, root=ROOT)
    if errors:
        print("ATOMICS_INVALID", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "ATOMICS_OK "
        f"directives={len(data['directives'])} "
        f"stacks={len(data['stacks'])} "
        f"prompt_packs={len(data['prompt_packs'])} "
        f"sources={len(data['sources'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
