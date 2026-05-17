# ADHLBS Research-Backed Card Gap Audit

Date: 2026-05-16

Repo: `repository root`

Branch / head at audit start: `main` / `e2302c6 Generate ADHLBS docs from atomics`

Scope: research-backed missing-card and source-expansion pass for the atomics-driven ADHLBS single-file artifact. Durable changes were made only through `atomics/**`, `tools/build_docs_index.py`, and generated `docs/index.html`.

## Summary

The audit searched standards, government, security-foundation, engineering-canon, official-project, arXiv, and `.edu`/university-adjacent sources. The strongest gaps were not in the existing lean/agent-control spine; they were in traceable architecture evaluation, architecture communication, compatibility/versioning, supply-chain evidence, structured observability, excessive agency, and AI risk governance.

Patch outcome:

| Area | Outcome |
|---|---|
| Directive cards | Added 11 source-backed cards |
| Source records | Added 13 source records and corrected the OWASP Excessive Agency URL |
| Prompt packs | Added source refs to affected packs; pack counts unchanged |
| Generator | Renders directive `source_refs` as inert source IDs inside card details |
| Generated artifact | Rebuilt `docs/index.html` from atomics; no hand-edit |
| Deferred | Idempotency-Key, project-management frameworks, golden eval set, RACI/DACI, and similar candidates need stronger fit or user decision |

Remote link limitation: web search and targeted source inspection ran, but no crawler-style dead-link validation was run. `REMOTE_LINK_CHECK_NOT_RUN`.

## Searches Run

Required concrete searches were run across the requested source classes, including:

```text
site:edu software engineering requirements specification MUST SHOULD MAY
site:edu software architecture decision record ADR
site:edu software engineering architecture tradeoff analysis method
site:edu LLM agent evaluation benchmark
site:edu human AI collaboration coding benchmark
site:arxiv.org LLM agent evaluation survey
site:arxiv.org agentic reasoning frameworks survey
site:arxiv.org context engineering large language models
site:arxiv.org prompt injection LLM agents
site:arxiv.org LLM coding agents human AI collaboration
site:arxiv.org architectural decision records LLM software architecture
site:nist.gov AI RMF generative AI profile
site:owasp.org Top 10 for LLM Applications 2025
site:rfc-editor.org RFC 2119 MUST SHOULD MAY
site:sre.google SLO error budget
site:sei.cmu.edu architecture decision records software architecture
```

Additional searches covered SBOM, SLSA, OpenTelemetry, W3C Trace Context, C4, SemVer, Google AIP compatibility guidance, RACI, INVEST, MoSCoW, and SMART.

## 1. Source Inventory

