#!/usr/bin/env python3
"""Build docs/index.html from atomics/** records."""

from __future__ import annotations

import html
import hashlib
import json
import os
import sys
from pathlib import Path

from check_adhlbs_atomics import (
    GENERATED_BANNER,
    directive_copy,
    directive_terse_copy,
    load_atomics,
    pack_copy,
    search_text,
    source_url_copy,
    stack_full_copy,
    stack_short_copy,
    validate_atomics,
)
from check_docs_index_offline import check_html_offline_safe


ROOT = Path(__file__).resolve().parents[1]
DOCS_INDEX = ROOT / "docs" / "index.html"
TMP_INDEX = ROOT / "docs" / "index.html.tmp"
MANIFEST_ID = "adhlbs-build-manifest"
GENERATOR_VERSION = "2026-05-17.audit2"
MANIFEST_SOURCE_PATHS = [
    "atomics/adhlbs.schema.json",
    "atomics/directives.json",
    "atomics/prompt_packs.json",
    "atomics/sections.json",
    "atomics/sources.json",
    "atomics/stacks.json",
    "atomics/ui_copy.json",
]
GENERATOR_PATHS = [
    "tools/build_docs_index.py",
    "tools/check_adhlbs_atomics.py",
    "tools/check_docs_index_offline.py",
]

RISK_RANK = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
RISK_CLASS = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high", "Critical": "risk-critical"}


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def text(value: object) -> str:
    return html.escape(str(value or ""), quote=False)


