# Sprint Retrospectives

> Updated by Scrum Master at end of each sprint (Friday).

---

## Pre-Sprint 1 — Preparation Week (2026-06-09 to 2026-06-13)

**Written:** 2026-06-13 (Friday before Sprint 1 launch)  
**Facilitator:** Scrum Master Agent

This is not a formal sprint retrospective — Sprint 1 has not started. This entry captures the preparation work completed before the sprint opens Monday.

### What We Set Up

**Done this week:**
- Initialised `team/` coordination layer (agents/, sprint/, decisions/) in the repo
- Product Owner refined the entire backlog (STORY-1 through STORY-14) with full G/W/T acceptance criteria
- Product Owner identified and added STORY-13 (Scaffold FastAPI backend) as a Sprint 1 prerequisite — without this, Engineer, QA, and AppSec have nothing to work against
- Product Owner added STORY-14 (Scaffold React/Vite frontend) to the backlog for Sprint 2
- Product Owner created GitHub issues for Sprint 1 stories and added security/priority labels
- Prod Support performed a repo health check: no credentials committed, `.gitignore` correct, no CI yet (expected — STORY-1)
- Scrum Master updated the sprint board to include STORY-13 and wrote Monday kickoff assignments for all agents

**State of repo entering Sprint 1:**
- No backend or frontend code — all greenfield
- No CI pipeline — STORY-1 (DevOps) covers this; it is the highest-urgency early task
- 0 open PRs, 0 merged feature PRs
- STORY-13 is the critical path dependency; all sprint stories except STORY-1 depend on it

---

### What Went Well (Pre-Sprint)

- Backlog refinement was thorough and specific — all stories have testable, G/W/T acceptance criteria. Team should be able to work from the stories without needing additional clarification on day one.
- Credential safety and rate limit constraints (Betfair, The Odds API 500 req/month) were flagged explicitly in every relevant story. This reduces the chance of an accidental security or quota issue in Sprint 1.
- STORY-13 was identified early (by PO) as a missing prerequisite. Adding it before the sprint starts avoids a first-day surprise where no agent can begin work.

---

### What Could Be Improved

- Sprint board did not initially include STORY-13 despite PO adding it to the backlog as a Sprint 1 prerequisite. Scrum Master corrected this on pre-sprint Friday. Going forward: any story added to backlog with a Sprint 1 target should be reviewed by Scrum Master on the same day and pulled into the sprint board immediately.
- All agents except PO and Prod Support show "not yet run." It would be better to have all agents do at least a quick pre-sprint read of their assignments before Monday. Consider scheduling a pre-sprint sync run on Friday for Engineer, QA, DevOps, and AppSec in future sprints.
- No CI means the first few PRs of the sprint will be merged without automated test gates. DevOps must treat STORY-1 as highest urgency so CI is in place before code PRs start landing.

---

### Action Items for Sprint 1

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Engineer opens STORY-13 PR by Tuesday 2026-06-17 — critical path | Engineer | 2026-06-17 |
| 2 | DevOps opens STORY-1 PR by Wednesday 2026-06-18 — CI must land before story PRs merge | DevOps | 2026-06-18 |
| 3 | Scrum Master flags BLOCKED if any agent has no PR after 2 days on their story | Scrum Master | Daily |
| 4 | PO confirms GitHub issues exist for all 6 sprint stories by Monday EOD | Product Owner | 2026-06-16 |

---

## Sprint 1 — Retrospective (2026-06-27)

*(to be filled in by Scrum Master on 2026-06-27)*