| Source | Source class | Topic | URL | Why relevant | Candidate cards supported | Confidence |
|---|---|---|---|---|---|---|
| RFC 2119 | STANDARD | Requirement keywords | https://www.rfc-editor.org/rfc/rfc2119 | Canonical MUST/SHOULD/MAY meanings | Existing `ARCH-ADR-RFC`, `PACK-SPEC` | High |
| RFC 8174 | STANDARD | BCP 14 clarification | https://www.rfc-editor.org/rfc/rfc8174 | Clarifies uppercase normative keyword use | Existing `ARCH-ADR-RFC`, `PACK-SPEC` | High |
| CMU SEI ATAM | EDU | Architecture tradeoff analysis | https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-2/ | Quality-attribute and tradeoff evaluation method | `ARCH-ATAM` | High |
| C4 Model | OFFICIAL_DOCS | Architecture communication | https://c4model.com/ | Official project docs for context/container/component/code views | `ARCH-C4-MODEL` | High |
| SemVer 2.0.0 | STANDARD | Version compatibility | https://semver.org/spec/v2.0.0.html | Stable public API versioning rules | `ARCH-SEMVER`, `ARCH-BACKWARD-COMPATIBILITY` | High |
| Google AIP-180 | OFFICIAL_DOCS | Backward compatibility | https://google.aip.dev/180 | Practical API compatibility dimensions | `ARCH-BACKWARD-COMPATIBILITY` | High |
| Google SRE SLO | ENGINEERING_CANON | SLO/error budget | https://sre.google/workbook/implementing-slos/ | SLO and error budget operating model | Existing `REL-SLI-SLO-ERROR-BUDGET` | High |
| Google SRE Incident Response | ENGINEERING_CANON | Runbooks/incidents | https://sre.google/workbook/incident-response/ | Runbooks, escalation, validation, post-incident handoff | Existing `REL-RUNBOOK` | High |
| Google SRE Postmortem Culture | ENGINEERING_CANON | Postmortems | https://sre.google/sre-book/postmortem-culture/ | Blameless learning and recurrence prevention | Existing `REL-POSTMORTEM` | High |
| OpenTelemetry Signals | OFFICIAL_DOCS | Observability | https://opentelemetry.io/docs/concepts/signals/ | Traces, metrics, logs, baggage, profiles | Existing `REL-OTEL`, `REL-OBSERVABILITY` | High |
| OpenTelemetry Logs | OFFICIAL_DOCS | Structured logs | https://opentelemetry.io/docs/concepts/signals/logs/ | Log signal and correlation context | `REL-STRUCTURED-LOGS` | High |
| W3C Trace Context | STANDARD | Trace propagation | https://www.w3.org/TR/trace-context/ | Traceparent/tracestate interoperability | `REL-TRACE-CONTEXT` | High |
| OWASP LLM Top 10 | SECURITY_FOUNDATION | LLM security | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | LLM app risk taxonomy | Existing security cards, `SEC-EXCESSIVE-AGENCY` | High |
| OWASP LLM01 Prompt Injection | SECURITY_FOUNDATION | Prompt injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | Prompt injection definition and controls | Existing `SEC-PROMPT-INJECTION-DRILL`, `SEC-TRUST-BOUNDARY` | High |
| OWASP LLM06 Excessive Agency | SECURITY_FOUNDATION | Agent/tool authority | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | Tool/function/autonomy overreach | `SEC-EXCESSIVE-AGENCY` | High |
| OWASP ASVS | SECURITY_FOUNDATION | Security verification | https://owasp.org/www-project-application-security-verification-standard/ | Testable app-security requirements | `SEC-ASVS` | High |
| NIST SSDF | GOV | Secure software development | https://csrc.nist.gov/pubs/sp/800/218/final | Secure development and supply-chain practices | Existing `SEC-SUPPLY-CHAIN-GATE`, `SEC-SLSA`, `SEC-SBOM` | High |
| NTIA SBOM Minimum Elements | GOV | SBOM | https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom | Baseline SBOM element guidance | `SEC-SBOM` | High |
| SLSA v1.2 | OFFICIAL_DOCS | Supply-chain provenance | https://slsa.dev/spec/v1.2/ | Artifact/source/build provenance model | `SEC-SLSA` | High |
| NIST AI RMF 1.0 | GOV | AI risk governance | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 | Map/measure/manage/govern risk frame | `AGENT-AI-RMF` | High |
| NIST GenAI Profile | GOV | Generative AI risks | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | GenAI-specific profile for AI RMF | `AGENT-AI-RMF`, `PACK-SEC-HIGH` | High |
| arXiv Agent Evaluation Survey | ARXIV | Agent evals | https://arxiv.org/html/2503.16416v2 | Agent eval dimensions: planning, tool use, memory, reflection | Existing `AGENT-EVAL-HARNESS`, `FOUND-EVALS-FIRST` | Medium |
| Promptware Engineering | ARXIV | Prompt lifecycle | https://arxiv.org/abs/2503.02400 | Treat prompts as software artifacts | Existing `FOUND-PROMPTWARE-ENGINEERING` | Medium |
| IETF Idempotency-Key Draft | STANDARD | HTTP idempotency key | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | Useful but draft/volatile; existing idempotence card partially covers it | Candidate `STATE-IDEMPOTENCY-KEY` | Medium |
| Cornell RACI search result | EDU | Responsibility matrix | https://www.cornell.edu/ | `.edu` discovery only; not strong enough as source basis | RACI/DACI backlog | Low |
| University agile/INVEST search results | EDU | Requirements/project cards | `.edu` search results | Discovery basis only; not primary enough for immediate cards | INVEST/MoSCoW/SMART backlog | Low |

