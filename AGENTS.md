# AGENTS.md

Operational instructions for agents working on ADHLBS.

ADHLBS is a single-file, offline-safe, GitHub Pages-published reference sheet generated from atomics.

The public artifact is:

```text
docs/index.html
```

The source of truth is:

```text
atomics/**
```

Do not hand-edit `docs/index.html` for normal content changes.

---

## Core Rule

Use this workflow:

```text
RTFM -> ATOMICS -> BUILD -> CHECK -> PARITY -> REPORT
```

Meaning:

1. Read the relevant files first.
2. Edit canonical records under `atomics/**`.
3. Regenerate `docs/index.html`.
4. Run all checks.
5. Confirm live UI parity.
6. Report exact verification results.

---

## Source of Truth

Canonical content lives in:

```text
atomics/directives.json
atomics/stacks.json
atomics/prompt_packs.json
atomics/sources.json
atomics/sections.json
atomics/ui_copy.json
atomics/adhlbs.schema.json
```

Generated output lives in:

```text
docs/index.html
```

Tools live in:

```text
tools/build_docs_index.py
tools/check_adhlbs_atomics.py
tools/check_docs_index_freshness.py
tools/check_docs_index_offline.py
```

---

## Do Not Hand-Edit Generated HTML

`docs/index.html` is generated.

Do not directly edit generated card markup, stack rows, prompt packs, source rows, counts, search text, copy text, or category lists in `docs/index.html`.

Instead:

```text
edit atomics/** -> run tools/build_docs_index.py -> verify
```

Direct edits to `docs/index.html` are allowed only for emergency recovery, and must be moved back into the generator/atomics before completion.

---

## Adding a New Directive Card

To add a card:

1. Add one record to `atomics/directives.json`.
2. Use a stable unique `id`.
3. Fill required fields.
4. Add source refs if applicable.
5. Add related IDs only if those cards exist.
6. Run validation and rebuild.

A directive record should normally include:

```text
id
kind
name
expansion
why
directive
use
blocks
tags
aliases
source_class
related
negative_example
source_refs
```

Do not duplicate derived copy text unless the schema explicitly allows an override.

The generator should derive:

```text
visible card
search text
copy button text
terse copy text
category count
related links
metadata badges
```

---

## Editing an Existing Directive Card

When editing a card:

1. Find the canonical record in `atomics/directives.json`.
2. Change the smallest necessary fields.
3. Do not patch generated HTML by hand.
4. Rebuild.
5. Check the resulting card visually or with browser smoke.

Preserve existing IDs unless there is a strong reason to rename. Renaming IDs can break related links, anchors, search behavior, and prompt references.

---

## Adding or Editing a Stack

Stacks live in:

```text
atomics/stacks.json
```

A stack record should preserve:

```text
id
name
risk
tag
stack
use
avoid
stop
```

Valid risk values should remain consistent with the checker.

Stack copy text should derive from the canonical stack record.

Do not add visual-only labels to canonical stack names if that changes copied text unexpectedly.

---

## Adding or Editing a Prompt Pack

Prompt packs live in:

```text
atomics/prompt_packs.json
```

Preserve the baseline copy format unless intentionally changed:

```text
Normal:
Variants:
```

After editing packs, verify:

```text
copy all packs
individual pack copy
pack collapse/expand controls
search behavior
```

---

## Adding or Editing Sources

Sources live in:

```text
atomics/sources.json
```

Source URLs must remain inert/copyable text in the generated artifact.

Do not create active external links, remote script loads, images, iframes, stylesheets, or fetch behavior.

The offline artifact must not make network requests.

---

## Offline Safety Requirements

The generated page must remain offline-safe:

```text
no remote fonts
no external stylesheets
no external scripts
no external images
no iframes
no fetch/XHR/WebSocket/EventSource/sendBeacon/import/service-worker use
source URLs inert/copyable only
CSP preserved
```

Always run:

```text
python tools/check_docs_index_offline.py
```

---

## Required Verification

Before claiming success, run:

```text
python tools/check_adhlbs_atomics.py
python tools/build_docs_index.py
python tools/check_docs_index_freshness.py
python tools/check_docs_index_offline.py
python -m py_compile tools/*.py
git diff --check
git status --short
```

On PowerShell, use:

```powershell
Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
```

---

## Live-Parity Check

The generated `docs/index.html` must preserve the current rich UI shell.

Verify these are present and working:

```text
sticky toolbar
search input
category filter
print/reset controls
compact mode
result summary
nav counts
quick rail
default stack table
stack workstream filter
sort by risk
sort by ID
copy visible stacks
directive cards
copy and terse card buttons
expand/collapse card details
defense-in-depth section
Claude + Hermes Skills section
prompt packs
pack copy controls
pack collapse controls
sources table
inert source URLs
offline CSP
zero active remote assets
```

If any are missing or degraded, patch the atomics/generator/templates before committing.

---

## Browser Smoke

If possible, run a temporary local server and test the generated page through localhost.

Expected baseline counts:

```text
152 directive cards
25 stacks
20 prompt packs
48 sources
```

Also verify:

```text
search works
reset restores all
compact mode toggles
category filter works
stack workstream filter works
risk and ID sorting work
copy buttons work
card expand/collapse works
pack collapse works
no active remote assets
```

If browser smoke cannot be run, report:

```text
BROWSER_SMOKE_NOT_RUN
```

Do not claim browser verification passed unless it was actually run.

---

## Patch Discipline

Prefer small, reversible changes.

Allowed normal changes:

```text
atomics/**
tools/**
docs/index.html generated output
README.md workflow notes
docs/audits/**
.github/workflows/**
AGENTS.md
```

Avoid:

```text
visual redesign
framework migration
external dependencies
multi-page app conversion
server runtime
manual generated HTML edits
large semantic rewrites
deleting cards without proof
changing GitHub Pages settings
release mutation
```

---

## Andon / Failure Reporting

When a problem is found, report it immediately and plainly.

Use:

```text
Problem:
Surface:
Owner record:
Failure mode:
Patch:
Verification:
Remaining risk:
```

Do not hide malformed records, stale generated output, broken copy text, or parity regressions.

---

## Commit Policy

Before commit:

1. Confirm checks pass.
2. Confirm generated output is fresh.
3. Confirm `docs/index.html` remains rich and offline-safe.
4. Confirm no unrelated files are staged.
5. Review `git diff --stat`.
6. Review atomics diffs for concept-level clarity.
7. Report any unverified items.

Do not commit, push, tag, deploy, or mutate GitHub Pages unless explicitly authorized.

---

## Standard Completion Report

Return:

```text
1. files changed
2. atomics changed
3. generated output status
4. parity status
5. verification commands and results
6. browser smoke result
7. unverified items
8. commit readiness
9. confirmation of no push/deploy/release mutation unless authorized
```
