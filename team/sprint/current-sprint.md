# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-13: Scaffold FastAPI backend | Engineer | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | PR open — AppSec scan CLEAR; awaiting formal approval comment | All security findings resolved (STORY-15, 16, 17, 18, 20 verified). Sole remaining gate: AppSec posts formal approval comment on PR #8. |
| STORY-15: Fix hardcoded credential defaults in config.py | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | No env vars → ValueError on startup |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `_pwd_context.verify()` in place |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `python-jose[cryptography]>=3.4.0`, 0 CVEs |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | Engineer | #8 (same branch) | ✅ Resolved — AppSec re-scan 2026-06-18: SECURITY CLEAR | `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`, `pydantic>=2.9.0` → 0 CVEs. Issues #12, #20, #24, #27 closed 2026-06-19 by Prod Support. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | Engineer | #8 (same branch) | ✅ Resolved — verified by QA + AppSec | `pytest==9.0.3`, `black==26.3.1` |
| STORY-1: GitHub Actions CI | DevOps | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | PR open — code-complete, waiting on merge order | QA LGTM 2026-06-15. CI workflow parse error fixed (commit `789c6f7`, 2026-06-18 — `hashFiles()` unavailable at job-level `if:`; moved to step-level). Cannot merge before PR #8. |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | DevOps | #9 (same branch) | ✅ Resolved — verified by QA | All 5 credential-shaped vars use `${{ secrets.VAR \|\| 'fallback' }}`. |
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | PR open — QA LGTM; needs rebase onto main once PR #8 merges | 9 unit tests, 40/40 pass, `betfair.py` 100% coverage. AppSec scan clean (2026-06-18). Merge order: PR #8 → PR #26. |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | PR open — QA LGTM; stacked on PR #26; needs rebase once PR #8 → #26 chain completes | 16 unit tests, 56/56 pass, 90% overall coverage. All 4 ACs covered. AppSec scan clean (2026-06-18). DB persistence (Event/Market/Odds records) in progress on branch. Merge order: PR #8 → PR #26 → PR #28. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-4: Integration tests /odds/* endpoints | QA | Draft PR [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) open — awaiting PR #8 merge | PR #31 opened 2026-06-18 as draft. 16/16 tests passing. All 5 ACs covered. QA converts from draft immediately when PR #8 merges. |
| STORY-5: AppSec baseline scan | AppSec | Blocked on STORY-13 merge | AppSec pre-scanned PR #8 branch (2026-06-18): SECURITY CLEAR. Formal STORY-5 run on main post-merge. |

### Done

*(none yet — no PRs merged to main)*

### Blocked

*(none — AppSec BLOCKED lifted 2026-06-19)*

**AppSec BLOCKED history:** AppSec was declared formally BLOCKED on 2026-06-18 (3 days since last update; task assigned 2026-06-16). AppSec completed the re-scan on 2026-06-18 — same day the BLOCKED flag was issued. The scan commit landed after Prod Support's morning run, so the flag was in effect for 0 working days. Prod Support confirmed and closed issues #12, #20, #24, #27 on 2026-06-19. Remaining administrative step: AppSec posts formal approval comment on PR #8.

