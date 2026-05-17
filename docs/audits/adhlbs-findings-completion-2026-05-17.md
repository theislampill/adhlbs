# ADHLBS Findings Completion - 2026-05-17

This ledger represents every actionable finding from the Practical Audit. Status terms are constrained to DONE, ALREADY SATISFIED, TRANSFORMED / SUPERSEDED, BLOCKED, or NOT APPLICABLE.

Baseline before changes:

```text
python tools/check_adhlbs_atomics.py -> ATOMICS_OK directives=166 stacks=25 prompt_packs=20 sources=62
python tools/build_docs_index.py -> BUILD_OK directives=166 stacks=25 prompt_packs=20 sources=62 output=docs/index.html
python tools/check_docs_index_freshness.py -> FRESHNESS_OK docs/index.html matches atomics build
python tools/check_docs_index_offline.py -> OFFLINE_CHECK_OK docs/index.html
Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName } -> pass
npm test / python -m pytest -> not run; no package.json or pyproject.toml present
```

## Findings

| ID | Finding | Status | Evidence files | Verification command | Remaining risk |
|---|---|---:|---|---|---|
| P1-GENERATED-TRUTH | End-to-end generated artifact truth | DONE | `tools/build_docs_index.py`, `tools/check_docs_index_freshness.py`, `docs/index.html` | `python tools/build_docs_index.py`; `python tools/check_docs_index_freshness.py` | Manifest uses a deterministic source-content fallback marker rather than a circular post-commit SHA. |
| P1-BEHAVIOR-SMOKE | Behavior smoke/eval evidence | DONE | `tests/behavior/adhlbs_behavior_smokes.json`, `tools/check_behavior_smokes.py` | `python tools/check_behavior_smokes.py` | Fixture-only; no live model run or measured model improvement claimed. |
| P2-SCHEMA | Harden `atomics/adhlbs.schema.json` | DONE | `atomics/adhlbs.schema.json`, `tools/check_adhlbs_atomics.py` | `python tools/check_adhlbs_atomics.py` | JSON Schema is strengthened; stdlib checker enforces the repo-critical pieces without external jsonschema dependency. |
| P2-EXTRACTION-FINDINGS | Resolve `atomics/extraction_findings.json` | DONE | `AGENTS.md`, `tools/check_adhlbs_atomics.py`, `atomics/extraction_findings.json` | `python tools/check_adhlbs_atomics.py` | Sidecar remains in atomics as intake-only historical evidence; checker blocks undocumented new sidecars. |
| P1P2-PROMPTS-NOT-ENFORCEMENT | Prompt guidance is not enforcement | DONE | `atomics/sections.json`, `tools/build_docs_index.py`, `docs/index.html` | `python tools/check_adhlbs_atomics.py`; `python tools/check_docs_index_browser_static.py` | Source-backed section is static guidance; enforcement still depends on external harness/app controls. |
| P1-BROWSER-UI-PARITY | Browser/UI parity automation | DONE | `tools/check_docs_index_browser_static.py`, `.github/workflows/verify.yml`, `docs/index.html` | `python tools/check_docs_index_browser_static.py` | Static DOM parity only; no live browser/clipboard execution claimed. |
| P3-COMMON-TASKS | Public common tasks launcher | DONE | `atomics/sections.json`, `tools/build_docs_index.py`, `docs/index.html` | `python tools/build_docs_index.py`; `python tools/check_docs_index_browser_static.py` | Launcher prompts are starter frames, not task-specific generated plans. |
| P2-SOURCE-FRESHNESS | Source freshness metadata and checker | DONE | `atomics/sources.json`, `tools/check_source_freshness.py`, `docs/index.html` | `python tools/check_source_freshness.py` | Future date drift will intentionally fail when source review ages past policy. |
| P1-STRUCTURED-WITNESS | Structured audit/witness artifacts | DONE | `docs/audits/adhlbs-findings-completion-2026-05-17.md`, `docs/audits/adhlbs-findings-completion-2026-05-17.json` | `python tools/check_adhlbs_atomics.py`; final ledger review | Ledger is manually curated from command receipts. |
| P3-LICENSE | License decision | ALREADY SATISFIED | `README.md` | `Get-ChildItem -Force -File | Where-Object { $_.Name -match '^(LICENSE|LICENCE)(\\..*)?$|^COPYING$' }` | No license file exists; README already says default copyright applies. Owner choice still needed for reuse. |
| P3-RELEASE-READINESS | Release/provenance readiness | DONE | `CHANGELOG.md`, `.github/workflows/verify.yml`, this ledger | `git tag --list`; `git log --oneline --decorate -5`; CI-equivalent checks | No tag/release was created; release remains pending owner authorization. |
| P4-DIRECTIVE-QUALITY | Acronym density / directive quality audit | DONE | `docs/audits/adhlbs-directive-quality-audit-2026-05-17.md`, `docs/audits/adhlbs-directive-quality-audit-2026-05-17.json`, `tools/check_directive_quality.py`, `atomics/directives.json` | `python tools/check_directive_quality.py` | 138 strengthen items and 2 merge candidates remain tracked by exact ID in the audit JSON. |

## Verification Commands

```text
python tools/check_adhlbs_atomics.py
python tools/build_docs_index.py
python tools/check_docs_index_freshness.py
python tools/check_docs_index_offline.py
python tools/check_docs_index_browser_static.py
python tools/check_source_freshness.py
python tools/check_behavior_smokes.py
python tools/check_directive_quality.py
Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
git diff --check
```

## Release Readiness

Local state check:

```text
branch: main
latest commit: 4b7f842 Generate ADHLBS from atomics and refine operator cards
tags: none observed locally
license: no LICENSE/COPYING file; README states default copyright applies
```

Suggested release title:

```text
ADHLBS audit hardening: provenance, checks, behavior fixtures
```

Draft release notes:

```text
- Add generated artifact build manifest and stricter freshness validation.
- Harden atomic validation for IDs, references, sidecars, schema/UI copy, source metadata, and duplicate IDs.
- Add static UI parity, source freshness, behavior smoke fixture, and directive quality audit checks.
- Add generated common-task launcher and prompt-guidance-is-not-enforcement surface.
- Add completion and release-readiness audit artifacts.
```
