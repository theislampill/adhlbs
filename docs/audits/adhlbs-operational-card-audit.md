# ADHLBS Operational Card Audit

Date: 2026-05-16

Repo: `C:\adhlbs`

Branch / head at audit start: `main` / `e2302c6 Generate ADHLBS docs from atomics`

Scope: paste-test the recent research-backed cards and sample existing cards for operator usefulness. This audit treats ADHLBS as an operator sheet for Codex/Hermes/Claude project work, not a glossary.

## Summary

The recent research-backed additions were sourceable, but several still needed stronger pasteable operator language. A passing card must tell an agent when to invoke the concept, what action to take, what mistake it blocks, what evidence or stop condition is required, and how it composes with nearby cards/stacks/packs.

Patch outcome:

| Area | Outcome |
|---|---|
| Recent additions | All 11 rewritten toward trigger/action/verify-stop wording |
| Existing sampled cards | 7 obvious operator gaps tightened |
| New cards | Added 3 highly operational cards: `STATE-IDEMPOTENCY-KEY`, `ARCH-DEPRECATION-POLICY`, `TEST-GOLDEN-EVAL-SET` |
| Source records | Added `IETF-IDEMPOTENCY-KEY` as candidate-stability source |
| Prompt packs | Added idempotency source refs to CI/spec packs; eval pack already covered |
| Schema | No `stop`/`verify` fields added in this pass; recommendation recorded below |

Schema recommendation: add optional `stop` and `verify` fields later, then derive copy text from `directive + use + blocks + stop + verify`. For this pass, stop/verify language was encoded into `directive`, `use`, and `blocks` to avoid a broad schema migration.

## 1. Recent Additions Paste-Test Table

| Card ID | Current problem | Operational classification | Rewrite needed | Patch status |
|---|---|---|---|---|
| `ARCH-ATAM` | Good trigger, but needed explicit evidence output | MISSING_VERIFICATION | Add quality attributes, risks, tradeoffs, rejected options, owner | PATCHED |
| `ARCH-C4-MODEL` | Risked reading as diagram notation | MISSING_STOP_CONDITION | Add start-at-context, stop-before-code, box verification | PATCHED |
| `ARCH-SEMVER` | Versioning rule, but needed release-decision gate | MISSING_VERIFICATION | Add classify diff, block understated version bump, verify notes/tests | PATCHED |
| `ARCH-BACKWARD-COMPATIBILITY` | Good concept, needed project-flow stop point | MISSING_STOP_CONDITION | Add old consumers, examples, migration path, compatibility tests | PATCHED |
| `SEC-EXCESSIVE-AGENCY` | Strong idea, needed concrete authority checklist | MISSING_VERIFICATION | Add allowed/denied/HITL/rollback/logs/self-authorization check | PATCHED |
| `SEC-SBOM` | Inventory-driven but needed failure condition | MISSING_STOP_CONDITION | Add stop when vulnerable component cannot map to artifact | PATCHED |
| `SEC-SLSA` | Provenance-driven but needed release stop | MISSING_VERIFICATION | Add artifact-source-builder trace and fail-closed mismatch | PATCHED |
| `SEC-ASVS` | Could become source-backed checklist | MISSING_PROJECT_FLOW_USE | Add select level/control IDs before implementation and cite tests | PATCHED |
| `REL-STRUCTURED-LOGS` | Operational, but could be generic logging advice | MISSING_VERIFICATION | Add stable fields, no secrets, filterability | PATCHED |
| `REL-TRACE-CONTEXT` | Good concept, needed debugging stop condition | MISSING_STOP_CONDITION | Add cross-boundary trigger and end-to-end failure path requirement | PATCHED |
| `AGENT-AI-RMF` | Governance concept risked compliance theater | MISSING_PROJECT_FLOW_USE | Add high-impact trigger, harms/users/controls/owner/review trigger | PATCHED |

## 2. Operator Rewrite Table

| Card ID | Trigger | Action | Blocks | Verify/Stop | Related flow |
|---|---|---|---|---|---|
| `ARCH-ATAM` | Architecture choice with real quality tradeoffs | Name quality attributes, candidate approaches, risks, sensitivity/tradeoff points, rejected options | Preference/fashion/single-metric architecture | Verify risk owner, affected attributes, evidence for selected option | ADR, C4, compatibility matrix |
| `ARCH-C4-MODEL` | Architecture talk too abstract or diagram too mixed | Start system context, then containers/components only as needed | Code diagrams before actor/system/container boundaries | Verify box name, responsibility, owner/boundary, relationship; stop before code detail unless needed | ATAM, interface contracts |
| `ARCH-SEMVER` | Release/version change | Classify diff as breaking/additive-compatible/patch | Version bump hides compatibility impact | Verify release notes/tests match classification | Backcompat, deprecation policy |
| `ARCH-BACKWARD-COMPATIBILITY` | Changing consumed API/schema/prompt/skill/output | Identify old consumers, examples, migration path, deprecation window | Old clients break silently | Stop if matrix/tests missing for supported consumers | Compatibility matrix, SemVer |
| `SEC-EXCESSIVE-AGENCY` | Granting tools/writes/browser/external/deploy authority | Constrain allowed/denied actions, approval, rollback, logs, stop conditions | Agent uses broad available authority | Verify model cannot self-authorize beyond boundary | Capability allowlist, approval threshold |
| `SEC-SBOM` | Release/dependency review/software handoff | List components, versions, suppliers, dependency relationships, timestamps/provenance | Unknown affected components | Stop if vulnerable component cannot map to artifacts | Supply-chain gate, SLSA |
| `SEC-SLSA` | High-trust release/artifact | Generate and verify provenance from artifact to source and builder | Tampered or untraceable artifacts | Fail closed on missing/mismatched provenance | Supply-chain gate, SBOM |
| `SEC-ASVS` | Web/app security in scope | Choose ASVS level/control IDs before implementation | Generic security signoff | Stop if acceptance criteria are generic/untestable | CSP/CORS/CSRF, output filter |
| `REL-STRUCTURED-LOGS` | Audit/diagnosis needed | Emit stable fields for event, component, operation, actor/request, trace, result, safe error | Prose logs and secret leaks | Verify no secrets and queryable/filterable fields | Observability, trace context |
| `REL-TRACE-CONTEXT` | Flow crosses services/jobs/tools/files/queues | Preserve one request/task identity through logs/errors/handoffs/receipts | Disconnected debugging | Stop debugging claims if failure path cannot be followed end-to-end | Structured logs, OTel |
| `AGENT-AI-RMF` | High-impact agent capability/release | Map harms/users, measure controls, assign owner, manage residual risk | Safety as vibes after implementation | Stop if risk/control/owner/review trigger absent | Eval harness, approval threshold, excessive agency |
| `STATE-IDEMPOTENCY-KEY` | Retrying non-idempotent writes/tool actions | Generate stable operation ID; persist first result; reject conflicting reuse | Duplicate side effects | Verify duplicate attempts do not duplicate effects | Idempotence, retry+jitter, approval threshold |
| `ARCH-DEPRECATION-POLICY` | Removing/changing supported behavior | Name replacement, notice, timeline, compatibility window, usage signal, removal condition | Surprise removals | Stop if consumers cannot migrate safely | Backcompat, SemVer, compatibility matrix |
| `TEST-GOLDEN-EVAL-SET` | Prompt/skill/agent behavior change | Maintain success/failure/adversarial/long-context/source-conflict fixtures and rerun | Vibe-tuned prompts | Stop if changed behavior is not measured against baseline | Eval harness, Evals First, Golden Master |

## 3. Missing Operational Cards Table

| Candidate | Why operational | Best form: card/stack/pack | Existing overlap | Recommendation |
|---|---|---|---|---|
| `STATE-IDEMPOTENCY-KEY` | Directly changes retry/write behavior and prevents duplicate side effects | Card | `STATE-IDEMPOTENCE`, `REL-RETRY-JITTER` | ADD_NOW_AS_CARD |
| Golden Eval Set | Turns prompt/skill changes into repeatable before/after verification | Card | `AGENT-EVAL-HARNESS`, `TEST-GOLDEN-MASTER` | ADD_NOW_AS_CARD |
| Deprecation Policy | Gives concrete removal workflow for compatibility-sensitive changes | Card | `ARCH-BACKWARD-COMPATIBILITY`, `ARCH-SEMVER` | ADD_NOW_AS_CARD |
| Risk Register | Useful only if tied to owner/mitigation/review trigger | Pack/stack clause | `AGENT-AI-RMF`, `SEC-STRIDE` | BACKLOG |
| RACI/DACI | Can clarify authority, but would need a PM/decision-rights cluster | Pack clause | `ARCH-OWNER-FIRST`, `SEC-APPROVAL-THRESHOLD` | BACKLOG |
| INVEST | Helpful for backlog story quality, weak fit for current agent operator sheet | Pack clause | `AGENT-DEFINE-DONE` | BACKLOG |
| MoSCoW | Priority sorting, but overlaps requirement language and can be PM bloat | Pack clause | `ARCH-ADR-RFC`, `PACK-SPEC` | REJECT_AS_BLOAT |
| Wardley Mapping | Strategy tool too large for a compact directive card | Stack or separate guide | Limited | REJECT_AS_BLOAT |
| Supply-chain stack | Good operating recipe for release/provenance work | Stack | `SEC-SUPPLY-CHAIN-GATE`, `SEC-SBOM`, `SEC-SLSA` | ADD_TO_PROMPT_PACK_OR_STACK_LATER |
| AI-risk stack | Good for high-impact agent release | Stack | `AGENT-AI-RMF`, `AGENT-EVAL-HARNESS`, `SEC-APPROVAL-THRESHOLD` | ADD_TO_PROMPT_PACK_OR_STACK_LATER |
| Observability stack | Good for distributed debugging work | Stack | `REL-OBSERVABILITY`, `REL-STRUCTURED-LOGS`, `REL-TRACE-CONTEXT` | ADD_TO_PROMPT_PACK_OR_STACK_LATER |
| Feature Flag | Operational for rollout, but no source basis in atomics yet | Card | `REL-ROLLBACK`, `REL-GRACEFUL-DEGRADATION` | BACKLOG_AFTER_SOURCE |
| Canary | Operational for release risk, but needs source-backed rollout framing | Stack/card | `REL-ROLLBACK`, `REL-OBSERVABILITY` | BACKLOG_AFTER_SOURCE |
| Migration Plan | Operational but current rollback/idempotence/backcompat coverage is strong | Pack clause | `REL-ROLLBACK`, `STATE-IDEMPOTENCE`, `ARCH-BACKWARD-COMPATIBILITY` | MERGE_INTO_EXISTING |
| Rollback Plan | Already operational | Existing card | `REL-ROLLBACK` | MERGE_INTO_EXISTING |
| Compatibility Contract | Already split across matrix/backcompat/interface contract | Existing cards | `ARCH-COMPATIBILITY-MATRIX`, `ARCH-BACKWARD-COMPATIBILITY` | MERGE_INTO_EXISTING |
| Tool Permission Matrix | Useful, but better as capability allowlist wording | Existing card | `SEC-CAPABILITY-ALLOWLIST`, `SEC-EXCESSIVE-AGENCY` | MERGE_INTO_EXISTING |
| Context Window Budget | Already operational for long agent sessions | Existing card | `AGENT-CONTEXT-BUDGET` | MERGE_INTO_EXISTING |

## 4. Rearrangement Table

| Item | Current location | Better location | Reason | Patch status |
|---|---|---|---|---|
| `ARCH-ATAM` | Architecture card | Keep as card | It changes architecture decision flow; related to ADR/C4/matrix | Related links patched |
| `ARCH-C4-MODEL` | Architecture card | Keep as card | It controls architecture explanation scope; not merely a diagram note | Related links patched |
| `ARCH-SEMVER` | Architecture card | Keep as card | Release-version decision belongs near compatibility | Related links patched |
| `ARCH-BACKWARD-COMPATIBILITY` | Architecture card | Keep as card | Applies to schemas/prompts/generated artifacts, not only code | Related links patched |
| `SEC-EXCESSIVE-AGENCY` | Security card | Keep as card | Security placement is correct; directly controls tool grant decisions | Related links patched |
| `SEC-SBOM` | Security card | Keep as card | Separate from supply-chain gate because it produces specific release evidence | No move |
| `SEC-SLSA` | Security card | Keep as card | Separate from SBOM because provenance/build verification changes action | No move |
| `SEC-ASVS` | Security card | Keep as card | App security verification standard belongs with web/security acceptance criteria | No move |
| `REL-STRUCTURED-LOGS` | Reliability card | Keep as card | Operational telemetry primitive; supports observability stack later | No move |
| `REL-TRACE-CONTEXT` | Reliability card | Keep as card | Debugging/handoff identity is operational, not just observability theory | No move |
| `AGENT-AI-RMF` | Agent Control card | Could be stack later | As a card it gates high-impact agent changes; stack deferred | Kept as card |
| `STATE-IDEMPOTENCY-KEY` | New State card | Keep as card | More concrete than general idempotence and highly pasteable for retry/write flows | Added |
| `ARCH-DEPRECATION-POLICY` | New Architecture card | Keep as card | Concrete compatibility/removal workflow | Added |
| `TEST-GOLDEN-EVAL-SET` | New Testing / Verification card | Keep as card | Stronger paste-test value than generic eval source note | Added |
| Supply-chain provenance sequence | Backlog stack | Stack later | Top-of-page stack changes need curation | Deferred |
| AI-risk release sequence | Backlog stack | Stack later | Good composition but too broad for this patch | Deferred |
| Observability trace sequence | Backlog stack | Stack later | Useful but current individual cards suffice | Deferred |

## 5. Research-to-Operator Table

