# ADHLBS Layout, Interaction, Content, and Card-Taxonomy Audit

Date: 2026-05-16
Repo: `repository root`
Branch: `main`
Current baseline: atomics-driven generator workflow already present.

## Summary

This audit followed `RTFM -> SUBAGENT AUDIT -> FINDINGS -> SMALL PATCHES -> BUILD -> CHECK -> BROWSER SMOKE -> REPORT`.

Literal subagents were used for Layout/IA, Interaction/Copy, Card Field Quality, Prompt Pack Quality, Added Card Gap Analysis, and Source/Evidence. Generator/Checker and Accessibility/Mobile/Print were emulated locally after the subagent limit was reached.

The generated artifact remains `docs/index.html`. Durable changes were made through `atomics/**`, `tools/build_docs_index.py`, `tools/check_adhlbs_atomics.py`, and `AGENTS.md`; `docs/index.html` was regenerated, not hand-edited.

Primary patch decision: prompt packs already respond to global search, so the smallest honest fix was to keep both controls and rename/align behavior:

- `Copy all packs`: copies all prompt packs, ignoring current search.
- `Copy filtered packs`: copies only prompt packs currently visible after search.
- Bulk pack copy now uses the same canonical `data-copy` text as individual pack buttons.
- Prompt pack variants are now canonical `Normal`, `Strict`, and `Exploratory` records instead of a combined second bucket.

## Subagent Coverage

| Pass | Mode | Scope | Result |
|---|---|---|---|
| A Layout / Information Architecture | Literal subagent | Full page structure, section order, control fit | Completed |
| B Interaction / Copy Behavior | Literal subagent | Copy buttons, filters, reset, sorting, collapse controls | Completed |
| C Card Field Quality | Literal subagent | 152 directive cards and generated card text | Completed |
| D Prompt Pack Quality | Literal subagent | 20 prompt packs, variants, copy behavior | Completed |
| E Additional Card Gap Analysis | Literal subagent | Missing high-leverage directive backlog | Completed |
| F Source / Evidence Audit | Literal subagent | 48 sources and source refs | Completed |
| G Generator / Atomics / Checker Audit | Emulated locally | Generator, validators, freshness/offline checks, CI | Completed |
| H Accessibility / Mobile / Print Audit | Emulated locally | Labels, semantics, keyboard, mobile, print | Completed |

## Section Layout Table

| Section | Purpose | Current issue | User impact | Smallest fix | Patch status |
|---|---|---|---|---|---|
| Header | Establish artifact identity and offline contract | Good; no visual redesign needed | Low risk | Leave unchanged | No patch |
| Sticky toolbar | Global search, card category filter, print, reset, compact, summary | Search placeholder said directives although it filters stacks, cards, packs, and sources | Users underuse global search | Rename placeholder to describe all surfaces | Patched |
| Nav | Jump links and counts | Counts are clear and generated | Low risk | Leave unchanged | No patch |
| Quick rail | Fast-copy operating defaults | Copy buttons all had generic `Copy text` aria labels | Screen reader users cannot distinguish buttons | Add contextual quick-copy aria labels | Patched |
| Default Dispatch Stacks | Fast task routing | Risk sort label did not say direction | Sort effect is not obvious | Rename to `Sort by risk high-first` | Patched |
| Defense in Depth | Compact D1-D10 LLM-agent controls | Defense names were stored in posture strings, producing awkward heading composition risk | Headings could appear malformed as `D1 · · Scope...` | Split `name` and `posture`; join only non-empty heading parts | Patched |
| Directive Cards | Canonical directive library | Huge section dominates page; category headers were styled spans | Scanning and heading navigation weaker than necessary | Render category names as `h3` while preserving visual class | Patched |
| Claude + Hermes Skills | Agent runtime and skill governance | Valuable but buried after all cards | Users may miss it | Consider moving before cards or packs | Needs user decision |
| Ready-to-Paste Packs | Paste-ready behavior packs | Adjacent `Copy all` and `Copy visible` appeared identical | Confusing bulk-copy choice | Rename visible to filtered and make copy source canonical | Patched |
| Sources | Evidence table with inert URLs | `Trust / DOI` column label overclaimed because most rows are trust/source notes, not DOI | Column semantics unclear | Rename to `Trust / source note` | Patched |
| Footer | Artifact closeout | No issue found | Low risk | Leave unchanged | No patch |
| Print behavior | Offline/PDF export | Closed prompt-pack details may not fully print in some browsers | Print may omit non-open pack variants | Consider print-specific expansion or guidance | Needs user decision |
| Mobile behavior | Same artifact on narrow screens | Existing stack/table responsive rules are good | Low risk | Browser-smoke mobile width | Checked in browser smoke |
| Compact mode | Dense scanning | Behavior is useful; hides closed pack details as expected | Low risk | Leave unchanged | No patch |

