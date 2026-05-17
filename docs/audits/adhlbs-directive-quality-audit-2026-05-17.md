# ADHLBS Directive Quality Audit - 2026-05-17

Second-pass correction: inventory is DONE, remediation remains PARTIAL. This report now removes the additional behavior-smoke-critical records strengthened in the correction pass from the backlog, while preserving exact remaining backlog IDs.

- Total records: 211
- Counts: {'keep': 75, 'strengthen': 134, 'merge': 2}
- Patched high-impact IDs: CORE-DRY, CORE-SSOT, AGENT-RTFM, AGENT-TRACE, AGENT-CITE-OR-RETRACT, AGENT-SMOKE-BEFORE-CLAIM, SEC-LEAST-PRIVILEGE, SEC-APP-LAYER-GATE, SEC-PROMPT-INJECTION-DRILL, LEAN-ANDON, AGENT-FAIL-LOUD, AGENT-DEFINE-DONE, AGENT-PROMISE-DISCIPLINE, SEC-FAIL-CLOSED, SEC-OUTPUT-FILTER
- Remaining backlog count: 136

## Remaining Backlog IDs

- CORE-KISS
- CORE-YAGNI
- CORE-SRP
- CORE-SOC
- CORE-IH
- CORE-OCP
- CORE-LOD
- CORE-LOP
- CORE-SLAP
- ARCH-INTERFACE-CONTRACT
- ARCH-OWNER-FIRST
- ARCH-CC
- ARCH-DDD-BC
- ARCH-SOLID
- ARCH-GRASP
- ARCH-PORTS-AMP-ADAPTERS
- ARCH-CQRS
- ARCH-CONWAY-CHECK
- ARCH-ADR
- ARCH-API-FIRST
- ARCH-BFF
- STATE-ACID
- STATE-BASE
- STATE-CAP
- STATE-ATOMICS
- STATE-ATOMIC-PATCH
- STATE-INVARIANTS
- STATE-OUTBOX-PATTERN
- STATE-FIFO
- STATE-RTO-RPO
- STATE-PACELC
- COMP-CANONICALIZATION
- COMP-IR
- COMP-AST
- COMP-CFG
- COMP-SSA
- COMP-PARSE-DON-T-VALIDATE
- COMP-SCHEMA-GATE
- COMP-LOWERING
- COMP-NORMAL-FORM
- COMP-PHASE-SEPARATION
- WEB-HTML-FIRST
- WEB-WCAG
- WEB-POUR
- WEB-A11Y
- WEB-I18N-L10N
- WEB-RTL-BIDI
- WEB-PE
- WEB-RWD
- WEB-MOBILE-FIRST
- WEB-ARIA-LAST
- WEB-FEATURE-DETECTION
- WEB-CONTENT-FIRST
- TEST-TDD
- TEST-BDD
- TEST-UNIT-TEST
- TEST-INTEGRATION-TEST
- TEST-E2E
- TEST-PBT
- TEST-MT
- TEST-MUTATION-TESTING
- TEST-GOLDEN-MASTER
- TEST-GOLDEN-EVAL-SET
- TEST-CHARACTERIZATION-TEST
- TEST-CONTRACT-TEST
- TEST-SMOKE-TEST
- AGENT-PLAN-PERSIST
- AGENT-BUDGETED-SEARCH
- AGENT-PARALLEL-CONTEXT
- AGENT-TOOL-PREAMBLE
- AGENT-TOOL-POLICY
- AGENT-READ-ONLY-FIRST
- AGENT-CONTEXT-BUDGET
- AGENT-PROGRESSIVE-DISCLOSURE
- AGENT-STRUCTURED-OUTPUT
- AGENT-QUOTE-FIRST-GROUNDING
- AGENT-EVAL-HARNESS
- AGENT-AI-RMF
- AGENT-TRIGGER-EVALS
- AGENT-DIFF-FIRST
- AGENT-PLAN-CLOSURE
- SEC-DID
- SEC-TRUST-BOUNDARY
- SEC-NO-SECRETS-IN-PROMPTS
- SEC-STRIDE
- SEC-DREAD
- SEC-CONFUSED-DEPUTY-CHECK
- SEC-SECRET-EGRESS-FILTER
- SEC-SUPPLY-CHAIN-GATE
- SEC-ZTA
- SEC-RBAC-ABAC
- SEC-CSP-CORS-CSRF
- REL-BACKPRESSURE
- REL-CIRCUIT-BREAKER
- REL-BULKHEAD
- REL-TIMEOUTS
- REL-RETRY-JITTER
- REL-DLQ
- REL-OTEL
- REL-TRACE-CONTEXT
- REL-SLI-SLO-ERROR-BUDGET
- REL-MTTR-MTBF
- REL-12FA
- REL-ROLLBACK
- REL-RUNBOOK
- REL-POSTMORTEM
- REL-GRACEFUL-DEGRADATION
- LEAN-KAIZEN
- LEAN-JIDOKA
- LEAN-GENCHI-GENBUTSU
- LEAN-GEMBA
- LEAN-POKA-YOKE
- LEAN-MUDA-MURA-MURI
- LEAN-HANSEI
- LEAN-NEMAWASHI
- LEAN-PDCA
- LEAN-5-WHYS
- LEAN-HOSHIN-KANRI
- FOUND-SKILL-ENGINEERING
- FOUND-SKILL-TRUST-TIERS
- FOUND-ACG
- FOUND-REACT
- FOUND-REFLECT-REPAIR
- FOUND-PLANNER-EXECUTOR
- FOUND-VERIFIER-ROLE
- FOUND-MEMORY-HYGIENE
- FOUND-TOOL-USE-TAXONOMY
- FOUND-PROMPTWARE-ENGINEERING
- FOUND-MCP-BOUNDARY
- FOUND-CONTEXT-ENGINEERING
- FOUND-RAG-GROUNDING
- FOUND-EVALS-FIRST
- FOUND-SKILL-LIFECYCLE
- DESIGN-CUPID
- PACK-LEGACY
- PACK-LEGACY-V2

