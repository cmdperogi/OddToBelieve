# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress
*(none yet — sprint starts Monday)*

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-1: GitHub Actions CI | DevOps | TODO | |
| STORY-2: Unit tests BetfairClient | Engineer + QA | TODO | |
| STORY-3: Unit tests OddsApiService | Engineer + QA | TODO | |
| STORY-4: Integration tests /odds/* | QA | TODO | |
| STORY-5: AppSec baseline scan | AppSec | TODO | |

### Done
*(none yet)*

### Blocked
*(none)*

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.

### Scrum Master
- Initialize team/ directory in repo ✓
- Monday: run sprint planning, confirm story assignments above
- Daily: read all agent status files, update this board, flag blockers

### Product Owner
- Monday: create GitHub issues for STORY-1 through STORY-5
- Ongoing: refine backlog, add acceptance criteria to STORY-6+

### Engineer
- Pick up STORY-2 (BetfairClient unit tests) — create branch `agent/engineer/unit-tests-betfair`
- After STORY-2 merged: pick up STORY-3

### QA
- Review any open PRs from Engineer
- After Engineer opens STORY-2 PR: review and approve or request changes
- Independently: write integration tests (STORY-4) on branch `agent/qa/integration-tests-odds`

### DevOps
- Pick up STORY-1: create `.github/workflows/ci.yml` on branch `agent/devops/github-actions-ci`

### AppSec
- Pick up STORY-5: run Bandit + pip-audit, open GitHub issues for findings

### Prod Support
- Triage any open GitHub issues
- Check for blockers in team/agents/ status files
- Morning: report on repo health in team/agents/prod-support.md

---

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests
