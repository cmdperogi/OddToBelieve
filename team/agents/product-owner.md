# Product Owner — Status

**Last updated:** 2026-07-13

---

## Backlog Refinement — 2026-07-13 (Monday, Sprint 3 Day 1)

**Sprint 3 start:** 2026-07-13  
**Sprint 3 end:** 2026-07-24

---

### Sprint 2 Final Outcome (closed 2026-07-10)

**Done (merged to main):**
- STORY-3 (PR #28): Merged 2026-07-03T20:51:59Z ✅
- STORY-4 (PR #31): Merged 2026-07-03T20:52:07Z ✅
- STORY-10 (PR #47): Merged 2026-07-08T09:07Z ✅
- STORY-11 (PR #48): Merged 2026-07-08T09:09Z ✅

**Carry-overs (all gates clear, DevOps missed Sprint 2 merge deadline):**
- STORY-7 (PR #52): QA LGTM ✅, AppSec CLEAR ✅ (2026-07-09), CI GREEN ✅. DevOps did not merge on 2026-07-10. Now a Sprint 3 P1 carry-over.
- STORY-14 (PR #53): Same status as STORY-7. Now a Sprint 3 P1 carry-over.

**Deferred to Sprint 3 (planned from 2026-07-08):**
- STORY-21a: No Engineer PR opened in Sprint 2. Deferred.
- STORY-21b: PO D25 confirmed — STORY-21a prerequisite not completed, STORY-21b moves to Sprint 3.

Sprint 2 final velocity: **4/6 stories Done** (STORY-7 and STORY-14 not merged by DevOps). Sprint goal partially met: health/logging complete; rate guard and frontend scaffold carry over.

**Known code issue identified during Sprint 3 refinement (2026-07-13):**  
PR #31 (STORY-4) was branched from a pre-STORY-3 version of main. Its merge resolved in favour of the STORY-4 branch tree, dropping from main: (1) `_persist()` method from `OddsApiService`, (2) `db: Session | None = None` parameter in `fetch()`, and (3) `test_odds_api_service.py` (546 lines). Confirmed via `git diff c5fa096..de55f02`. Reference implementation at commit `2ed2ce2`. Addressed by new STORY-25.

---

### Sprint 3 Planning Decisions (2026-07-13)

**D30: STORY-6 descoped — Vitest setup and component tests now covered by STORY-23a.**

STORY-23a (OddsTable component) explicitly includes Vitest installation and component tests (4 test scenarios: happy-path, empty-state, loading, error). STORY-6's first three ACs are fully subsumed by STORY-23a. STORY-6's unique remaining value is the CI gate: ensuring `npm test` runs in the GitHub Actions workflow and blocks PR merge on test failure. STORY-6 is renamed to "Wire frontend Vitest tests to CI pipeline (merge gate)", scoped down to XS estimate, and now depends on STORY-14 + STORY-23a.

**D31: STORY-25 added — Restore OddsApiService DB persistence layer.**

`OddsApiService._persist()` and the `db: Session | None = None` parameter in `fetch()` were lost from main when PR #31 (STORY-4) merged on 2026-07-03. This was a silent regression — no test failure was raised because the unit tests for `_persist()` (`test_odds_api_service.py`) were also dropped in the same merge. The absence of `_persist()` directly blocks STORY-21b: the Odds API scheduler cannot write to the database without it. STORY-25 is classified P2 (Sprint 3 ready), S estimate. It must be completed after STORY-7 merges (so STORY-25 builds on the correct `odds_api.py` base including the rate guard singleton). GitHub issue to be created. Priority in Sprint 3: Day 2 (after STORY-7 merges and Engineer completes STORY-21a Day 1).

**D32: STORY-21b dependency updated — now depends on STORY-21a, STORY-7, AND STORY-25.**

Previously STORY-21b depended on STORY-21a and STORY-7. STORY-25 is now an explicit prerequisite: the Odds API scheduler calls `OddsApiService.fetch(db=session)` which requires the `db` parameter to exist. Added to backlog and GitHub issue #42 comment to be updated.

**D33: Sprint 3 scope — top 7 stories confirmed.**

| Priority | Story | Estimate | Status | Day |
|----------|-------|----------|--------|-----|
| P1 | STORY-7 (carry-over, PR #52) | S | DevOps merge today | Day 1 |
| P1 | STORY-14 (carry-over, PR #53) | S | DevOps merge today | Day 1 |
| P2 | STORY-21a (Betfair scheduler) | S | Engineer start Day 1 | Day 1–2 |
| P2 | STORY-24 (datetime.utcnow fix) | XS | Engineer Day 1 bundle | Day 1 |
| P2 | STORY-25 (Restore _persist()) | S | Engineer after STORY-7 merges | Day 2 |
| P2 | STORY-21b (Odds API scheduler) | S | After 21a + 7 + 25 | Day 3–4 |
| P3 | STORY-22 (Frontend login) | S | After STORY-14 merges | Day 2+ |

Sprint 3 capacity: 7 stories (2 carry-over DevOps merges + 5 new). Achievable if DevOps acts on Day 1.

**D34: Issue #54 (ecdsa CVE) — confirmed not a Sprint 3 blocker.**

ecdsa 0.19.2 PYSEC-2026-1325 (Minerva timing-attack, LOW severity) has no upstream fix available. Accepted risk per AppSec (2026-07-09). AppSec to monitor for upstream patch in Sprint 3 scans. No story required. No impact on Sprint 3 scope.

**D35: ACs improved for top 5 unstarted Sprint 3 stories.**

Stories refined today with additional acceptance criteria:
- **STORY-21a:** Added `(source_id, source)` upsert key AC (clarifies Betfair event ID mapping) and `Market`/`Odds` refresh pattern AC (existing Odds rows deleted before new ones inserted — prevents price accumulation).
- **STORY-24:** Added lambda-form AC for `default=` callable — `lambda: datetime.now(timezone.utc)` is preferred over a bare function reference to ensure a fresh datetime per row rather than capturing at import time.
- **STORY-25:** New story, full ACs written from scratch covering the `db` parameter, persistence behaviour, backward compatibility, upsert idempotency, exception handling, and test requirements.
- **STORY-21b:** Added exception-handling AC — if `_persist()` raises a DB exception during the Odds API poll cycle, the scheduler logs ERROR (no credentials) and continues without crashing.
- **STORY-22:** ACs already comprehensive (8 ACs including tab-close persistence). No changes needed.

---

## Backlog Refinement — 2026-07-06 (Monday, Sprint 2 Day 6 of 10)

**Sprint 2 status:** 4 days remaining (ends 2026-07-10). Sprint risk: HIGH.

**Sprint 2 status:** 4 days remaining (ends 2026-07-10). Sprint risk: HIGH.

---

### Sprint 2 Progress Assessment (2026-07-06)

**Carry-overs (Sprint 1) — CONFIRMED DONE:**
- STORY-3 (PR #28): Merged 2026-07-03T20:51:59Z ✅ — DevOps finally acted after 11-day stall. Issue #4 closed.
- STORY-4 (PR #31): Merged 2026-07-03T20:52:07Z ✅ — merged 8 seconds after PR #28 per merge convention. Issue #5 closed.
- Escalation issue #46: Confirmed closed (no longer in open issues list).

**Sprint 2 stories in review:**
- STORY-10 (PR #47): CI GREEN, awaiting QA LGTM + AppSec CLEAR.
- STORY-11 (PR #48): CI GREEN, awaiting QA LGTM + AppSec CLEAR.

**Sprint 2 stories unblocked but not started (CRITICAL):**
- STORY-7: Unblocked since STORY-3 merged 2026-07-03. 3 days without action.
- STORY-14: Never blocked. Sprint 2 Day 6 with no PR. Critically late.
- STORY-21a: Unblocked since STORY-3 merged 2026-07-03. 3 days without action.

**Sprint 2 sprint risk:** Zero Sprint 2 stories merged to main as of Day 6. With 4 days remaining, STORY-7, STORY-21a, and STORY-14 must start today to have any chance of completing Sprint 2's core goal. STORY-21b is at risk.

---

### Decisions Made — 2026-07-06

**D23: STORY-3 and STORY-4 confirmed Done.**

Both carry-over PRs merged 2026-07-03 by DevOps. PR #28 (STORY-3) at 20:51:59Z; PR #31 (STORY-4) at 20:52:07Z — 8 seconds apart, sequential merge per convention. P1 backlog section is now empty. Issues #4 and #5 closed today. Escalation #46 already closed. Superseded STORY-21 issue #33 closed (replaced by #41/#42).

**D24: STORY-7 and STORY-21a are now unblocked — Engineer must start today.**

Both were blocked on STORY-3 (PR #28), which merged 2026-07-03. Engineer has not started either story in the 3 days since unblocking (Day 3 to Day 6 gap). Sprint 2 ends Friday 2026-07-10. Engineer must open PRs for both stories by Wednesday 2026-07-08 to have any chance of full sprint completion.

**D25: STORY-21b remains in Sprint 2 scope but is AT RISK — reassessment Wednesday 2026-07-08.**

STORY-21b depends on both STORY-21a and STORY-7. With 4 days remaining and neither dependency started, the pipeline is extremely tight: STORY-7 PR → merge → STORY-21a PR → merge → STORY-21b PR → merge = 3 sequential PR cycles in 4 days. PO will reassess Wednesday 2026-07-08: if STORY-21a has no open PR by end of Wednesday, STORY-21b drops to Sprint 3. This is a firm date, not a soft deadline.

**D26: STORY-23 formally split into STORY-23a and STORY-23b.**

Original STORY-23 was M-estimate (too large for the 1-2 day target, per split policy). Split rationale:
- **STORY-23a** (S): OddsTable component — props-based render, loading/empty/error states, Vitest tests. No live API calls. Can be built and tested purely against mock data. Issue #49.
- **STORY-23b** (S): Live API wiring — GET /odds/events call, auth header, 401 redirect, error propagation. Depends on STORY-23a. Issue #50.

Original issue #35 closed. The split keeps each story independently deliverable and testable.

**D27: STORY-24 added — Fix datetime.utcnow() deprecated calls.**

Flagged in 4 consecutive prod-support audit runs (2026-06-30, 2026-07-01, 2026-07-02, 2026-07-03). Locations: `auth.py:21` (JWT expiry calc) and `db/models.py:47` (Column default). Non-breaking on Python 3.11 (current runtime), but `DeprecationWarning` noise and a future Python upgrade risk. XS estimate — two-file change. P3 cleanup. Issue #51 created. No AWS, no data-source, no rate-limit impact.

**D28: Improved ACs for 5 Sprint 2 unstarted stories.**

Stories refined today with additional acceptance criteria:
- **STORY-7:** Added startup-state AC — when no Odds API response has been received yet (app just started), `GET /odds/api-status` must return `{"requests_remaining": null, "guard_active": false}`. Prior ACs only covered guard-fire and guard-recovery states; the initial null state was unspecified.
- **STORY-21a:** Added empty-event-list AC — when `BetfairClient.list_events()` returns an empty list, the scheduler must emit an INFO log with event count 0 and not crash. Prior ACs only covered non-empty results and auth failure.
- **STORY-14:** Added HTML title tag AC — `<title>` must read "OddToBelieve", not "Vite + React" or any Vite default. Catches a common scaffold shortcut that leaves the default title in place.
- **STORY-21b:** Added startup guard state AC — on first poll cycle before any API response header has been received, guard must be inactive and the HTTP request must proceed. Mirrors the startup-state AC added to STORY-7.
- **STORY-22:** Added tab-close persistence AC — closing the browser tab must NOT persist the JWT; on reopen the user is sent to `/login`. Reinforces the in-memory-only constraint against an accidental `sessionStorage` fallback a developer might add "just in case".

**D29: Closed stale/superseded GitHub issues.**

- #4 (STORY-3): Closed — PR #28 merged.
- #5 (STORY-4): Closed — PR #31 merged.
- #33 (STORY-21 original): Closed — superseded by #41 (STORY-21a) and #42 (STORY-21b).
- #35 (STORY-23 original): Closed — replaced by #49 (STORY-23a) and #50 (STORY-23b).

---

## Backlog Refinement — 2026-06-29 (Monday, Sprint 2 Day 1)

**Sprint 1 end:** 2026-06-27  
**Sprint 2 start:** 2026-06-29

---

### Sprint 1 Outcome Assessment

Sprint 1 ended with two stories not merged:
- **STORY-3** (PR #28): Rebased 2026-06-25, 62/62 passing, AppSec CLEAR. QA did not re-verify final rebase HEAD before sprint end; DevOps did not merge.
- **STORY-4** (PR #31): All gates clear since 2026-06-23; blocked on #28.

Velocity: 11 of 13 stories Done (including all 6 security stories). Sprint goal (CI + test coverage + security baseline) is **partially met** — CI and security are in place; test coverage baseline is incomplete without STORY-3 and STORY-4.

---

### Sprint 2 Planning Decisions (2026-06-29)

**D15: STORY-3 and STORY-4 escalated to P1 carry-overs.**

Both PRs carry into Sprint 2 as the highest-priority items. No Sprint 2 feature work starts until both PRs land on main. QA re-verifies PR #28 today; DevOps merges PR #28 then PR #31 sequentially. This is the first action for Sprint 2.

**D16: Sprint 2 scope confirmed — 6 stories.**

| Story | Estimate | Parallel? | Blocked Until |
|-------|----------|-----------|---------------|
| STORY-10: /health endpoint | XS | No (start today) | — |
| STORY-11: Structured logging | S | Yes (parallel with STORY-10) | — |
| STORY-7: Rate limit guard | S | No | STORY-3 merges |
| STORY-21a: Betfair polling job | S | No | STORY-3 merges |
| STORY-21b: Odds API polling job | S | No | STORY-21a + STORY-7 |
| STORY-14: Frontend scaffold | S | Yes (parallel with backend stories) | — |

Estimated Sprint 2 capacity: 6 stories × avg 1.5 days = 9 dev-days. Feasible within 2-week sprint.

**D17: STORY-21 split into STORY-21a (Betfair poll) and STORY-21b (Odds API poll).**

STORY-21 was M-estimate. The 1-2 day target requires splitting all M+ stories. Split rationale:
- STORY-21a focuses solely on the Betfair APScheduler job, upsert logic, and error resilience. Self-contained; deliverable in 1 day.
- STORY-21b adds the Odds API poll job with rate guard integration. Depends on STORY-21a and STORY-7. Deliverable in 1 day once those land.

Original GitHub issue #33 remains open as reference; new issues #41 (21a) and #42 (21b) created today.

**D18: GitHub issues created for Sprint 2 stories and remaining P3 stories.**

New issues created today:
- #38: STORY-10 /health endpoint
- #39: STORY-11 Structured logging
- #40: STORY-7 Rate limit guard
- #41: STORY-21a Betfair polling job
- #42: STORY-21b Odds API polling job
- #43: STORY-6 Vitest frontend tests
- #44: STORY-8 Sport filter UI
- #45: STORY-9 Loading states and error handling

**D19: Issue #3 (STORY-2) close is overdue.**

STORY-2 (BetfairClient) merged via PR #26 on 2026-06-23. Issue #3 was not closed then. Prod Support must close it today.

**D20: Accept STORY-23 at M estimate — no split yet.**

STORY-23 (frontend dashboard) is M-estimate but depends on STORY-14 + STORY-22 which are not started. It is Sprint 2+ scope. Split deferred until closer to sprint pick-up; revisit at Sprint 3 planning if STORY-23 is pulled in.

**D21: STORY-10 and STORY-11 are safe to start immediately on Sprint 2 Day 1.**

Both depend only on STORY-13 (already merged). Engineer should pick up STORY-10 (/health endpoint) and STORY-11 (structured logging) today while waiting for carry-over PRs to clear. STORY-14 (frontend scaffold) can also start in parallel.

**D22: Improved ACs written for top 5 unstarted Sprint 2 stories.**

Stories refined today with additional/improved acceptance criteria:
- **STORY-10:** Added `Content-Type: application/json` response header AC.
- **STORY-11:** Added module-name-in-log AC for debuggability. Credential-exposure constraint made explicit.
- **STORY-7:** Added guard deactivation AC — when `x-requests-remaining` recovers to ≥ 50, `guard_active` must return false. Prior ACs only described one-way (fire) behaviour.
- **STORY-21a:** Added idempotent upsert AC (updates on `source_id`, no duplicate rows) and BetfairClient mock requirement.
- **STORY-14:** Added TypeScript (`tsconfig.json`) requirement (`.tsx` not `.jsx`) and placeholder home-page AC (not a generic Vite starter page).

---

## Last Refinement

**Date:** 2026-06-22 (Monday, Sprint 1 Day 7 of 10)  
**Sprint start:** 2026-06-16  
**Sprint end:** 2026-06-27

---

## Backlog Changes (2026-06-22)

### Stories Added

| Story | Priority | Rationale |
|-------|----------|-----------|
| STORY-21: Add APScheduler background polling job | P2 (Sprint-Ready) | Core functionality gap: `scheduler.py` is specified in CLAUDE.md but no story existed. Depends on STORY-2 + STORY-3. ⚠️ Introduces `ODDS_API_POLL_INTERVAL_MINUTES` (default: 360 min) — separate from `BETFAIR_POLL_INTERVAL_MINUTES` (60 min) to stay within 500 req/month Odds API cap. |
| STORY-22: Frontend login page + JWT token management | P3 | Frontend auth flow is a prerequisite for any usable dashboard. Depends on STORY-14. JWT stored in React context (in-memory only — not localStorage, XSS risk). |
| STORY-23: Frontend main dashboard — events and odds table | P3 | Core user-facing view. No story existed for the OddsTable component or the `GET /odds/events` display. Depends on STORY-14 + STORY-22. |

### Stories Restructured

| Story | Change |
|-------|--------|
| STORY-12 | Formally split into STORY-12a (backend matching) and STORY-12b (frontend display). Original story removed. See decision D8. |
| STORY-10, STORY-11, STORY-7 | Promoted from P3 to P2 — these are sprint-ready once the current PR merge cascade completes. |
| STORY-15 through STORY-20 | Moved from P1 to Done — all six security stories are resolved and verified. P1 now has no active blockers. |
| STORY-14 | AC improved: added explicit `.env.local` / `VITE_API_BASE_URL` acceptance criterion (no hardcoded API URLs in source files). |

### Decisions Made (2026-06-22)

**D8: STORY-12 formally split into STORY-12a and STORY-12b.**

The PO flagged this split as pending at Sprint 2 planning (decision recorded 2026-06-13). We are now 5 days from Sprint 1 end — the right time to formalise. STORY-12a (backend cross-source matching, `GET /odds/comparison`) is S-estimate and is the dependency. STORY-12b (frontend comparison view) is also S-estimate and depends on STORY-12a and STORY-14. Both are P3 / Sprint 2+ scope. GitHub issues to be created.

**D9: STORY-21 added — APScheduler polling job. ⚠️ `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min (6h), not 60 min.**

The default `ODDS_POLL_INTERVAL_MINUTES=60` in CLAUDE.md is unsafe for The Odds API: 60 min × 24 h × 30 days = 720 requests/month against a 500 req/month hard cap. STORY-21 introduces a separate `ODDS_API_POLL_INTERVAL_MINUTES` environment variable (default: 360 min = 4 calls/day × 30 days = 120 req/month) independent from `BETFAIR_POLL_INTERVAL_MINUTES` (60 min, no cap). The existing rate guard (STORY-7) is the safety net but must not be the primary monthly budget control. CLAUDE.md should be updated when STORY-21 is implemented to document both variables.

**D10: STORY-22 (Frontend login) and STORY-23 (Frontend main dashboard) added.**

No stories existed for the core frontend user flow. STORY-22 specifies JWT stored in React context (in-memory), not `localStorage` or `sessionStorage`, to avoid XSS credential exposure. This is a non-negotiable security constraint. STORY-23 specifies the `OddsTable` component with loading, empty, and error states — intentional overlap with STORY-9 (loading/error) is resolved by making STORY-23 implement the states for the main table, and STORY-9 address the global error boundary.

**D11: Sprint 1 capacity assessment — RECOVERABLE.**

As of 2026-06-22 (Sprint 1 Day 7), all security stories are resolved. Four PRs are open in the merge cascade (#8, #9, #26, #28) plus one draft (#31). The sole gate is AppSec's formal approval comment on PR #8. With 4 working days remaining (through 2026-06-27), the sprint goal (CI + test coverage + security baseline) is achievable if the cascade starts by 2026-06-23. If AppSec comment is not posted by end of 2026-06-22 (today), Scrum Master should escalate immediately — each day of delay risks pushing STORY-4 and STORY-5 out of Sprint 1.

**D12: STORY-3 DB persistence is in scope for STORY-3 — no new story needed.**

The engineer noted DB persistence (`Event`/`Market`/`Odds` records) is in progress on the PR #28 branch. AC 3 of STORY-3 already covers this ("When odds are parsed, Then `Event`, `Market`, and `Odds` records are created with correct field values"). No story split required — this is implementation of an existing AC, not scope expansion.

**D13: STORY-10 (/health) and STORY-11 (logging) promoted to P2.**

Both depend only on STORY-13 (PR #8) which is about to merge. Both are XS/S estimate and are natural Sprint 2 first-day tasks for the engineer. Promoted from P3 to P2 to signal they are next in the backend queue.

**D14: STORY-7 (rate limit guard) promoted to P2.**

Depends on STORY-3, which is in PR. Rate guard is mandatory before STORY-21 (scheduler) can be considered complete. Moved to P2 to keep it visible as a Sprint 2 early pick-up.

---

## Previous Refinement

**Date:** 2026-06-16 (Monday, Sprint 1 kickoff day)  
**Sprint start:** 2026-06-16  
**Sprint end:** 2026-06-27

---

## Backlog Changes (this session)

### Stories Added

| Story | Priority | Rationale |
|-------|----------|-----------|
| STORY-15: Fix hardcoded credential defaults in config.py | P1 Blocker (CRITICAL) | AppSec issue #10: `SECRET_KEY`, `admin_username`, `admin_password` all have insecure Pydantic defaults. A missing `.env` file causes the app to start with forgeable JWTs and trivial admin credentials. Must be fixed before PR #8 merges. |
| STORY-16: Fix plain-text admin password comparison — use bcrypt | P1 Blocker (HIGH) | AppSec issue #13: `auth.py` imports `CryptContext` (bcrypt) but compares passwords with `==`. Contradicts CLAUDE.md design ("login password hashed at startup"). Timing attack risk. Must be fixed before PR #8 merges. |
| STORY-17: Upgrade python-jose to ≥3.4.0 or migrate to PyJWT | P1 Blocker (HIGH) | AppSec issue #11: `python-jose==3.3.0` has 3 CVEs (PYSEC-2024-232, PYSEC-2024-233, PYSEC-2025-185) enabling JWT algorithm confusion attacks. Must be fixed before PR #8 merges. |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | P1 Blocker (HIGH) | AppSec issue #12: `python-multipart==0.0.9` has 4 CVEs; `starlette==0.37.2` has 3 CVEs. Minimum safe: multipart 0.0.27, fastapi 0.115.0. Must be fixed before PR #8 merges. |
| STORY-19: Migrate CI credential-shaped env vars to GitHub Actions secrets pattern | P1 Blocker (LOW) | AppSec issue #16: CI YAML commits credential-shaped values (including Betfair-named vars) as plaintext. Values are test placeholders now, but the pattern is a credential-exposure risk. Must be fixed before PR #9 merges. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | P1 (LOW) | AppSec issue #15: `pytest==8.2.2` (CVE-2025-71176) and `black==24.4.2` (CVE-2026-32274). Dev deps, no production exposure. Bundle with PR #8 fixes since all touch `requirements.txt`. |

### Decisions Made

#### 2026-06-16 — Sprint 1 Kickoff Security Triage

**D1: Six new stories added to Priority 1 (STORY-15 through STORY-20).**

The AppSec agent reviewed PR #8 (STORY-13 backend scaffold) and PR #9 (STORY-1 CI) before sprint kickoff. Seven security issues were filed (#10–#16). Six require stories; one is a documented design exception (see D5).

STORY-15, 16, 17, 18 are hard blocks on PR #8 merging. STORY-19 blocks PR #9. STORY-20 is LOW severity (dev deps) and can be bundled.

**D2: PR #8 (STORY-13) cannot merge until STORY-15, 16, 17, 18 are resolved.**

The engineer must fix all four security issues on branch `agent/engineer/scaffold-fastapi` before the PR is approved. Since all four are XS-estimate code changes within files already in the PR, the preferred approach is to fix them in the same PR branch rather than open separate PRs.

**D3: PR #9 (STORY-1 CI) cannot merge until STORY-19 is resolved.**

DevOps must update the CI YAML to use `${{ secrets.VAR || 'fallback' }}` patterns for all credential-shaped environment variables before the CI PR is approved.

**D4: python-jose upgrade decision.**

Recommending `python-jose[cryptography]>=3.4.0` as the minimal-change path (same library, fixes all 3 CVEs). If the engineer finds the library API has breaking changes at 3.4.0, migrating to `PyJWT>=2.8.0` is the preferred alternative (more actively maintained). PO does not mandate which path — engineer decides during implementation.

**D5: /health endpoint remains public — design exception documented.**

AppSec issue #14 flags `/health` as missing `UserDep` (auth dependency). PO decision: **no story created, no fix required.** `/health` is intentionally unauthenticated per STORY-10 AC ("Given the backend is running, When GET /health is called with no auth token, Then HTTP 200 is returned"). This is standard liveness probe design (load balancers and monitoring tools cannot present JWTs). The exception must be documented in `CLAUDE.md` as a named auth exception alongside `POST /auth/token`. AppSec agent: record this as an accepted/documented exception in `team/agents/appsec.md` and close issue #14 with an explanation.

**D6: No split decisions this session.**

STORY-15–18 are all XS and fit within one engineer-day. STORY-12 (odds comparison) remains M — re-evaluate at Sprint 2 planning. No other stories are candidates for splitting.

**D7: Sprint 1 capacity concern — flagged to Scrum Master.**

Sprint 1 now carries 6 planned stories (STORY-13, 1, 2, 3, 4, 5) plus 6 security bugs (STORY-15–20). The four Critical/High security fixes (STORY-15–18) must be resolved before STORY-13 merges, which itself blocks STORY-2, 3, 4, 5. If the engineer cannot resolve the security fixes by Wednesday, STORY-2 and STORY-3 will be at risk for this sprint. Scrum Master should flag this on the sprint board.

---

## Previous Refinement

**Date:** 2026-06-13 (Monday, Sprint 1 pre-kick-off)

### Stories Added (2026-06-13)

| Story | Priority | Rationale |
|-------|----------|-----------|
| STORY-13: Scaffold FastAPI backend | Sprint-Ready (P2) | Repo contains only `team/` — no backend/ code exists. Hard prerequisite for STORY-2, 3, 4, 5. Added to Sprint 1. |
| STORY-14: Scaffold React/Vite frontend | Backlog (P3) | No frontend/ directory exists. Prerequisite for STORY-6, 8, 9. Targeting Sprint 2. |

### Stories Updated (2026-06-13)

| Story | Change |
|-------|--------|
| STORY-2 | Renamed to "Implement BetfairClient + unit tests (TDD)". Clarified that the service must be *implemented* (not just tested) — use TDD. Added AC: no real HTTP calls in tests; no credentials in output. |
| STORY-3 | Renamed to "Implement OddsApiService + unit tests (TDD)". Same rationale. Odds API rate limit warning added to story header. |
| STORY-4 | Added AC: services must be mocked in integration test suite — no real Betfair or Odds API calls. |
| STORY-5 | Added `Depends on: STORY-13` — Bandit needs `backend/app/` to scan; pip-audit needs `requirements.txt`. |
| STORY-6 | Rewrote AC to full G/W/T format. Added empty-state and CI-blocking criteria. |
| STORY-7 | Rewrote AC to full G/W/T format. Added `/odds/api-status` guard_active states for both fire and no-fire cases. |
| STORY-8 | Rewrote AC to full G/W/T format. Added "clear both filters" criterion. |
| STORY-9 | Rewrote AC to full G/W/T format. |
| STORY-10 | Rewrote AC to full G/W/T format. Specified 200 response even when db is unreachable (liveness semantics). |
| STORY-11 | Rewrote AC to full G/W/T format. Explicit no-credentials constraint for logs. |
| STORY-12 | Added single-source "N/A" criterion. Flagged potential split into backend (matching) + frontend (display). Odds API rate limit warning added. |

### Split Decisions (2026-06-13)

- **STORY-12** kept as one M-estimate story for now. Flag for potential split at Sprint 2 planning if cross-source event matching (name + time fuzzy match) proves complex. Candidates: STORY-12a (backend matching) / STORY-12b (frontend display + highlight).

### Decisions Made (2026-06-13)

1. **No code in repo.** Only `team/` exists. Added STORY-13 (backend scaffold) to Sprint 1 as the first story the engineer should pick up. Sprint 1 goal unchanged: CI, test coverage baseline, AppSec baseline.

2. **TDD approach for STORY-2 and STORY-3.** Stories renamed to make clear that the service *implementation* is in scope, not just the tests. Developer writes tests and code together. This avoids needing separate "Implement BetfairClient" and "test BetfairClient" stories.

3. **The Odds API rate limit (500 req/month) flagged on:** STORY-3, STORY-7, STORY-11, STORY-12. No new polling patterns to be introduced without PO sign-off. Any story that touches The Odds API must include the rate limit note.

4. **No AWS, no web scraping, no new data sources.** Constraints confirmed unchanged for Sprint 1 and the current backlog.

5. **Betfair credential safety.** Added explicit AC constraint to STORY-2 and STORY-11: credentials and session tokens must never appear in test output, log output, or fixtures.

6. **GitHub issues.** No issues existed before this session. Created issues for Sprint 1 scope: STORY-13, STORY-1, STORY-2, STORY-3, STORY-4, STORY-5, and STORY-14 (next-sprint scaffold).

---

## Constraints Reference (non-negotiable)

| Constraint | Detail |
|------------|--------|
| No AWS | Local only — SQLite, local uvicorn, local Vite |
| No web scraping | Only official APIs: Betfair Exchange API and The Odds API |
| The Odds API limit | 500 req/month hard cap — flag any story that touches it |
| No new data sources | Must get PO sign-off before adding any third data source |
| Credential safety | Betfair username/password/session token must never appear in logs, API responses, test output, or version-controlled files |
| Poll interval | Do not change `ODDS_POLL_INTERVAL_MINUTES` without checking rate limit headroom |
| /health exception | `GET /health` is intentionally unauthenticated — liveness probe. Named exception; not a bug. |
