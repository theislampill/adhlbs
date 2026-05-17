# ADHLBS Atomics Generation Report

## Summary

ADHLBS was migrated from a hand-maintained `docs/index.html` source of truth to an atomics-driven workflow. Canonical records now live under `atomics/**`; `tools/build_docs_index.py` renders the single-file GitHub Pages artifact at `docs/index.html`; checkers validate atomics, freshness, offline safety, and generated coverage.

No commit, push, tag, deploy, GitHub Pages setting change, or release mutation was performed.

## Repo Inventory

Baseline:

- `README.md`: existed; UTF-16LE encoded.
- `docs/index.html`: existed; static single-file HTML artifact.
- `.github/workflows/**`: did not exist.
- `tools/**`: did not exist.
- `atomics/**`: did not exist.
- package/build scripts: none found.

Created:

- `atomics/adhlbs.schema.json`
- `atomics/directives.json`
- `atomics/stacks.json`
- `atomics/prompt_packs.json`
- `atomics/sources.json`
- `atomics/sections.json`
- `atomics/ui_copy.json`
- `atomics/extraction_findings.json`
- `tools/build_docs_index.py`
- `tools/check_adhlbs_atomics.py`
- `tools/check_docs_index_freshness.py`
- `tools/check_docs_index_offline.py`
- `.github/workflows/verify.yml`
- `docs/audits/adhlbs-atomics-generation-report.md`

Changed:

- `README.md`
- `docs/index.html`

## Atomics Structure

- `directives.json`: 152 directive cards; owns category, name, expansion, why, directive, use, blocks, tags, aliases, source class, related IDs, negative example, and source refs.
- `stacks.json`: 25 dispatch stacks; owns ID, name, risk, workstream tag, stack, use, avoid, stop, and recommended flag.
- `prompt_packs.json`: 20 prompt packs; owns title, tag, risk, source refs, and variants.
- `sources.json`: 48 source records; owns title, inert URL text, source type, stability, notes, supports, last checked, and trust/DOI note.
- `sections.json`: site metadata, section headings, quick rail records, category metadata, legends, defense controls, skill section copy, source map, and footer copy.
- `ui_copy.json`: preserved inline CSS and JS mechanics from the current artifact.

## Pipeline Walk

### 1. Current `docs/index.html`

- Purpose: preserve existing offline-safe UI mechanics and extract current content.
- Owner source: pre-migration `docs/index.html`.
- Generated output: draft atomics.
- Checker/gate: parser counts and extraction findings.
- Failure mode: malformed visible fields or stale hidden search/copy text become canonical.
- Muda: content, copy text, search text, counts, and source table were all embedded in one file.
- Mura: most cards were structured, but one card had shifted fields and many hidden search attributes had serialized list text.
- Muri: operators had to edit HTML, data, copy text, and generated-like metadata together.
- Recommended countermeasure: atomics extraction plus validator and generated freshness check.

### 2. Extracted Atomics

- Purpose: make records the source of truth.
- Owner source: `atomics/*.json`.
- Generated output: rendered cards, stacks, packs, source rows, counts, and copy text.
- Checker/gate: `python tools/check_adhlbs_atomics.py`.
- Failure mode: duplicate IDs, missing fields, bad refs, malformed URLs, invalid risk/stability, split tags.
- Muda: duplicate copy/search data removed from records.
- Mura: normalized `WEB-MOBILE-FIRST`; source refs checked for packs.
- Muri: record-level diffs replace giant HTML-only content edits.
- Recommended countermeasure: keep future content changes in atomics, not HTML.

### 3. Schema / Validator

- Purpose: deterministic guardrails without external dependencies.
- Owner source: `atomics/adhlbs.schema.json` and `tools/check_adhlbs_atomics.py`.
- Generated output: pass/fail stdout/stderr.
- Checker/gate: validator exit code.
- Failure mode: unknown category, unknown source ref, broken related ID, empty directive, invalid risk, malformed URL, missing generated representation.
- Muda: prevents manual duplicate counts and copy overrides.
- Mura: enforces consistent record shape across all categories.
- Muri: reduces reviewer burden by failing early.
- Recommended countermeasure: run validator before and after generation.

