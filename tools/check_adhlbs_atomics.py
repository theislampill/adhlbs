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
from datetime import date
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
ALLOWED_PROMPT_VARIANTS = ["Normal", "Strict", "Exploratory"]
PROMPT_VARIANT_GATE_TOKENS = ("Acceptance:", "Verification:", "Done when:", "Check:", "verify", "check", "stop", "deny", "retract")
STACK_QUALITY_TOKENS = (
    "verify",
    "verification",
    "check",
    "test",
    "evidence",
    "source",
    "approval",
    "authorized",
    "human",
    "allowlist",
    "gate",
    "backup",
    "rollback",
    "regression",
    "baseline",
    "behavior",
    "criteria",
    "validation",
    "limits",
    "eval",
    "smoke",
    "keyboard",
    "contrast",
    "screen-reader",
    "fresh",
    "receipt",
    "producer",
    "consumer",
    "defect",
    "root cause",
    "measured",
    "risk",
)
HIGH_RISK_STACK_GATE_TOKENS = ("approval", "authorized", "human", "allowlist", "gate", "backup", "rollback", "hitl")
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9]*(?:-[A-Z0-9]+)*$")
HTML_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CANONICAL_ATOMIC_FILES = {
    "adhlbs.schema.json",
    "directives.json",
    "prompt_packs.json",
    "sections.json",
    "sources.json",
    "stacks.json",
    "ui_copy.json",
}
INTAKE_ONLY_ATOMIC_FILES = {"extraction_findings.json"}
ALLOWED_ATOMIC_FILES = CANONICAL_ATOMIC_FILES | INTAKE_ONLY_ATOMIC_FILES
ALLOWED_SOURCE_TYPES = {
    "Agent research",
    "AI governance",
    "API design",
    "Architecture",
    "Classic SE",
    "Classic SE paper",
    "Design patterns",
    "Hermes docs",
    "IETF draft",
    "IETF RFC",
    "Knowledge management",
    "Lean / Toyota",
    "LLM security",
    "Observability",
    "Official AI docs",
    "Reliability",
    "Security",
    "Security / candidate",
    "State / data",
    "Supply chain security",
    "Testing",
    "Versioning",
    "Web architecture",
    "Web docs",
    "Web standard",
}
ALLOWED_SOURCE_CLASSES = {
    "Agent",
    "Agent research",
    "API design",
    "Architecture",
    "Architecture model",
    "Classic SE",
    "CMU SEI",
    "Compiler",
    "Data/state",
    "Government guidance",
    "IETF draft",
    "Lean",
    "NIST",
    "Official spec",
    "OpenTelemetry",
    "OWASP",
    "OWASP LLM",
    "Reliability",
    "Security",
    "Source",
    "Verification",
    "W3C / OTel",
    "Web standard",
}
ALLOWED_FIELDS = {
    "directives": {
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
        "aliases",
        "source_class",
        "recognition",
        "metadata",
        "related",
        "negative_example",
        "source_refs",
    },
    "stacks": {
        "id",
        "html_id",
        "name",
        "risk",
        "tag",
        "stack",
        "use",
        "avoid",
        "stop",
        "recommended",
    },
    "prompt_packs": {"id", "html_id", "title", "tag", "risk", "source_refs", "variants", "agent_variants", "notes"},
    "sources": {
        "id",
        "title",
        "url",
        "source_type",
        "stability",
        "notes",
        "supports",
        "last_checked",
        "trust",
    },
}
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