| Source | Concept | Operational lesson | Card/stack/pack effect |
|---|---|---|---|
| CMU SEI ATAM | Architecture tradeoffs | Do not choose architecture without quality attributes, risks, and tradeoffs | `ARCH-ATAM` rewrite: quality attributes, tradeoffs, risk owner |
| C4 Model | Architecture views | Pick the smallest useful zoom level for the stakeholder decision | `ARCH-C4-MODEL` rewrite: context first, stop before code detail |
| SemVer | Compatibility signaling | Version number must match compatibility impact | `ARCH-SEMVER` rewrite; supports deprecation/backcompat |
| Google AIP-180 | Backward compatibility | Compatibility has source, wire, and semantic dimensions | `ARCH-BACKWARD-COMPATIBILITY`, `ARCH-DEPRECATION-POLICY` |
| OWASP LLM06 Excessive Agency | Tool/autonomy overreach | Scope agent capabilities before execution, not after prompt wording | `SEC-EXCESSIVE-AGENCY`, `SEC-CAPABILITY-ALLOWLIST` |
| NTIA SBOM | Component transparency | Release review needs component inventory evidence | `SEC-SBOM` rewrite |
| SLSA | Artifact provenance | Trust requires artifact-to-source/build traceability | `SEC-SLSA` rewrite |
| OWASP ASVS | Security verification | Security acceptance criteria should name testable control IDs | `SEC-ASVS` rewrite |
| OpenTelemetry Logs | Structured telemetry | Logs need stable fields and correlation, not prose-only messages | `REL-STRUCTURED-LOGS` rewrite |
| W3C Trace Context | Correlation identity | Cross-boundary work needs a stable trace/task identity | `REL-TRACE-CONTEXT` rewrite |
| NIST AI RMF / GenAI Profile | AI risk governance | High-impact agent changes need harms, controls, owner, and review trigger | `AGENT-AI-RMF` rewrite; AI-risk stack deferred |
| IETF Idempotency-Key draft | Retry-safe writes | Non-idempotent retries need one operation identity and duplicate-result handling | Added `STATE-IDEMPOTENCY-KEY` |
| arXiv agent evaluation survey | Agent eval dimensions | Prompt/skill changes need repeatable behavior fixtures | Added `TEST-GOLDEN-EVAL-SET`; tightened eval harness |

## Sampled Existing Cards

| Card ID | Classification | Problem | Patch status |
|---|---|---|---|
| `STATE-IDEMPOTENCE` | MISSING_VERIFICATION | Too short; did not say how to verify rerun safety | PATCHED |
| `SEC-CAPABILITY-ALLOWLIST` | MISSING_STOP_CONDITION | Did not specify denied actions or model self-grant risk | PATCHED |
| `SEC-APPROVAL-THRESHOLD` | MISSING_PROJECT_FLOW_USE | Needed exact action classes and approval evidence | PATCHED |
| `ARCH-COMPATIBILITY-MATRIX` | MISSING_VERIFICATION | Matrix concept lacked old/new example verification | PATCHED |
| `AGENT-EVAL-HARNESS` | MISSING_STOP_CONDITION | Needed baseline/failure target stop condition | PATCHED |
| `TEST-GOLDEN-MASTER` | MISSING_VERIFICATION | Needed reproducible baseline stop condition | PATCHED |
| `REL-OBSERVABILITY` | MISSING_VERIFICATION | Needed queryable signal, not noisy logs | PATCHED |
| `AGENT-CONTEXT-BUDGET` | OPERATIONAL_PASS | Clear long-session behavior trigger | NO PATCH |
| `AGENT-DIFF-FIRST` | OPERATIONAL_PASS | Clear stop condition and authority boundary | NO PATCH |
| `AGENT-SMOKE-BEFORE-CLAIM` | OPERATIONAL_PASS | Clear verification behavior | NO PATCH |
| `REL-ROLLBACK` | OPERATIONAL_PASS | Already has deploy/migration trigger and verification | NO PATCH |
| `REL-RUNBOOK` | OPERATIONAL_PASS | Already executable response path | NO PATCH |

## Files Changed By This Audit

Expected durable changes:

```text
atomics/directives.json
atomics/prompt_packs.json
atomics/sources.json
docs/index.html
docs/audits/adhlbs-operational-card-audit.md
```

Pre-existing dirty files from the layout/research passes remain in the worktree and were not reverted.

## Verification Plan

Run:

```powershell
python tools/check_adhlbs_atomics.py
python tools/build_docs_index.py
python tools/check_docs_index_freshness.py
python tools/check_docs_index_offline.py
Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
git diff --check
git status --short
```

Browser smoke should confirm:

```text
166 directive cards
25 stacks
20 prompt packs
62 sources
new/rewritten cards searchable
copy text action-shaped
terse copy useful when pasted
related links work
source refs inert
offline CSP retained
zero active remote assets
```