## Inventory

| ID | Type | Status | Reason |
| --- | --- | --- | --- |
| `CORE-DRY` | directive | keep | patched high-impact behavior-smoke gap |
| `CORE-KISS` | directive | strengthen | track for strengthening |
| `CORE-YAGNI` | directive | strengthen | track for strengthening |
| `CORE-SSOT` | directive | keep | patched high-impact behavior-smoke gap |
| `CORE-SRP` | directive | strengthen | track for strengthening |
| `CORE-SOC` | directive | strengthen | track for strengthening |
| `CORE-IH` | directive | strengthen | track for strengthening |
| `CORE-OCP` | directive | strengthen | track for strengthening |
| `CORE-LOD` | directive | strengthen | track for strengthening |
| `CORE-LOP` | directive | strengthen | track for strengthening |
| `CORE-SLAP` | directive | strengthen | track for strengthening |
| `ARCH-INTERFACE-CONTRACT` | directive | strengthen | track for strengthening |
| `ARCH-OWNER-FIRST` | directive | strengthen | track for strengthening |
| `ARCH-CC` | directive | strengthen | track for strengthening |
| `ARCH-DDD-BC` | directive | strengthen | track for strengthening |
| `ARCH-SOLID` | directive | strengthen | track for strengthening |
| `ARCH-GRASP` | directive | strengthen | track for strengthening |
| `ARCH-PORTS-AMP-ADAPTERS` | directive | strengthen | track for strengthening |
| `ARCH-CQRS` | directive | strengthen | track for strengthening |
| `ARCH-CONWAY-CHECK` | directive | strengthen | track for strengthening |
| `ARCH-COMPATIBILITY-MATRIX` | directive | keep | operational enough for current pass |
| `ARCH-ADR` | directive | strengthen | track for strengthening |
| `ARCH-API-FIRST` | directive | strengthen | track for strengthening |
| `ARCH-BFF` | directive | strengthen | track for strengthening |
| `ARCH-ADR-RFC` | directive | keep | operational enough for current pass |
| `ARCH-ATAM` | directive | keep | operational enough for current pass |
| `ARCH-C4-MODEL` | directive | keep | operational enough for current pass |
| `ARCH-SEMVER` | directive | keep | operational enough for current pass |
| `ARCH-BACKWARD-COMPATIBILITY` | directive | keep | operational enough for current pass |
| `ARCH-DEPRECATION-POLICY` | directive | keep | operational enough for current pass |
| `STATE-ACID` | directive | strengthen | track for strengthening |
| `STATE-BASE` | directive | strengthen | track for strengthening |
| `STATE-CAP` | directive | strengthen | track for strengthening |
| `STATE-ATOMICS` | directive | strengthen | track for strengthening |
| `STATE-ATOMIC-PATCH` | directive | strengthen | track for strengthening |
| `STATE-IDEMPOTENCE` | directive | keep | operational enough for current pass |
| `STATE-IDEMPOTENCY-KEY` | directive | keep | operational enough for current pass |
| `STATE-INVARIANTS` | directive | strengthen | track for strengthening |
| `STATE-OUTBOX-PATTERN` | directive | strengthen | track for strengthening |
| `STATE-FIFO` | directive | strengthen | track for strengthening |
| `STATE-RTO-RPO` | directive | strengthen | track for strengthening |
| `STATE-PACELC` | directive | strengthen | track for strengthening |
| `COMP-CANONICALIZATION` | directive | strengthen | track for strengthening |
| `COMP-IR` | directive | strengthen | track for strengthening |
| `COMP-AST` | directive | strengthen | track for strengthening |
| `COMP-CFG` | directive | strengthen | track for strengthening |
| `COMP-SSA` | directive | strengthen | track for strengthening |
| `COMP-PARSE-DON-T-VALIDATE` | directive | strengthen | track for strengthening |
| `COMP-SCHEMA-GATE` | directive | strengthen | track for strengthening |
| `COMP-LOWERING` | directive | strengthen | track for strengthening |
| `COMP-NORMAL-FORM` | directive | strengthen | track for strengthening |
| `COMP-PHASE-SEPARATION` | directive | strengthen | track for strengthening |
| `WEB-HTML-FIRST` | directive | strengthen | track for strengthening |
| `WEB-WCAG` | directive | strengthen | track for strengthening |
| `WEB-POUR` | directive | strengthen | track for strengthening |
| `WEB-A11Y` | directive | strengthen | track for strengthening |
| `WEB-I18N-L10N` | directive | strengthen | track for strengthening |
| `WEB-RTL-BIDI` | directive | strengthen | track for strengthening |
| `WEB-PE` | directive | strengthen | track for strengthening |
| `WEB-RWD` | directive | strengthen | track for strengthening |
| `WEB-MOBILE-FIRST` | directive | strengthen | track for strengthening |
| `WEB-ARIA-LAST` | directive | strengthen | track for strengthening |
| `WEB-FEATURE-DETECTION` | directive | strengthen | track for strengthening |
| `WEB-CONTENT-FIRST` | directive | strengthen | track for strengthening |
| `TEST-TDD` | directive | strengthen | track for strengthening |
| `TEST-BDD` | directive | strengthen | track for strengthening |
| `TEST-UNIT-TEST` | directive | strengthen | track for strengthening |
| `TEST-INTEGRATION-TEST` | directive | strengthen | track for strengthening |
| `TEST-E2E` | directive | strengthen | track for strengthening |
| `TEST-PBT` | directive | strengthen | track for strengthening |
| `TEST-MT` | directive | strengthen | track for strengthening |
| `TEST-MUTATION-TESTING` | directive | strengthen | track for strengthening |
| `TEST-GOLDEN-MASTER` | directive | strengthen | track for strengthening |
| `TEST-GOLDEN-EVAL-SET` | directive | strengthen | track for strengthening |
| `TEST-CHARACTERIZATION-TEST` | directive | strengthen | track for strengthening |
| `TEST-CONTRACT-TEST` | directive | strengthen | track for strengthening |
| `TEST-SMOKE-TEST` | directive | strengthen | track for strengthening |
| `AGENT-RTFM` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-TRACE` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-DEFINE-DONE` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-PLAN-PERSIST` | directive | strengthen | track for strengthening |
| `AGENT-BUDGETED-SEARCH` | directive | strengthen | track for strengthening |
| `AGENT-PARALLEL-CONTEXT` | directive | strengthen | track for strengthening |
| `AGENT-TOOL-PREAMBLE` | directive | strengthen | track for strengthening |
| `AGENT-TOOL-POLICY` | directive | strengthen | track for strengthening |
| `AGENT-READ-ONLY-FIRST` | directive | strengthen | track for strengthening |
| `AGENT-CONTEXT-BUDGET` | directive | strengthen | track for strengthening |
| `AGENT-PROGRESSIVE-DISCLOSURE` | directive | strengthen | track for strengthening |
| `AGENT-STRUCTURED-OUTPUT` | directive | strengthen | track for strengthening |
| `AGENT-QUOTE-FIRST-GROUNDING` | directive | strengthen | track for strengthening |
| `AGENT-CITE-OR-RETRACT` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-EVAL-HARNESS` | directive | strengthen | track for strengthening |
| `AGENT-AI-RMF` | directive | strengthen | track for strengthening |
| `AGENT-TRIGGER-EVALS` | directive | strengthen | track for strengthening |
| `AGENT-SMOKE-BEFORE-CLAIM` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-DIFF-FIRST` | directive | strengthen | track for strengthening |
| `AGENT-PLAN-CLOSURE` | directive | strengthen | track for strengthening |
| `AGENT-FAIL-LOUD` | directive | keep | patched high-impact behavior-smoke gap |
| `AGENT-PROMISE-DISCIPLINE` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-DID` | directive | strengthen | track for strengthening |
| `SEC-TRUST-BOUNDARY` | directive | strengthen | track for strengthening |
| `SEC-LEAST-PRIVILEGE` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-FAIL-CLOSED` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-NO-SECRETS-IN-PROMPTS` | directive | strengthen | track for strengthening |
| `SEC-APP-LAYER-GATE` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-OUTPUT-FILTER` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-CAPABILITY-ALLOWLIST` | directive | keep | operational enough for current pass |
| `SEC-APPROVAL-THRESHOLD` | directive | keep | operational enough for current pass |
| `SEC-STRIDE` | directive | strengthen | track for strengthening |
| `SEC-DREAD` | directive | strengthen | track for strengthening |
| `SEC-CONFUSED-DEPUTY-CHECK` | directive | strengthen | track for strengthening |
| `SEC-PROMPT-INJECTION-DRILL` | directive | keep | patched high-impact behavior-smoke gap |
| `SEC-SECRET-EGRESS-FILTER` | directive | strengthen | track for strengthening |
| `SEC-SUPPLY-CHAIN-GATE` | directive | strengthen | track for strengthening |
| `SEC-ZTA` | directive | strengthen | track for strengthening |
| `SEC-RBAC-ABAC` | directive | strengthen | track for strengthening |
| `SEC-CSP-CORS-CSRF` | directive | strengthen | track for strengthening |
| `SEC-EXCESSIVE-AGENCY` | directive | keep | operational enough for current pass |
| `SEC-SBOM` | directive | keep | operational enough for current pass |
| `SEC-SLSA` | directive | keep | operational enough for current pass |
| `SEC-ASVS` | directive | keep | operational enough for current pass |
| `REL-BACKPRESSURE` | directive | strengthen | track for strengthening |
| `REL-CIRCUIT-BREAKER` | directive | strengthen | track for strengthening |
| `REL-BULKHEAD` | directive | strengthen | track for strengthening |
| `REL-TIMEOUTS` | directive | strengthen | track for strengthening |
| `REL-RETRY-JITTER` | directive | strengthen | track for strengthening |
| `REL-DLQ` | directive | strengthen | track for strengthening |
| `REL-OBSERVABILITY` | directive | keep | operational enough for current pass |
| `REL-OTEL` | directive | strengthen | track for strengthening |
| `REL-STRUCTURED-LOGS` | directive | keep | operational enough for current pass |
| `REL-TRACE-CONTEXT` | directive | strengthen | track for strengthening |
| `REL-SLI-SLO-ERROR-BUDGET` | directive | strengthen | track for strengthening |
| `REL-MTTR-MTBF` | directive | strengthen | track for strengthening |
| `REL-12FA` | directive | strengthen | track for strengthening |
| `REL-ROLLBACK` | directive | strengthen | track for strengthening |
| `REL-RUNBOOK` | directive | strengthen | track for strengthening |
| `REL-POSTMORTEM` | directive | strengthen | track for strengthening |
| `REL-GRACEFUL-DEGRADATION` | directive | strengthen | track for strengthening |
| `LEAN-KAIZEN` | directive | strengthen | track for strengthening |
| `LEAN-JIDOKA` | directive | strengthen | track for strengthening |
| `LEAN-ANDON` | directive | keep | patched high-impact behavior-smoke gap |
| `LEAN-GENCHI-GENBUTSU` | directive | strengthen | track for strengthening |
| `LEAN-GEMBA` | directive | strengthen | track for strengthening |
| `LEAN-POKA-YOKE` | directive | strengthen | track for strengthening |
| `LEAN-MUDA-MURA-MURI` | directive | strengthen | track for strengthening |
| `LEAN-HANSEI` | directive | strengthen | track for strengthening |
| `LEAN-NEMAWASHI` | directive | strengthen | track for strengthening |
| `LEAN-PDCA` | directive | strengthen | track for strengthening |
| `LEAN-5-WHYS` | directive | strengthen | track for strengthening |
| `LEAN-HOSHIN-KANRI` | directive | strengthen | track for strengthening |
| `FOUND-SKILL-ENGINEERING` | directive | strengthen | track for strengthening |
| `FOUND-SKILL-TRUST-TIERS` | directive | strengthen | track for strengthening |
| `FOUND-ACG` | directive | strengthen | track for strengthening |
| `FOUND-REACT` | directive | strengthen | track for strengthening |
| `FOUND-REFLECT-REPAIR` | directive | strengthen | track for strengthening |
| `FOUND-PLANNER-EXECUTOR` | directive | strengthen | track for strengthening |
| `FOUND-VERIFIER-ROLE` | directive | strengthen | track for strengthening |
| `FOUND-MEMORY-HYGIENE` | directive | strengthen | track for strengthening |
| `FOUND-TOOL-USE-TAXONOMY` | directive | strengthen | track for strengthening |
| `FOUND-PROMPTWARE-ENGINEERING` | directive | strengthen | track for strengthening |
| `FOUND-MCP-BOUNDARY` | directive | strengthen | track for strengthening |
| `FOUND-CONTEXT-ENGINEERING` | directive | strengthen | track for strengthening |
| `FOUND-RAG-GROUNDING` | directive | strengthen | track for strengthening |
| `FOUND-EVALS-FIRST` | directive | strengthen | track for strengthening |
| `FOUND-SKILL-LIFECYCLE` | directive | strengthen | track for strengthening |
| `DESIGN-CUPID` | directive | strengthen | track for strengthening |
| `STACK-CODE-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-DATA-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-AGENT-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-SEC-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-RESEARCH-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-AUTO-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-WEB-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-LEGACY-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-SPEC-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-SEC-02` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-PERF-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-REL-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-WEB-02` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-TEST-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-LEAN-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-HARNESS-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-PROMPT-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-CI-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-A11Y-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-RAG-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-SKILL-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-REDTEAM-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-CONTRACT-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-DOCS-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `STACK-BROWSER-01` | stack | keep | stack has use/avoid/stop and bounded workstream |
| `PACK-REPO-STRICT` | prompt_pack | keep | agent variants added for repo pack |
| `PACK-SKILL-STRICT` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-SEC-HIGH` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-RESEARCH` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-HERMES` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-WEB` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-ARCH` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-TEST` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-LEGACY` | prompt_pack | merge | merge candidate due overlapping legacy refactor packs |
| `PACK-SPEC` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-PROMPTWARE` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-CI` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-SKILL-TRUST` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-HARNESS` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-RAG` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-A11Y` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-I18N` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-SUPPLY` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-EVAL` | prompt_pack | keep | pack has Normal/Strict/Exploratory variants and source basis |
| `PACK-LEGACY-V2` | prompt_pack | merge | merge candidate due overlapping legacy refactor packs |