## 2. Existing Coverage Map

| Topic | Existing card/stack/pack | Coverage quality | Gap | Action |
|---|---|---|---|---|
| MUST/SHOULD/MAY / BCP 14 | `ARCH-ADR-RFC`, `PACK-SPEC`, `RFC-2119`, `RFC-8174` | GOOD | Card lacked source refs | Added refs to `ARCH-ADR-RFC` |
| ADR | `ARCH-ADR`, `ARCH-ADR-RFC` | GOOD | No immediate gap | No card added |
| Architecture quality tradeoffs | None explicit | MISSING | Existing ADR captures decision record but not quality-attribute evaluation | Added `ARCH-ATAM` |
| Architecture diagrams | None explicit | PARTIAL | Interface contracts exist but no audience-specific view model | Added `ARCH-C4-MODEL` |
| Semantic versioning | `ARCH-COMPATIBILITY-MATRIX` partial | PARTIAL | Compatibility matrix lacks release-number semantics | Added `ARCH-SEMVER` |
| Backward compatibility | `ARCH-COMPATIBILITY-MATRIX` partial | PARTIAL | No explicit source/wire/semantic compatibility guard | Added `ARCH-BACKWARD-COMPATIBILITY` |
| SLO/SLI/Error Budget | `REL-SLI-SLO-ERROR-BUDGET` | GOOD | Card lacked source refs | Added `GOOGLE-SRE-SLO` ref |
| Runbook | `REL-RUNBOOK` | GOOD | Card lacked source refs | Added Google SRE incident-response ref |
| Postmortem | `REL-POSTMORTEM` | GOOD | Card lacked source refs | Added Google SRE postmortem ref |
| Observability | `REL-OBSERVABILITY`, `REL-OTEL` | PARTIAL | Missing structured-log and trace-context primitives | Added `REL-STRUCTURED-LOGS`, `REL-TRACE-CONTEXT`; added source refs |
| Backpressure / DLQ / retries | `REL-BACKPRESSURE`, `REL-DLQ`, `REL-RETRY-JITTER` | GOOD | No immediate gap | No card added |
| SBOM | `SEC-SUPPLY-CHAIN-GATE` partial | PARTIAL | Dependency inventory deserves named check | Added `SEC-SBOM` |
| SLSA | `SEC-SUPPLY-CHAIN-GATE` partial | PARTIAL | Provenance/build integrity deserves named check | Added `SEC-SLSA` |
| ASVS | Security cards partial | PARTIAL | Testable app-security requirement set absent | Added `SEC-ASVS` |
| OWASP LLM Excessive Agency | `SEC-CAPABILITY-ALLOWLIST`, `SEC-APPROVAL-THRESHOLD` partial | PARTIAL | Named LLM-agent failure mode absent | Added `SEC-EXCESSIVE-AGENCY` and corrected source URL |
| Prompt injection | `SEC-PROMPT-INJECTION-DRILL`, `SEC-TRUST-BOUNDARY` | GOOD | Cards lacked source refs | Added OWASP/NCSC refs |
| AI RMF / GenAI Profile | None explicit | MISSING | Risk governance useful for agent capability releases | Added `AGENT-AI-RMF` |
| Eval-driven development | `AGENT-EVAL-HARNESS`, `FOUND-EVALS-FIRST`, `PACK-EVAL` | GOOD | Cards lacked source refs | Added `AGENT-EVAL-2503` refs |
| Context window budget | `AGENT-CONTEXT-BUDGET`, `FOUND-CONTEXT-ENGINEERING` | GOOD | No immediate source-backed change | No card added |
| RACI/DACI | None explicit | MISSING | Useful but not core enough without new project-management cluster | `NEEDS_USER_DECISION` |
| INVEST/MoSCoW/SMART | None explicit | MISSING | Useful, but could bloat ADHLBS into PM glossary | `NEEDS_USER_DECISION` |

