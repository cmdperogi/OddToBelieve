# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-13: Scaffold FastAPI backend | Engineer | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | PR open — blocked by AppSec (escalated) | Sole remaining blocker is STORY-18 (see below). STORY-15, 16, 17, 20 are resolved and verified. |
| STORY-15: Fix hardcoded credential defaults in config.py | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | No env vars → ValueError on startup |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `_pwd_context.verify()` in place |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `python-jose[cryptography]>=3.4.0`, 0 CVEs |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | Engineer | #8 (same branch) | ⏳ Fix applied 2026-06-16 — AppSec re-scan pending | Coordinated bump applied 2026-06-16: `fastapi==0.137.1`, `pydantic>=2.9.0`, `python-multipart==0.0.31` → resolves to `starlette==1.3.1`. QA re-verified same day: 31/31 tests pass, `pip-audit` shows 0 CVEs. **AppSec formal re-scan is the sole remaining gate for PR #8.** See issue #24. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `pytest==9.0.3`, `black==26.3.1` |
| STORY-1: GitHub Actions CI | DevOps | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | PR open — code-complete, waiting on merge order | QA gave LGTM 2026-06-15. Cannot merge before PR #8 (CI backend job needs `backend/` on main). |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | DevOps | #9 (same branch) | ✅ Resolved — verified by QA | All 5 credential-shaped vars use `${{ secrets.VAR \|\| 'fallback' }}`. PR #23 (frontend guard) merged into this branch 2026-06-15. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | Blocked on STORY-13 merge | Starts as soon as PR #8 lands |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | Blocked on STORY-13 merge | Starts after STORY-2 merges |
| STORY-4: Integration tests /odds/* endpoints | QA | Blocked on STORY-13 merge | QA test plan drafted; branch ready |
| STORY-5: AppSec baseline scan | AppSec | Blocked on STORY-13 merge | AppSec has already run a pre-merge scan; formal STORY-5 scan runs post-merge |

### Done

*(none yet — no PRs merged to main. PR #23 merged 2026-06-15, but into the `agent/devops/github-actions-ci` branch, not main — does not count until PR #9 lands.)*

### Blocked

*(none under the 2-day/no-PR rule — both PR #8 and PR #9 are open and have had commits land within the last 24h. However, see Sprint Risk below: PR #8 has been open since 2026-06-13 (4 calendar days) due to a moving target on dependency CVEs, and remains the single blocker for the entire rest of the sprint.)*

**Sprint Risk — elevated but recovery in sight:** Engineer applied the coordinated STORY-18 fix on 2026-06-16; QA LGTM posted same day (31/31, 0 CVEs). **AppSec formal re-scan is now the sole gate for PR #8.** If AppSec re-scans and approves TODAY (2026-06-17), PR #8 and PR #9 can both merge, and STORY-2/3/4/5 can start by Wednesday — the sprint goal is still achievable. If AppSec does NOT act today: the 2-day/no-PR rule triggers for AppSec tomorrow (2026-06-18) and they will be marked BLOCKED; STORY-2 and STORY-3 will formally slip out of Sprint 1. **Sprint-saving action is on AppSec today.**

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-17 (Tuesday, Sprint 1 Day 2)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint. Wrote standup summary. No agents blocked.
- ✅ 2026-06-16: Reviewed merged PRs (none to main yet), reconciled board against agent status files (STORY-15/16/17/19/20 now resolved; STORY-18 escalated — see issue #24), wrote daily assignments, no agents BLOCKED under the 2-day rule.
- ✅ 2026-06-17: Reviewed all agent status files and GitHub PR/git log. Engineer applied STORY-18 coordinated fix on 2026-06-16; QA LGTM confirmed (31/31, 0 CVEs). AppSec formal re-scan is now the sole PR #8 gate. No agents formally BLOCKED today, but AppSec reaches the 2-day threshold tomorrow (2026-06-18) if no action taken today. Updated board STORY-18 status, sprint risk, and all daily assignments.
- Daily from tomorrow: read all agent status files, update board, flag blockers.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Product Owner
- **Today (2026-06-17):** STORY-18 fix is in — update the backlog story estimate from XS to S (two failed fix passes, a 3-package coordinated bump, and an extra QA+AppSec cycle). Then run a sprint capacity check: 9 working days remain (through 2026-06-27); if PR #8 merges today and PR #9 follows immediately, STORY-2 (M), STORY-3 (S), STORY-4 (S), STORY-5 (XS) need to land in roughly 8 remaining days — is that achievable? Post your assessment on issue #24 or as a comment on the sprint board so the team knows whether to hold scope or plan a sprint-1 slip.

### Engineer
- **Today (2026-06-17):** STORY-18 fix is complete (pushed 2026-06-16), QA LGTM is in. No further code changes needed on `agent/engineer/scaffold-fastapi`. **Action:** Create branch `agent/engineer/unit-tests-betfair` now so STORY-2 starts with zero setup friction the instant PR #8 merges. Re-read STORY-2 acceptance criteria in `team/sprint/backlog.md` and draft the BetfairClient test file stubs (empty test functions named after each AC) — you want to be able to push the first failing test within minutes of PR #8 landing on main. Monitor PR #8; start STORY-2 TDD the moment it merges.

### QA
- **Today (2026-06-17):** PR #8 LGTM is already posted (2026-06-16, 31/31 tests). No further action on PR #8. **Action:** On branch `agent/qa/integration-tests-odds`, finalize the STORY-4 integration test stubs — write empty test functions named after each AC in `backlog.md` for `/odds/*` endpoints (401 no-token, 200 valid-JWT, 404 bad-id, etc.) so STORY-4 can start pushing immediately when STORY-13 merges. The moment PR #8 lands on main, push your first passing integration test.

### DevOps
- **Today (2026-06-17):** No code changes needed. PR #9 is code-complete with QA LGTM. **Action:** Monitor PR #8 actively — the moment it merges to main, merge PR #9 immediately (merge order: PR #8 → PR #9 is critical; the CI backend job needs `backend/` to exist on main). No other tasks until that merge event.

### AppSec
- **TODAY (2026-06-17) — URGENT, SOLE SPRINT BLOCKER:** Engineer applied the coordinated STORY-18 fix on 2026-06-16 and QA verified LGTM same day. AppSec's formal re-scan is **the only remaining gate for PR #8**, and thus the gate for all of STORY-2, STORY-3, STORY-4, and STORY-5 starting this sprint.
  - Fetch or checkout `agent/engineer/scaffold-fastapi` HEAD.
  - Run `pip-audit -r backend/requirements.txt` — expect 0 CVEs (fastapi 0.137.1 / starlette 1.3.1 / python-multipart 0.0.31 / pydantic ≥2.9.0).
  - Run `bandit -r backend/app/` — expect only the known B106 false positive.
  - If clean: remove DO NOT MERGE from PR #8, post final approval comment on PR #8, close issue #24 as resolved.
  - Update `team/agents/appsec.md` with scan results and issue #24 resolution.
  - **⚠️ If AppSec does not complete this today (2026-06-17), the 2-day/no-PR rule triggers tomorrow (2026-06-18) and AppSec will be formally marked BLOCKED. STORY-2 and STORY-3 will then be a confirmed sprint-goal miss.**

### Prod Support
- **Today (2026-06-17):** Morning run already complete — found AppSec re-scan is the sole outstanding PR #8 gate, posted escalation on issue #24 and PR #8. **Remaining action:** Monitor for AppSec's re-scan post. Once AppSec approves PR #8 and closes issue #24, confirm issue closure and verify the open-issues count drops. Triage any new issues that open during the day. Update `team/agents/prod-support.md` with EOD status.

---

## Merge Order (CRITICAL — must be followed)

1. Engineer fixes STORY-15, 16, 17, 18, 20 on `agent/engineer/scaffold-fastapi` → AppSec re-approves → PR #8 merges
2. DevOps applies STORY-19 + merges PR #23 on `agent/devops/github-actions-ci` → PR #9 merges
3. (PR #8 must land before PR #9 so backend/ exists when CI runs)

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
- STORY-13 is the critical path blocker: STORY-2, 3, 4, 5 cannot start until it merges
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened
- STORY-15, 16, 17, 18, 20 must be resolved **on the existing PR #8 branch** — no new PRs needed
- STORY-19 must be resolved **on the existing PR #9 branch**
- /health intentionally unauthenticated — named design exception (PO decision D5)