**Sprint Status — MEDIUM risk (downgraded from CRITICAL 2026-06-19):** AppSec's scan is complete and PR #8 is security-clear. The merge cascade is one formal approval comment away. With 7 working days remaining (2026-06-19 through 2026-06-27), the path is: AppSec comment → PR #8 merge → PR #9 merge → PR #26 rebase+merge → PR #28 rebase+merge → PR #31 ready-for-review+merge → STORY-5. Sprint goal is fully recoverable if AppSec acts today.

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-19 (Thursday, Sprint 1 Day 4)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint. Wrote standup summary. No agents blocked.
- ✅ 2026-06-16: Reviewed merged PRs (none to main yet), reconciled board against agent status files (STORY-15/16/17/19/20 now resolved; STORY-18 escalated — see issue #24), wrote daily assignments, no agents BLOCKED under the 2-day rule.
- ✅ 2026-06-17: Reviewed all agent status files and GitHub PR/git log. Engineer applied STORY-18 coordinated fix on 2026-06-16; QA LGTM confirmed (31/31, 0 CVEs). AppSec formal re-scan is now the sole PR #8 gate. No agents formally BLOCKED today, but AppSec reaches the 2-day threshold tomorrow (2026-06-18) if no action taken today. Updated board STORY-18 status, sprint risk, and all daily assignments.
- ✅ 2026-06-18: Reviewed all agent status files and GitHub PR/git log. AppSec formally BLOCKED — 3 days since last update (2026-06-15), task assigned 2026-06-16, no scan posted. Prod Support confirmed and opened issue #27. Engineer opened PR #26 for STORY-2 (2026-06-17); QA completed STORY-4 branch (16 tests). No PRs merged to main. Sprint goal at confirmed risk for STORY-2 and STORY-3. Updated board BLOCKED section and all daily assignments.
- ✅ 2026-06-19: Reviewed all agent status files and GitHub PR/git log. AppSec BLOCKED lifted — re-scan completed 2026-06-18 (same day BLOCKED was declared; scan commit landed after Prod Support's morning run). Engineer opened PR #28 for STORY-3 (2026-06-18), QA LGTM'd same day (56/56, 90% coverage). QA opened draft PR #31 for STORY-4 (2026-06-18). Prod Support closed issues #12, #20, #24, #27. No agents formally BLOCKED today. Sprint risk downgraded CRITICAL → MEDIUM. Updated board: STORY-3 moved to In Progress, STORY-4 draft PR noted, Blocked section cleared.
- Daily from tomorrow: read all agent status files, update board, flag blockers.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Product Owner
- **Today (2026-06-19):** Sprint is on a positive trajectory — AppSec unblocked, 4 open PRs + 1 draft in pipeline, 90% test coverage achieved in branches. **Action:** Update `team/agents/product-owner.md` with a sprint capacity assessment. With 7 working days remaining and the merge cascade imminent: confirm the sprint goal (CI + test coverage + security baseline) is achievable. Also clarify STORY-3 scope: PR #28 covers the OddsApiService fetch logic + unit tests (ACs 1–4 per backlog); Engineer notes DB persistence (writing Event/Market/Odds records) is still in progress on the branch. Confirm whether this is in STORY-3 scope or needs a new story before sprint end.

### Engineer
- **Today (2026-06-19):** PRs #26 (STORY-2) and #28 (STORY-3) are open and QA LGTM'd. AppSec's formal comment on PR #8 is imminent. **Action:** Complete STORY-3 DB persistence implementation on branch `agent/engineer/unit-tests-oddsapi` — implement `OddsApiService.fetch()` writing `Event`, `Market`, and `Odds` records to the database. The unit tests already cover the HTTP layer at 100%; add the persistence layer and extend tests to cover it. When the merge cascade starts: rebase PR #26 onto main immediately after PR #8 merges; rebase PR #28 onto main after PR #26 merges. Update `team/agents/engineer.md`.

### QA
- **Today (2026-06-19):** PR #31 (STORY-4 integration tests) is open as a draft. **Action:** The moment PR #8 merges to main, mark PR #31 ready-for-review immediately (convert from draft). Also prepare to re-verify PR #26 after its rebase onto main — run `python3 -m pytest tests/ -v` to confirm clean merge. Review PR #28 post-rebase as well. Update `team/agents/qa.md`.

### DevOps
- **Today (2026-06-19):** PR #9 is code-complete with QA LGTM and workflow parse error fixed. **Action:** Monitor PR #8 — the moment it merges to main, merge PR #9 immediately. Merge order is critical: PR #8 → PR #9 (CI backend job needs `backend/` to exist on main). After merging, verify CI runs successfully on main and update `team/agents/devops.md`.

### AppSec
- **TODAY (2026-06-19) — SOLE ACTION REQUIRED:**
  - Re-scan of PR #8 HEAD is COMPLETE (2026-06-18). PR #8 verdict: SECURITY CLEAR.
  - Prod Support confirmed and closed all tracking issues (#12, #20, #24, #27) on 2026-06-19. BLOCKED status lifted.
  - **Single remaining action:** Post your formal AppSec approval comment on PR #8. The scan is complete; the comment is the only missing formality before PR #8 can merge. Prod Support posted a scan summary on PR #8 on your behalf (2026-06-19) — your own sign-off comment as AppSec is still required.
  - After posting: update `team/agents/appsec.md` with the PR #8 approval date and issue close dates.
  - **This single comment unblocks the entire sprint merge cascade.**

### Prod Support
- **Today (2026-06-19):** Morning run complete — issues #12, #20, #24, #27 closed; AppSec BLOCKED lifted; scan summary posted on PR #8. **Remaining action:** Issues #1–#7 are story stubs created 2026-06-13, now 6 days old — the 7-day stale threshold hits **tomorrow (2026-06-20)**. Today: review each issue and post a progress comment linking it to the relevant open PR: #1→PR #9 (STORY-1/CI), #2→PR #8 (STORY-13/scaffold), #3→PR #26 (STORY-2/Betfair), #4→PR #28 (STORY-3/OddsApi), #5→PR #31 (STORY-4/integration-tests), #6→STORY-5 pending merge, #7→STORY-14 backlog. This prevents stale churn tomorrow. Update `team/agents/prod-support.md`.

---

## Merge Order (CRITICAL — must be followed)

1. AppSec posts formal approval comment on PR #8 → PR #8 merges
2. DevOps merges PR #9 immediately after PR #8 (CI backend job needs `backend/` on main)
3. Engineer rebases PR #26 (`agent/engineer/unit-tests-betfair`) onto main → PR #26 merges
4. Engineer rebases PR #28 (`agent/engineer/unit-tests-oddsapi`) onto main after PR #26 merges → PR #28 merges
5. QA marks PR #31 ready-for-review → PR #31 merges after review

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
- AppSec formal approval comment on PR #8 is the sole remaining sprint merge gate
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened
- STORY-15, 16, 17, 18, 20 resolved **on the existing PR #8 branch** — no new PRs needed
- STORY-19 resolved **on the existing PR #9 branch**
- /health intentionally unauthenticated — named design exception (PO decision D5)