### 4. Generator

- Purpose: render `docs/index.html` from atomics.
- Owner source: `tools/build_docs_index.py` plus `atomics/**`.
- Generated output: `docs/index.html`.
- Checker/gate: temp-file validation before atomic replace.
- Failure mode: invalid atomics or unsafe generated HTML aborts before replacing the old file.
- Muda: generated counts/search/copy/source rows replace hand edits.
- Mura: every record follows one render path.
- Muri: content edits no longer require hand-editing UI markup.
- Recommended countermeasure: edit atomics, run generator, review atomics diff first.

### 5. Generated `docs/index.html`

- Purpose: public GitHub Pages artifact.
- Owner source: atomics and generator.
- Generated output: single-file static HTML.
- Checker/gate: generated banner, section presence, derived copy checks, offline scanner.
- Failure mode: stale or hand-edited artifact fails freshness/coverage checks.
- Muda: no external assets or runtime build dependencies.
- Mura: categories and counts derive from records.
- Muri: the artifact remains large but is no longer the editing surface.
- Recommended countermeasure: do not hand-edit except emergency recovery.

### 6. Freshness Checker

- Purpose: prove `docs/index.html` equals a fresh render.
- Owner source: `tools/check_docs_index_freshness.py`.
- Generated output: temp HTML for comparison.
- Checker/gate: byte-for-byte compare.
- Failure mode: stale generated artifact.
- Muda: eliminates manual “did I rebuild?” checks.
- Mura: same render path as the generator.
- Muri: small command gives a crisp stale/fresh answer.
- Recommended countermeasure: run before commit and in CI.

### 7. Offline Checker

- Purpose: enforce no active network behavior.
- Owner source: `tools/check_docs_index_offline.py`.
- Generated output: pass/fail report.
- Checker/gate: forbidden token and active remote URL scan.
- Failure mode: active `href/src/action`, external scripts/styles/images/iframes, or fetch-like APIs.
- Muda: no network runtime or asset pipeline.
- Mura: source URLs remain inert text and copy buttons.
- Muri: reviewers do not need to inspect every URL manually.
- Recommended countermeasure: keep URLs in `sources.json`; render only as `<code>` and `data-copy`.

### 8. README Workflow

- Purpose: document the new workflow.
- Owner source: `README.md`.
- Generated output: concise operator instructions.
- Checker/gate: manual review; README is preexisting UTF-16LE.
- Failure mode: users hand-edit `docs/index.html`.
- Muda: removes obsolete commit/push-only update instructions.
- Mura: aligns docs with tools.
- Muri: fewer hidden steps.
- Recommended countermeasure: consider converting README to UTF-8 in a separate cleanup if desired.

### 9. Optional CI

- Purpose: run the same checks on PR/push.
- Owner source: `.github/workflows/verify.yml`.
- Generated output: GitHub Actions check results.
- Checker/gate: Python tools, freshness, offline scan, py_compile, diff whitespace.
- Failure mode: CI cannot prove deployed Pages settings, only repo artifact correctness.
- Muda: no package manager or external dependency install.
- Mura: CI mirrors local commands.
- Muri: minimal workflow; no release/deploy mutation.
- Recommended countermeasure: user decides whether to keep CI before commit.

### 10. Git Diff Review

- Purpose: make the migration reviewable.
- Owner source: git diff/status.
- Generated output: changed file list and stat.
- Checker/gate: `git diff --check`.
- Failure mode: initial generated artifact diff is large; README appears binary because it was already UTF-16LE.
- Muda: future conceptual diffs should happen in atomics.
- Mura: generated artifact diff is secondary after this migration.
- Muri: first migration review is heavier than future record edits.
- Recommended countermeasure: review atomics/tools first, then generated artifact freshness.

## Malformed / Current-Content Findings

