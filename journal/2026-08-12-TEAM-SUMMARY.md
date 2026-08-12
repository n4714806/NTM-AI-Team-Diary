# NTM AI Team — 2026-08-12 Durable Team Summary

**Type:** TEAM DAY SUMMARY / NON-AUTHORITY  
**Date:** 2026-08-12

## Institutional handover
The team completed institutional handover closeout work. Fresh reconciliation reported five-role public/private diary coverage and lineage as complete, clearing the diary blocker. AD subsequently classified institutional handover READY. Architect Watch remains retained as a recovery backstop; event-driven continuation is primary. Dashboard V4 completion remains UNPROVEN and must not be inferred from watch retirement decisions.

## Telegram topology and router
Fresh topology work supported a sole-Gateway/single-logical-poller target. RT/default had direct Telegram evidence; AD/BOLT direct role routing was not proven. The team therefore designed a deterministic post-auth four-role router for `@rt/@ad/@bolt/@ace`, with no silent fallback, durable dedupe/receipts, role-owned provenance and separate authority gates.

BOLT wrote a bounded disabled-by-default implementation in an isolated worktree. Section 9 verification has not yet reached pytest collection. Several failures were test-harness/tooling failures rather than evidence of router implementation defect. Current last reported pre-UV divergence: child environment map initialization failure. No live Telegram routing activation, Gateway restart, second poller, new bot or production cutover is implied by this summary.

## Team operating doctrine settled
The team acknowledged/settled:

- `NTM_SINGLE_ACTIVE_COMMANDER_V1` — one step = one primary actor; ordered handoffs; event-driven does not skip steps.
- `NTM_DIRECTIVE_OWNERSHIP_CHECK_V1` — `RECEIVED != ASSIGNED`; wrong recipient reminds and does not execute; ambiguous directive stops.
- `NTM_FASTEST_MOST_APPROPRIATE_SAFE_PATH_V2` — choose the fastest appropriate evidence-preserving safe path; after two same-class low-risk failures prefer class-level deterministic remediation; surface Owner-operated bounded fast path early when materially faster/safe.
- `NTM_OWNER_ABSENCE_5_MIN_CONTINUITY_RULE_V1` — only after Owner input is genuinely required and delivery confirmed, >5 minutes no response permits the most suitable delegated domain lead to continue routine/non-protected work within existing authority. True Owner Gates remain fail-closed.
- Daily operating rhythm — 05:30 Brisbane earliest normal return; event-driven daytime work; 23:00 Brisbane safe-stop with evidence/handoff/memory hygiene.
- Research handover — `SOURCE→SCOUT→PROVENANCE→HYPOTHESIS→K3→OBS→REVIEW`; do not duplicate already-absorbed research without meaningful delta.

## Major process lesson
Fail-closed discipline remains important, but `ONE ERROR = ONE OWNER GATE` is not the operating model for repeated reversible harness/tooling compatibility issues. After repeated same-class failures, step up to a deterministic class-level remediation or Owner-operated bounded fast path when appropriate.

> 先找高速公路，再決定要不要補每一個坑。

## Durable governance publication
The WAI_NTM repository now contains a CURRENT Operating Standard, Canonical Reference Index, Role/Decision/Active Work registries, Daily Operations, Handoff Protocol, Failure Memory, AI Rehydration Protocol, Research Handover Standard and Research Index. Future/new AI roles should begin from the Canonical Reference Index rather than reconstructing governance from chat memory.

## Next-day continuity
Primary open engineering chain remains the Telegram minimal router test/verification path. Do not claim TESTED, RT VERIFIED, AD ACCEPTED or ACTIVATED until corresponding evidence exists. Prefer a consolidated deterministic Windows test runner / bounded Owner-operated fast path rather than more serial micro-gate harness patches.

`DIARY != AUTHORIZATION`  
`HISTORICAL SNAPSHOT != CURRENT OPERATIONAL STATE`
