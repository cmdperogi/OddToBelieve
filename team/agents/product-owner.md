# Product Owner — Status

**Last updated:** 2026-06-13

---

## Last Refinement

**Date:** 2026-06-13 (Monday, Sprint 1 pre-kick-off)  
**Sprint start:** 2026-06-16  
**Sprint end:** 2026-06-27

---

## Backlog Changes (this session)

### Stories Added

| Story | Priority | Rationale |
|-------|----------|-----------|
| STORY-13: Scaffold FastAPI backend | Sprint-Ready (P2) | Repo contains only `team/` — no backend/ code exists. Hard prerequisite for STORY-2, 3, 4, 5. Added to Sprint 1. |
| STORY-14: Scaffold React/Vite frontend | Backlog (P3) | No frontend/ directory exists. Prerequisite for STORY-6, 8, 9. Targeting Sprint 2. |

### Stories Updated

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

### Split Decisions

- **STORY-12** kept as one M-estimate story for now. Flag for potential split at Sprint 2 planning if cross-source event matching (name + time fuzzy match) proves complex. Candidates: STORY-12a (backend matching) / STORY-12b (frontend display + highlight).

---

## Decisions Made

### 2026-06-13

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
| Credential safety | Betfair username/password/session token must never appear in logs, API responses, or test output |
| Poll interval | Do not change `ODDS_POLL_INTERVAL_MINUTES` without checking rate limit headroom |