Problem:
`WEB-MOBILE-FIRST` had shifted visible fields: directive contained `['web', 'responsive']`, use was empty, blocks held intended use text, and tags were split into characters.
Surface:
Directive card and copy buttons in current `docs/index.html`.
Owner record:
`atomics/directives.json` record `WEB-MOBILE-FIRST`.
Failure mode:
Bad copy text and misleading visible fields.
Suggested correction:
Use current `why` as directive, current blocks as use, joined character tags as blocks, and parsed pre list as tags.
Status:
Corrected in atomics and generated artifact; documented in `atomics/extraction_findings.json`.

Problem:
146 directive `data-search` attributes contained Python-style serialized tag lists.
Surface:
Hidden search metadata in current `docs/index.html`.
Owner record:
All affected directive records.
Failure mode:
Search text drift and noisy hidden metadata.
Suggested correction:
Derive search text from canonical record fields during render.
Status:
Corrected by generator.

## Muda / Mura / Muri Findings

- Muda: manual counts, duplicate copy text, duplicate search text, repeated source support text, and generated-like metadata embedded in HTML.
- Mura: one malformed card, hidden search metadata inconsistencies, and uneven source linkage between packs and cards.
- Muri: `docs/index.html` was carrying content model, UI, copy text, search index, source table, and public artifact responsibilities at once.

## Hansei

Gap:
One malformed visible directive card.
Cause:
Previous manual/generated field mapping shifted values without a schema gate.
Countermeasure:
Validator rejects empty use, split-character tags, and empty directives; generator derives copy text.
Follow-up evidence:
`python tools/check_adhlbs_atomics.py` passed and browser copy smoke returned corrected DRY copy.

Gap:
Manual counts and search metadata could drift.
Cause:
Counts/search were embedded in HTML.
Countermeasure:
Generator derives nav counts, group counts, search blobs, and copy text.
Follow-up evidence:
Freshness check passed and manual inspection found 25 stacks, 152 cards, 20 packs, 48 sources.

Gap:
Source URLs could accidentally become active links.
Cause:
URLs live in HTML near action buttons.
Countermeasure:
Offline checker rejects active remote `href/src/action` and external asset/script/fetch patterns.
Follow-up evidence:
`python tools/check_docs_index_offline.py` passed; browser smoke saw 0 active remote assets and 0 external anchors.

Gap:
Generated freshness was previously unprovable.
Cause:
No generator/checker existed.
Countermeasure:
Generator writes temp, validates, atomically replaces; freshness checker compares temp render to artifact.
Follow-up evidence:
`python tools/check_docs_index_freshness.py` passed.

## PDCA Actions

- Plan: extract current content into atomics. Do: created JSON records. Check: validator counts and extraction findings. Act: normalized one malformed card.
- Plan: make output reproducible. Do: added generator with temp-file write and replace. Check: build and freshness passed. Act: generated banner added.
- Plan: preserve offline safety. Do: added offline scanner and inert source rendering. Check: static and browser smoke found no active remote assets. Act: CI runs scanner.
- Plan: document workflow. Do: updated README and audit. Check: commands listed and artifact remains `/docs/index.html`. Act: next review can focus on atomics/tools.

## Nemawashi Decisions

- Proposed change: atomics file layout under `atomics/*.json`.
  Affected owners: content editors and reviewers.
  Affected generated surfaces: cards, stacks, packs, sources, counts, search, copy text.
  Affected checkers: all.
  Affected public artifact: `docs/index.html`.
  Tradeoffs: more files, but concept-level diffs.
  Rollback: restore `docs/index.html` from git and remove atomics/tools.
  Decision needed: approve keeping this layout.

- Proposed change: keep minimal CI workflow.
  Affected owners: PR authors.
  Affected generated surfaces: none directly.
  Affected checkers: runs local checks in GitHub Actions.
  Affected public artifact: no deployment mutation.
  Tradeoffs: one new workflow, no Pages setting changes.
  Rollback: remove `.github/workflows/verify.yml`.
  Decision needed: approve keeping CI.

- Proposed change: normalize `WEB-MOBILE-FIRST`.
  Affected owners: directive content.
  Affected generated surfaces: Mobile First card and copy text.
  Affected checkers: validator.
  Affected public artifact: corrected visible card.
  Tradeoffs: fixes plainly malformed mapping without broader semantic rewrite.
  Rollback: edit the atomic record.
  Decision needed: confirm the normalized wording is acceptable.

