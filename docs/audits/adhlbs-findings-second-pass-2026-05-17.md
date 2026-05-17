# ADHLBS Findings Second-Pass Addendum - 2026-05-17

Second-pass correction addendum. It preserves first-pass artifacts and reclassifies overstated fixture/static/local evidence.

- Model runs executed: false
- Live Pages checked: false
- Commit/push/tag/deploy/release performed: false

| Finding | Previous status | Corrected status | Reason | Command/result | Remaining risk |
| --- | --- | --- | --- | --- | --- |
| P3-LICENSE | ALREADY SATISFIED | OWNER DECISION REQUIRED | No LICENSE/LICENCE/COPYING file exists and no owner instruction selected a license. README states no license has been selected and default copyright applies. | `Get-ChildItem -Force | Where-Object { $_.Name -match '^(LICENSE|LICENCE)(\.|$|$)|^COPYING(\.|$|$)' } | Select-Object -ExpandProperty Name` -> No license file names were returned. | Reuse terms remain legally unresolved until the owner chooses a license or explicitly keeps all rights reserved. |
| P1-BEHAVIOR-EVAL-MATRIX | DONE | PARTIAL | The fixture now covers all five required conditions across all six classes, but evidence_level remains fixture-only and model_runs_executed=false. | `python tools/check_behavior_smokes.py` -> BEHAVIOR_SMOKES_OK fixtures=6 conditions=5 evidence_level=fixture-only model_runs_executed=false | No local or live model runs were executed; no measured behavior improvement is claimed. |
| P1-BROWSER-UI-PARITY | DONE | PARTIAL | Static DOM parity remains, and a new live local Chrome/CDP smoke exercises UI behavior, clipboard, keyboard, and print. Evidence is still local-only, not live Pages/public artifact proof. | `python tools/check_docs_index_browser_static.py; python tools/check_docs_index_browser_live.py` -> BROWSER_STATIC_CHECK_OK directives=166 stacks=25 prompt_packs=20 sources=62 common_tasks=5 mode=static-dom; BROWSER_LIVE_CHECK_OK checks=29 tab_steps=14 unique_focus_targets=14 clipboard=checked keyboard=checked print=checked protocol=file mode=chrome-cdp-local | No pushed CI/browser run or live Pages browser smoke has been performed. |
| P1-A11Y-CLOSURE | NOT RUN | PARTIAL | A static accessibility checker verifies semantic controls, labels, focus CSS, keyboard hooks, no positive tabindex, and no-JS fallback. The live browser smoke also exercises Tab and Escape locally. This is not a screen-reader, contrast, or manual assistive-tech audit. | `python tools/check_docs_index_accessibility_static.py; python tools/check_docs_index_browser_live.py` -> ACCESSIBILITY_STATIC_CHECK_OK semantic_controls=checked labels=checked focusability=checked keyboard_hooks=checked no_keyboard_trap=static-only no_js_fallback=checked mode=static-only; BROWSER_LIVE_CHECK_OK checks=29 tab_steps=14 unique_focus_targets=14 clipboard=checked keyboard=checked print=checked protocol=file mode=chrome-cdp-local | Screen reader behavior, contrast measurement, and manual keyboard review remain unverified. |
| P1-LIVE-PUBLIC-PROVENANCE | DONE | PARTIAL | A release/publication gate now preserves the trust boundary: source marker is local/partial, while post-push Actions, live Pages URL, live manifest match, and live copy/source surfaces remain NOT RUN. | `python tools/check_publication_gate.py` -> PUBLICATION_GATE_PARTIAL checked=5 not_run=4 mode=local-gate | No commit, push, tag, deploy, release, GitHub Actions run, live Pages fetch, or live artifact comparison was done. |
| P4-DIRECTIVE-QUALITY | DONE | PARTIAL | Inventory is done, but remediation remains partial. Another high-impact batch used by behavior smokes was strengthened; exact remaining backlog IDs are preserved. | `python tools/check_directive_quality.py` -> DIRECTIVE_QUALITY_OK records=211 patched_high_impact=15 statuses={'keep': 75, 'strengthen': 134, 'merge': 2} | Remediation backlog remains: 136 IDs (CORE-KISS, CORE-YAGNI, CORE-SRP, CORE-SOC, CORE-IH, CORE-OCP, CORE-LOD, CORE-LOP, CORE-SLAP, ARCH-INTERFACE-CONTRACT, ARCH-OWNER-FIRST, ARCH-CC, ARCH-DDD-BC, ARCH-SOLID, ARCH-GRASP, ARCH-PORTS-AMP-ADAPTERS, ARCH-CQRS, ARCH-CONWAY-CHECK, ARCH-ADR, ARCH-API-FIRST...). |
| P2-AGENT-SPECIFIC-PACK-VARIANTS | NOT RUN | DONE | PACK-REPO-STRICT now preserves one semantic core and adds Codex, Claude Code, and Hermes variants covering repo instruction files, approval/sandbox/tool boundaries, verification/reporting style, and no-push/no-release gates. | `python tools/check_adhlbs_atomics.py; python tools/build_docs_index.py; python tools/check_docs_index_freshness.py` -> ATOMICS_OK directives=166 stacks=25 prompt_packs=20 sources=62; BUILD_OK directives=166 stacks=25 prompt_packs=20 sources=62 output=docs/index.html; FRESHNESS_OK docs/index.html matches atomics build directives=166 stacks=25 prompt_packs=20 sources=62 common_tasks=5 schema_version=2026-05-17.audit2 generator_hash=b007e902e3af808a | Only the repo-agent pack has platform-specific variants; other packs remain semantic-core only. |
| P3-COMMON-TASK-LAUNCHER | DONE | DONE | All five required starter tasks are present and now include before/after examples plus explicit placeholder policy. The atomics checker validates task IDs and example fields. | `python tools/check_adhlbs_atomics.py; python tools/build_docs_index.py; python tools/check_docs_index_freshness.py` -> ATOMICS_OK directives=166 stacks=25 prompt_packs=20 sources=62; BUILD_OK directives=166 stacks=25 prompt_packs=20 sources=62 output=docs/index.html; FRESHNESS_OK docs/index.html matches atomics build directives=166 stacks=25 prompt_packs=20 sources=62 common_tasks=5 schema_version=2026-05-17.audit2 generator_hash=b007e902e3af808a | No human usability study was performed; copy safety is checked structurally only. |
| P1-SECOND-PASS-LEDGER | NOT RUN | DONE | Second-pass markdown and JSON addenda were added without rewriting the first-pass completion artifacts. | `python tools/check_publication_gate.py; python tools/check_behavior_smokes.py; python tools/check_directive_quality.py` -> Second-pass addendum records previous status, corrected status, reason, files changed, command run, and remaining risk for each corrected item. | The ledger is local until committed/pushed. |

