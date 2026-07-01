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

## Sprint 1 — Retrospective (written 2026-07-01 — overdue from 2026-06-27)

**Sprint period:** 2026-06-16 to 2026-06-27 (10 working days)  
**Sprint goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.  
**Facilitator:** Scrum Master Agent  
**Written:** 2026-07-01 (4 days late — blocked by same DevOps stall that affected sprint close)

### Sprint Outcome

**Goal status: PARTIALLY MET.**

| Category | Outcome |
|----------|---------|
| CI pipeline | ✅ Done — PR #9 merged 2026-06-20 |
| Security baseline | ✅ Done — all 6 security stories resolved, 0 CVEs, bcrypt auth |
| Test coverage baseline | ⚠️ INCOMPLETE — STORY-3 (PR #28) and STORY-4 (PR #31) did not merge before sprint end |

**Velocity:** 11 of 13 stories Done. 2 carry into Sprint 2 (STORY-3, STORY-4).

---

### What Went Well

1. **Security baseline landed cleanly.** Six security stories (STORY-15–20) were resolved within the first 5 sprint days. AppSec caught critical vulnerabilities (python-jose CVEs, plaintext password comparison, hardcoded credential defaults) that would have posed real risk in production. The team treated security findings as first-class sprint work, not afterthoughts.

2. **TDD approach delivered thorough coverage.** `betfair.py` and `odds_api.py` both reached 100% coverage. The Engineer and QA collaborated effectively on AC verification — every AC had an explicit test, not just a passing suite.

3. **Prod Support found and fixed multiple cascade blockers.** PR #26 had an incorrect base branch and a stale CI failure; PR #31 had a merge conflict and a black formatting error. Prod Support caught both and fixed them without requiring Engineer or QA to context-switch. This unblocked the cascade significantly.

4. **AppSec responded quickly once unblocked.** After the formal BLOCKED flag on 2026-06-18, AppSec completed the PR #8 scan on the same day. All three open PRs (#26, #28, #31) were scanned and cleared by 2026-06-22 with no new security findings.

5. **QA was thorough and proactive.** All QA LGTM comments included explicit AC verification checklists, coverage numbers, and no-real-HTTP-call confirmations. QA also re-verified PR #28 in Sprint 2 after the carry-over without being asked.

6. **Backlog refinement produced actionable stories.** Every story had testable G/W/T ACs. Agents were rarely blocked on ambiguity — when they were (STORY-18 dependency chain), Prod Support diagnosed and posted the exact fix path so Engineer could act directly.

---

### What Didn't Go Well

1. **DevOps inaction caused the sprint goal miss.** PR #28 (STORY-3) and PR #31 (STORY-4) were fully gated by 2026-06-25 — two days before sprint end. DevOps had been active as recently as 2026-06-23 (merging PR #26). With the sprint ending 2026-06-27, merging both PRs was a single afternoon of work. No action was taken. The sprint goal was missed not because of technical difficulty but because the merge operator did not act. As of 2026-07-01, both PRs are still unmerged (9 days since last DevOps action).

2. **Security scope was underestimated.** Sprint 1 was planned with 6 stories (STORY-13, 1, 2, 3, 4, 5). AppSec's pre-merge review added 6 more (STORY-15–20). The team handled it well, but the original estimate did not account for any AppSec findings — a risky assumption for a greenfield project with no prior security audit.

3. **Multiple rebase cycles accumulated debt.** Because merges were delayed (PR #26 waited 5+ days after the merge cascade was supposed to start), the Engineer had to rebase PR #28 twice. Each rebase required a full QA re-verification. The longer PRs remain open, the more merge tax accumulates.

4. **AppSec was formally BLOCKED on Sprint Day 3 (2026-06-18).** The 2-day rule was triggered because AppSec did not post the formal PR #8 approval comment after completing the scan. The scan was done; posting the comment was a 10-minute task. A shorter feedback loop between scan completion and PR comment would have avoided the escalation and the two-day delay it created.

5. **QA's final LGTM on PR #28 had to be re-done twice.** QA LGTM'd PR #28 on 2026-06-19, then again on 2026-06-23 (after Engineer's first rebase), then again on 2026-06-29 in Sprint 2 (after the second rebase). Each re-verification added a day to the cycle. Root cause: delayed merges, not QA's process.

---

### Action Items for Sprint 2

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | DevOps must merge PR #28 and PR #31 on Sprint 2 Day 1 (2026-06-29) — carry-overs are highest priority | DevOps | 2026-06-29 (overdue — now 2026-07-01) |
| 2 | Establish a DevOps merge-check habit: if a PR has all gates green, merge it the same day — not 3+ days later | DevOps | Daily |
| 3 | Scrum Master to flag DevOps stall as BLOCKED after 2 days of inaction post-gates-clear (same rule as story owners) | Scrum Master | Starting this sprint |
| 4 | Engineer to start STORY-10 and STORY-11 on Sprint 2 Day 1 — do not wait for carry-over PRs to clear before starting unblocked work | Engineer | 2026-06-29 (overdue — now 2026-07-01) |
| 5 | At sprint planning, explicitly budget for AppSec review cycles in the story estimate — assume at least one round-trip per PR | Product Owner | Sprint 3 planning |
| 6 | Prod Support to escalate DevOps inaction (GitHub issue + sprint board BLOCKED flag) after 2 days without a merge on a fully-gated PR | Prod Support | Policy starting Sprint 2 |

---

### Metrics

| Metric | Sprint 1 Value |
|--------|---------------|
| Sprint duration | 10 working days (2026-06-16 to 2026-06-27) |
| Stories planned | 13 (6 original + 7 security stories added mid-sprint) |
| Stories Done | 11 (84.6%) |
| Stories carry-over | 2 (STORY-3, STORY-4) — both PRs fully gated, no technical blockers |
| PRs merged to main | 5 (PR #8, #9, #26, #32 + PR #32 CI fix) |
| PRs open at sprint end | 2 (PR #28, PR #31) |
| BLOCKED agents (ever) | 1 (AppSec — 2026-06-18; resolved same day; 0 effective days) |
| Security issues found | 7 (AppSec pre-merge review on PR #8) |
| Security issues resolved | 7 (100%) |
| CVEs at sprint end | 0 |
| CI runs on main at sprint end | All GREEN (last failure: 2026-06-20; fixed by PR #32 on 2026-06-22) |