## Control Behavior Table

| Control | Current label | Actual behavior | Confusing? | Recommended behavior/label | Patch status |
|---|---|---|---|---|---|
| Global search | Search directives... | Filters cards, stacks, packs, sources | Yes | `Search directives, stacks, packs, sources...` | Patched |
| Category filter | All categories | Filters directive cards only | Slight | Keep label and aria as card category filter | No patch |
| Print/PDF | Print / PDF | Calls `window.print()` | No | Keep | No patch |
| Reset | Reset | Clears search, category, stack filter | Slight | `Reset filters` | Patched |
| Compact view | Compact view | Toggles compact mode | No | Keep | No patch |
| Result summary | Ready then counts | Counts visible stacks/cards/packs/sources | No | Keep | No patch |
| Quick rail copy | Copy | Copies that quick block | Aria was generic | Contextual aria per block | Patched |
| Stack workstream filter | Workstream | Filters stack rows | No | Keep | No patch |
| Sort risk | Sort by risk | Sorts high-first | Yes | `Sort by risk high-first` | Patched |
| Sort ID | Sort by ID | Sorts stacks by ID | No | Keep | No patch |
| Copy visible stacks | Copy visible stacks | Copies visible stack rows after search/filter | No | Keep | No patch |
| Stack Short | Short | Copies stack name and stack expression | Slight but acceptable in table context | Keep | No patch |
| Stack Full | Full | Copies full stack contract | No | Keep | No patch |
| Copy visible cards | Copy visible cards | Copies visible directive cards | No | Keep | No patch |
| Card Copy | Copy | Copies canonical full directive text | No | Keep | No patch |
| Card Terse | Terse | Copies terse directive from same record | Slight for non-expert users | Consider `Copy terse` later | Needs user decision |
| Expand card details | Expand card details | Opens visible card details | No | Keep | No patch |
| Collapse card details | Collapse card details | Closes card details | No | Keep | No patch |
| Copy all packs | Copy all packs | Copies all packs regardless of search | Previously ambiguous next to visible | Keep and clarify aria | Patched |
| Copy visible packs | Copy visible packs | Copies visible packs after search | Yes | `Copy filtered packs` | Patched |
| Individual pack copy | Copy pack | Copies canonical pack text | No | Keep | No patch |
| Collapse pack details | Collapse pack details | Closes pack details | No | Keep | No patch |
| Copy visible source URLs | Copy visible source URLs | Copies visible source URLs | No | Keep | No patch |
| Copy source keys | Copy source keys | Copies visible source keys only | Yes | `Copy visible source keys` | Patched |
| Source Copy URL | Copy URL | Copies inert URL text | No | Keep inert | No patch |

## Card Quality Table