## Directive Quality Remaining Backlog IDs

- `CORE-KISS`
- `CORE-YAGNI`
- `CORE-SRP`
- `CORE-SOC`
- `CORE-IH`
- `CORE-OCP`
- `CORE-LOD`
- `CORE-LOP`
- `CORE-SLAP`
- `ARCH-INTERFACE-CONTRACT`
- `ARCH-OWNER-FIRST`
- `ARCH-CC`
- `ARCH-DDD-BC`
- `ARCH-SOLID`
- `ARCH-GRASP`
- `ARCH-PORTS-AMP-ADAPTERS`
- `ARCH-CQRS`
- `ARCH-CONWAY-CHECK`
- `ARCH-ADR`
- `ARCH-API-FIRST`
- `ARCH-BFF`
- `STATE-ACID`
- `STATE-BASE`
- `STATE-CAP`
- `STATE-ATOMICS`
- `STATE-ATOMIC-PATCH`
- `STATE-INVARIANTS`
- `STATE-OUTBOX-PATTERN`
- `STATE-FIFO`
- `STATE-RTO-RPO`
- `STATE-PACELC`
- `COMP-CANONICALIZATION`
- `COMP-IR`
- `COMP-AST`
- `COMP-CFG`
- `COMP-SSA`
- `COMP-PARSE-DON-T-VALIDATE`
- `COMP-SCHEMA-GATE`
- `COMP-LOWERING`
- `COMP-NORMAL-FORM`
- `COMP-PHASE-SEPARATION`
- `WEB-HTML-FIRST`
- `WEB-WCAG`
- `WEB-POUR`
- `WEB-A11Y`
- `WEB-I18N-L10N`
- `WEB-RTL-BIDI`
- `WEB-PE`
- `WEB-RWD`
- `WEB-MOBILE-FIRST`
- `WEB-ARIA-LAST`
- `WEB-FEATURE-DETECTION`
- `WEB-CONTENT-FIRST`
- `TEST-TDD`
- `TEST-BDD`
- `TEST-UNIT-TEST`
- `TEST-INTEGRATION-TEST`
- `TEST-E2E`
- `TEST-PBT`
- `TEST-MT`
- `TEST-MUTATION-TESTING`
- `TEST-GOLDEN-MASTER`
- `TEST-GOLDEN-EVAL-SET`
- `TEST-CHARACTERIZATION-TEST`
- `TEST-CONTRACT-TEST`
- `TEST-SMOKE-TEST`
- `AGENT-PLAN-PERSIST`
- `AGENT-BUDGETED-SEARCH`
- `AGENT-PARALLEL-CONTEXT`
- `AGENT-TOOL-PREAMBLE`
- `AGENT-TOOL-POLICY`
- `AGENT-READ-ONLY-FIRST`
- `AGENT-CONTEXT-BUDGET`
- `AGENT-PROGRESSIVE-DISCLOSURE`
- `AGENT-STRUCTURED-OUTPUT`
- `AGENT-QUOTE-FIRST-GROUNDING`
- `AGENT-EVAL-HARNESS`
- `AGENT-AI-RMF`
- `AGENT-TRIGGER-EVALS`
- `AGENT-DIFF-FIRST`
- `AGENT-PLAN-CLOSURE`
- `SEC-DID`
- `SEC-TRUST-BOUNDARY`
- `SEC-NO-SECRETS-IN-PROMPTS`
- `SEC-STRIDE`
- `SEC-DREAD`
- `SEC-CONFUSED-DEPUTY-CHECK`
- `SEC-SECRET-EGRESS-FILTER`
- `SEC-SUPPLY-CHAIN-GATE`
- `SEC-ZTA`
- `SEC-RBAC-ABAC`
- `SEC-CSP-CORS-CSRF`
- `REL-BACKPRESSURE`
- `REL-CIRCUIT-BREAKER`
- `REL-BULKHEAD`
- `REL-TIMEOUTS`
- `REL-RETRY-JITTER`
- `REL-DLQ`
- `REL-OTEL`
- `REL-TRACE-CONTEXT`
- `REL-SLI-SLO-ERROR-BUDGET`
- `REL-MTTR-MTBF`
- `REL-12FA`
- `REL-ROLLBACK`
- `REL-RUNBOOK`
- `REL-POSTMORTEM`
- `REL-GRACEFUL-DEGRADATION`
- `LEAN-KAIZEN`
- `LEAN-JIDOKA`
- `LEAN-GENCHI-GENBUTSU`
- `LEAN-GEMBA`
- `LEAN-POKA-YOKE`
- `LEAN-MUDA-MURA-MURI`
- `LEAN-HANSEI`
- `LEAN-NEMAWASHI`
- `LEAN-PDCA`
- `LEAN-5-WHYS`
- `LEAN-HOSHIN-KANRI`
- `FOUND-SKILL-ENGINEERING`
- `FOUND-SKILL-TRUST-TIERS`
- `FOUND-ACG`
- `FOUND-REACT`
- `FOUND-REFLECT-REPAIR`
- `FOUND-PLANNER-EXECUTOR`
- `FOUND-VERIFIER-ROLE`
- `FOUND-MEMORY-HYGIENE`
- `FOUND-TOOL-USE-TAXONOMY`
- `FOUND-PROMPTWARE-ENGINEERING`
- `FOUND-MCP-BOUNDARY`
- `FOUND-CONTEXT-ENGINEERING`
- `FOUND-RAG-GROUNDING`
- `FOUND-EVALS-FIRST`
- `FOUND-SKILL-LIFECYCLE`
- `DESIGN-CUPID`
- `PACK-LEGACY`
- `PACK-LEGACY-V2`
