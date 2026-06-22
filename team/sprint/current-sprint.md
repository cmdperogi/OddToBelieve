# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | **REBASE OVERDUE** — QA LGTM (40/40); PR #8 merged 2026-06-20; rebase onto main has not started (2 days elapsed) | 9 unit tests, 100% betfair.py coverage. Rebase must happen TODAY. Merge after: PR #32 merges to green CI. |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | **STACKED** — QA LGTM (62/62, 91% coverage); DB persistence complete; waiting on PR #26 rebase + merge | 22 unit tests (16 HTTP + 6 persistence). Merge order: PR #26 → PR #28. |

### CI Fix (Blocking main — DevOps)

| PR | Owner | Status | Notes |
|----|-------|--------|-------|
| [#32](https://github.com/cmdperogi/OddToBelieve/pull/32) | DevOps | Open — CI-verified ✅; awaiting merge | One-line fix: CI `ADMIN_PASSWORD` fallback `'test-password'` → `'changeme'`. Two CI runs on main failing (401 Unauthorized) until this lands. 31/31 pass on PR #32 branch. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-4: Integration tests /odds/* endpoints | QA | **Draft PR [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) — MUST CONVERT TO READY-FOR-REVIEW TODAY** | PR #8 merged 2026-06-20 — trigger condition hit 2 days ago. 16/16 tests passing. All 5 ACs covered. |

### Done

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-13: Scaffold FastAPI backend | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | ✅ 2026-06-20 | All security findings resolved. AppSec CLEAR. QA LGTM 31/31. |
| STORY-1: GitHub Actions CI pipeline | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | ✅ 2026-06-20 | Merged immediately after PR #8 per sprint merge order. CI now active on main. |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | #9 (same branch) | ✅ 2026-06-20 | All 5 credential-shaped vars use `${{ secrets.VAR \|\| 'fallback' }}`. |
| STORY-5: AppSec baseline scan | — | ✅ 2026-06-20 | Bandit: B106 false positive only. pip-audit: 0 CVEs. Issue #6 closed 2026-06-22. |
| STORY-15: Fix hardcoded credential defaults in config.py | #8 (same branch) | ✅ 2026-06-20 | No plaintext defaults remain; `ValueError` on startup if env vars unset. Issue #17 closed. |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | #8 (same branch) | ✅ 2026-06-20 | `_pwd_context.verify()` in place. Issue #18 closed. |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | #8 (same branch) | ✅ 2026-06-20 | `python-jose[cryptography]>=3.4.0`, 0 CVEs. Issue #19 closed. |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | #8 (same branch) | ✅ 2026-06-20 | `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`. Issues #20, #24, #25 closed. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | #8 (same branch) | ✅ 2026-06-20 | `pytest==9.0.3`, `black==26.3.1`. Issue #22 closed. |

### Blocked

*(none — all agents have open PRs; rebase delays are urgent but not formally BLOCKED)*

**Sprint Status — HIGH risk (upgraded from MEDIUM 2026-06-22):** PRs #8 and #9 merged June 20 — sprint goal's CI and security baseline are achieved. However, the rebase cascade that was supposed to start immediately on June 20 has not started (2 days elapsed). CI on main is currently FAILING due to ADMIN_PASSWORD mismatch (PR #32 fix awaiting merge). With 5 working days remaining (June 22–27), full sprint recovery is still possible IF: PR #32 merges today, Engineer rebases PR #26 today, PR #31 converts from draft today, and the cascade completes by June 25. Every further day of delay risks STORY-2, STORY-3, and STORY-4 slipping out of Sprint 1.

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-22 (Monday, Sprint 1 Day 7 of 10)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint.
- ✅ 2026-06-16: Reconciled board against agent status files; daily assignments; sprint risk noted.
- ✅ 2026-06-17: Reviewed all agent/PR status. AppSec reaches 2-day threshold tomorrow. Updated board and assignments.
- ✅ 2026-06-18: AppSec formally BLOCKED (3 days no action). Prod Support confirmed; issue #27 opened. Updated board.
- ✅ 2026-06-19: AppSec BLOCKED lifted — scan completed 2026-06-18. Engineer opened PR #28 (STORY-3). QA opened draft PR #31 (STORY-4). Sprint risk downgraded CRITICAL → MEDIUM.
- ✅ 2026-06-22: PRs #8 and #9 merged 2026-06-20. STORY-13, STORY-1, STORY-19, STORY-5 moved to Done. Rebase cascade 2 days overdue; CI failing on main (PR #32 fix queued). Sprint risk upgraded to HIGH. Note: today is Monday (Sprint 1 Day 7); no new stories pulled into Sprint 1 — scope is locked for last week. Sprint 2 planning on June 29.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Engineer
- **Today (2026-06-22) — URGENT ACTION REQUIRED:** PR #8 merged 2026-06-20. Your assigned rebase of PR #26 was due immediately on June 20. **TWO DAYS HAVE PASSED.** Do not update the status file before completing this:
  1. Rebase branch `agent/engineer/unit-tests-betfair` onto current main.
  2. Run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` — expect 40 tests (31 from main + 9 Betfair unit tests), all passing.
  3. Push rebase; post a comment on PR #26 confirming rebase complete and tests passing.
  4. When PR #26 merges: immediately rebase `agent/engineer/unit-tests-oddsapi` onto main; run 62-test suite; push.
  - Update `team/agents/engineer.md` with rebase status.

### QA
- **Today (2026-06-22) — URGENT ACTION REQUIRED:** PR #8 merged 2026-06-20 — your trigger to convert PR #31 from draft was two days ago. **Convert PR #31 to ready-for-review NOW.** Also: as soon as Engineer pushes the rebase of PR #26, run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` on the rebased branch and confirm 40/40 passing. Post LGTM comment on PR #26 if clean. Update `team/agents/qa.md`.

### DevOps
- **Today (2026-06-22) — CRITICAL: MERGE PR #32.** CI on main has been FAILING since June 20 (two consecutive runs, all 401 Unauthorized — ADMIN_PASSWORD mismatch). PR #32 (`agent/devops/fix-ci-admin-password`) is a one-line fix that is CI-verified (31/31 on its branch). Merge it immediately to restore CI green on main. After merging: confirm CI run succeeds on main (31 tests, no 401 errors). Then stand ready to merge PR #26 as soon as Engineer completes the rebase. Update `team/agents/devops.md`.

### AppSec
- **Today (2026-06-22):** STORY-5 formal baseline scan is complete (2026-06-20). Your next action: scan the rebased versions of PR #26 (`agent/engineer/unit-tests-betfair`) and PR #28 (`agent/engineer/unit-tests-oddsapi`) after Engineer pushes rebases. Both branches were previously cleared (2026-06-18), but confirm no new dependencies or code paths were introduced during the rebase. Post a scan status comment on each PR before they merge. Update `team/agents/appsec.md`.

### Product Owner
- **Today (2026-06-22):** Backlog refinement complete — decisions D8–D14, STORY-21/22/23 added, STORY-12 split into 12a/12b. ✅ No further action required today. Optionally: confirm the Sprint 1 Done definition with the team. Done count is currently 5 stories (STORY-13, 1, 19, 5 + security bundle 15/16/17/18/20 as a block). STORY-2, 3, 4 remain the outstanding sprint deliverables — all achievable by June 27 if the rebase cascade starts today.

### Prod Support
- **Today (2026-06-22):** Issues #1, #2, #6 closed; stale comments posted on #3, #4, #5, #7. **Remaining action:** Monitor the rebase situation. If branch `agent/engineer/unit-tests-betfair` shows no new commits by end of today (June 22), open a tracking issue flagging the 2-day rebase delay. Also: check CI on main after PR #32 merges — confirm backend job goes green (expect 31 tests). Update `team/agents/prod-support.md`.

---

## Merge Order (CRITICAL — must be followed)

1. ~~AppSec posts formal approval comment on PR #8 → PR #8 merges~~ ✅ DONE (2026-06-20)
2. ~~DevOps merges PR #9 immediately after PR #8~~ ✅ DONE (2026-06-20)
3. **DevOps merges PR #32** (CI ADMIN_PASSWORD fix) → CI goes green on main
4. **Engineer rebases PR #26** (`agent/engineer/unit-tests-betfair`) onto main → PR #26 merges
5. **Engineer rebases PR #28** (`agent/engineer/unit-tests-oddsapi`) onto main after PR #26 merges → PR #28 merges
6. **QA converts PR #31** to ready-for-review → PR #31 merges after review

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
- ~~AppSec formal approval comment on PR #8 is the sole remaining sprint merge gate~~ — superseded; PR #8 merged 2026-06-20
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened
- STORY-15, 16, 17, 18, 20 resolved on PR #8 branch — merged 2026-06-20
- STORY-19 resolved on PR #9 branch — merged 2026-06-20
- /health intentionally unauthenticated — named design exception (PO decision D5)
- CI on main currently FAILING: `ADMIN_PASSWORD` mismatch (CI uses `'test-password'`; conftest uses `'changeme'`). Fix: PR #32. Do NOT merge PR #26 or PR #28 before PR #32 merges — tests will fail in CI.
- Monday 2026-06-22: no new stories added to Sprint 1 (scope locked for final week). Sprint 2 planning: Monday 2026-06-29.
