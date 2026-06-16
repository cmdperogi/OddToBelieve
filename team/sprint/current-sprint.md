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
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | Engineer | #8 (same branch) | ⚠️ ESCALATED — first fix insufficient | `fastapi==0.115.0` pulled in starlette 0.38.6 (3 new CVEs, issue #24/#25). 2026-06-16 re-scan by Prod Support found it's worse: 11 CVEs now across starlette + python-multipart 0.0.27. Verified fix requires a coordinated bump: `fastapi==0.137.1` + `pydantic>=2.9.0` (was 2.7.4) + `python-multipart==0.0.31`. Full details + verified version chain on issue #24. This is now the **sole blocker** for PR #8. |
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

**Sprint Risk — escalating:** Every fix applied to clear STORY-18's CVEs so far has surfaced new CVEs on re-scan (python-jose → clean, but multipart/starlette fix introduced new starlette CVEs, and now new python-multipart CVEs too). Prod Support's 2026-06-16 re-scan determined the real fix is a coordinated 3-package version bump (fastapi, pydantic, python-multipart), not another single-line pin. If this isn't resolved by Wednesday 2026-06-18, STORY-2/3/4/5 (and the PO's D7 capacity concern) become a real sprint-goal miss, not just a risk.

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-16 (Monday, Sprint 1 Day 1)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint. Wrote standup summary. No agents blocked.
- ✅ 2026-06-16: Reviewed merged PRs (none to main yet), reconciled board against agent status files (STORY-15/16/17/19/20 now resolved; STORY-18 escalated — see issue #24), wrote daily assignments, no agents BLOCKED under the 2-day rule. Sprint planning already covered by PO's kickoff session this morning (D1–D7) — no new backlog pull needed given the existing D7 capacity concern.
- Daily from tomorrow: read all agent status files, update board, flag blockers.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Product Owner
- ✅ 2026-06-16 (this morning): Added STORY-15–20 to backlog; documented decisions D1–D7. Closed issue #14 design exception. Sprint 1 capacity concern flagged (D7).
- **Today, remaining:** No new backlog grooming needed — sprint composition is set (STORY-13, 1, 2, 3, 4, 5, 15–20). Monitor PR #8: the STORY-18 fix has now failed AppSec re-scan twice (issue #24/#25) and Prod Support's escalation today shows the real fix is a 3-package coordinated bump, not the XS estimate originally given. **Action:** re-estimate STORY-18 (was XS, is now at least S/M) so the D7 capacity risk reflects reality, and decide whether STORY-2/3 need to slip to keep the sprint goal achievable if PR #8 isn't merged by Wednesday.
- Ongoing: Monitor PR #8 and PR #9 for merge. Once STORY-13 merges, confirm Engineer picks up STORY-2 immediately.

### Engineer
- **Today (2026-06-16) — CRITICAL PATH, single remaining item on PR #8:** STORY-15, 16, 17, 20 are done and verified — no action needed on those. **STORY-18 needs a second pass** on branch `agent/engineer/scaffold-fastapi`:
  - Full findings + verified version-compatibility chain are posted on GitHub issue #24 (Prod Support, 2026-06-16) — read that comment before starting, it already did the PyPI metadata legwork.
  - Apply the coordinated bump in `backend/requirements.txt`: `fastapi==0.137.1` (was 0.115.0), `pydantic>=2.9.0` (was 2.7.4), `python-multipart==0.0.31` (was 0.0.27).
  - Run `pip-audit -r backend/requirements.txt` — confirm zero CVEs for starlette, python-multipart, fastapi.
  - Run `pytest tests/ -v --cov=app` — all 27 existing tests must still pass. The pydantic 2.7.4 → 2.9.0 bump may change validation error shapes/messages — check `test_security_fixes.py` and `test_scaffold.py` assertions that match on error text, fix if needed.
  - Push to `agent/engineer/scaffold-fastapi`, update engineer.md with results. This is the only thing blocking PR #8 from merging.
- After PR #8 merges: pick up STORY-2 on branch `agent/engineer/unit-tests-betfair`.

### QA
- **Today (2026-06-16):** Standby until Engineer pushes the STORY-18 dependency bump (fastapi 0.137.1 / pydantic ≥2.9.0 / python-multipart 0.0.31) to `agent/engineer/scaffold-fastapi`. Once pushed:
  - Run `pytest tests/ -v --cov=app --cov-report=term-missing` — confirm all 27 tests still pass under the new pydantic/fastapi versions.
  - Specifically check validation-error-shape assertions in `test_security_fixes.py` and `test_scaffold.py` for breakage from the pydantic 2.9 bump.
  - Update qa.md with results; re-post LGTM on PR #8 or flag new issues.
- When STORY-13 merges: immediately start STORY-4 integration tests on branch `agent/qa/integration-tests-odds`.

### DevOps
- **Today (2026-06-16):** STORY-1 and STORY-19 are both code-complete on PR #9 and already have QA LGTM — no further changes needed on the branch. **Action:** monitor PR #8; as soon as it merges to main, merge PR #9 immediately (merge order: PR #8 → PR #9, since the CI backend job needs `backend/` to exist on main). No code changes required from you today unless PR #8's STORY-18 fix touches anything DevOps owns (it doesn't).

### AppSec
- **Today (2026-06-16):** Standby until Engineer pushes the STORY-18 dependency bump to `agent/engineer/scaffold-fastapi`. Once pushed:
  - Re-run `pip-audit -r backend/requirements.txt` — confirm zero CVEs across starlette, python-multipart, fastapi, pydantic.
  - Re-run `bandit -r backend/app/` — confirm only the known B106 false positive remains.
  - If clean: remove DO NOT MERGE from PR #8, post final approval, close issue #24.
  - Update appsec.md with new scan results and the resolution of #24.

### Prod Support
- ✅ 2026-06-16 (this morning): Triaged 11 open issues (none stale), closed duplicate #25, re-ran pip-audit on PR #8 branch and found the STORY-18 fix is insufficient (11 CVEs now, not 3) — posted verified coordinated-bump fix path on issue #24 for Engineer to pick up.
- **Today, remaining:** Monitor PR #8 for the Engineer's STORY-18 follow-up commit. Re-run `pip-audit` once pushed to sanity-check before AppSec's formal re-scan. Update prod-support.md with results. No further new investigation needed today — the blocker is fully diagnosed and hand-off is complete.

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
