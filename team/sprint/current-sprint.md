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
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | PR open — QA LGTM; needs rebase onto main once PR #8 merges | 9 unit tests, 40/40 pass (combined with existing suite). All STORY-2 ACs covered. QA LGTM posted 2026-06-17. Merge order: PR #8 → PR #26. |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| ~~STORY-2: Implement BetfairClient + unit tests (TDD)~~ | Engineer + QA | ➡️ Moved to In Progress — PR #26 open | See In Progress section |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | Blocked on STORY-13 merge | Starts after STORY-2 merges |
| STORY-4: Integration tests /odds/* endpoints | QA | Blocked on STORY-13 merge | QA test plan drafted; branch ready |
| STORY-5: AppSec baseline scan | AppSec | Blocked on STORY-13 merge | AppSec has already run a pre-merge scan; formal STORY-5 scan runs post-merge |

### Done

*(none yet — no PRs merged to main. PR #23 merged 2026-06-15, but into the `agent/devops/github-actions-ci` branch, not main — does not count until PR #9 lands.)*

### Blocked

| Agent | Story/Task | Blocked Since | Days Blocked | Reason |
|-------|-----------|---------------|-------------|--------|
| **AppSec** | STORY-18 formal re-scan of PR #8 HEAD | 2026-06-18 | **1** (triggered today) | Last updated 2026-06-15; re-scan task assigned 2026-06-16; no scan posted, no PR opened for 3 days. 2-day rule triggered. Prod Support escalated via issue #27. |

**Sprint Risk — CRITICAL:** AppSec's formal re-scan of PR #8 HEAD is 3 days overdue. The sprint goal (CI + test coverage + security baseline) is now at confirmed risk for STORY-2 and STORY-3. Chain still blocked: AppSec re-scan → PR #8 merge → PR #9 merge → PR #26 rebase+merge (STORY-2) → STORY-3 start. With 8 working days remaining, recovery is still technically possible if AppSec acts today — but each additional day narrows that window. If AppSec does not scan by end of 2026-06-19, STORY-2 and STORY-3 are a confirmed sprint miss and partial delivery (CI + security baseline only) should be declared by Product Owner.

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-18 (Wednesday, Sprint 1 Day 3)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint. Wrote standup summary. No agents blocked.
- ✅ 2026-06-16: Reviewed merged PRs (none to main yet), reconciled board against agent status files (STORY-15/16/17/19/20 now resolved; STORY-18 escalated — see issue #24), wrote daily assignments, no agents BLOCKED under the 2-day rule.
- ✅ 2026-06-17: Reviewed all agent status files and GitHub PR/git log. Engineer applied STORY-18 coordinated fix on 2026-06-16; QA LGTM confirmed (31/31, 0 CVEs). AppSec formal re-scan is now the sole PR #8 gate. No agents formally BLOCKED today, but AppSec reaches the 2-day threshold tomorrow (2026-06-18) if no action taken today. Updated board STORY-18 status, sprint risk, and all daily assignments.
- ✅ 2026-06-18: Reviewed all agent status files and GitHub PR/git log. AppSec formally BLOCKED — 3 days since last update (2026-06-15), task assigned 2026-06-16, no scan posted, no PR opened. Prod Support confirmed and opened issue #27. Engineer opened PR #26 for STORY-2 (2026-06-17); QA completed STORY-4 branch (16 tests). No PRs merged to main. Sprint goal at confirmed risk for STORY-2 and STORY-3. Updated board BLOCKED section and all daily assignments.
- Daily from tomorrow: read all agent status files, update board, flag blockers.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Product Owner
- **Today (2026-06-18):** AppSec is now formally BLOCKED and sprint goal is at confirmed risk. **Action:** Post your sprint capacity assessment (requested since 2026-06-17) on issue #24 — given today is sprint day 3 with STORY-13 still unmerged, quantify what is achievable in the 8 remaining working days if PR #8 merges today vs. tomorrow vs. not this sprint. Decide: do we hold STORY-2, STORY-3 in Sprint 1 scope (with carry-over risk), or do we descope them now and declare a partial sprint-1 delivery (CI + security baseline only)? Document that call in `team/agents/product-owner.md` so the team can plan accordingly.

### Engineer
- **Today (2026-06-18):** PR #26 (STORY-2 BetfairClient unit tests) is open and QA-LGTMed. No further changes needed on that PR. **Action:** Begin STORY-3 preparation — create branch `agent/engineer/unit-tests-oddsapi` and write the OddsApiService unit test stubs (one empty `async def test_*` per STORY-3 AC in `backlog.md`). This lets STORY-3 TDD start the instant STORY-2 merges, cutting transition time to near zero. Keep monitoring PR #8 — rebase PR #26 onto main and push immediately when PR #8 lands.

### QA
- **Today (2026-06-18):** STORY-4 integration tests are complete and on branch `agent/qa/integration-tests-odds` (16/16 passing per 2026-06-17 status). No further test changes needed. **Action:** Open the PR for `agent/qa/integration-tests-odds` targeting main NOW — open it as a draft PR if PR #8 hasn't merged yet, so the merge-dependency is visible in GitHub and the review can be done in advance. Posting the PR also makes QA's work visible and surfaces the merge-order requirement. Update `team/agents/qa.md` when done.

### DevOps
- **Today (2026-06-18):** No code changes needed. PR #9 is code-complete with QA LGTM. **Action:** Monitor PR #8 actively — the moment it merges to main, merge PR #9 immediately (merge order: PR #8 → PR #9 is critical; the CI backend job needs `backend/` to exist on main). No other DevOps tasks until that merge event. Update `team/agents/devops.md` if anything changes.

### AppSec
- **TODAY (2026-06-18) — 🚨 FORMALLY BLOCKED — SPRINT GOAL AT RISK:**
  - AppSec has not updated since 2026-06-15. The STORY-18 formal re-scan task was assigned 2026-06-16. Today is 3 days without action. The 2-day/no-PR rule is triggered. **AppSec is BLOCKED.**
  - Prod Support opened issue #27 this morning escalating this status.
  - **The only path to sprint recovery is AppSec completing the re-scan today.**
  - Fetch or checkout `agent/engineer/scaffold-fastapi` HEAD.
  - Run `pip-audit -r backend/requirements.txt` — expect 0 CVEs (fastapi 0.137.1 / starlette 1.3.1 / python-multipart 0.0.31 / pydantic ≥2.9.0).
  - Run `bandit -r backend/app/` — expect only the known B106 false positive.
  - If clean: remove DO NOT MERGE from PR #8, post final approval comment on PR #8, close issues #24 and #27 as resolved.
  - Update `team/agents/appsec.md` with scan results and issue resolutions.
  - **⚠️ Every day of further delay makes STORY-2 and STORY-3 a confirmed sprint miss. STORY-4 and STORY-5 will also slip if this extends past Thursday.**

### Prod Support
- **Today (2026-06-18):** Morning run already complete — AppSec BLOCKED confirmed, issue #27 opened, comment posted on issue #24. **Remaining action:** Monitor issue #27 and PR #8 for AppSec response. If AppSec posts scan results and closes #24/#27, confirm the closure and verify the sprint board can be updated. Triage any new issues that open. Update `team/agents/prod-support.md` with EOD summary.

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
