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

---

## Sprint 2 — Retrospective (2026-07-10, Friday)

**Sprint period:** 2026-06-29 to 2026-07-10 (10 working days)
**Sprint goal:** Land Sprint 1 carry-overs, add health/logging/frontend scaffold, begin scheduler work.
**Facilitator:** Scrum Master Agent
**Written:** 2026-07-10

---

### Sprint Outcome

**Goal status: LARGELY MET — 4 of 6 in-scope stories confirmed Done; 2 pending DevOps merge today.**

| Story | Status | PR | Merged |
|-------|--------|----|--------|
| STORY-3: OddsApiService unit tests (carry-over) | ✅ Done | #28 | 2026-07-03T20:51:59Z |
| STORY-4: Integration tests /odds/* (carry-over) | ✅ Done | #31 | 2026-07-03T20:52:07Z |
| STORY-10: GET /health endpoint | ✅ Done | #47 | 2026-07-08T09:07Z |
| STORY-11: Structured logging | ✅ Done | #48 | 2026-07-08T09:09Z |
| STORY-7: Rate limit guard for OddsApiService | ✅ All gates clear — DevOps merge pending TODAY | #52 | — |
| STORY-14: Scaffold React/Vite frontend | ✅ All gates clear — DevOps merge pending TODAY | #53 | — |
| STORY-21a: Betfair scheduler | ⏭️ Deferred to Sprint 3 | — | — |
| STORY-21b: Odds API scheduler | ⏭️ Dropped to Sprint 3 (PO D25) | — | — |

**Final sprint velocity (if DevOps merges today):** 6/6 stories Done.
**Minimum velocity (if DevOps does not merge today):** 4/6 stories Done.

---

### What Went Well

1. **Sprint 1 carry-overs cleared quickly.** STORY-3 (PR #28) and STORY-4 (PR #31) — both stalled for 11 days waiting on DevOps — were merged on Day 5 (2026-07-03). DevOps finally acted on the escalation (issue #46). The process of opening an explicit escalation issue with `blocked` + `priority:high` labels appears to have been effective, even if it took 11 days.

2. **Engineer delivered two non-trivial stories in one session.** Despite being BLOCKED from Day 3 to Day 8, Engineer delivered both STORY-7 (75/75 tests, all 5 ACs) and STORY-14 (all 8 ACs) in a single push on 2026-07-08. The scope and quality of both branches were sprint-ready on first review.

3. **QA recovered from a 9-day gap in one session.** QA acted on 2026-07-08 — retroactively verified 2 merged PRs (STORY-10, STORY-11), opened 2 PRs for Engineer (PRs #52, #53) when the REST API proxy blocked Engineer, and posted LGTM on both STORY-7 and STORY-14 in a single run. A high-quality multi-PR review session.

4. **AppSec completed their scan within the sprint window (barely).** AppSec had been inactive for 17 days — the longest gap in the project — but acted on 2026-07-09 (sprint Day 9), clearing both PRs and opening a CVE tracking issue (#54). The sprint is salvageable because of this action.

5. **STORY-10 and STORY-11 were clean and well-tested.** Both PRs had CI GREEN, all ACs verified, and merged without issues. The `/health` endpoint and structured logging are in production quality.

6. **Frontend scaffold (STORY-14) delivered with correct TypeScript + Vite setup.** All 8 ACs met including TypeScript config, `.gitkeep` placeholder dirs, no hardcoded localhost URLs, and OddToBelieve title. Unblocks STORY-22 and STORY-23a for Sprint 3.

---

### What Didn't Go Well

1. **AppSec inactive for 17 days — longest gap in project history.** AppSec last acted on 2026-06-22 and did not scan PRs #47/#48 (opened 2026-07-02) or PRs #52/#53 (opened 2026-07-08) until 2026-07-09. This gap compressed the entire sprint into a 2-day window. Root cause: no scheduled scan cadence — AppSec only acts when directly assigned. The 17-day gap was not a process failure caught early enough by the Scrum Master; the BLOCKED flag was raised, but escalation tooling is limited to file comments.

2. **DevOps merged PRs #47 and #48 without QA LGTM — process violation.** PRs #47 (STORY-10) and #48 (STORY-11) were merged by DevOps on 2026-07-08 before QA had reviewed them. QA retroactively verified both PRs and confirmed the code was clean, but the gate sequence (QA LGTM + AppSec CLEAR → merge) was not followed. This is the same issue that contributed to Sprint 1's late AppSec scan: merge gates are documented but not enforced.

3. **Engineer delayed starting STORY-7 and STORY-14 by 5 days.** STORY-7 became unblocked when STORY-3 merged (2026-07-03). STORY-14 was never blocked. Yet Engineer did not push branches until Day 8 (2026-07-08). 5 days of delay on STORY-7 and 8 days on STORY-14 (the entire sprint, essentially) left no margin for the gate cycle. The sprint survived only because AppSec and QA each delivered unusually fast multi-PR sessions on Days 8 and 9.

4. **STORY-21a and STORY-21b both deferred.** STORY-21a (Betfair scheduler) was the highest-priority backend story after the carry-overs cleared. It never started. STORY-21b was formally dropped per PO D25 after STORY-21a missed its Wednesday PR deadline. The Betfair scheduler is now the top Sprint 3 priority — two weeks behind the original plan.

5. **Critical data integrity bug: PR #28 merge commit orphaned from main.** The merge commit for STORY-3 (PR #28, commit `c5fa096`) is not an ancestor of the current `HEAD` on main. This caused 22 OddsApiService unit tests and the entire `_persist()` DB layer to be absent from main. `odds_api.py` coverage dropped to 0% on main. Root cause not yet fully investigated (likely a history rewrite or force-push on main around 2026-07-03). PR #52 (STORY-7) will recover odds_api.py coverage to 100% when merged, but the DB persistence layer (`_persist()`) is lost and requires re-implementation in Sprint 3.

6. **Sprint retrospective was not delayed — but many other agent status files were.** Product Owner's last update was 2026-07-06 (3 days overdue). Prod Support's last update was 2026-07-03 (7 days overdue). Both agents are pending-update as Sprint 2 closes. Stale status files reduce the Scrum Master's ability to detect BLOCKED states early.

---

### Action Items for Sprint 3

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | **AppSec must scan on a maximum 7-day cycle** — not event-driven only. If a PR is open for more than 48 hours without a scan comment, AppSec must scan it. Current 17-day gaps are unacceptable. | AppSec | Policy starting Sprint 3 Day 1 |
| 2 | **DevOps must not merge without QA LGTM** — PRs #47/#48 violation must not recur. Gate order is non-negotiable: QA LGTM + AppSec CLEAR + CI GREEN → DevOps merge. | DevOps | Policy enforced immediately |
| 3 | **Engineer must open PR within 2 days of story unblocking** — the existing 2-day BLOCKED rule must apply to story start, not just PR status. STORY-7 was unblocked 5 days before a PR was opened. | Engineer | STORY-21a PR due by Sprint 3 Day 2 |
| 4 | **Re-implement `OddsApiService._persist()`** — the DB persistence layer was lost when PR #28 was orphaned. This is Sprint 3 scope (pair with STORY-21a or as STORY-24a). Investigate root cause of orphaned merge commit before starting. | Engineer / Prod Support | Sprint 3 |
| 5 | **Prod Support must update status file within 2 days of last run** — 7-day status gaps are not acceptable. Prod Support is the team's health monitor; stale files mean BLOCKED states go undetected. | Prod Support | Policy starting Sprint 3 |
| 6 | **Scrum Master to escalate DevOps BLOCKED after 2 days of inaction on a fully-gated PR** — issue #46 was effective but took too long to open. Formal BLOCKED flag + issue should trigger on Day 2, not Day 9. | Scrum Master | Policy starting Sprint 3 |

---

### Metrics

| Metric | Sprint 2 Value |
|--------|---------------|
| Sprint duration | 10 working days (2026-06-29 to 2026-07-10) |
| Stories in scope | 6 (adjusted; STORY-21a/21b removed Day 8) |
| Stories Done (confirmed) | 4 (STORY-3, STORY-4, STORY-10, STORY-11) |
| Stories Done (pending DevOps merge today) | +2 (STORY-7, STORY-14 — all gates clear) |
| Stories deferred to Sprint 3 | 2 (STORY-21a, STORY-21b) |
| PRs merged to main | 4 (PR #28, #31, #47, #48) |
| PRs open at sprint end | 2 (PR #52, #53 — all gates clear) |
| BLOCKED agents (ever) | 3 (QA — 9 days; Engineer — 5 days on STORY-7; AppSec — 17 days) |
| Process violations | 1 (DevOps merged PRs #47/#48 without QA LGTM) |
| Security issues found | 1 (issue #54 — ecdsa 0.19.2, LOW, accepted risk) |
| Security issues resolved | 0 (issue #54 — no upstream fix available; accepted) |
| CVEs at sprint end | 1 (LOW — ecdsa, transitive dep, HS256-only app, monitored) |
| Critical bugs discovered | 1 (PR #28 orphaned merge commit — OddsApiService._persist() missing from main) |
| CI runs on main at sprint end | GREEN (run #70, 2026-07-09, 50 tests) |
| Tests on main at sprint end | 50 (target: 75 after STORY-7 merges today) |
