# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | **READY TO MERGE** — CI GREEN (run 28008765198) ✅; QA LGTM ✅; AppSec CLEAR ✅; base set to `main` ✅ | Prod Support rebased onto main HEAD (`e3f90b0`) 2026-06-23; CI green. DevOps: merge this now. |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | **STACKED** — QA LGTM (62/62, 91% coverage); AppSec CLEAR ✅; waiting on PR #26 merge + Engineer rebase | Merge order: PR #26 → Engineer rebases PR #28 → PR #28 merges. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-4: Integration tests /odds/* endpoints | QA | **PR [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) READY-FOR-REVIEW** — CI GREEN (run 28009005581) ✅; AppSec CLEAR ✅ | Converted from draft 2026-06-22. Prod Support rebased + black-fixed 2026-06-23. Merge after PR #28. |

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
| CI Fix: Align ADMIN_PASSWORD fallback with test fixtures | [#32](https://github.com/cmdperogi/OddToBelieve/pull/32) | ✅ 2026-06-22 | One-line fix: `'test-password'` → `'changeme'`. CI GREEN since merge (run 27941596842). |

### Blocked

*(none — all agents have open PRs or completed tasks)*

**Sprint Status — MEDIUM risk (downgraded from HIGH 2026-06-22):** The merge cascade is now fully unblocked as of 2026-06-23. PR #32 merged and CI is GREEN on main. PR #26 is CI-green and ready for DevOps to merge TODAY. PR #28 is clean and awaiting the rebase cascade. PR #31 is ready-for-review and CI-green. With 4 working days remaining (June 23–27), all three stories (STORY-2, STORY-3, STORY-4) are achievable IF DevOps merges PR #26 today and Engineer rebases PR #28 immediately after.

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-23 (Tuesday, Sprint 1 Day 8 of 10)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint.
- ✅ 2026-06-16: Reconciled board against agent status files; daily assignments; sprint risk noted.
- ✅ 2026-06-17: Reviewed all agent/PR status. AppSec reaches 2-day threshold tomorrow. Updated board and assignments.
- ✅ 2026-06-18: AppSec formally BLOCKED (3 days no action). Prod Support confirmed; issue #27 opened. Updated board.
- ✅ 2026-06-19: AppSec BLOCKED lifted — scan completed 2026-06-18. Engineer opened PR #28 (STORY-3). QA opened draft PR #31 (STORY-4). Sprint risk downgraded CRITICAL → MEDIUM.
- ✅ 2026-06-22: PRs #8 and #9 merged 2026-06-20. STORY-13, STORY-1, STORY-19, STORY-5 moved to Done. Rebase cascade 2 days overdue; CI failing on main (PR #32 fix queued). Sprint risk upgraded to HIGH.
- ✅ 2026-06-23: PR #32 merged (CI GREEN). Engineer rebased PR #26; Prod Support fixed CI base and conflict; PR #26 CI GREEN. PR #31 ready-for-review and CI GREEN. Sprint risk downgraded to MEDIUM. DevOps must merge PR #26 today to complete the cascade.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Engineer
- **Today (2026-06-23) — STAND BY TO REBASE PR #28:** PR #26 is CI GREEN and ready to merge — DevOps is merging it today. The moment PR #26 merges to main:
  1. Rebase branch `agent/engineer/unit-tests-oddsapi` onto the new main HEAD.
  2. Run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` — expect 62 tests all passing (40 from main + 22 OddsApi unit tests).
  3. Push rebase; post a comment on PR #28 confirming rebase complete and tests passing.
  - Update `team/agents/engineer.md` with rebase status.
  - Do NOT start new work until PR #28 rebase is pushed — the cascade must complete before Sprint 1 ends.

### QA
- **Today (2026-06-23) — TWO TASKS:**
  1. **Review PR #31:** It is ready-for-review and CI GREEN (post Prod Support black fix). Confirm 16/16 integration tests pass on the current branch HEAD (`6d09ba7`) and all 5 STORY-4 ACs are covered. Post LGTM comment. Merge after PR #28 lands.
  2. **Stand by for PR #28 rebase:** As soon as Engineer pushes the PR #28 rebase, run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` on the rebased branch and confirm 62/62 passing. Post final LGTM on PR #28.
  - Update `team/agents/qa.md`.

### DevOps
- **Today (2026-06-23) — CRITICAL: MERGE PR #26 NOW.** All gates are green: CI GREEN (run 28008765198) ✅, QA LGTM ✅, AppSec CLEAR ✅, base set to `main` ✅. This is the highest-priority action in the sprint today.
  1. Merge PR #26 (`agent/engineer/unit-tests-betfair`) into main.
  2. Confirm post-merge CI run on main is green (expect 40 tests passing, including 9 Betfair unit tests now on main).
  3. After Engineer rebases PR #28 and QA LGTMs: merge PR #28 into main.
  4. After PR #28 merges: merge PR #31 into main (QA LGTM + AppSec CLEAR already in place).
  - Update `team/agents/devops.md` after each merge.

### AppSec
- **Today (2026-06-23):** All open PRs (#26, #28, #31) were scanned and cleared 2026-06-22 — sign-off comments posted on each. No new security action required unless new code is pushed to these branches.
  - After Engineer pushes the PR #28 rebase: confirm no new dependencies or security-relevant code paths were introduced during the rebase. Post a brief confirmation comment on PR #28 before DevOps merges it.
  - Update `team/agents/appsec.md` after re-check.

### Product Owner
- **Today (2026-06-23):** No action required. Backlog refinement is complete (decisions D8–D14, 2026-06-22). Monitor sprint progress — if all three PRs (#26, #28, #31) merge by June 25, consider pulling STORY-10 (/health endpoint) into Sprint 1 as a bonus delivery (XS estimate, depends only on STORY-13 which is on main). Otherwise, hold for Sprint 2.

### Prod Support
- **Today (2026-06-23):** Excellent work fixing PR #26 and PR #31. Monitoring tasks:
  1. After PR #26 merges: confirm CI run on main is green (expect 40 tests — 31 scaffold + 9 Betfair unit tests).
  2. After PR #28 merges: confirm CI run on main is green (expect 62 tests).
  3. After PR #31 merges: confirm CI run on main is green (expect 62 tests — PR #31 adds no new backend tests to main, only the integration test file; confirm no regressions).
  4. Check issues #3 and #4 — these are now approaching resolution (PRs ready to merge). Close #3 (STORY-2) when PR #26 merges; close #4 (STORY-3) when PR #28 merges.
  - Update `team/agents/prod-support.md`.

---

## Merge Order (CRITICAL — must be followed)

1. ~~AppSec posts formal approval comment on PR #8 → PR #8 merges~~ ✅ DONE (2026-06-20)
2. ~~DevOps merges PR #9 immediately after PR #8~~ ✅ DONE (2026-06-20)
3. ~~**DevOps merges PR #32** (CI ADMIN_PASSWORD fix) → CI goes green on main~~ ✅ DONE (2026-06-22)
4. **DevOps merges PR #26** (`agent/engineer/unit-tests-betfair`) — CI GREEN, all gates clear → MERGE TODAY
5. **Engineer rebases PR #28** (`agent/engineer/unit-tests-oddsapi`) onto main after PR #26 merges → PR #28 merges
6. **DevOps merges PR #31** (`agent/qa/integration-tests-odds`) after PR #28 merges and QA confirms LGTM

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
- ~~AppSec formal approval comment on PR #8 is the sole remaining sprint merge gate~~ — superseded; PR #8 merged 2026-06-20
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened
- STORY-15, 16, 17, 18, 20 resolved on PR #8 branch — merged 2026-06-20
- STORY-19 resolved on PR #9 branch — merged 2026-06-20
- /health intentionally unauthenticated — named design exception (PO decision D5)
- ~~CI on main currently FAILING~~ — FIXED: PR #32 merged 2026-06-22; CI GREEN since run 27941596842
- Monday 2026-06-22: no new stories added to Sprint 1 (scope locked for final week). Sprint 2 planning: Monday 2026-06-29.
- 2026-06-23: Prod Support fixed PR #26 (base → main, rebase onto HEAD) and PR #31 (conflict resolution + black formatting). Both CI GREEN.