## Hoshin Alignment

- Objective: keep ADHLBS single-file, offline-safe, GitHub Pages-published, and generated from traceable atomics.
- Owner: `atomics/**` for content; `tools/build_docs_index.py` for rendering; `docs/index.html` for public artifact.
- Metric/check: validator, freshness checker, offline checker, py_compile, browser smoke.
- Review trigger: any atomics edit, generator edit, or generated artifact diff.

## ZTA Trust Boundaries

- Trust boundary: hand-edited `docs/index.html`.
  Policy: do not trust it after atomics exist.
  Verification: freshness checker.
  Failure consequence: stale or drifted public artifact.
  Countermeasure: generated banner and CI check.

- Trust boundary: source URLs.
  Policy: treat as inert copyable text, never active loads.
  Verification: offline checker and browser smoke.
  Failure consequence: network contact from offline artifact.
  Countermeasure: render as `<code class="urltext">` plus copy button only.

- Trust boundary: copied prompt/directive text.
  Policy: derive copy from canonical records.
  Verification: generator validation checks derived `data-copy`.
  Failure consequence: stale or malformed copy buttons.
  Countermeasure: no `copy_text` fields unless matching derivation.

- Trust boundary: counts and categories.
  Policy: derive from atomics.
  Verification: generator validation and manual inspection.
  Failure consequence: misleading nav/group counts.
  Countermeasure: generated counts.

- Trust boundary: local build success.
  Policy: report exact commands and failures.
  Verification: verification section below.
  Failure consequence: false confidence.
  Countermeasure: explicit stdout/stderr outcomes.

## Verification Results

- `python tools/check_adhlbs_atomics.py`: `ATOMICS_OK directives=152 stacks=25 prompt_packs=20 sources=48`
- `python tools/build_docs_index.py`: `BUILD_OK directives=152 stacks=25 prompt_packs=20 sources=48 output=docs/index.html`
- `python tools/check_docs_index_freshness.py`: `FRESHNESS_OK docs/index.html matches atomics build`
- `python tools/check_docs_index_offline.py`: `OFFLINE_CHECK_OK docs/index.html`
- `python -m py_compile tools/build_docs_index.py tools/check_adhlbs_atomics.py tools/check_docs_index_freshness.py tools/check_docs_index_offline.py`: passed with exit code 0.
- `git diff --check`: passed with exit code 0.
- Browser smoke via temporary `http://127.0.0.1:8765/`: title loaded; 152 cards, 25 stacks, 20 packs, 48 sources; compact mode toggled; search for `Mobile First` returned 1 card; reset returned all records; Security filter returned 18 cards; DRY copy button wrote derived text to clipboard; active remote assets and external anchors were 0.
- Live parity against `e59cc0d` via temporary `http://127.0.0.1:8766/`: baseline and generated current both had sticky toolbar, search, category filter, print/reset, compact mode, result summary, nav counts, quick rail, 25 stack rows, stack workstream filter, risk/ID sort, copy-visible-stacks control, 152 directive cards, copy/terse card buttons, expand/collapse card details, 10 defense controls, Claude + Hermes Skills section, 20 prompt packs, copy pack controls, 48 source rows, inert source URLs, offline CSP, and zero active remote assets.
- Live parity corrections made before this report: restored baseline `class="section"` wrappers for generated sections; restored `#collapsePackDetails` so the preserved script wires the pack collapse control; restored `copyAllPacks` primary styling/aria label; removed recommendation stars from canonical stack names so stack copy text matches `e59cc0d`; adjusted prompt-pack copy derivation to match baseline `Normal:` / `Variants:` formatting.

## Unverified Items

- No GitHub Pages settings were inspected or changed.
- No release/deploy behavior was tested.
- No remote link/dead-link checking was run.
- README remains UTF-16LE from the baseline, so normal git diff treats it as binary.

## Next Step

Review the atomics layout, the `WEB-MOBILE-FIRST` normalization, and the optional CI workflow. If accepted, commit in a normal review flow; do not deploy or change Pages settings unless separately authorized.