## 3. Candidate Card Backlog

| Candidate ID | Name | Category | Proposed directive | Why it belongs | Primary source basis | Secondary source basis | Overlap with existing cards | Risk of bloat | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| `ARCH-ATAM` | ATAM | Architecture | Evaluate quality-attribute tradeoffs with scenarios and risks before approving architecture. | Captures architecture evaluation, not just decision recording. | CMU SEI ATAM | ADR, compatibility matrix | Low overlap with ADR | Low | ADD_NOW |
| `ARCH-C4-MODEL` | C4 Model | Architecture | Use context/container/component/code views to explain architecture at the right zoom level. | Agents often produce unreadable diagrams; C4 gives a compact scaffold. | C4 Model docs | Interface contracts | Low | Low | ADD_NOW |
| `ARCH-SEMVER` | SemVer | Architecture | Encode compatibility risk in major/minor/patch version changes. | Important for APIs, packages, skills, schemas, generated artifacts. | SemVer 2.0.0 | Compatibility matrix | Medium | Low | ADD_NOW |
| `ARCH-BACKWARD-COMPATIBILITY` | Backward Compatibility | Architecture | Check source, wire, and semantic compatibility before changing consumed surfaces. | Keeps generated/agent artifacts safe for existing consumers. | Google AIP-180 | SemVer | Medium | Low | ADD_NOW |
| `SEC-EXCESSIVE-AGENCY` | Excessive Agency | Security | Reduce tool/function/permission/autonomy before adding prompts. | OWASP LLM Top 10 names this agent-specific risk. | OWASP LLM06 | OWASP LLM Top 10 | Medium with allowlist/approval | Low | ADD_NOW |
| `SEC-SBOM` | SBOM | Security | Require component inventory for releases and dependency review. | Supply-chain risk is hard to audit without component names. | NTIA SBOM | NIST SSDF | Medium with supply-chain gate | Low | ADD_NOW |
| `SEC-SLSA` | SLSA | Security | Generate and verify provenance for high-value artifacts. | Adds build/source provenance discipline beyond inventory. | SLSA spec | NIST SSDF | Medium with supply-chain gate | Low | ADD_NOW |
| `SEC-ASVS` | ASVS | Security | Use ASVS control IDs for web/app security acceptance criteria. | Converts security review into testable controls. | OWASP ASVS | OWASP foundation | Low | Low | ADD_NOW |
| `REL-STRUCTURED-LOGS` | Structured Logs | Reliability | Log events with stable fields and no secrets. | Improves agent/job auditability and operational diagnosis. | OpenTelemetry Logs | OTel signals | Medium with observability | Low | ADD_NOW |
| `REL-TRACE-CONTEXT` | Trace Context | Reliability | Propagate trace IDs across services/tools/queues. | Agent workflows need correlation across tool boundaries. | W3C Trace Context | OpenTelemetry Signals | Medium with observability | Low | ADD_NOW |
| `AGENT-AI-RMF` | AI RMF | Agent Control | Map, measure, manage, and govern risk before material agent releases. | Adds governance-level risk frame for agent capability changes. | NIST AI RMF | NIST GenAI Profile | Low | Low | ADD_NOW |
| `STATE-IDEMPOTENCY-KEY` | Idempotency Key | State | Use explicit idempotency keys for retried unsafe operations. | Very useful for tool/HTTP agents, but current IETF draft is volatile and `STATE-IDEMPOTENCE` partially covers it. | IETF draft | Existing idempotence card | Medium | Medium | ADD_AFTER_SOURCE |
| `TEST-GOLDEN-EVAL-SET` | Golden Eval Set | Testing / Verification | Maintain stable fixtures for regression and behavior drift. | Existing eval cards cover the idea but not named golden sets. | arXiv agent eval survey | Existing `TEST-GOLDEN-MASTER` | High | Medium | MERGE_WITH_EXISTING |
| `AGENT-HUMAN-ESCALATION-THRESHOLD` | Human Escalation Threshold | Security | Escalate before high-impact or low-confidence actions. | Existing `SEC-APPROVAL-THRESHOLD` already covers it well. | OWASP Excessive Agency | NIST AI RMF | High | High | DO_NOT_ADD |
| `PM-RACI-DACI` | RACI / DACI | Lean / Kaizen or new PM category | Name decision/role authority before collaborative work. | Useful for projects, but category fit is weak and source basis was not strong enough. | `.edu` discovery only | None selected | Low | High | NEEDS_USER_DECISION |
| `PM-INVEST` | INVEST | Lean / Kaizen or new PM category | Check stories for independent/negotiable/valuable/estimable/small/testable. | Helpful for backlog grooming, but ADHLBS is not currently a PM glossary. | `.edu` discovery only | Agile sources needed | Low | High | NEEDS_USER_DECISION |
| `PM-MOSCOW` | MoSCoW | Lean / Kaizen or new PM category | Separate Must/Should/Could/Won't priority. | Useful but overlaps with RFC keyword discipline and can bloat. | `.edu` discovery only | Product requirements source needed | Medium | High | NEEDS_USER_DECISION |
| `PM-SMART` | SMART Goals | Lean / Kaizen or new PM category | Make goals specific/measurable/achievable/relevant/time-bound. | Generic utility, but weak fit for this agent directive sheet. | `.edu` discovery only | PM canon needed | Low | High | DO_NOT_ADD |
| `STRATEGY-WARDLEY` | Wardley Mapping | Design Patterns & Tradeoffs | Map value chain and evolution before strategy choices. | Potentially useful, but too large a strategic method for this pass. | Source not selected | None | Low | High | NEEDS_USER_DECISION |
| `DECISION-LOG` | Decision Log | Architecture / Lean | Log decisions, status, owner, and revisit trigger. | Existing ADR already covers structural decisions. | ADR/ATAM sources | Existing ADR | High | Medium | MERGE_WITH_EXISTING |
| `RISK-REGISTER` | Risk Register | Security / Lean | Track risks, owners, mitigations, review date. | Overlaps with AI RMF and threat-model cards; could become useful later. | NIST AI RMF | Threat model cards | Medium | Medium | ADD_AFTER_SOURCE |