| Card ID | Classification | Issue | Action | Patch status |
|---|---|---|---|---|
| All 152 directive cards | MISSING_SOURCE | Every directive has `source_refs: []` despite matching sources for many records | Populate refs in a dedicated source-mapping pass and render directive source refs | Needs user decision |
| All 152 directive cards | TOO_VAGUE | Negative examples are mostly generic migration text | Replace by category in small batches | Needs user decision |
| 123 cards | WEAK_RELATED | Related links are mostly repeated category triads rather than semantic links | Refine related links by cluster | Needs user decision |
| CORE-DRY | FIELD_SHIFT_RISK | Directive describes the generated sheet workflow more than the general DRY principle | Decide whether ADHLBS-specific framing is intended | Needs user decision |
| CORE-KISS | FIELD_SHIFT_RISK | Similar product-specific framing risk | Review wording in taxonomy pass | Needs user decision |
| CORE-SSOT | FIELD_SHIFT_RISK | Similar product-specific framing risk | Review wording in taxonomy pass | Needs user decision |
| ARCH-GRASP | FIELD_SHIFT_RISK | General principle contains migration/page wording risk | Review wording in taxonomy pass | Needs user decision |
| STATE-ACID | FIELD_SHIFT_RISK | General principle contains generator-write framing risk | Review wording in taxonomy pass | Needs user decision |
| LEAN-GENCHI-GENBUTSU | FIELD_SHIFT_RISK | General principle contains repo-audit framing risk | Review wording in taxonomy pass | Needs user decision |
| ARCH-SOLID | TOO_VERBOSE | Directive is 294 chars; terse copy is not really terse | Add explicit terse override support or shorten directive | Needs user decision |
| DESIGN-CUPID | BAD_CATEGORY | Singleton category `Design Patterns & Tradeoffs` has only CUPID | Move CUPID to Architecture or populate category | Needs user decision |
| CORE-YAGNI | GOOD | Compact and aligned | Leave | No patch |
| STATE-IDEMPOTENCE | GOOD | Compact and aligned | Leave | No patch |
| COMP-SCHEMA-GATE | GOOD | Compact and aligned | Leave | No patch |
| WEB-HTML-FIRST | GOOD | Compact and aligned | Leave | No patch |
| TEST-SMOKE-TEST | GOOD | Compact and aligned | Leave | No patch |
| AGENT-RTFM | GOOD | Compact and aligned | Leave | No patch |
| SEC-TRUST-BOUNDARY | GOOD | Compact and aligned | Leave | No patch |
| REL-BACKPRESSURE | GOOD | Compact and aligned | Leave | No patch |

## Prompt Pack Table

| Pack ID | Classification | Issue | Action | Patch status |
|---|---|---|---|---|
| All 20 packs | VARIANTS_NOT_DISTINCT | Normal was separate, but Strict and Exploratory were merged into one `Strict / Exploratory variants` detail | Split into three canonical variants | Patched |
| All 20 packs | COPY_BEHAVIOR | Bulk pack copy reconstructed from DOM while individual copy used canonical `data-copy` | Make bulk copy use canonical pack copy | Patched |
| PACK-RESEARCH | TOO_GENERIC | Source basis and use case are broad | Review and sharpen in a pack-quality pass | Needs user decision |
| PACK-LEGACY and PACK-LEGACY-V2 | DUPLICATE_PACK | Strong overlap between legacy refactor packs | Merge or clearly separate use cases | Needs user decision |
| PACK-REPO-STRICT | GOOD | Distinct Normal, Strict, Exploratory after patch | Leave | Patched |
| PACK-SEC-HIGH | GOOD | High-risk safety role clear | Leave | Patched |
| PACK-CI | GOOD | Generator workflow role clear | Leave | Patched |
| PACK-A11Y | GOOD | Accessibility role clear | Leave | Patched |
| PACK-SUPPLY | GOOD | Supply-chain role clear | Leave | Patched |

## Added/Missing Card Backlog

