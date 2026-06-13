# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress
*(sprint starts Monday 2026-06-16)*

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-13: Scaffold FastAPI backend | Engineer | TODO | ⚠️ Hard prerequisite — STORY-2, 3, 4, 5 all depend on this. Engineer starts here Monday. |
| STORY-1: GitHub Actions CI | DevOps | TODO | Can start in parallel with STORY-13 |
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | TODO | Blocked on STORY-13 |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | TODO | Blocked on STORY-13 |
| STORY-4: Integration tests /odds/* endpoints | QA | TODO | Blocked on STORY-13 |
| STORY-5: AppSec baseline scan | AppSec | TODO | Blocked on STORY-13 |

### Done
*(none yet — sprint starts Monday)*

### Blocked
*(none — sprint has not started)*

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.
> **Last updated:** 2026-06-13 (Friday, pre-sprint kickoff prep)

### Scrum Master
- ✅ 2026-06-13: Wrote pre-sprint retrospective; updated sprint board to include STORY-13; set Monday assignments
- Daily from Monday: read all agent status files, update board, flag blockers
- Friday 2026-06-27: write Sprint 1 retrospective

### Product Owner
- **Monday 2026-06-16:** Create GitHub issues for ALL Sprint 1 stories: STORY-13 (#1 already created per PO log), STORY-1 (#2), STORY-2 (#3), STORY-3 (#4), STORY-4 (#5), STORY-5 (#6). Confirm issues have `story` label and acceptance criteria linked.
- Ongoing: refine STORY-6 through STORY-12 in backlog; flag any story needing split before Sprint 2 planning

### Engineer
- **Monday 2026-06-16:** Start STORY-13 (Scaffold FastAPI backend) on branch `agent/engineer/scaffold-fastapi`. Create `backend/` with layout from CLAUDE.md: `app/`, `tests/unit/`, `tests/integration/`, `requirements.txt`. Server must start with `uvicorn app.main:app --reload` on port 8000 and GET /docs must load.
- After STORY-13 merged: pick up STORY-2 (BetfairClient TDD) on branch `agent/engineer/unit-tests-betfair`
- After STORY-2 merged: pick up STORY-3 (OddsApiService TDD) on branch `agent/engineer/unit-tests-odds-api`

### QA
- **Monday 2026-06-16:** Review STORY-13 acceptance criteria in backlog.md. Draft integration test plan for STORY-4 (/odds/* endpoints) — identify which fixtures and mocks will be needed once STORY-13 is merged.
- When Engineer opens STORY-13 PR: review against AC — verify `uvicorn` starts, `/docs` loads, `pytest tests/` runs without import errors, `ruff` is clean.
- When STORY-13 merges: start STORY-4 integration tests on branch `agent/qa/integration-tests-odds`
- When Engineer opens STORY-2 or STORY-3 PR: review and approve or request changes within the same sprint day

### DevOps
- **Monday 2026-06-16:** Start STORY-1 (GitHub Actions CI) on branch `agent/devops/github-actions-ci`. Create `.github/workflows/ci.yml`. CI must run backend lint (`ruff`) + `pytest`, and frontend lint (`npm run lint`) + `npm run build` on every PR. PRs must be blocked from merge on failure.
- STORY-1 can run in parallel with Engineer's STORY-13 — coordinate so CI workflow is ready before first feature PR lands.

### AppSec
- **Monday 2026-06-16:** Review STORY-5 AC in backlog.md. Prepare execution plan for Bandit + pip-audit. Document any known CVE risks in `team/agents/appsec.md`.
- When STORY-13 merges: immediately run STORY-5 — execute `bandit -r backend/app/` and `pip-audit -r backend/requirements.txt`. Record all findings in `team/agents/appsec.md`. Open a GitHub issue for each HIGH or CRITICAL finding.

### Prod Support
- **Monday 2026-06-16:** Triage GitHub issues created by PO; confirm `story` and priority labels are applied. Report on CI status (STORY-1 not yet merged — no CI yet; flag this risk in `team/agents/prod-support.md`).
- Daily: check `team/agents/` files for BLOCKED flags; escalate to Scrum Master comment in `team/agents/scrum-master.md`
- Watch for any direct pushes to `main` (policy violation) — all changes must go through PR

---

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
- STORY-13 is the critical path blocker: STORY-2, 3, 4, 5 cannot start until it merges
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened
