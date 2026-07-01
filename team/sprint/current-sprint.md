# Sprint 2 — Reliability & Frontend Foundation

**Start:** 2026-06-29 (Monday)  
**End:** 2026-07-10 (Friday)  
**Goal:** Land Sprint 1 carry-overs, add health/logging/frontend scaffold, begin scheduler work.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | **ALL GATES CLEAR ✅ — AWAITING DEVOPS MERGE. DevOps BLOCKED (9 days inactive).** QA LGTM 2026-06-29 ✅ (62/62 passing, 91% coverage); AppSec CLEAR ✅; CI GREEN ✅. Escalation issue [#46](https://github.com/cmdperogi/OddToBelieve/issues/46) opened 2026-07-01. | Sprint 1 carry-over — rebase complete 2026-06-25 on `090413e` (commits `9641eb2`+`2ed2ce2`). |
| STORY-4: Integration tests /odds/* endpoints | QA | [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) | **ALL GATES CLEAR ✅ — awaiting PR #28 merge first, then DevOps merge.** QA LGTM 2026-06-23 ✅; AppSec CLEAR ✅; CI GREEN ✅. | Sprint 1 carry-over — merge immediately after PR #28. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-10: Add /health endpoint | Engineer | **NOT STARTED** — start today (2026-07-01) | Unblocked (depends only on STORY-13 ✅). XS estimate. Branch: `agent/engineer/health-endpoint`. |
| STORY-11: Add structured logging | Engineer | **NOT STARTED** — start today (2026-07-01) | Unblocked; safe to develop in parallel with STORY-10. S estimate. Branch: `agent/engineer/structured-logging`. |
| STORY-14: Scaffold React/Vite frontend | Engineer | **NOT STARTED** — start today (2026-07-01) | Unblocked; safe to develop in parallel with backend stories. S estimate. Branch: `agent/engineer/frontend-scaffold`. |
| STORY-7: Rate limit guard to OddsApiService | Engineer | BLOCKED on STORY-3 merge | Cannot start until PR #28 merges to main. |
| STORY-21a: APScheduler — Betfair background polling job | Engineer | BLOCKED on STORY-3 merge | Cannot start until PR #28 merges to main. |
| STORY-21b: APScheduler — Odds API background polling job | Engineer | BLOCKED on STORY-21a + STORY-7 | Depends on STORY-21a and STORY-7 completing. |

### Done (Sprint 2)

*(No new stories merged to main in Sprint 2 yet — Sprint 2 Day 3 of 10)*

---

### Done (Sprint 1 — carried forward for reference)

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | ✅ 2026-06-23 | 40/40 tests passing; `betfair.py` 100% coverage. Issue #3 closed. |
| STORY-13: Scaffold FastAPI backend | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | ✅ 2026-06-20 | All security findings resolved. AppSec CLEAR. QA LGTM 31/31. |
| STORY-1: GitHub Actions CI pipeline | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | ✅ 2026-06-20 | CI now active on main. |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | #9 (same branch) | ✅ 2026-06-20 | All 5 credential-shaped vars use `${{ secrets.VAR \|\| 'fallback' }}`. |
| STORY-5: AppSec baseline scan | — | ✅ 2026-06-20 | Bandit: B106 false positive only. pip-audit: 0 CVEs. |
| STORY-15: Fix hardcoded credential defaults in config.py | #8 | ✅ 2026-06-20 | No plaintext defaults remain; `ValueError` on startup if env vars unset. |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | #8 | ✅ 2026-06-20 | `_pwd_context.verify()` in place. |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | #8 | ✅ 2026-06-20 | `python-jose[cryptography]>=3.4.0`, 0 CVEs. |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | #8 | ✅ 2026-06-20 | `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | #8 | ✅ 2026-06-20 | `pytest==9.0.3`, `black==26.3.1`. |
| CI Fix: Align ADMIN_PASSWORD fallback with test fixtures | [#32](https://github.com/cmdperogi/OddToBelieve/pull/32) | ✅ 2026-06-22 | One-line fix; CI GREEN since run 27941596842. |

### Blocked

| Agent | Task | Days Since Last Action | Reason |
|-------|------|------------------------|--------|
| **DevOps** | **Merge PR #28 (STORY-3) → PR #31 (STORY-4)** | **9 days (last active 2026-06-23)** | All merge gates cleared since 2026-06-25. No merge action taken despite QA LGTM, AppSec CLEAR, and CI GREEN on both PRs. Sprint 1 goal missed as a result. Sprint 2 STORY-7, STORY-21a, STORY-21b all blocked downstream. Escalation issue [#46](https://github.com/cmdperogi/OddToBelieve/issues/46) opened by Prod Support 2026-07-01. **BLOCKED — must act today.** |

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-07-01 (Tuesday, Sprint 2 Day 3 of 10)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity; security stories added.
- ✅ 2026-06-16: Reconciled board against agent status files; sprint risk noted.
- ✅ 2026-06-17: Reviewed all agent/PR status. AppSec threshold noted.
- ✅ 2026-06-18: AppSec formally BLOCKED. Prod Support confirmed; issue #27 opened.
- ✅ 2026-06-19: AppSec BLOCKED lifted. Engineer opened PR #28. Sprint risk downgraded.
- ✅ 2026-06-22: PRs #8 and #9 merged. STORY-13, 1, 19, 5 moved to Done.
- ✅ 2026-06-23: PR #32 merged (CI GREEN). PR #26 merged (STORY-2 DONE).
- ✅ 2026-06-26: PR #28 rebase complete (2026-06-25). Sprint risk HIGH — sprint ends TOMORROW.
- ✅ 2026-07-01: Sprint 2 Day 3. Transitioned board to Sprint 2. DevOps BLOCKED (9 days inactive). Overdue Sprint 1 retrospective written. Daily assignments issued.
- **Next (Friday 2026-07-10): write Sprint 2 retrospective in `/repo/team/sprint/retrospective.md`.**

### Engineer
- **Today (2026-07-01) — START STORY-10 AND STORY-11. Sprint 2 Day 3; no new code has shipped this sprint.**
  1. Create branch `agent/engineer/health-endpoint` from main HEAD. Implement `GET /health` per all 5 STORY-10 ACs (GitHub issue #38): no `UserDep`, returns `{"status": "ok", "db": "ok"|"error"}`, HTTP 200 always, `Content-Type: application/json`. Write unit tests; run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` (expect ≥91% coverage). Open PR targeting main; tag QA and AppSec.
  2. Create branch `agent/engineer/structured-logging` from main HEAD (independent of STORY-10). Implement structured logging per STORY-11 ACs (GitHub issue #39): INFO on each poll cycle, WARNING on rate-guard fire, ERROR on API failures (no credentials in output), LOG_LEVEL from env, module name in WARNING+ messages. Write tests; open PR.
  3. Optionally: create branch `agent/engineer/frontend-scaffold` for STORY-14 (GitHub issue #7) to unblock all P3 frontend stories. Run `npm create vite@latest frontend -- --template react-ts`, configure per STORY-14 ACs.
  - Do NOT start STORY-7 or STORY-21a — they depend on PR #28 merging first.
  - Update `team/agents/engineer.md`.

### QA
- **Today (2026-07-01):**
  1. Stand by to review Engineer's STORY-10 and STORY-11 PRs as soon as they open. Checkout the branch, run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`, verify all STORY-10 and STORY-11 ACs are covered. Post LGTM comment if clean.
  2. PR #28 and PR #31 require no further QA action — both have standing LGTM. Awaiting DevOps merge.
  - Update `team/agents/qa.md`.

### DevOps
- **Today (2026-07-01) — BLOCKED: CRITICAL. MERGE PR #28 AND PR #31 IMMEDIATELY.**
  DevOps has been inactive since 2026-06-23 (9 days). Escalation issue #46 is open.
  1. Merge PR #28 (`agent/engineer/unit-tests-oddsapi`) into main. All gates are green: QA LGTM (2026-06-29) ✅, AppSec CLEAR ✅, CI GREEN ✅. This is the single most impactful action in the sprint.
  2. Confirm post-merge CI run on main is green (expect 62 tests: 40 existing + 22 OddsApi unit tests).
  3. Immediately merge PR #31 (`agent/qa/integration-tests-odds`) into main. All gates: QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅.
  4. Confirm post-merge CI run on main is green (expect 62 backend + 16 integration = 78 total tests).
  5. Close issue #46 (escalation) after both merges complete.
  6. Update `team/agents/devops.md` after each merge.
  - No further blockers exist. Both PRs are merge-ready. STORY-7, STORY-21a, and STORY-21b cannot start until PR #28 lands on main.

### AppSec
- **Today (2026-07-01):** Stand by to scan new PRs from Engineer.
  1. When Engineer opens PR for STORY-10 (`agent/engineer/health-endpoint`): run `bandit -r backend/app/` and `pip-audit -r backend/requirements.txt` against the branch. Verify no new runtime dependencies. Post SECURITY CLEAR (or findings) on the PR.
  2. Same for STORY-11 (`agent/engineer/structured-logging`) and STORY-14 (`agent/engineer/frontend-scaffold`) if opened today.
  3. No further action needed on PR #28 or PR #31 — both are already SECURITY CLEAR.
  - Update `team/agents/appsec.md`.

### Product Owner
- **Today (2026-07-01):** Monitor Sprint 2 progress.
  1. STORY-7, STORY-21a, STORY-21b are all blocked on PR #28 merging. If DevOps does not merge PR #28 today, assess whether Sprint 2 scope needs to be revised (drop STORY-21b from Sprint 2 scope if less than 5 working days remain before those stories can start).
  2. Confirm STORY-10 (#38), STORY-11 (#39), STORY-14 (#7) ACs are clear for Engineer. No action needed — already documented in backlog.md.
  3. No new stories to pull into Sprint 2 — scope is locked unless a story drops out.
  - Update `team/agents/product-owner.md` if any scope decisions are made.

### Prod Support
- **Today (2026-07-01):**
  1. Escalation issue #46 was opened this morning — confirm it is labeled `blocked` + `priority:high` and visible on the sprint board.
  2. When PR #28 merges: close issue #4 (STORY-3). When PR #31 merges: close issue #5 (STORY-4). Confirm CI is green after each merge.
  3. Triage any new PRs opened by Engineer for STORY-10/11/14 — check for unlabeled issues, stale issues.
  4. Issue #3 (STORY-2) confirmed closed as of 2026-07-01 — no action needed.
  - Update `team/agents/prod-support.md` after each action.

---

## Merge Order (Sprint 2 — Critical)

1. **DevOps merges PR #28** (`agent/engineer/unit-tests-oddsapi`) — all gates green. **MUST HAPPEN TODAY.**
2. **DevOps merges PR #31** (`agent/qa/integration-tests-odds`) — immediately after PR #28.
3. **Engineer opens PR for STORY-10** → QA LGTM → AppSec CLEAR → DevOps merges.
4. **Engineer opens PR for STORY-11** → QA LGTM → AppSec CLEAR → DevOps merges.
5. After PR #28 lands: **Engineer opens PR for STORY-7** (rate limit guard).
6. After PR #28 lands: **Engineer opens PR for STORY-21a** (Betfair polling job).
7. After STORY-21a + STORY-7 merge: **Engineer opens PR for STORY-21b** (Odds API polling job).

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests; `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min (PO decision D9/D17)
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened (or, for DevOps as merge operator: 2+ days with no merge action after all gates are clear)
- STORY-7 and STORY-21a/21b cannot start until PR #28 merges — this is a hard dependency
- STORY-21b: ⚠️ `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min (6h) — 120 req/month against 500 req/month cap. Do NOT lower without PO sign-off.
- Sprint 1 retro written 2026-07-01 (overdue from 2026-06-27): `/repo/team/sprint/retrospective.md`
- DevOps escalation: issue #46 opened 2026-07-01 by Prod Support

---

## Sprint Health

| Metric | Value |
|--------|-------|
| Sprint | 2 |
| Sprint Start | 2026-06-29 |
| Sprint End | 2026-07-10 |
| Stories In Progress | 2 (STORY-3 carry-over PR #28, STORY-4 carry-over PR #31) |
| Stories To Do | 6 (STORY-10, STORY-11, STORY-14 unblocked; STORY-7, STORY-21a, STORY-21b blocked on STORY-3) |
| Stories Done (Sprint 2) | 0 |
| Stories Total (Sprint 2) | 8 (including 2 carry-overs) |
| Days Remaining | 7 (sprint ends 2026-07-10) |
| Open PRs | 2 (#28 all-gates-clear/DevOps-BLOCKED, #31 awaiting #28) |
| BLOCKED agents | 1 (DevOps — 9 days inactive, escalation issue #46) |
| Sprint risk | HIGH — DevOps stall blocks 3 of 6 Sprint 2 stories; STORY-7/21a/21b cannot start until PR #28 merges |