| Candidate | Category | Why | Overlap | Source needed | Recommendation |
|---|---|---|---|---|---|
| RFC 2119 / MUST SHOULD MAY | Spec/API | Requirement language is high leverage | PACK-SPEC and interface contract | Existing RFC sources | Merge with existing |
| ADR | Architecture | Decision traceability | ARCH-ADR-RFC exists | Existing or add ADR source | Merge with existing |
| C4 model | Architecture | Architecture communication | Partial architecture overlap | Add source | Add after source |
| OODA loop | Agent/Lean | Fast decision loop | Lean/PDCA overlap | Add source | Add after source |
| Wardley Mapping | Strategy | Situational awareness | No direct card | Add source | Add after source |
| INVEST | Product | Story quality | No direct card | Add source | Add after source |
| MoSCoW | Product | Prioritization | No direct card | Add source | Add after source |
| SMART | Product/Planning | Goal clarity | Hoshin/PDCA overlap | Add source | Add after source |
| SLO / SLI / SLA | Reliability | Service target clarity | Reliability category | SRE source exists | Merge with existing |
| Error budget | Reliability | Release/risk governor | SRE source exists | SRE source exists | Merge with existing |
| Runbook | Reliability | Operational recovery | Ops cards overlap | Add or existing SRE | Merge with existing |
| Postmortem | Reliability/Lean | Learning after incident | Hansei/5 Whys overlap | Existing lean/SRE likely | Merge with existing |
| RACI / DACI | Governance | Ownership clarity | OWNER FIRST overlap | Add source | Add after source |
| SBOM | Security | Supply-chain inventory | PACK-SUPPLY and NIST | Existing NIST/OWASP | Needs user decision |
| SLSA | Security | Build provenance | Supply-chain overlap | Add source | Add after source |
| OWASP ASVS | Security | Verification standard | Source exists | Existing source | Needs user decision |
| Threat Modeling as Code | Security | Automatable threat models | STRIDE/DREAD overlap | Add source | Add after source |
| Context Window Budget | Agent Control | Prevent context sprawl | Agent budget cards overlap | Existing agent sources | Merge with existing |
| Prompt Injection Boundary | Security/Agent | Core LLM boundary | Existing security cards | OWASP/NCSC exist | Merge with existing |
| Eval-Driven Development | Agent/Test | Measurement loop | Eval pack and test cards | Existing eval source | Merge with existing |
| Golden Test Set | Test/Agent | Stable eval suite | Existing testing/eval cards | Existing sources | Needs user decision |
| Canary Release | Reliability | Safer rollout | Release stack overlap | Add source | Add after source |
| Feature Flag | Reliability/Product | Controlled rollout | Release stack overlap | Add source | Add after source |
| Backwards Compatibility | Architecture/API | API stability | Existing API/contract cards | Existing or add source | Merge with existing |
| Migration Plan | State/Data | Safer change rollout | Data/migration stack | Existing sources | Needs user decision |
| Deprecation Policy | API/Product | Controlled removal | Compatibility overlap | Add source | Needs user decision |
| Observability | Reliability | Understand runtime behavior | Reliability stack overlap | Existing SRE source | Merge with existing |
| Structured Logs | Reliability | Debuggable traces | Observability overlap | Existing SRE source | Needs user decision |
| Trace IDs | Reliability | Cross-service tracing | Observability overlap | Existing SRE source | Needs user decision |
| Idempotency Key | State/API | Safe retries | Idempotence card overlap | Existing state/API basis | Needs user decision |
| Rate Limit / Backpressure | Reliability | Protect capacity | REL-BACKPRESSURE exists | Existing Azure/SRE | Merge with existing |
| Queue / Retry / DLQ | Reliability | Async recovery | Reliability overlap | Existing Azure/SRE | Merge with existing |
| Human Escalation Threshold | Agent Safety | Clear HITL boundary | HITL/approval overlap | Existing security/agent | Merge with existing |

## Source/Evidence Table