## 4. Candidate Stack Backlog

| Stack ID | Name | Risk | Workstream | Stack sequence | Use | Avoid | Stop | Source basis | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| `STACK-SUPPLY-PROVENANCE` | Supply provenance release stack | High | Security | `RTFM -> SBOM -> SLSA -> SSDF -> BUILD -> CHECK -> REPORT` | Release/package/artifact handoff | Small local-only patch | If provenance cannot be generated or verified | NIST SSDF, NTIA SBOM, SLSA | ADD_AFTER_USER_DECISION |
| `STACK-AI-RISK-RELEASE` | Agent risk release stack | High | Agent Control | `AI RMF -> EVAL HARNESS -> APPROVAL THRESHOLD -> SMOKE -> REPORT` | Material agent autonomy or sensitive workflow | Cosmetic prompt-only edits | If harms/owner/controls are unnamed | NIST AI RMF, GenAI Profile | ADD_AFTER_USER_DECISION |
| `STACK-OBSERVABILITY-TRACE` | Traceable ops stack | Medium | Reliability | `OBSERVABILITY -> STRUCTURED LOGS -> TRACE CONTEXT -> RUNBOOK -> POSTMORTEM` | Distributed agent/tool workflow | Static doc-only edit | If no join key exists across events | OTel, W3C Trace Context, Google SRE | ADD_AFTER_USER_DECISION |