def validate_atomic_file_policy(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    atomics = root / "atomics"
    files = {path.name for path in atomics.glob("*.json")}
    unexpected = files - ALLOWED_ATOMIC_FILES
    missing = CANONICAL_ATOMIC_FILES - files
    if unexpected:
        errors.append(f"atomics: undocumented JSON sidecar(s): {sorted(unexpected)}")
    if missing:
        errors.append(f"atomics: missing canonical JSON file(s): {sorted(missing)}")
    sidecar = atomics / "extraction_findings.json"
    if sidecar.exists():
        try:
            payload = load_json(sidecar)
        except Exception as exc:
            errors.append(f"atomics: extraction_findings.json cannot be parsed: {exc}")
            return errors
        if not isinstance(payload, dict):
            errors.append("atomics: extraction_findings.json must be an object")
            return errors
        allowed = {"normalizations", "counts", "current_html_findings"}
        extra = set(payload) - allowed
        missing_sidecar = allowed - set(payload)
        if extra:
            errors.append(f"atomics: extraction_findings.json has unexpected key(s): {sorted(extra)}")
        if missing_sidecar:
            errors.append(f"atomics: extraction_findings.json missing key(s): {sorted(missing_sidecar)}")
        if not isinstance(payload.get("normalizations"), list):
            errors.append("atomics: extraction_findings.json normalizations must be a list")
        if not isinstance(payload.get("counts"), dict):
            errors.append("atomics: extraction_findings.json counts must be an object")
        if not isinstance(payload.get("current_html_findings"), list):
            errors.append("atomics: extraction_findings.json current_html_findings must be a list")
    return errors


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
    for variant in record.get("agent_variants", []):
        label = norm(variant.get("label"))
        body = norm(variant.get("body"))
        repo = norm(variant.get("repo_instruction_file_usage"))
        tools = norm(variant.get("approval_sandbox_tool_boundaries"))
        verification = norm(variant.get("verification_reporting_style"))
        gate = norm(variant.get("no_push_no_release_gate"))
        chunks.append(
            f"{label} agent variant:\n"
            f"{body}\n"
            f"Repo instructions: {repo}\n"
            f"Tool boundaries: {tools}\n"
            f"Verification/reporting: {verification}\n"
            f"Release gate: {gate}"
        )
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


def additional_property_errors(label: str, records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    allowed = ALLOWED_FIELDS[label]
    for idx, record in enumerate(records, start=1):
        rid = norm(record.get("id")) or f"record {idx}"
        extra = set(record) - allowed
        if extra:
            errors.append(f"{label}:{rid}: unexpected field(s): {sorted(extra)}")
    return errors


def id_pattern_errors(label: str, records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for idx, record in enumerate(records, start=1):
        rid = norm(record.get("id"))
        html_id = norm(record.get("html_id"))
        if not rid:
            continue
        if not ID_RE.fullmatch(rid):
            errors.append(f"{label}:{rid or idx}: id does not match {ID_RE.pattern}")
        if html_id and not HTML_ID_RE.fullmatch(html_id):
            errors.append(f"{label}:{rid}: html_id does not match {HTML_ID_RE.pattern}")
        if html_id and html_id != rid.lower():
            errors.append(f"{label}:{rid}: html_id must be lowercase id; got {html_id!r}")
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


def valid_date_error(label: str, rid: str, field: str, value: object) -> str | None:
    text_value = norm(value)
    if not DATE_RE.fullmatch(text_value):
        return f"{label}:{rid}: {field} must be YYYY-MM-DD; got {text_value!r}"
    try:
        parsed = date.fromisoformat(text_value)
    except ValueError:
        return f"{label}:{rid}: {field} is not a valid calendar date: {text_value!r}"
    if parsed > date.today():
        return f"{label}:{rid}: {field} is in the future: {text_value!r}"
    return None


def validate_url(source: dict[str, object]) -> str | None:
    url = norm(source.get("url"))
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return f"sources:{source.get('id')}: malformed URL field {url!r}"
    return None


def collect_ids(value: object, path: str = "atomics") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        if isinstance(value.get("id"), str):
            found.append((value["id"], path))
        for key, child in value.items():
            found.extend(collect_ids(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for idx, child in enumerate(value, start=1):
            found.extend(collect_ids(child, f"{path}[{idx}]"))
    return found


def cross_duplicate_errors(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    candidates: list[tuple[str, str]] = []
    for label in ["directives", "stacks", "prompt_packs", "sources"]:
        candidates.extend(collect_ids(data[label], label))
    candidates.extend(collect_ids(data["sections"], "sections"))
    candidates.extend(collect_ids(data["ui_copy"], "ui_copy"))
    seen: dict[str, str] = {}
    for rid, path in candidates:
        nrid = norm(rid)
        if not nrid:
            continue
        if nrid in seen:
            errors.append(f"atomics: duplicate id {nrid!r} appears at {seen[nrid]} and {path}")
        seen[nrid] = path
    return errors


def collect_field_refs(value: object, field: str, path: str = "atomics") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        if field in value and isinstance(value[field], list):
            found.extend((norm(item), f"{path}.{field}") for item in value[field])
        for key, child in value.items():
            found.extend(collect_field_refs(child, field, f"{path}.{key}"))
    elif isinstance(value, list):
        for idx, child in enumerate(value, start=1):
            found.extend(collect_field_refs(child, field, f"{path}[{idx}]"))
    return found


def validate_sections(sections: dict[str, object], source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    required = {
        "site",
        "section_heads",
        "quick_rail",
        "categories",
        "stack_tags",
        "defense_controls",
        "enforcement_boundary",
        "common_tasks",
        "footer",
    }
    missing = required - set(sections)
    if missing:
        errors.append(f"sections: missing required section key(s): {sorted(missing)}")
    heads = sections.get("section_heads", {})
    if isinstance(heads, dict):
        for key in ["stacks", "defense", "cards", "skills", "packs", "sources", "common_tasks"]:
            if key not in heads:
                errors.append(f"sections: section_heads missing {key!r}")
    else:
        errors.append("sections: section_heads must be an object")
    boundary = sections.get("enforcement_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("sections: enforcement_boundary must be an object")
    else:
        for field in ["title", "summary", "source_refs", "controls"]:
            if field not in boundary:
                errors.append(f"sections: enforcement_boundary missing {field}")
        topics = {
            "prompt-guidance",
            "permissions-sandboxing",
            "deterministic-validation",
            "human-approval",
            "network-boundaries",
            "untrusted-data",
        }
        controls = boundary.get("controls", [])
        if not isinstance(controls, list):
            errors.append("sections: enforcement_boundary.controls must be a list")
        else:
            seen_topics = {norm(item.get("topic")) for item in controls if isinstance(item, dict)}
            missing_topics = topics - seen_topics
            if missing_topics:
                errors.append(f"sections: enforcement_boundary missing topic(s): {sorted(missing_topics)}")
            for idx, item in enumerate(controls, start=1):
                if not isinstance(item, dict):
                    errors.append(f"sections: enforcement_boundary.controls[{idx}] must be an object")
                    continue
                for field in ["topic", "label", "boundary", "enforced_by", "fails_if"]:
                    if not norm(item.get(field)):
                        errors.append(f"sections: enforcement_boundary.controls[{idx}] missing/empty {field}")
        refs = boundary.get("source_refs", [])
        if not isinstance(refs, list) or not refs:
            errors.append("sections: enforcement_boundary.source_refs must be a non-empty list")
    common_tasks = sections.get("common_tasks", [])
    required_tasks = {
        "repo-edit",
        "generated-artifact-edit",
        "security-sensitive-workflow",
        "repo-audit",
        "codex-task-prompt-generation",
    }
    if not isinstance(common_tasks, list):
        errors.append("sections: common_tasks must be a list")
    else:
        task_ids = {norm(item.get("id")) for item in common_tasks if isinstance(item, dict)}
        missing_tasks = required_tasks - task_ids
        if missing_tasks:
            errors.append(f"sections: common_tasks missing task(s): {sorted(missing_tasks)}")
        common_head = sections.get("section_heads", {}).get("common_tasks", {}) if isinstance(sections.get("section_heads"), dict) else {}
        common_description = norm(common_head.get("description")).lower() if isinstance(common_head, dict) else ""
        if "stack" not in common_description or "first" not in common_description:
            errors.append("sections: common_tasks description must elevate default stacks as the first starting point")
        for idx, item in enumerate(common_tasks, start=1):
            if not isinstance(item, dict):
                errors.append(f"sections: common_tasks[{idx}] must be an object")
                continue
            for field in ["id", "title", "use", "prompt", "before_example", "after_example", "placeholder_policy", "source_refs"]:
                if field not in item:
                    errors.append(f"sections: common_tasks[{idx}] missing {field}")
            if not norm(item.get("prompt")):
                errors.append(f"sections: common_tasks[{idx}] has empty prompt")
            if "[" in norm(item.get("prompt")) and "placeholder" not in norm(item.get("placeholder_policy")).lower():
                errors.append(f"sections: common_tasks[{idx}] prompt has placeholders but placeholder_policy does not label them")
            if not norm(item.get("before_example")) or not norm(item.get("after_example")):
                errors.append(f"sections: common_tasks[{idx}] must include before/after examples")
            if not isinstance(item.get("source_refs"), list) or not item.get("source_refs"):
                errors.append(f"sections: common_tasks[{idx}] source_refs must be a non-empty list")
    for ref, path in collect_field_refs(sections, "source_refs", "sections"):
        if ref and ref not in source_ids:
            errors.append(f"{path}: unknown source ref {ref!r}")
    return errors


def validate_ui_copy(ui_copy: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(ui_copy, dict):
        return ["ui_copy: must be an object"]
    allowed = {"style", "script"}
    missing = allowed - set(ui_copy)
    extra = set(ui_copy) - allowed
    if missing:
        errors.append(f"ui_copy: missing required key(s): {sorted(missing)}")
    if extra:
        errors.append(f"ui_copy: unexpected key(s): {sorted(extra)}")
    for key in allowed:
        if not norm(ui_copy.get(key)):
            errors.append(f"ui_copy: {key} must be a non-empty string")
    return errors


def validate_atomics(
    data: dict[str, object],
    *,
    root: Path = ROOT,
    check_generated_presence: bool = True,
) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_atomic_file_policy(root))
    directives = list(data["directives"])
    stacks = list(data["stacks"])
    packs = list(data["prompt_packs"])
    sources = list(data["sources"])
    sections = dict(data["sections"])
    ui_copy = data.get("ui_copy")

    for label, records in [
        ("directives", directives),
        ("stacks", stacks),
        ("prompt_packs", packs),
        ("sources", sources),
    ]:
        errors.extend(duplicate_errors(label, records))
        errors.extend(additional_property_errors(label, records))
        errors.extend(id_pattern_errors(label, records))
        errors.extend(required_errors(label, records))
    errors.extend(cross_duplicate_errors(data))

    directive_ids = {norm(r.get("id")) for r in directives}
    source_ids = {norm(r.get("id")) for r in sources}
    categories = {norm(c.get("name")) for c in sections.get("categories", [])}
    stack_tags = {norm(t.get("value")) for t in sections.get("stack_tags", [])}
    errors.extend(validate_sections(sections, source_ids))
    errors.extend(validate_ui_copy(ui_copy))

    for record in directives:
        rid = norm(record.get("id"))
        if norm(record.get("kind")) not in categories:
            errors.append(f"directives:{rid}: unknown category/kind {record.get('kind')!r}")
        if norm(record.get("source_class")) not in ALLOWED_SOURCE_CLASSES:
            errors.append(f"directives:{rid}: invalid source_class {record.get('source_class')!r}")
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
        stop_text = norm(record.get("stop")).lower()
        stack_quality_blob = " ".join(norm(record.get(field)).lower() for field in ["stack", "use", "avoid", "stop"])
        if "stop" not in stop_text:
            errors.append(f"stacks:{rid}: stop condition must visibly say when to stop")
        if not any(token in stack_quality_blob for token in STACK_QUALITY_TOKENS):
            errors.append(f"stacks:{rid}: stack must include a verification, evidence, stop, or gate signal")
        if norm(record.get("risk")) in {"High", "Critical"} and not any(token in stack_quality_blob for token in HIGH_RISK_STACK_GATE_TOKENS):
            errors.append(f"stacks:{rid}: high-risk stack must include approval, authorization, gate, backup, or rollback language")
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
            body = norm(variant.get("body"))
            label = norm(variant.get("label"))
            if not body:
                errors.append(f"prompt_packs:{rid}: variant {idx} missing body")
            elif len(body.split()) < 8:
                errors.append(f"prompt_packs:{rid}: variant {label or idx} is too thin to be a usable prompt variant")
            if label == "Normal" and ("Acceptance:" not in body or "Verification:" not in body):
                errors.append(f"prompt_packs:{rid}: Normal variant must include Acceptance and Verification clauses")
            if label in {"Strict", "Exploratory"} and ("Done when:" not in body or "Verification:" not in body):
                errors.append(f"prompt_packs:{rid}: {label} variant must include Done when and Verification clauses")
            if body and not any(token.lower() in body.lower() for token in PROMPT_VARIANT_GATE_TOKENS):
                errors.append(f"prompt_packs:{rid}: variant {label or idx} lacks acceptance, verification, done-when, or gate wording")
        labels = [norm(variant.get("label")) for variant in record.get("variants", [])]
        if labels != ALLOWED_PROMPT_VARIANTS:
            errors.append(f"prompt_packs:{rid}: expected {ALLOWED_PROMPT_VARIANTS!r} variants; got {labels!r}")
        if "agent_variants" in record:
            agent_variants = record.get("agent_variants")
            if not isinstance(agent_variants, list):
                errors.append(f"prompt_packs:{rid}: agent_variants must be a list")
            else:
                labels = [norm(item.get("label")) for item in agent_variants if isinstance(item, dict)]
                expected_labels = ["Codex", "Claude Code", "Hermes"]
                if labels != expected_labels:
                    errors.append(f"prompt_packs:{rid}: expected agent_variants {expected_labels!r}; got {labels!r}")
                for idx, item in enumerate(agent_variants, start=1):
                    if not isinstance(item, dict):
                        errors.append(f"prompt_packs:{rid}: agent_variants[{idx}] must be an object")
                        continue
                    extra = set(item) - {"label", "repo_instruction_file_usage", "approval_sandbox_tool_boundaries", "verification_reporting_style", "no_push_no_release_gate", "body"}
                    if extra:
                        errors.append(f"prompt_packs:{rid}: agent_variants[{idx}] unexpected field(s): {sorted(extra)}")
                    for field in ["label", "repo_instruction_file_usage", "approval_sandbox_tool_boundaries", "verification_reporting_style", "no_push_no_release_gate", "body"]:
                        if not norm(item.get(field)):
                            errors.append(f"prompt_packs:{rid}: agent_variants[{idx}] missing/empty {field}")
        if "copy_text" in record and norm(record["copy_text"]) != pack_copy(record):
            errors.append(f"prompt_packs:{rid}: copy_text override does not match derived copy")

    for record in sources:
        rid = norm(record.get("id"))
        if norm(record.get("stability")).lower() not in ALLOWED_STABILITY:
            errors.append(f"sources:{rid}: invalid stability {record.get('stability')!r}")
        if norm(record.get("source_type")) not in ALLOWED_SOURCE_TYPES:
            errors.append(f"sources:{rid}: invalid source_type {record.get('source_type')!r}")
        date_error = valid_date_error("sources", rid, "last_checked", record.get("last_checked"))
        if date_error:
            errors.append(date_error)
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