| Source/Card | Issue | Risk | Action | Patch status |
|---|---|---|---|---|
| All directive cards | `source_refs` are empty | Source table is not traceably connected to cards | Populate in a dedicated pass; then render refs in cards | Needs user decision |
| OWASP-AGENCY | Title/URL mismatch: title says Excessive Agency, URL path points to sensitive information disclosure | Possible overclaim | Verify correct OWASP page and update source | Needs user decision |
| HERMES-README | Weak source class for research-backed claim | Evidence may overstate source | Consider stronger/pinned source | Needs user decision |
| GRASP-LARMAN | Secondary URL while title implies Larman/book provenance | Source confidence risk | Rename title or add primary source | Needs user decision |
| AGENT-HARNESS | Awesome-list/project source used as agent harness basis | Source overclaim risk | Rename as candidate/community source or add stronger paper | Needs user decision |
| CANDIDATE-CUPID | Candidate and unused by directive refs | Loose source | Keep if CUPID stays, otherwise review | Needs user decision |
| ATLASSIAN-SSOT | Unused by directive refs | Traceability gap | Link to SSOT card if accepted | Needs user decision |
| MS-SOLID | Unused by directive refs | Traceability gap | Link to SOLID card if accepted | Needs user decision |
| Source URL rendering | Inert code text with copy button | Good offline posture | Keep inert and no active external links | No patch |
| Remote link checking | Not run | Dead links may remain | Report `REMOTE_LINK_CHECK_NOT_RUN` | No patch |

## Generator/Checker Table

| File/checker | Protects | Gap | Risk | Action |
|---|---|---|---|---|
| `tools/build_docs_index.py` | Rich generated UI shell | Some labels were honest-but-unclear | Product quality drag | Patched labels and headings |
| `tools/build_docs_index.py` | Directive cards | Directive `source_refs` are not rendered | Refs remain invisible after future mapping | Recommend rendering source refs in card details |
| `tools/check_adhlbs_atomics.py` | Required fields, duplicate IDs, refs, counts | Prompt pack variant shape was not strict | Combined variants could drift back | Patched exact Normal/Strict/Exploratory check |
| `tools/check_docs_index_freshness.py` | Generated output freshness | Good | Stale output blocked by check | No patch |
| `tools/check_docs_index_offline.py` | Offline safety | Good for active loads and forbidden APIs | No remote link liveness check by design | No patch |
| `atomics/adhlbs.schema.json` | Descriptive schema | Python validator is actual gate | Schema may lag checker | Keep checker as deterministic gate |
| `.github/workflows/verify.yml` | CI parity | Mirrors required Python checks | Good | No patch |
| Proposed redundant-control check | Control clarity | Could be brittle without browser state | False positives likely | Do not add yet |

## Accessibility/Mobile/Print Table

| Surface | Issue | Impact | Action | Patch status |
|---|---|---|---|---|
| Quick rail copy buttons | Generic aria labels | Screen reader users cannot tell which copy button is focused | Add contextual aria labels | Patched |
| Category group names | Styled spans instead of headings | Heading navigation weaker | Render as `h3.group-name` | Patched |
| Reset button | Generic label | Slight ambiguity | Rename `Reset filters` | Patched |
| Source keys copy | Label omitted visibility condition | Slight ambiguity under search | Rename `Copy visible source keys` | Patched |
| Keyboard focus | Existing focus-visible rule is strong | Good | Keep | No patch |
| Skip link | Present | Good | Keep | No patch |
| Reduced motion | Present | Good | Keep | No patch |
| Mobile stack table | Existing responsive card layout | Good | Smoke through mobile viewport | Browser smoke |
| Prompt packs mobile | Grid collapses to one column | Good | Smoke through mobile viewport | Browser smoke |
| Print | Closed prompt-pack details may stay collapsed | Possible PDF omission of Strict/Exploratory bodies | Consider print expansion strategy later | Needs user decision |
| Contrast | Existing dark/light surfaces appear readable | Low risk | Browser smoke only | No patch |

## Patches Made

| Surface | Change |
|---|---|
| Prompt packs | Split combined `Strict / Exploratory variants` into separate `Strict` and `Exploratory` records for all 20 packs |
| Prompt packs | Renamed `Copy visible packs` to `Copy filtered packs` |
| Prompt packs | Clarified `Copy all packs` aria behavior and made bulk copy derive from canonical pack copy |
| Validator | Added exact prompt-pack variant guard: `Normal`, `Strict`, `Exploratory` |
| Defense section | Normalized defense control `name` and `posture` fields |
| Defense section | Changed details summary to `Breaks if absent / control` |
| Toolbar | Changed search placeholder and reset label |
| Stacks | Changed risk sort label to `Sort by risk high-first` |
| Cards | Rendered category names as `h3.group-name` |
| Sources | Changed key copy label and `Trust / source note` column label |
| AGENTS.md | Updated prompt-pack operating guidance for distinct variants |

## Items Needing User Decision

| Item | Decision needed |
|---|---|
| Directive source refs | Whether to map all 152 directive cards to source refs now and render them visibly |
| Negative examples | Whether to replace generic negative examples category-by-category |
| Related links | Whether to refine repeated related-card triads into semantic links |
| Section order | Whether to move Skills and Prompt Packs before the large Directive Cards section |
| DESIGN-CUPID | Move into Architecture or populate the singleton category |
| Legacy packs | Merge `PACK-LEGACY` and `PACK-LEGACY-V2`, or sharpen their separate roles |
| Print behavior | Whether print should force all prompt-pack variant bodies visible |
| Card additions | Whether to add backlog candidates such as SBOM, OWASP ASVS, Golden Test Set, Migration Plan, Deprecation Policy, Structured Logs, Trace IDs, or Idempotency Key |

## Verification Results

Full local checks after patching:

| Command | Result |
|---|---|
| `python tools/check_adhlbs_atomics.py` | `ATOMICS_OK directives=152 stacks=25 prompt_packs=20 sources=48` |
| `python tools/build_docs_index.py` | `BUILD_OK directives=152 stacks=25 prompt_packs=20 sources=48 output=docs/index.html` |
| `python tools/check_docs_index_freshness.py` | `FRESHNESS_OK docs/index.html matches atomics build` |
| `python tools/check_docs_index_offline.py` | `OFFLINE_CHECK_OK docs/index.html` |
| `Get-ChildItem tools -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }` | Passed with no output |
| `git diff --check` | Passed; only autocrlf warnings were printed |

Browser smoke through `http://127.0.0.1:8765/`:

| Check | Result |
|---|---|
| Initial counts | 25 stacks, 152 cards, 20 packs, 48 sources |
| Search `RAG` | 2 stacks, 25 cards, 3 packs, 1 source |
| Reset filters | Restored 25 stacks, 152 cards, 20 packs, 48 sources |
| Category filter `Security` | 18 cards |
| Stack filter `security` | 3 stacks |
| Risk sort | High-first ordering verified |
| ID sort | Ascending stack ID ordering verified |
| Compact mode | Toggled on and back off |
| Card expand/collapse | Expanded 304 card details, then collapsed to 0 |
| Pack collapse | Collapsed pack details to 0 open details |
| Directive copy and terse buttons | Click handlers showed copy toast |
| Pack copy controls | `Copy filtered packs` saw 3 visible pack payloads after search; `Copy all packs` retained 20 payloads |
| Source URLs/offline assets | Active external load selectors: 0 |
| Offline CSP | `connect-src 'none'` present |
| Mobile-responsive rules | Viewport meta present and 5 max-width media rules detected |

Browser limitation: the in-app browser virtual clipboard was unavailable, so clipboard payloads were verified through canonical `data-copy` attributes plus click/toast behavior, not by reading the native clipboard.

## Unverified

| Item | Status |
|---|---|
| Remote link liveness | `REMOTE_LINK_CHECK_NOT_RUN` |
| Native clipboard payload read | Browser virtual clipboard unavailable; click/toast and canonical `data-copy` payloads verified |
| True mobile viewport resize | In-app browser API did not expose viewport resizing; responsive viewport meta and max-width CSS rules were inspected |
| Full semantic source mapping | Not attempted in this pass |
| All negative example rewrites | Not attempted in this pass |
| Section reorder | Not attempted pending user decision |

## Commit Readiness Note

No commit, push, tag, deploy, GitHub Pages setting change, or release mutation was performed as part of this audit.
