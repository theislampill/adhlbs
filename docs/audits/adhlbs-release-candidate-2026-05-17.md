# ADHLBS Release Candidate Ledger - 2026-05-17

**Verdict:** LOCAL RELEASE CANDIDATE: checks pass locally; public release remains blocked on owner license decision and authorized push/deploy/live verification.

- Commit/push/tag/deploy/release performed: false
- Live Pages checked: false
- Model runs executed: false
- docs/index.html fresh: true
- CI includes relevant local/static/fixture checks: true

## Corrected Status Table

| Finding | Status | Evidence | Remaining proof gap | Next action |
| --- | --- | --- | --- | --- |
| Generated artifact truth | DONE locally | `docs/index.html`, `tools/build_docs_index.py`, `tools/check_docs_index_freshness.py` | Public commit/Pages provenance remains gated separately. | After authorized push, compare live Pages manifest to repo artifact. |
| Schema / atomics / sidecar policy | DONE locally | `atomics/adhlbs.schema.json`, `tools/check_adhlbs_atomics.py`, `atomics/extraction_findings.json` | No external jsonschema runtime is used; stdlib checker owns repo-critical enforcement. | Keep checker in CI. |
| Prompt guidance is not enforcement | DONE locally | `atomics/sections.json`, `docs/index.html` | Actual enforcement still depends on external app/harness permissions, validation, and approvals. | Do not describe prompt text as a security boundary. |
| Behavior evidence | PARTIAL / FIXTURE-ONLY | `tests/behavior/adhlbs_behavior_smokes.json`, `tools/check_behavior_smokes.py` | No controlled model runs and no measured behavior improvement claim. | Run controlled model evals before A/B improvement claims. |
| Browser/UI parity | PARTIAL / LOCAL-ONLY | `tools/check_docs_index_browser_static.py`, `tools/check_docs_index_browser_live.py` | No deployed Pages browser proof. | Run smoke against live Pages after authorized deployment. |
| Accessibility | PARTIAL / STATIC+LOCAL | `tools/check_docs_index_accessibility_static.py`, `tools/check_docs_index_browser_live.py` | Screen reader, contrast, and full manual keyboard review not run. | Run manual accessibility pass before claiming full accessibility closure. |
| Common-task launcher | DONE locally | `atomics/sections.json`, `docs/index.html` | No user study; copy-safety is structural. | None required for release-candidate proof hygiene. |
| Agent-specific repo pack variants | DONE scoped to PACK-REPO-STRICT | `atomics/prompt_packs.json`, `tools/check_adhlbs_atomics.py`, `docs/index.html` | This does not claim every prompt pack has Codex/Claude Code/Hermes variants. | Add platform variants to other packs only when concrete task evidence needs them. |
| Prompt-pack variant quality | DONE locally | `atomics/prompt_packs.json`, `tools/check_adhlbs_atomics.py` | Quality is structural text validation, not live prompt performance. | Use behavior evals before performance claims. |
| Stack quality gates | DONE locally | `atomics/stacks.json`, `tools/check_adhlbs_atomics.py` | Checker enforces visible use/avoid/stop and gate/evidence language; it does not prove runtime enforcement. | Add task-specific stack checks when new high-risk stacks are introduced. |
| Directive quality remediation | PARTIAL remediation / DONE inventory | `docs/audits/adhlbs-directive-quality-audit-2026-05-17.json`, `tools/check_directive_quality.py` | 136 backlog IDs remain. | Treat remaining_backlog_ids as post-release remediation unless owner wants another cleanup pass. |
| License | OWNER DECISION REQUIRED | `README.md` | No LICENSE/COPYING file exists and owner has not selected license terms. | Owner chooses a license or confirms all-rights-reserved stance. |
| Public provenance / release | PARTIAL / NOT RUN publicly | `docs/audits/adhlbs-publication-gate-2026-05-17.json`, `tools/check_publication_gate.py` | No commit, push, post-push CI run, tag, deploy, release, live URL check, or live manifest comparison. | Run owner-authorized push/deploy verification sequence. |
| CI coverage | DONE for non-public local/CI checks | `.github/workflows/verify.yml` | Post-push Actions pass not run; live Pages proof not in CI. | Inspect Actions after push and run live Pages checklist. |
| Audit evidence path hygiene | DONE locally | `tools/check_audit_evidence_links.py`, `docs/audits/*.md`, `docs/audits/*.json` | None for local absolute path pattern currently checked. | Keep checker in CI. |

## Verification Results