No new stacks were added in this pass because the current 25-stack set is already dense and stack additions change top-of-page operating defaults more than card additions.

## 5. Prompt Pack Improvement Backlog

| Pack | Research-backed issue | Proposed improvement | Source basis | Risk | Recommendation |
|---|---|---|---|---|---|
| `PACK-SEC-HIGH` | LLM security source basis was broad | Add explicit prompt-injection, excessive-agency, and AI RMF source refs | OWASP LLM01, OWASP LLM06, NIST AI RMF | Low | PATCHED_SOURCE_REFS |
| `PACK-ARCH` | Architecture pack lacked tradeoff/diagram source basis | Add ATAM and C4 source refs | CMU SEI ATAM, C4 Model | Low | PATCHED_SOURCE_REFS |
| `PACK-SPEC` | Spec pack should also cover compatibility/versioning | Add Google AIP-180 and SemVer source refs | Google AIP-180, SemVer | Low | PATCHED_SOURCE_REFS |
| `PACK-CI` | CI generator pack should reflect provenance/SBOM evidence | Add SLSA and NTIA SBOM refs | SLSA, NTIA SBOM | Low | PATCHED_SOURCE_REFS |
| `PACK-SUPPLY` | Supply-chain review pack lacked SBOM/SLSA refs | Add SBOM and SLSA source refs | NTIA SBOM, SLSA | Low | PATCHED_SOURCE_REFS |
| `PACK-EVAL` | Eval pack can tie to risk governance | Add NIST AI RMF source ref | NIST AI RMF | Low | PATCHED_SOURCE_REF |
| Prompt pack bodies | Existing body wording is compact and recently normalized | No body rewrite in this pass | Current audit/layout pass | Medium | DEFER |

## 6. Source Table Additions

| Source ID | Title | URL | Source type | Stability | Supports | Add now? |
|---|---|---|---|---|---|---|
| `NIST-AI-RMF` | NIST AI Risk Management Framework 1.0 | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 | AI governance | stable | AI RMF, Agent Risk Governance | yes |
| `NIST-GENAI-PROFILE` | NIST AI RMF Generative AI Profile | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | AI governance | stable | AI RMF, Generative AI Risk | yes |
| `SEI-ATAM` | CMU SEI Architecture Tradeoff Analysis Method | https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-2/ | Architecture | stable | ATAM, Architecture Tradeoff Analysis | yes |
| `C4-MODEL` | C4 Model for Visualising Software Architecture | https://c4model.com/ | Architecture | stable | C4 Model, Architecture Communication | yes |
| `SEMVER` | Semantic Versioning 2.0.0 | https://semver.org/spec/v2.0.0.html | Versioning | stable | Semantic Versioning, Deprecation Policy | yes |
| `GOOGLE-AIP-180` | Google AIP-180 Backwards Compatibility | https://google.aip.dev/180 | API design | stable | Backwards Compatibility, API Contracts | yes |
| `NTIA-SBOM` | NTIA Minimum Elements for a Software Bill of Materials | https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom | Security | stable | SBOM, Supply Chain | yes |
| `SLSA` | SLSA Specification v1.2 | https://slsa.dev/spec/v1.2/ | Supply chain security | stable | SLSA, Supply Chain Provenance | yes |
| `OTEL-SIGNALS` | OpenTelemetry Signals | https://opentelemetry.io/docs/concepts/signals/ | Observability | volatile | Observability, OTel | yes |
| `OTEL-LOGS` | OpenTelemetry Logs | https://opentelemetry.io/docs/concepts/signals/logs/ | Observability | volatile | Structured Logs, OTel | yes |
| `W3C-TRACE-CONTEXT` | W3C Trace Context | https://www.w3.org/TR/trace-context/ | Web standard | stable | Trace Context, Trace ID | yes |
| `GOOGLE-SRE-POSTMORTEM` | Google SRE Book: Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | Reliability | stable | Postmortem, Incident Learning | yes |
| `GOOGLE-SRE-INCIDENT-RESPONSE` | Google SRE Workbook: Incident Response | https://sre.google/workbook/incident-response/ | Reliability | stable | Runbook, Incident Response | yes |

