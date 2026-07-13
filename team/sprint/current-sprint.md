# Sprint 3 — Scheduler, Persistence Restore & Frontend Auth

**Start:** 2026-07-13 (Monday)  
**End:** 2026-07-24 (Friday)  
**Goal:** Land Sprint 2 carry-over merges (Day 1), implement Betfair/Odds API schedulers, restore DB persistence layer, and ship frontend login.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-7: Rate limit guard to OddsApiService | Engineer | [#52](https://github.com/cmdperogi/OddToBelieve/pull/52) | **QA LGTM ✅ — AppSec CLEAR ✅ (2026-07-09) — DevOps OVERDUE (missed 2026-07-10 deadline, now Sprint 3 Day 1)** | All gates clear since 2026-07-09. DevOps must merge TODAY. |
| STORY-14: Scaffold React/Vite frontend | Engineer | [#53](https://github.com/cmdperogi/OddToBelieve/pull/53) | **QA LGTM ✅ — AppSec CLEAR ✅ (2026-07-09) — DevOps OVERDUE (missed 2026-07-10 deadline, now Sprint 3 Day 1)** | All gates clear since 2026-07-09. DevOps must merge TODAY after PR #52. |
| STORY-21a: APScheduler Betfair polling job | Engineer | — | **Sprint 3 Day 1 — Engineer to start TODAY** | Branch: `agent/engineer/betfair-scheduler`. Depends on STORY-2 ✅, STORY-3 ✅. |
| STORY-24: Fix datetime.utcnow() deprecation | Engineer | — | **Sprint 3 Day 1 — Engineer to bundle with STORY-21a or open as quick standalone PR** | XS estimate. Two files: `auth.py:21`, `db/models.py:47`. |

### To Do

| Story | Owner | Blocked Until | Notes |
|-------|-------|---------------|-------|
| STORY-25: Restore OddsApiService DB persistence | Engineer | STORY-7 merges | Start Day 2. Rebuild `_persist()` + `db` param. Ref: commit `2ed2ce2` on STORY-3 branch. |
| STORY-22: Frontend login page + JWT management | Engineer | STORY-14 merges | Start Day 2. JWT in React context (in-memory only, never localStorage). |
| STORY-21b: APScheduler Odds API polling job | Engineer | STORY-21a + STORY-7 + STORY-25 | Day 3–4 at earliest. `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min. |

### Done (Sprint 3)

*(none yet — Sprint 3 started today)*

---

### Done (Sprint 2)

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-10: Add /health endpoint | [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) | ✅ 2026-07-08T09:07Z | 60/60 tests passing on main post-merge. All 5 STORY-10 ACs verified. Issue #38 closed. |
| STORY-11: Add structured logging | [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) | ✅ 2026-07-08T09:09Z | 60/60 tests. All STORY-11 ACs verified. Rebase required on merge (main.py import conflict). Issue #39 closed. |
| STORY-3: Implement OddsApiService + unit tests (TDD) | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | ✅ 2026-07-03T20:51:59Z | 62/62 tests, 91% coverage. AppSec CLEAR. Issue #4 closed. |
| STORY-4: Integration tests /odds/* endpoints | [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) | ✅ 2026-07-03T20:52:07Z | All gates. Issue #5 closed. **Known issue: PR #31 merge dropped `_persist()` from main (tracked in STORY-25).** |

---

### Done (Sprint 1 — reference)

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | ✅ 2026-06-23 | 40/40 tests, 100% coverage. |
| STORY-13: Scaffold FastAPI backend | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | ✅ 2026-06-20 | Security baseline established. |
| STORY-1: GitHub Actions CI pipeline | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | ✅ 2026-06-20 | CI active on main. |
| STORY-19: Migrate CI credential-shaped env vars to secrets | #9 | ✅ 2026-06-20 | |
| STORY-5: AppSec baseline scan | — | ✅ 2026-06-20 | Bandit: B106 FP only. pip-audit: 0 CVEs. |
| STORY-15–18, 20: Security fixes | #8 | ✅ 2026-06-20 | All credential/CVE fixes resolved. |

---

### Blocked

| Agent | Story | Days Blocked | Reason |
|-------|-------|-------------|--------|
| **DevOps** | STORY-7 (PR #52) + STORY-14 (PR #53) | **4 days (since 2026-07-09 gates cleared)** | All gates cleared 2026-07-09. Merge was due 2026-07-10 (Sprint 2 final day). Not merged. Sprint 3 Day 1 — **DevOps must merge both PRs TODAY.** |

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-07-13 (Monday, Sprint 3 Day 1 of 10)

### Scrum Master
- ✅ 2026-07-13: Sprint 3 Day 1. Transitioned board to Sprint 3. DevOps BLOCKED (missed Sprint 2 merge deadline — 4 days since gates cleared). STORY-7 and STORY-14 carry over as P1. Sprint 3 planning confirmed (PO completed 2026-07-13). Daily assignments issued for all agents. Sprint 3 scope: STORY-21a (Day 1), STORY-24 (Day 1), STORY-25 (Day 2, after STORY-7), STORY-22 (Day 2, after STORY-14), STORY-21b (Day 3-4, after 21a+7+25).

### DevOps
- **TODAY (2026-07-13) — BLOCKED / CRITICAL:** PRs #52 and #53 have been merge-ready since 2026-07-09 (QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅). The Sprint 2 merge deadline (2026-07-10) was missed. These are the **#1 priority for Sprint 3 Day 1.**
  1. **Merge PR #52 (STORY-7, branch `agent/engineer/rate-limit-guard`) into main.** Expect ~75 tests post-merge. Confirm `app/services/odds_api.py` coverage recovers to 100%.
  2. **Merge PR #53 (STORY-14, branch `agent/engineer/frontend-scaffold`) into main immediately after PR #52.** Frontend-only — frontend CI steps activate (`npm run build`, `npm run lint`). Confirm frontend CI passes.
  3. Merge order: PR #52 → PR #53. No rebase expected (both branches were CI-verified 2026-07-09).
  4. After merges: close issues #40 (STORY-7) and #7 (STORY-14).
  5. **Update `team/agents/devops.md`** with merge results, post-merge CI run number, and test count.

### Engineer
- **TODAY (2026-07-13) — Sprint 3 Day 1:**
  1. **Start STORY-21a (APScheduler — Betfair polling job).** Branch: `agent/engineer/betfair-scheduler`. Implement: APScheduler job registered at `BETFAIR_POLL_INTERVAL_MINUTES` (default: 60 min); `BetfairClient` singleton (not a new instance per cycle); `Event`/`Market`/`Odds` upsert with `source="betfair"`, upsert key `(source_id, source)`; `Odds` rows deleted before new ones inserted per event (refresh pattern); empty-list case logs INFO with count 0; auth failure logs ERROR (no credentials) and scheduler continues. All tests mock `BetfairClient` — zero real API calls.
  2. **Bundle STORY-24 (datetime.utcnow fix)** — open as a separate XS PR or commit on the same STORY-21a branch if clean. Two files only: `auth.py:21` → `datetime.now(timezone.utc)`, `db/models.py:47` → `lambda: datetime.now(timezone.utc)`. Run `python -W error::DeprecationWarning -m pytest tests/` to verify no DeprecationWarnings.
  3. **After STORY-7 (PR #52) merges:** Start STORY-25 (restore `OddsApiService._persist()` + `db: Session | None = None` parameter). Reference implementation: commit `2ed2ce2` on branch `agent/engineer/unit-tests-oddsapi`. Build on top of the merged PR #52 code (which includes rate guard singleton).
  4. **Update `team/agents/engineer.md`** with Sprint 3 Day 1 status.

### QA
- **TODAY (2026-07-13) — Sprint 3 Day 1:**
  1. **Post-merge verification (after DevOps merges PR #52):** Confirm main test count reaches ~75 tests. Verify `app/services/odds_api.py` is at 100% coverage (recovery from the orphaned PR #28 merge). Run `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`.
  2. **Post-merge verification (after DevOps merges PR #53):** Confirm frontend CI passes (`npm run build`, `npm run lint`). Verify `src/components/.gitkeep` and `src/hooks/.gitkeep` are present on main.
  3. **Review queue prep:** STORY-21a and STORY-24 PRs expected from Engineer today/tomorrow — review as soon as opened. STORY-25 PR expected Day 2.
  4. **Update `team/agents/qa.md`** with Sprint 3 Day 1 coverage numbers after merges land.

### AppSec
- **TODAY (2026-07-13) — Sprint 3 Day 1:**
  1. **No new scans required today** — PRs #52 and #53 already have SECURITY CLEAR (2026-07-09). No code changes since then; standing CLEAR holds.
  2. **When Engineer opens STORY-21a PR:** Run `bandit -r backend/app/` and `pip-audit -r backend/requirements.txt` against the branch. Key items to check: scheduler credentials never in logs, `BetfairClient` session token never logged, no new runtime dependencies that introduce CVEs.
  3. **When Engineer opens STORY-24 PR:** Quick scan — no new code paths introduced (two-line fix). Verify no credential changes.
  4. **Monitor issue #54** (ecdsa 0.19.2 PYSEC-2026-1325, LOW, no upstream fix). Re-check at each Sprint 3 scan cycle.
  5. **Update `team/agents/appsec.md`** confirming Sprint 3 scan readiness.

### Product Owner
- **TODAY (2026-07-13) — Sprint 3 Day 1 (COMPLETE):**
  - Sprint 3 planning complete (decisions D30–D35 in `team/agents/product-owner.md`, 2026-07-13).
  - STORY-25 added as prerequisite for STORY-21b (D31). STORY-6 descoped to CI gate only (D30). STORY-21b dependency chain updated (D32). Sprint 3 scope confirmed as 7 stories (D33). Issue #54 not a Sprint 3 blocker (D34). ACs improved for top 5 stories (D35).
  - **Action:** Confirm STORY-25 GitHub issue is created (creation blocked by REST API in previous sessions — must be done manually or via DevOps/Prod Support with API access).
  - Monitor Sprint 3 progress; flag any scope changes.

### Prod Support
- **TODAY (2026-07-13) — Sprint 3 Day 1 (triage overdue since 2026-07-03):**
  1. **After DevOps merges PR #52 and PR #53:** Close GitHub issues #40 (STORY-7) and #7 (STORY-14). Verify `story` label on both PRs.
  2. **GitHub issue #54** (ecdsa CVE) — verify it is open and labeled correctly.
  3. **Create GitHub issue for STORY-25** if API access available this session (issue title: `[STORY-25] Restore OddsApiService DB persistence layer`; label: `story`; link to PO decision D31).
  4. **Code audit on main** after PR #52 merges: confirm `GET /odds/api-status` is JWT-protected; rate-limit guard logs only request count; no credentials in log output. After PR #53 merges: confirm no hardcoded URLs in `frontend/src/`.
  5. **Git log audit** — verify no code pushed directly to main since 2026-07-03.
  6. **Update `team/agents/prod-support.md`** with Sprint 3 Day 1 triage summary.

---

### (Previous day assignments — 2026-07-10 — archived)
- DevOps: ❌ FAILED TO ACT — PRs #52 and #53 not merged on final sprint day. Both had all gates clear. Sprint 2 closes at 4/6 stories Done.
- AppSec: ✅ Acted 2026-07-09 — SECURITY CLEAR on PRs #52 and #53. Issue #54 opened. No action needed today.
- QA: ✅ LGTMs on PRs #52 and #53 held. No new commits on either branch.
- Engineer: ✅ No code action required. Sprint 3 prep.
- Product Owner: ✅ Completed Sprint 3 planning (2026-07-13).
- Prod Support: ⚠️ Still pending triage since 2026-07-03 (10 days).

---

## Merge Order (Sprint 3)

1. **PR #52 (STORY-7) — DevOps merges TODAY** (overdue from Sprint 2). Expect ~75 tests. QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅.
2. **PR #53 (STORY-14) — DevOps merges TODAY, after PR #52.** Frontend-only. QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅. Frontend CI activates.
3. **STORY-24 PR** (Engineer Day 1) — Two-file fix; QA review + AppSec scan same day.
4. **STORY-21a PR** (Engineer Day 1–2) — Betfair scheduler; full gate cycle.
5. **STORY-25 PR** (Engineer Day 2, after STORY-7 merges) — Restore `_persist()`; must build on PR #52 base.
6. **STORY-22 PR** (Engineer Day 2+, after STORY-14 merges) — Frontend login.
7. **STORY-21b PR** (Engineer Day 3–4, after STORY-21a + STORY-7 + STORY-25 merge) — Odds API scheduler.

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — `ODDS_API_POLL_INTERVAL_MINUTES` must default to **360 min** (PO D9/D17). Do not lower without PO sign-off.
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened (or, for DevOps as merge operator: 2+ days with no merge action after all gates are clear)
- **⚠️ DB persistence regression (Sprint 3 critical):** PR #28 merge commit `c5fa096` is orphaned from current main ancestry — `_persist()` method, `db` parameter in `fetch()`, and 22 OddsApiService unit tests are absent from main. `odds_api.py` coverage is 0% until PR #52 (STORY-7) merges (then recovers to 100%); full persistence requires STORY-25 (Sprint 3).
- **⚠️ Process violations from Sprint 2 (documented in retrospective):**
  1. PRs #47/#48 merged by DevOps without prior QA LGTM — QA gate must precede DevOps merge (no exceptions)
  2. DevOps missed Sprint 2 final-day merge deadline on PRs #52/#53 — both PRs now carry to Sprint 3

---

## Sprint Health

| Metric | Value |
|--------|-------|
| Sprint | 3 |
| Sprint Start | 2026-07-13 |
| Sprint End | 2026-07-24 |
| Stories In Progress | 4 (STORY-7 PR #52 overdue DevOps merge; STORY-14 PR #53 overdue DevOps merge; STORY-21a Engineer Day 1; STORY-24 Engineer Day 1) |
| Stories To Do | 3 (STORY-25, STORY-22, STORY-21b — unblocked on prior merges) |
| Stories Done (Sprint 3) | 0 |
| Stories Total (Sprint 3) | 7 |
| Days Remaining | 10 (Sprint 3 ends 2026-07-24) |
| Open PRs | 2 (#52 STORY-7 overdue DevOps; #53 STORY-14 overdue DevOps) |
| BLOCKED agents | 1 (DevOps — 4 days since gates cleared on PRs #52/#53; missed Sprint 2 merge deadline) |
| Sprint risk | HIGH — Sprint 3 Day 1 and DevOps still has not merged carry-over PRs. Every day of further DevOps delay compresses the window for STORY-25 and STORY-21b (which depend on STORY-7 landing). |