def nl2br(value: object) -> str:
    return "<br/>".join(text(value).splitlines())


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def combined_hash(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in paths:
        path = ROOT / relative
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def source_tree_state(source_hash: str) -> dict[str, str]:
    return {
        "mode": "deterministic-source-content",
        "source_commit": "not-embedded-precommit-safe",
        "fallback_dirty_tree_marker": source_hash[:16],
    }


def build_manifest(data: dict[str, object]) -> dict[str, object]:
    sections = data["sections"]
    ui_copy = data["ui_copy"]
    source_hash = combined_hash(MANIFEST_SOURCE_PATHS)
    generator_hash = combined_hash(GENERATOR_PATHS)
    source_files = {path: sha256_file(ROOT / path) for path in MANIFEST_SOURCE_PATHS}
    generator_files = {path: sha256_file(ROOT / path) for path in GENERATOR_PATHS}
    return {
        "manifest_version": 1,
        "build_marker": "deterministic-no-wallclock",
        "schema_version": data["schema"].get("version", ""),
        "generator_version": GENERATOR_VERSION,
        "generator_hash": generator_hash,
        "source_tree": source_tree_state(source_hash),
        "source_hash": source_hash,
        "source_files": source_files,
        "generator_files": generator_files,
        "counts": {
            "directives": len(data["directives"]),
            "stacks": len(data["stacks"]),
            "prompt_packs": len(data["prompt_packs"]),
            "sources": len(data["sources"]),
            "sections": len(sections),
            "section_heads": len(sections.get("section_heads", {})),
            "categories": len(sections.get("categories", [])),
            "defense_controls": len(sections.get("defense_controls", [])),
            "common_tasks": len(sections.get("common_tasks", [])),
            "ui_copy_blocks": len(ui_copy),
            "ui_copy_style_bytes": len(str(ui_copy.get("style", "")).encode("utf-8")),
            "ui_copy_script_bytes": len(str(ui_copy.get("script", "")).encode("utf-8")),
        },
    }


def render_manifest(data: dict[str, object]) -> str:
    payload = json.dumps(build_manifest(data), sort_keys=True, separators=(",", ":"))
    return f'<script id="{MANIFEST_ID}" type="application/json">{text(payload)}</script>\n'


def extract_manifest(html_text: str) -> dict[str, object] | None:
    start_token = f'<script id="{MANIFEST_ID}" type="application/json">'
    end_token = "</script>"
    start = html_text.find(start_token)
    if start == -1:
        return None
    start += len(start_token)
    end = html_text.find(end_token, start)
    if end == -1:
        return None
    payload = html.unescape(html_text[start:end])
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    return parsed


def category_class(sections: dict[str, object], kind: str) -> str:
    for category in sections.get("categories", []):
        if category.get("name") == kind and category.get("class"):
            return str(category["class"])
    return "cat-" + "".join(ch if ch.isalnum() else "-" for ch in kind.lower()).strip("-")


def render_quick_rail(items: list[dict[str, object]]) -> str:
    chunks = ['<div aria-label="Fast copy directives" class="quick-rail">']
    for item in items:
        copy = f"{item['title']}: {item['code']}\n{item['description']}"
        chunks.append(
            '<div class="quick-card">'
            f"<b>{text(item['title'])}</b>"
            f"<code>{text(item['code'])}</code>"
            f"<p>{text(item['description'])}</p>"
            f'<button aria-label="Copy quick directive: {e(item["title"])}" '
            f'class="copy micro" data-copy="{e(copy)}" type="button">Copy</button>'
            "</div>"
        )
    chunks.append("</div>")
    return "".join(chunks)


def render_common_tasks(data: dict[str, object]) -> str:
    sections = data["sections"]
    head = sections["section_heads"]["common_tasks"]
    chunks = [
        '<div class="section-divider"></div><section class="section" id="common-tasks">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
        '<div class="quick-rail">',
    ]
    for item in sections.get("common_tasks", []):
        refs = " ".join(f"[{ref}]" for ref in item.get("source_refs", []))
        chunks.append(
            f'<article class="quick-card" data-common-task-id="{e(item["id"])}" '
            f'data-search="{e(search_text(item))}">'
            f"<b>{text(item['title'])}</b>"
            f"<p>{text(item['use'])}</p>"
            f"<code>{text(item['prompt'])}</code>"
            f'<p class="related"><b>Before:</b> {text(item.get("before_example", ""))}</p>'
            f'<p class="related"><b>After:</b> {text(item.get("after_example", ""))}</p>'
            f'<p class="related"><b>Placeholder policy:</b> {text(item.get("placeholder_policy", ""))}</p>'
            f'<p class="related source-refs">Sources: {text(refs)}</p>'
            f'<button aria-label="Copy common task: {e(item["title"])}" class="copy micro" '
            f'data-copy="{e(item["prompt"])}" type="button">Copy</button>'
            "</article>"
        )
    chunks.append("</div></section>")
    return "".join(chunks)


def render_stack_section(data: dict[str, object]) -> str:
    sections = data["sections"]
    stacks = data["stacks"]
    head = sections["section_heads"]["stacks"]
    quick = sections.get("quick_rail", [{}])[0]
    chunks = [
        '<section id="stacks">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
    ]
    if quick:
        chunks.append(
            '<div class="print-default">Universal default: '
            f'<code>{text(quick["code"])}</code>. {text(quick["description"])}</div>'
        )
    chunks.append('<div class="v7-panel"><b>Abbreviation legend:</b><div class="chiprow">')
    for item in sections.get("abbrev_legend", []):
        chunks.append(f'<span class="chip">{text(item)}</span>')
    chunks.append("</div><b>Risk legend:</b><div class=\"chiprow\">")
    for item in sections.get("risk_legend", []):
        risk = item.get("risk", "")
        chunks.append(
            f'<span class="chip"><span class="risk {RISK_CLASS.get(risk, "")}">{text(risk)}</span> '
            f'{text(item.get("description", ""))}</span>'
        )
    chunks.append("</div></div>")
    chunks.append(
        '<div class="stack-controls"><label class="chip" for="stackTag">Workstream</label>'
        '<select id="stackTag"><option value="">All stack workstreams</option>'
    )
    for tag in sections.get("stack_tags", []):
        chunks.append(f'<option value="{e(tag["value"])}">{text(tag["label"])}</option>')
    chunks.append(
        '</select><button class="secondary" id="sortRisk" type="button">Sort by risk high-first</button>'
        '<button class="secondary" id="sortStackId" type="button">Sort by ID</button>'
        '<button class="secondary" id="copyVisibleStacks" type="button">Copy visible stacks</button>'
        '<button class="secondary" id="collapseStackDetails" type="button">Collapse stack details</button></div>'
    )
    chunks.append(
        '<div class="stack-table-wrap"><table class="stack-table" id="stacksTable">'
        "<caption>Dispatch stacks: choose the smallest stack matching task, risk, and stop condition.</caption>"
        "<thead><tr><th>ID</th><th>Task</th><th>Type</th><th>Stack</th><th>Details</th><th>Copy</th></tr></thead><tbody>"
    )
    for record in stacks:
        risk = record["risk"]
        q = search_text(record)
        chunks.append(
            f'<tr data-risk="{e(risk)}" data-risk-rank="{RISK_RANK.get(risk, 0)}" '
            f'data-search="{e(q)}" data-stack-id="{e(record["id"])}" data-tag="{e(record["tag"])}" id="{e(record["html_id"])}">'
            f'<td><span class="stack-id">{text(record["id"])}</span></td>'
            f'<td class="stack-name" title="Avoid if: {e(record["avoid"])}">'
        )
        if record.get("recommended"):
            chunks.append('<span class="rec-star" title="Recommended default">★</span>')
        chunks.append(
            f'{text(record["name"])}<span class="risk {RISK_CLASS.get(risk, "")}">{text(risk)}</span></td>'
            f'<td><span class="chip light">{text(record["tag"])}</span></td>'
            f'<td><code>{text(record["stack"])}</code></td>'
            '<td class="stack-details"><details><summary>Use / Avoid / Stop</summary>'
            f'<p><b>Use:</b> {text(record["use"])}</p>'
            f'<p><b>Avoid:</b> {text(record["avoid"])}</p>'
            f'<p><b>Stop:</b> {text(record["stop"])}</p>'
            '</details></td><td><div class="copy-row">'
            f'<button aria-label="Short for {e(record["id"])}" class="copy small" data-copy="{e(stack_short_copy(record))}" type="button">Short</button>'
            f'<button aria-label="Full for {e(record["id"])}" class="copy small" data-copy="{e(stack_full_copy(record))}" type="button">Full</button>'
            "</div></td></tr>"
        )
    chunks.append("</tbody></table></div></section>")
    return "".join(chunks)


def render_defense_section(data: dict[str, object]) -> str:
    sections = data["sections"]
    head = sections["section_heads"]["defense"]
    boundary = sections.get("enforcement_boundary", {})
    chunks = [
        '<div class="section-divider"></div><section class="section" id="defense">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
        f'<div class="defense-note">{text(sections.get("defense_note", ""))}</div>',
    ]
    if boundary:
        refs = " ".join(f"[{ref}]" for ref in boundary.get("source_refs", []))
        chunks.append(
            '<div class="panel light" id="prompt-guidance-not-enforcement">'
            f'<h2>{text(boundary["title"])}</h2>'
            f'<p>{text(boundary["summary"])}</p>'
            '<table class="mini-table"><thead><tr><th>Surface</th><th>Boundary</th><th>Enforced by</th><th>Fails if</th></tr></thead><tbody>'
        )
        for record in boundary.get("controls", []):
            chunks.append(
                f'<tr data-boundary-topic="{e(record["topic"])}">'
                f'<td><b>{text(record["label"])}</b></td>'
                f'<td>{text(record["boundary"])}</td>'
                f'<td>{text(record["enforced_by"])}</td>'
                f'<td>{text(record["fails_if"])}</td></tr>'
            )
        chunks.append(
            "</tbody></table>"
            f'<p class="related source-refs">Sources: {text(refs)}</p>'
            "</div>"
        )
    chunks.append('<div class="defense-v7">')
    for record in sections.get("defense_controls", []):
        deterministic = "yes" if "Yes" in record.get("badge", "") else "warn"
        chunks.append(
            '<div class="defense-card">'
            f'<h3>{text(" · ".join(part for part in [record["id"], record["name"], record["posture"]] if part))}</h3>'
            f'<span class="badge {deterministic}">{text(record["badge"])}</span>'
            f'<p>{text(record["map"])}</p>'
            '<details class="defense-detail"><summary>Breaks if absent / control</summary>'
            f'<p><b>Breaks if absent:</b> {text(record["breaks_if_absent"])}</p>'
            f'<p><b>Control:</b> {text(record["control"])}</p>'
            "</details></div>"
        )
    chunks.append("</div><details class=\"print-checklist\"><summary>Print-friendly defense checklist</summary><ul>")
    for item in sections.get("defense_print_checklist", []):
        chunks.append(f"<li>{text(item)}</li>")
    chunks.append("</ul></details></section>")
    return "".join(chunks)


def render_card(record: dict[str, object], data: dict[str, object]) -> str:
    sections = data["sections"]
    directives_by_id = {item["id"]: item for item in data["directives"]}
    cat = category_class(sections, record["kind"])
    q = search_text(
        record["kind"],
        record["name"],
        record["expansion"],
        record["why"],
        record["directive"],
        record["blocks"],
        record["use"],
        record["tags"],
        record["aliases"],
        record["id"],
        record["source_class"],
        record["related"],
        record["negative_example"],
        record.get("source_refs", []),
    )
    chunks = [
        f'<article class="card {e(cat)}" data-card-id="{e(record["id"])}" data-kind="{e(record["kind"])}" '
        f'data-search="{e(q)}" id="{e(record["html_id"])}" tabindex="-1">',
        '<div class="card-top">',
        f'<span class="pill">{text(record["kind"])}</span>',
        f'<button aria-label="Copy directive for {e(record["name"])}" class="copy" data-copy="{e(directive_copy(record))}" type="button">Copy</button>',
        f'<button aria-label="Terse directive for {e(record["name"])}" class="copy" data-copy="{e(directive_terse_copy(record))}" data-copy-kind="terse" type="button">Terse</button>',
        "</div>",
        f"<h3>{text(record['name'])}</h3>",
        '<div class="card-meta">',
        f'<span class="meta-badge">{text(record["id"])}</span>',
    ]
    if record.get("source_class"):
        chunks.append(f'<span class="meta-badge src">{text(record["source_class"])}</span>')
    if record.get("recognition"):
        chunks.append(f'<span class="meta-badge acr">{text(record["recognition"])}</span>')
    for badge in record.get("metadata", []):
        chunks.append(f'<span class="meta-badge">{text(badge)}</span>')
    chunks.extend(
        [
            "</div>",
            f'<p class="expansion">{text(record["expansion"])}</p>',
            f'<p class="why">{text(record["why"])}</p>',
            f"<pre>{text(record['directive'])}</pre>",
            "<details><summary>Use / blocks / tags</summary>",
            f'<p><b>Use:</b> {text(record["use"])}</p>',
            f'<p><b>Blocks:</b> {text(record["blocks"])}</p>',
            '<div class="tags">',
        ]
    )
    for tag in record.get("tags", []):
        chunks.append(f"<span>{text(tag)}</span>")
    chunks.append("</div></details><details class=\"card-details\"><summary>Guardrail / related</summary>")
    if record.get("related"):
        chunks.append('<p class="related">Related: ')
        links = []
        for related_id in record["related"]:
            target = directives_by_id[related_id]
            links.append(f'<a href="#{e(target["html_id"])}">{text(target["name"])}</a>')
        chunks.append(" · ".join(links))
        chunks.append("</p>")
    if record.get("negative_example"):
        chunks.append(f'<p class="related">Negative example: {text(record["negative_example"])}</p>')
    if record.get("source_refs"):
        chunks.append('<p class="related source-refs">Sources: ')
        refs = [
            f'<code data-source-ref="{e(ref)}">[{text(ref)}]</code>'
            for ref in record.get("source_refs", [])
        ]
        chunks.append(" · ".join(refs))
        chunks.append("</p>")
    chunks.append("</details></article>")
    return "".join(chunks)


def render_cards_section(data: dict[str, object]) -> str:
    sections = data["sections"]
    directives = data["directives"]
    head = sections["section_heads"]["cards"]
    chunks = [
        '<div class="section-divider"></div><section class="section" id="cards">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
        '<div class="section-actions cards-actions">'
        '<button class="secondary" id="copyVisibleCards" type="button">Copy visible cards</button>'
        '<button class="secondary" id="expandAll" type="button">Expand card details</button>'
        '<button class="secondary" id="collapseAll" type="button">Collapse card details</button></div>',
    ]
    for category in sections.get("categories", []):
        records = [r for r in directives if r["kind"] == category["name"]]
        if not records:
            continue
        chunks.append(
            f'<section class="card-group" data-group="{e(category["name"])}">'
            '<div class="group-header">'
            f'<div class="group-icon {e(category["class"])}">{text(category["icon"])}</div>'
            f'<h3 class="group-name">{text(category["name"])}</h3>'
            f'<span class="group-desc">{text(category["description"])}</span>'
            f'<span class="group-count">{len(records)} directives</span>'
            '</div><div class="group-grid">'
        )
        for record in records:
            chunks.append(render_card(record, data))
        chunks.append("</div></section>")
    chunks.append("</section>")
    return "".join(chunks)


def render_packs_section(data: dict[str, object]) -> str:
    sections = data["sections"]
    head = sections["section_heads"]["packs"]
    chunks = [
        '<div class="section-divider"></div><section class="section" id="packs">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
        '<div class="packs-actions">'
        '<button aria-label="Copy every prompt pack, ignoring current search" class="primary" id="copyAllPacks" type="button">Copy all packs</button>'
        '<button aria-label="Copy prompt packs matching current search" class="secondary" id="copyVisiblePacks" type="button">Copy filtered packs</button>'
        '<button class="secondary" id="collapsePackDetails" type="button">Collapse pack details</button></div>',
        '<div class="packs-grid">',
    ]
    for record in data["prompt_packs"]:
        q = search_text(record)
        refs = ", ".join(f"[{ref}]" for ref in record.get("source_refs", []))
        risk_class = " risk-warn" if record.get("risk") in {"High", "Critical"} else ""
        chunks.append(
            f'<article class="promptbox" data-pack-id="{e(record["id"])}" data-risk="{e(record["risk"])}" '
            f'data-tag="{e(record["tag"])}" data-search="{e(q)}" id="{e(record["html_id"])}">'
            '<div class="promptbox-header">'
            f'<h3>{text(record["title"])}</h3><span class="promptbox-tag">{text(record["tag"])}</span></div>'
            '<div class="pack-meta">'
            f'<span>{text(record["id"])}</span><span class="{risk_class.strip()}">{text(record["risk"])} risk</span>'
            f'<span>Source: {text(refs)}</span></div>'
        )
        for variant in record.get("variants", []):
            open_attr = " open" if variant.get("open") else ""
            chunks.append(
                f"<details{open_attr}><summary>{text(variant['label'])}</summary>"
                f"<pre>{text(variant['body'])}</pre></details>"
            )
        if record.get("agent_variants"):
            chunks.append(
                f'<div class="agent-variants" data-agent-variants-for="{e(record["id"])}">'
                "<h4>Agent-specific variants</h4>"
            )
            for variant in record.get("agent_variants", []):
                body = (
                    f"{variant['body']}\n\n"
                    f"Repo instructions: {variant['repo_instruction_file_usage']}\n"
                    f"Tool boundaries: {variant['approval_sandbox_tool_boundaries']}\n"
                    f"Verification/reporting: {variant['verification_reporting_style']}\n"
                    f"Release gate: {variant['no_push_no_release_gate']}"
                )
                chunks.append(
                    f'<details class="agent-variant" data-agent-variant="{e(variant["label"])}">'
                    f'<summary>{text(variant["label"])}</summary><pre>{text(body)}</pre></details>'
                )
            chunks.append("</div>")
        chunks.append(
            f'<button aria-label="Copy pack for {e(record["id"])}" class="copy" data-copy="{e(pack_copy(record))}" type="button">Copy pack</button>'
            "</article>"
        )
    chunks.append("</div></section>")
    return "".join(chunks)


def render_sources_section(data: dict[str, object]) -> str:
    sections = data["sections"]
    head = sections["section_heads"]["sources"]
    chunks = [
        '<div class="section-divider"></div><section class="section" id="sources">',
        f'<div class="section-head"><h2>{text(head["title"])}</h2><p>{text(head["description"])}</p></div>',
        '<div class="source-tools">'
        '<button class="secondary" id="copyVisibleSources" type="button">Copy visible source URLs</button>'
        '<button class="secondary" id="copySourceKeys" type="button">Copy visible source keys</button></div>',
        f'<div class="source-map">{text(sections.get("source_map", ""))}</div>',
        '<div class="sources-wrap"><table class="sources" id="sourcesTable">'
        '<caption>Sources are shown as inert text so the file does not contact the network.</caption>'
        '<thead><tr><th>Key / Source</th><th>Contributed</th><th>Coverage</th><th>Last checked</th><th>Trust / source note</th><th>URL text</th></tr></thead><tbody>',
    ]
    for idx, record in enumerate(data["sources"], start=1):
        q = search_text(record)
        stable_class = "src-stable" if record["stability"] == "stable" else "src-volatile" if record["stability"] == "volatile" else ""
        chunks.append(
            f'<tr data-search="{e(q)}" data-source-id="{e(record["id"])}" data-source-rank="{idx}">'
            f'<td><span class="src-key">[{text(record["id"])}]</span><br/><b>{text(record["title"])}</b><br/>'
            f'<span class="src-badge">{text(record["source_type"])}</span> '
            f'<span class="src-badge {stable_class}">{text(record["stability"])}</span></td>'
            f'<td>{text(record["notes"])}</td>'
            f'<td>{text(", ".join(record.get("supports", [])))}</td>'
            f'<td>{text(record["last_checked"])}</td>'
            f'<td>{nl2br(record["trust"])}</td>'
            f'<td><code class="urltext">{text(record["url"])}</code><br/>'
            f'<button aria-label="Copy URL for [{e(record["id"])}]" class="copy small" data-copy="{e(source_url_copy(record))}" type="button">Copy URL</button></td>'
            "</tr>"
        )
    chunks.append("</tbody></table></div></section>")
    return "".join(chunks)


def render_html(data: dict[str, object]) -> str:
    sections = data["sections"]
    site = sections["site"]
    style = data["ui_copy"]["style"]
    script = data["ui_copy"]["script"]
    categories = sections.get("categories", [])
    chunks = [
        "<!DOCTYPE html>\n",
        f"{GENERATED_BANNER}\n",
        f'<html lang="{e(site.get("lang", "en"))}">\n<head>\n',
        '<meta charset="utf-8"/>\n',
        '<meta content="width=device-width, initial-scale=1" name="viewport"/>\n',
        f'<meta content="{text(site["csp"])}" http-equiv="Content-Security-Policy"/>\n',
        f"<title>{text(site['title'])}</title>\n",
        f"<style>\n{style}\n</style>\n",
        render_manifest(data),
        f'<meta content="{e(site["version_meta"])}" name="agent-directives-version"/></head>\n',
        '<body><a class="skip-link" href="#main">Skip to content</a>\n',
        '<header class="wrap">\n',
        f'<div class="eyebrow">{text(site["eyebrow"])}</div>\n',
        f'<h1>{site["h1"]}</h1>\n',
        f'<p class="subtitle">{text(site["subtitle"])}</p>\n',
        "</header>\n",
        '<main class="wrap" id="main" tabindex="-1">\n',
        '<div class="toolbar">\n',
        '<input aria-label="Search directives, stacks, packs, and sources" autocomplete="off" id="search" '
        'placeholder="Search directives, stacks, packs, sources..." type="search"/>\n',
        '<select aria-label="Filter directive card category" id="kind"><option value="">All categories</option>',
    ]
    for category in categories:
        chunks.append(f'<option>{text(category["name"])}</option>')
    chunks.extend(
        [
            "</select>\n",
            '<button class="primary" id="printBtn" type="button">Print / PDF</button>\n',
            '<button id="resetBtn" type="button">Reset filters</button>\n',
            '<button class="secondary" id="toggleDensity" type="button">Compact view</button>'
            '<span aria-live="polite" class="result-summary" id="resultSummary">Ready</span></div>\n',
            "<nav>\n",
            f'<a href="#stacks">Default Stacks<span class="toc-count">({len(data["stacks"])})</span></a>',
            f'<a href="#common-tasks">Common Tasks<span class="toc-count">({len(sections.get("common_tasks", []))})</span></a>',
            '<a href="#defense">Defense in Depth</a>',
            f'<a href="#cards">Directive Cards<span class="toc-count">({len(data["directives"])})</span></a>',
            '<a href="#skills">Claude + Hermes Skills</a>',
            f'<a href="#packs">Prompt Packs<span class="toc-count">({len(data["prompt_packs"])})</span></a>',
            f'<a href="#sources">Sources<span class="toc-count">({len(data["sources"])})</span></a>',
            "\n</nav>",
            render_quick_rail(sections.get("quick_rail", [])),
            render_common_tasks(data),
            render_stack_section(data),
            render_defense_section(data),
            render_cards_section(data),
        ]
    )
    skills_head = sections["section_heads"]["skills"]
    chunks.extend(
        [
            '<div class="section-divider"></div><section class="section" id="skills">',
            f'<div class="section-head"><h2>{text(skills_head["title"])}</h2><p>{text(skills_head["description"])}</p></div>',
            sections.get("skills_inner_html", ""),
            "</section>",
            render_packs_section(data),
            render_sources_section(data),
            "</main>\n",
            '<div aria-live="polite" class="toast" id="toast">Copied</div>\n',
        ]
    )
    footer = sections.get("footer", {})
    chunks.append('<footer class="wrap">')
    chunks.append(f'<p>{text(footer.get("text", ""))}</p>')
    chunks.append('<div aria-label="Offline integrity summary" class="integrity-strip">')
    for item in footer.get("integrity", []):
        chunks.append(f"<span>{text(item)}</span>")
    chunks.append("</div></footer>\n")
    chunks.append(f"<script>\n{script}\n</script>\n</body>\n</html>\n")
    return "".join(chunks)


def validate_generated_html(html_text: str, data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if GENERATED_BANNER not in html_text:
        errors.append("generated banner missing")
    manifest = extract_manifest(html_text)
    if manifest is None:
        errors.append("build manifest missing or malformed")
    else:
        expected_manifest = build_manifest(data)
        if manifest != expected_manifest:
            errors.append("build manifest does not match current atomics/generator state")
        expected_counts = expected_manifest["counts"]
        for key in ["directives", "stacks", "prompt_packs", "sources", "sections", "common_tasks", "ui_copy_blocks"]:
            if manifest.get("counts", {}).get(key) != expected_counts[key]:
                errors.append(f"build manifest count mismatch for {key}")
    for sid in ["common-tasks", "stacks", "defense", "cards", "skills", "packs", "sources"]:
        if f'id="{sid}"' not in html_text:
            errors.append(f"expected section #{sid} missing")
    if 'id="prompt-guidance-not-enforcement"' not in html_text:
        errors.append("prompt guidance is not enforcement surface missing")
    for topic in [
        "prompt-guidance",
        "permissions-sandboxing",
        "deterministic-validation",
        "human-approval",
        "network-boundaries",
        "untrusted-data",
    ]:
        if f'data-boundary-topic="{topic}"' not in html_text:
            errors.append(f"enforcement boundary topic {topic} missing from generated html")
    expected_counts = {
        "Default Stacks": len(data["stacks"]),
        "Common Tasks": len(data["sections"].get("common_tasks", [])),
        "Directive Cards": len(data["directives"]),
        "Prompt Packs": len(data["prompt_packs"]),
        "Sources": len(data["sources"]),
    }
    for label, count in expected_counts.items():
        if f">{label}<span class=\"toc-count\">({count})</span>" not in html_text:
            errors.append(f"nav count mismatch for {label}")
    for record in data["directives"]:
        if f'data-card-id="{e(record["id"])}"' not in html_text:
            errors.append(f"directive {record['id']} missing from generated html")
        if e(directive_copy(record)) not in html_text or e(directive_terse_copy(record)) not in html_text:
            errors.append(f"directive {record['id']} derived copy missing")
        for ref in record.get("source_refs", []):
            if f'data-source-ref="{e(ref)}"' not in html_text:
                errors.append(f"directive {record['id']} source ref {ref} missing from generated html")
    for record in data["stacks"]:
        if f'data-stack-id="{e(record["id"])}"' not in html_text:
            errors.append(f"stack {record['id']} missing from generated html")
        if e(stack_short_copy(record)) not in html_text or e(stack_full_copy(record)) not in html_text:
            errors.append(f"stack {record['id']} derived copy missing")
    for record in data["prompt_packs"]:
        if f'data-pack-id="{e(record["id"])}"' not in html_text:
            errors.append(f"prompt pack {record['id']} missing from generated html")
        if e(pack_copy(record)) not in html_text:
            errors.append(f"prompt pack {record['id']} derived copy missing")
        for variant in record.get("agent_variants", []):
            if f'data-agent-variant="{e(variant["label"])}"' not in html_text:
                errors.append(f"prompt pack {record['id']} agent variant {variant['label']} missing")
            for field in [
                "repo_instruction_file_usage",
                "approval_sandbox_tool_boundaries",
                "verification_reporting_style",
                "no_push_no_release_gate",
            ]:
                if e(variant[field]) not in html_text:
                    errors.append(f"prompt pack {record['id']} agent variant {variant['label']} missing {field}")
    for record in data["sections"].get("common_tasks", []):
        if f'data-common-task-id="{e(record["id"])}"' not in html_text:
            errors.append(f"common task {record['id']} missing from generated html")
        if e(record["prompt"]) not in html_text:
            errors.append(f"common task {record['id']} copy prompt missing")
        for field in ["before_example", "after_example", "placeholder_policy"]:
            if e(record.get(field, "")) not in html_text:
                errors.append(f"common task {record['id']} {field} missing from generated html")
    for record in data["sources"]:
        if f'data-source-id="{e(record["id"])}"' not in html_text:
            errors.append(f"source {record['id']} missing from generated html")
        if e(source_url_copy(record)) not in html_text:
            errors.append(f"source {record['id']} URL copy missing")
    errors.extend(check_html_offline_safe(html_text))
    return errors


def build() -> int:
    data = load_atomics(ROOT)
    errors = validate_atomics(data, root=ROOT, check_generated_presence=False)
    if errors:
        print("BUILD_ABORTED_ATOMICS_INVALID", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    html_text = render_html(data)
    TMP_INDEX.write_text(html_text, encoding="utf-8")
    errors = validate_generated_html(TMP_INDEX.read_text(encoding="utf-8"), data)
    if errors:
        print(f"BUILD_ABORTED_TMP_INVALID tmp={TMP_INDEX}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    os.replace(TMP_INDEX, DOCS_INDEX)
    print(
        "BUILD_OK "
        f"directives={len(data['directives'])} "
        f"stacks={len(data['stacks'])} "
        f"prompt_packs={len(data['prompt_packs'])} "
        f"sources={len(data['sources'])} "
        f"output={DOCS_INDEX}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
