# Sprint 2 — Reliability & Frontend Foundation

**Start:** 2026-06-29 (Monday)  
**End:** 2026-07-10 (Friday)  
**Goal:** Land Sprint 1 carry-overs, add health/logging/frontend scaffold, begin scheduler work.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-7: Rate limit guard to OddsApiService | Engineer | [#52](https://github.com/cmdperogi/OddToBelieve/pull/52) | **QA LGTM ✅ — AppSec BLOCKED (17 days no scan). FINAL DAY — sprint ends tomorrow Friday.** | Branch pushed 2026-07-08. PR created by QA 2026-07-08. 75/75 tests passing. All 5 STORY-7 ACs implemented. QA LGTM posted (review ID 4653158516). AppSec scan is the only remaining gate. |
| STORY-14: Scaffold React/Vite frontend | Engineer | [#53](https://github.com/cmdperogi/OddToBelieve/pull/53) | **QA LGTM ✅ — AppSec BLOCKED (17 days no scan). FINAL DAY — sprint ends tomorrow Friday.** | Branch pushed 2026-07-08. PR created by QA 2026-07-08. QA fix applied (`.gitkeep` for `src/components/` and `src/hooks/`). QA LGTM posted (review ID 4653159452). Independent of backend — no dependency on STORY-7. |

### To Do

*(All stories cleared — STORY-7 and STORY-14 moved to In Progress; STORY-21a and STORY-21b deferred to Sprint 3.)*

### Done (Sprint 2)

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-10: Add /health endpoint | [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) | ✅ 2026-07-08T09:07Z | 60/60 tests passing on main post-merge. All 5 STORY-10 ACs verified. DevOps merged; QA retroactively confirmed LGTM (code verified clean). CI GREEN run #59. Issue #38 closed. |
| STORY-11: Add structured logging | [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) | ✅ 2026-07-08T09:09Z | 60/60 tests passing on main post-merge. All STORY-11 ACs verified. DevOps merged (rebase required due to conflict with #47 on main.py imports); QA retroactively confirmed LGTM. CI GREEN. Issue #39 closed. |
| STORY-3: Implement OddsApiService + unit tests (TDD) | [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | ✅ 2026-07-03T20:51:59Z | 62/62 tests passing, 91% coverage. AppSec CLEAR. Issue #4 closed. 11-day DevOps stall finally resolved. |
| STORY-4: Integration tests /odds/* endpoints | [#31](https://github.com/cmdperogi/OddToBelieve/pull/31) | ✅ 2026-07-03T20:52:07Z | 8 seconds after PR #28 per merge order. All gates: QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅. Issue #5 closed. |

---

### Done (Sprint 1 — carried forward for reference)

| Story | PR | Merged | Notes |
|-------|----|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | [#26](https://github.com/cmdperogi/OddToBelieve/pull/26) | ✅ 2026-06-23 | 40/40 tests passing; `betfair.py` 100% coverage. Issue #3 closed. |
| STORY-13: Scaffold FastAPI backend | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | ✅ 2026-06-20 | All security findings resolved. AppSec CLEAR. QA LGTM 31/31. |
| STORY-1: GitHub Actions CI pipeline | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | ✅ 2026-06-20 | CI now active on main. |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | #9 (same branch) | ✅ 2026-06-20 | All 5 credential-shaped vars use `${{ secrets.VAR \|\| 'fallback' }}`. |
| STORY-5: AppSec baseline scan | — | ✅ 2026-06-20 | Bandit: B106 false positive only. pip-audit: 0 CVEs. |
| STORY-15: Fix hardcoded credential defaults in config.py | #8 | ✅ 2026-06-20 | No plaintext defaults remain; `ValueError` on startup if env vars unset. |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | #8 | ✅ 2026-06-20 | `_pwd_context.verify()` in place. |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | #8 | ✅ 2026-06-20 | `python-jose[cryptography]>=3.4.0`, 0 CVEs. |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | #8 | ✅ 2026-06-20 | `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`. |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | #8 | ✅ 2026-06-20 | `pytest==9.0.3`, `black==26.3.1`. |
| CI Fix: Align ADMIN_PASSWORD fallback with test fixtures | [#32](https://github.com/cmdperogi/OddToBelieve/pull/32) | ✅ 2026-06-22 | One-line fix; CI GREEN since run 27941596842. |

### Blocked

| Agent | Task | Days Since Last Action | Reason |
|-------|------|------------------------|--------|
| **AppSec** | **Scan PR #52 (STORY-7) and PR #53 (STORY-14)** | **17 days (last active 2026-06-22)** | PRs #52 and #53 opened 2026-07-08 with QA LGTM. No AppSec scan posted. PRs cannot merge without SECURITY CLEAR. **FINAL DAY — sprint ends tomorrow (Friday 2026-07-10). Must act today.** |

> **QA UNBLOCKED** — QA acted on 2026-07-08: retroactively verified PRs #47 and #48 post-merge; reviewed PR #52 (STORY-7) LGTM; reviewed PR #53 (STORY-14) LGTM with fix. QA last active 2026-07-08.
> **Engineer UNBLOCKED** — Engineer acted on 2026-07-08: pushed `agent/engineer/rate-limit-guard` (STORY-7, 75/75 tests) and `agent/engineer/frontend-scaffold` (STORY-14, all 8 ACs). PRs created by QA (#52, #53) as Engineer was blocked by REST API proxy restriction.
> **DevOps active** — Merged PR #47 (STORY-10) and PR #48 (STORY-11) on 2026-07-08. Standing by to merge PRs #52 and #53 the moment AppSec CLEAR lands today.
> **Process note** — PRs #47 and #48 were merged by DevOps on 2026-07-08 without a prior QA review gate (QA retroactively verified post-merge). This is a process violation to address in the Sprint 2 retrospective (Friday).

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-07-09 (Thursday, Sprint 2 Day 9 of 10)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity; security stories added.
- ✅ 2026-06-16: Reconciled board against agent status files; sprint risk noted.
- ✅ 2026-06-17: Reviewed all agent/PR status. AppSec threshold noted.
- ✅ 2026-06-18: AppSec formally BLOCKED. Prod Support confirmed; issue #27 opened.
- ✅ 2026-06-19: AppSec BLOCKED lifted. Engineer opened PR #28. Sprint risk downgraded.
- ✅ 2026-06-22: PRs #8 and #9 merged. STORY-13, 1, 19, 5 moved to Done.
- ✅ 2026-06-23: PR #32 merged (CI GREEN). PR #26 merged (STORY-2 DONE).
- ✅ 2026-06-26: PR #28 rebase complete (2026-06-25). Sprint risk HIGH — sprint ends TOMORROW.
- ✅ 2026-07-01: Sprint 2 Day 3. Transitioned board to Sprint 2. DevOps BLOCKED (9 days inactive). Overdue Sprint 1 retrospective written. Daily assignments issued.
- ✅ 2026-07-06: Sprint 2 Day 6. STORY-3 (PR #28) and STORY-4 (PR #31) moved to Done (merged 2026-07-03). PR #47 (STORY-10) and PR #48 (STORY-11) added to In Progress. QA BLOCKED (4 days, PRs #47/#48 unreviewed). AppSec BLOCKED (14 days, PRs #47/#48 unscanned). Engineer BLOCKED (STORY-7/21a/14 unstarted). DevOps BLOCKED status resolved. Daily assignments issued.
- ✅ 2026-07-08: Sprint 2 Day 8. No new PRs opened by Engineer since Day 6. QA still BLOCKED (9 days inactive). AppSec still BLOCKED (16 days inactive). STORY-21b officially dropped to Sprint 3 per PO D25 (no STORY-21a PR by EOD Wednesday). STORY-14 missed Tuesday deadline (PO D28). 2 days remain. Sprint 2 is CRITICAL — STORY-10 and STORY-11 are the only realistic completions. Daily assignments issued.
- ✅ 2026-07-09: Sprint 2 Day 9. STORY-10 (PR #47) and STORY-11 (PR #48) MERGED 2026-07-08 — moved to Done. Engineer pushed STORY-7 and STORY-14 branches 2026-07-08. QA created PRs #52 (#STORY-7) and #53 (STORY-14) and posted LGTM on both. AppSec remains BLOCKED (17 days, last active 2026-06-22) — sole gate on PRs #52 and #53. Sprint ends TOMORROW. Daily assignments issued.
- **Tomorrow (2026-07-10, Friday): Write Sprint 2 retrospective in `/repo/team/sprint/retrospective.md`.**

### AppSec
- **Today (2026-07-09) — BLOCKED: 17 days inactive. THIS IS THE FINAL DAY. Sprint ends TOMORROW (Friday 2026-07-10). Scan PR #52 and PR #53 today or they miss the sprint.**
  1. **PR #52 (STORY-7, branch `agent/engineer/rate-limit-guard`):** Checkout branch. Run `bandit -r backend/app/` (expect B106 false positive only — `GET /health` no-auth is PO design exception D5, `GET /odds/api-status` is JWT-protected). Run `pip-audit -r backend/requirements.txt` (expect 0 CVEs — no new runtime deps introduced). Verify `configure_logging()` in `logging_config.py` and the new `GET /odds/api-status` endpoint do not leak credentials — grep for `betfair_password`, `odds_api_key`, session token patterns. Post SECURITY CLEAR (or specific findings) as PR comment on #52.
  2. **PR #53 (STORY-14, branch `agent/engineer/frontend-scaffold`):** Frontend-only PR — no new Python code. Verify no hardcoded secrets or API keys in `frontend/src/`. Confirm `src/api/config.ts` reads from `import.meta.env.VITE_API_BASE_URL` only (no hardcoded `localhost:8000`). Confirm `requirements.txt` is unchanged. Post SECURITY CLEAR on PR #53. Lightweight scan — this should take 15 minutes.
  3. **Update `team/agents/appsec.md`** with scan results. This is sprint-critical.

### DevOps
- **Today (2026-07-09) — CRITICAL: Sprint ends TOMORROW. Merge PRs the moment AppSec CLEAR lands today.**
  1. The moment AppSec posts SECURITY CLEAR on PR #52 (STORY-7, branch `agent/engineer/rate-limit-guard`): merge PR #52 into main. Confirm CI green (expect ~75 tests: 60 existing + 15 new rate-limit-guard tests). Confirm `app/services/odds_api.py` coverage recovers to 100%.
  2. Immediately after PR #52: merge PR #53 (STORY-14, branch `agent/engineer/frontend-scaffold`) into main. Frontend-only — confirm frontend CI activates and passes (`npm run build`, `npm run lint`). No backend test count change expected.
  3. Merge order: PR #52 → PR #53. Both must merge today for sprint goal to be met.
  4. **Update `team/agents/devops.md`** with merge actions and post-merge CI results.

### QA
- **Today (2026-07-09):** All sprint PRs reviewed — no new reviews required.
  1. PRs #52 and #53 already have LGTM comments from 2026-07-08. No re-review needed unless AppSec raises code-change requests.
  2. Stand by to address any AppSec findings on PR #52 or PR #53 if specific fixes are required.
  3. After PR #52 merges: confirm main test count reaches ~75 tests and `app/services/odds_api.py` shows 100% coverage (recovery from the orphaned PR #28 merge issue noted in `team/agents/qa.md`).
  4. **Update `team/agents/qa.md`** to reflect completed sprint work if not already done.

### Engineer
- **Today (2026-07-09):** No new code tasks this sprint.
  1. PRs #52 (STORY-7) and #53 (STORY-14) are in review — no Engineer action needed unless AppSec flags specific code changes required.
  2. STORY-21a carries to Sprint 3 — do not start this sprint.
  3. If AppSec raises findings on PR #52 or #53, address promptly so DevOps can merge today.
  4. **Update `team/agents/engineer.md`** if there are status changes after merges.

### Product Owner
- **Today (2026-07-09):** Sprint 2 final day assessment.
  1. **Confirm STORY-21a carry to Sprint 3** in `team/agents/product-owner.md` — D25 confirmed STORY-21b dropped; STORY-21a also carries per Sprint 2 Day 9 board (insufficient time for full gate cycle).
  2. **Sprint 3 planning prep:** STORY-21a (Betfair polling) is the top Sprint 3 priority; STORY-21b (Odds API polling) follows once 21a merges. STORY-24 (datetime.utcnow fix, XS) can be bundled as a Day 1 quick win. STORY-22 (frontend login) and STORY-23a (OddsTable component) are now unblocked by STORY-14 if PR #53 merges today.
  3. Note sprint outcome: STORY-10, STORY-11 confirmed Done. STORY-7 and STORY-14 will be Done if AppSec acts today + DevOps merges today.
  4. **Update `team/agents/product-owner.md`** with final sprint assessment.

### Prod Support
- **Today (2026-07-09):**
  1. **Close GitHub issues #38 (STORY-10) and #39 (STORY-11)** — both stories merged 2026-07-08. Issues should be closed/labelled Done.
  2. **Verify PRs #52 and #53 carry `story` label** — add if missing. Post sprint-end urgency note on both PRs noting sprint ends tomorrow.
  3. Stale check on issues: #40 (STORY-7) and #7 (STORY-14) now have open PRs — comment with PR link and sprint-end date.
  4. Code audit on main HEAD (post PRs #47/#48 merge): check for regressions; confirm `configure_logging()` and `/health` endpoint look clean.
  5. **Update `team/agents/prod-support.md`** with today's triage.

### (Previous day assignments — 2026-07-08 — archived)
- Engineer: ✅ Pushed STORY-7 branch (75/75 tests) and STORY-14 branch (all 8 ACs). PRs created by QA (#52, #53) due to REST API proxy restriction.
- QA: ✅ Retroactively verified PRs #47 (STORY-10) and #48 (STORY-11) post-merge. Reviewed PR #52 (STORY-7) — LGTM posted. Reviewed PR #53 (STORY-14) — LGTM posted with gitkeep fix.
- DevOps: ✅ Merged PR #47 (STORY-10) at 09:07Z, PR #48 (STORY-11) at 09:09Z. CI GREEN (50 tests). Note: PRs merged without prior QA gate — process violation for Sprint 2 retro.
- AppSec: ❌ Still BLOCKED (17 days, last active 2026-06-22). Did not scan PRs #52 or #53.
- Product Owner: Pending — confirm STORY-21a/21b carry to Sprint 3.
- Prod Support: Pending — triage since 2026-07-03.

---

## Merge Order (Sprint 2 — Updated 2026-07-09)

1. ✅ **PR #28 merged 2026-07-03** (STORY-3) — DevOps.
2. ✅ **PR #31 merged 2026-07-03** (STORY-4) — DevOps.
3. ✅ **PR #47 merged 2026-07-08T09:07Z** (STORY-10) — DevOps. CI GREEN (60 tests).
4. ✅ **PR #48 merged 2026-07-08T09:09Z** (STORY-11) — DevOps. CI GREEN (60 tests; rebased to resolve main.py import conflict).
5. **AppSec CLEAR on PR #52 (STORY-7)** → **DevOps merges PR #52** today (2026-07-09). Expect ~75 tests. QA LGTM already posted.
6. **AppSec CLEAR on PR #53 (STORY-14)** → **DevOps merges PR #53** today (2026-07-09). Frontend-only — frontend CI activates. QA LGTM already posted. Independent of PR #52.
7. ~~STORY-21a: Deferred to Sprint 3.~~
8. ~~STORY-21b: Dropped to Sprint 3 per PO D25 (2026-07-08).~~

## Sprint Notes

- All code changes via PR to main — no direct pushes
- Branch naming: `agent/<role>/<short-slug>`
- The Odds API limit: 500 req/month — do not add polling in tests; `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min (PO decision D9/D17)
- An agent is BLOCKED if they have been on the same story for 2+ days with no PR opened (or, for DevOps as merge operator: 2+ days with no merge action after all gates are clear)
- STORY-7 and STORY-21a/21b cannot start until PR #28 merges — this is a hard dependency (**PR #28 MERGED 2026-07-03; STORY-7 and STORY-21a are now UNBLOCKED**)
- STORY-21b: ⚠️ `ODDS_API_POLL_INTERVAL_MINUTES` must default to 360 min (6h) — 120 req/month against 500 req/month cap. Do NOT lower without PO sign-off. **DROPPED TO SPRINT 3 per PO D25 (2026-07-08).**
- Sprint 1 retro written 2026-07-01 (overdue from 2026-06-27): `/repo/team/sprint/retrospective.md`
- DevOps escalation: issue #46 opened 2026-07-01; closed 2026-07-03 after merges
- STORY-21b DROPPED: No STORY-21a PR opened by EOD Wednesday 2026-07-08 → STORY-21b officially moves to Sprint 3 per PO D25. STORY-21a also carries to Sprint 3.
- **STORY-10 DONE (2026-07-08):** PR #47 merged. 60/60 tests on main. All 5 ACs verified.
- **STORY-11 DONE (2026-07-08):** PR #48 merged. 60/60 tests on main. All ACs verified.
- **STORY-7 PR #52 OPEN (2026-07-08):** QA LGTM posted. 75/75 tests. AppSec CLEAR is the sole remaining gate.
- **STORY-14 PR #53 OPEN (2026-07-08):** QA LGTM posted. All 8 ACs. AppSec CLEAR is the sole remaining gate.
- **⚠️ Process violation noted:** PRs #47 and #48 were merged by DevOps on 2026-07-08 without prior QA gate (QA review was retroactive post-merge). QA confirmed code was clean, but merge order must enforce gate completion before merge. Flag for Sprint 2 retrospective (Friday 2026-07-10).
- **⚠️ Critical bug (Sprint 3):** PR #28 merge commit `c5fa096` is orphaned from current main ancestry — 22 OddsApiService unit tests and `_persist()` DB layer are absent from main. `odds_api.py` coverage is 0% until PR #52 (STORY-7) merges (then recovers to 100%). DB persistence re-implementation is a Sprint 3 item.
- AppSec BLOCKED: 17 days (last active 2026-06-22). PRs #52 and #53 opened 2026-07-08 await scan. **Final day today (Thursday 2026-07-09).**

---

## Sprint Health

| Metric | Value |
|--------|-------|
| Sprint | 2 |
| Sprint Start | 2026-06-29 |
| Sprint End | 2026-07-10 (TOMORROW) |
| Stories In Progress | 2 (STORY-7 PR #52 QA LGTM/AppSec pending, STORY-14 PR #53 QA LGTM/AppSec pending) |
| Stories To Do | 0 (all cleared) |
| Stories Deferred to Sprint 3 | 2 (STORY-21a — insufficient time; STORY-21b — PO D25 drop confirmed 2026-07-08) |
| Stories Done (Sprint 2) | 4 (STORY-3 merged 2026-07-03, STORY-4 merged 2026-07-03, STORY-10 merged 2026-07-08, STORY-11 merged 2026-07-08) |
| Stories Total (Sprint 2) | 6 (adjusted: STORY-21a/21b removed from sprint scope) |
| Days Remaining | 1 (sprint ends 2026-07-10 Friday) |
| Open PRs | 2 (#52 STORY-7 QA LGTM ✅/AppSec pending 🔴, #53 STORY-14 QA LGTM ✅/AppSec pending 🔴) |
| BLOCKED agents | 1 (AppSec — 17 days inactive, last active 2026-06-22) |
| Sprint risk | HIGH — 1 day remains; AppSec is the sole gate on PRs #52 and #53; if AppSec acts today + DevOps merges today, sprint ends with 4 of 6 stories Done + STORY-7 and STORY-14 Done; if not, sprint ends with 4 Done |
