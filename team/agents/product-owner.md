# Product Owner — Status

**Last updated:** 2026-06-16

---

## Last Refinement

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