- `python tools/check_adhlbs_atomics.py` -> `ATOMICS_OK directives=166 stacks=25 prompt_packs=20 sources=62`
- `python tools/build_docs_index.py` -> `BUILD_OK directives=166 stacks=25 prompt_packs=20 sources=62 output=docs/index.html`
- `python tools/check_docs_index_freshness.py` -> `FRESHNESS_OK docs/index.html matches atomics build directives=166 stacks=25 prompt_packs=20 sources=62 common_tasks=5 schema_version=2026-05-17.audit3 generator_hash=1f60c64ee008f4ab`
- `python tools/check_docs_index_offline.py` -> `OFFLINE_CHECK_OK docs/index.html`
- `python tools/check_docs_index_browser_static.py` -> `BROWSER_STATIC_CHECK_OK directives=166 stacks=25 prompt_packs=20 sources=62 common_tasks=5 mode=static-dom`
- `python tools/check_docs_index_browser_live.py` -> `BROWSER_LIVE_CHECK_OK checks=29 tab_steps=14 unique_focus_targets=14 clipboard=checked keyboard=checked print=checked protocol=file mode=chrome-cdp-local`
- `python tools/check_docs_index_accessibility_static.py` -> `ACCESSIBILITY_STATIC_CHECK_OK semantic_controls=checked labels=checked focusability=checked keyboard_hooks=checked no_keyboard_trap=static-only no_js_fallback=checked mode=static-only`
- `python tools/check_source_freshness.py` -> `SOURCE_FRESHNESS_OK sources=62 stable=37 volatile=22 candidate=3 policy_days={'stable': 730, 'volatile': 180, 'candidate': 120}`
- `python tools/check_behavior_smokes.py` -> `BEHAVIOR_SMOKES_OK fixtures=6 conditions=5 patch_implied=checked evidence_level=fixture-only model_runs_executed=false`
- `python tools/check_directive_quality.py` -> `DIRECTIVE_QUALITY_OK records=211 patched_high_impact=15 statuses={'keep': 75, 'strengthen': 134, 'merge': 2}`
- `python tools/check_publication_gate.py` -> `PUBLICATION_GATE_PARTIAL checked=5 not_run=4 mode=local-gate`
- `python tools/check_audit_evidence_links.py` -> `AUDIT_EVIDENCE_LINKS_OK files=15 mode=repo-relative`
- `Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }` -> `pass`
- `git diff --check` -> `pass; CRLF conversion warnings only`

## CI Coverage Result

`.github/workflows/verify.yml` runs atomics, build, freshness, offline, static browser parity, local Chrome/CDP browser smoke, static accessibility, source freshness, behavior fixture validation, directive quality, publication gate, audit-link hygiene, Python compile, and diff whitespace checks. Public Pages proof remains outside CI until a deployment exists.

## Files Changed

### atomics
- `atomics/adhlbs.schema.json`
- `atomics/directives.json`
- `atomics/prompt_packs.json`
- `atomics/sections.json`
- `atomics/stacks.json`

### tools
- `tools/build_docs_index.py`
- `tools/check_adhlbs_atomics.py`
- `tools/check_docs_index_freshness.py`
- `tools/check_behavior_smokes.py`
- `tools/check_audit_evidence_links.py`
- `tools/check_docs_index_browser_static.py`
- `tools/check_docs_index_browser_live.py`
- `tools/check_docs_index_accessibility_static.py`
- `tools/check_source_freshness.py`
- `tools/check_directive_quality.py`
- `tools/check_publication_gate.py`

### docs
- `docs/index.html`
- `docs/audits/adhlbs-release-candidate-2026-05-17.md`
- `docs/audits/adhlbs-release-candidate-2026-05-17.json`
- `docs/audits/adhlbs-publication-gate-2026-05-17.md`
- `docs/audits/adhlbs-findings-second-pass-2026-05-17.md`

### workflow
- `.github/workflows/verify.yml`

### tests
- `tests/behavior/adhlbs_behavior_smokes.json`

## Remaining Non-Local Proof Gaps

- No controlled model runs; behavior evidence remains fixture-only.
- No live Pages verification; browser proof remains local Chrome/file proof.
- No manual screen-reader, contrast, or full keyboard accessibility pass.
- No post-push GitHub Actions run was observed.
- No commit, push, tag, deploy, release, or live manifest comparison was performed.

## Owner Decisions Required

- Choose license terms or intentionally keep all-rights-reserved.
- Authorize branch push/PR/release workflow.
- Decide whether directive remediation backlog is pre-release or post-release.

## Recommended Commit Message

`Harden ADHLBS audit checks and release evidence`

## Draft Release Notes

- Add generated artifact build manifest and stricter freshness validation.
- Harden atomic validation for IDs, references, sidecars, prompt-pack variant quality, stack gates, source metadata, and duplicate IDs.
- Add static UI parity, local Chrome/CDP browser smoke, static accessibility smoke, source freshness, behavior fixture, directive quality, publication gate, and audit-link hygiene checks.
- Add generated common-task launcher, agent-specific repo prompt-pack variants, and prompt-guidance-is-not-enforcement surface.
- Add release-candidate ledger that separates local proof from fixture-only, static-only, local-only, owner-decision, and public proof gaps.

## Owner-run Commands, Not Executed

```powershell
git status --short
git diff --stat
git diff --check
git switch -c audit-hardening-release-candidate
git add AGENTS.md CHANGELOG.md .github/workflows/verify.yml atomics tools tests docs
git commit -m "Harden ADHLBS audit checks and release evidence"
git push -u origin audit-hardening-release-candidate
```

Higher-risk direct main push, not executed:

```powershell
git add AGENTS.md CHANGELOG.md .github/workflows/verify.yml atomics tools tests docs
git commit -m "Harden ADHLBS audit checks and release evidence"
git push origin main
```

## Post-push / Post-deploy Verification Checklist

- Confirm GitHub Actions verify workflow passes for the pushed commit.
- Open the GitHub Pages URL after deployment.
- Fetch live HTML and compare its adhlbs-build-manifest to docs/index.html.
- Run live search/filter/copy/source smoke against the Pages URL.
- Record live URL, commit SHA, CI run URL, and manifest comparison in a release note or follow-up ledger.

## Exact Remaining Backlog IDs

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