Corrected existing source:

| Source ID | Correction | Reason |
|---|---|---|
| `OWASP-AGENCY` | URL changed to `https://genai.owasp.org/llmrisk/llm062025-excessive-agency/` | Existing title said Excessive Agency but URL pointed to Sensitive Information Disclosure |

## Added Cards

| Card | Category | Source refs | Patch reason |
|---|---|---|---|
| `ARCH-ATAM` | Architecture | `SEI-ATAM` | Adds quality-attribute tradeoff analysis |
| `ARCH-C4-MODEL` | Architecture | `C4-MODEL` | Adds architecture communication zoom levels |
| `ARCH-SEMVER` | Architecture | `SEMVER` | Adds explicit release compatibility semantics |
| `ARCH-BACKWARD-COMPATIBILITY` | Architecture | `GOOGLE-AIP-180`, `SEMVER` | Adds compatibility gate for consumed surfaces |
| `SEC-EXCESSIVE-AGENCY` | Security | `OWASP-AGENCY`, `OWASP-LLM` | Adds named LLM agent/tool overreach risk |
| `SEC-SBOM` | Security | `NTIA-SBOM`, `NIST-SSDF` | Adds supply-chain component inventory primitive |
| `SEC-SLSA` | Security | `SLSA`, `NIST-SSDF` | Adds supply-chain provenance/build integrity primitive |
| `SEC-ASVS` | Security | `OWASP-ASVS` | Adds testable app-security requirement standard |
| `REL-STRUCTURED-LOGS` | Reliability | `OTEL-LOGS` | Adds structured event/audit logging primitive |
| `REL-TRACE-CONTEXT` | Reliability | `W3C-TRACE-CONTEXT`, `OTEL-SIGNALS` | Adds trace correlation primitive |
| `AGENT-AI-RMF` | Agent Control | `NIST-AI-RMF`, `NIST-GENAI-PROFILE` | Adds agent release risk-governance frame |

## Guardrail Change

The generator now renders directive `source_refs` in card details:

```text
Sources: [SOURCE-ID] · [SOURCE-ID]
```

These are inert source IDs, not active links. The source table continues to render source URLs as copyable text only.

## Verification Notes

Commands to run after this audit:

```powershell
python tools/check_adhlbs_atomics.py
python tools/build_docs_index.py
python tools/check_docs_index_freshness.py
python tools/check_docs_index_offline.py
Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
git diff --check
git status --short
```

Expected generated counts after this pass:

```text
163 directive cards
25 stacks
20 prompt packs
61 sources
```

## Remaining User Decisions

| Decision | Why it needs user decision |
|---|---|
| Add a project-management category for RACI/DACI/INVEST/MoSCoW/SMART | These are useful but would shift ADHLBS toward a PM glossary |
| Add new stacks for supply-chain provenance / AI risk release / observability tracing | Stacks sit in the top operating-default path and should be intentionally curated |
| Merge golden eval set into existing eval cards | Existing coverage is good; adding another named eval card may duplicate `TEST-GOLDEN-MASTER` and `AGENT-EVAL-HARNESS` |
| Add Idempotency-Key card | Strong practical value, but the IETF source is still draft/volatile and `STATE-IDEMPOTENCE` already exists |
