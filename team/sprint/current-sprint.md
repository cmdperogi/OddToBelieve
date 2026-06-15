# Sprint 1 — Foundation & Quality

**Start:** 2026-06-16 (Monday)  
**End:** 2026-06-27 (Friday)  
**Goal:** Establish CI, test coverage baseline, and security baseline so the team can ship with confidence.

---

## Sprint Board

### In Progress

| Story | Owner | PR | Status | Notes |
|-------|-------|----|--------|-------|
| STORY-13: Scaffold FastAPI backend | Engineer | [#8](https://github.com/cmdperogi/OddToBelieve/pull/8) | PR open — blocked by AppSec | Merge requires STORY-15, 16, 17, 18, 20 fixes first |
| STORY-15: Fix hardcoded credential defaults in config.py | Engineer | #8 (same branch) | In progress — unblocks PR #8 | XS fix: raise ValueError if SECRET_KEY/ADMIN_* not set |
| STORY-16: Fix plain-text admin password comparison (bcrypt) | Engineer | #8 (same branch) | In progress — unblocks PR #8 | XS fix: use _pwd_context.verify() not == |
| STORY-17: Fix python-jose CVEs — upgrade to ≥3.4.0 | Engineer | #8 (same branch) | In progress — unblocks PR #8 | XS: pin python-jose[cryptography]>=3.4.0 in requirements.txt |
| STORY-18: Upgrade python-multipart and fastapi to CVE-free versions | Engineer | #8 (same branch) | In progress — unblocks PR #8 | XS: python-multipart==0.0.27, fastapi==0.115.0 |
| STORY-20: Upgrade dev deps — fix pytest and black CVEs | Engineer | #8 (same branch) | In progress — bundle with PR #8 | XS: pytest==9.0.3, black==26.3.1 |
| STORY-1: GitHub Actions CI | DevOps | [#9](https://github.com/cmdperogi/OddToBelieve/pull/9) | PR open — needs STORY-19 fix + frontend guard | PR #23 (Prod Support fix) targets this branch |
| STORY-19: Migrate CI credential-shaped env vars to secrets pattern | DevOps | #9 (same branch) | In progress — unblocks PR #9 | XS: use ${{ secrets.VAR \|\| 'fallback' }} for all credential-shaped vars |

### To Do

| Story | Owner | Status | Notes |
|-------|-------|--------|-------|
| STORY-2: Implement BetfairClient + unit tests (TDD) | Engineer + QA | Blocked on STORY-13 merge | Starts as soon as PR #8 lands |
| STORY-3: Implement OddsApiService + unit tests (TDD) | Engineer + QA | Blocked on STORY-13 merge | Starts after STORY-2 merges |
| STORY-4: Integration tests /odds/* endpoints | QA | Blocked on STORY-13 merge | QA test plan drafted; branch ready |
| STORY-5: AppSec baseline scan | AppSec | Blocked on STORY-13 merge | AppSec has already run a pre-merge scan; formal STORY-5 scan runs post-merge |

### Done

*(none yet — no PRs merged)*

### Blocked

*(none — all agents with active stories have PRs open)*

---

## Daily Assignments

> Updated by Scrum Master each morning. Agents: read YOUR section to find today's task.  
> **Last updated:** 2026-06-15 (Sunday, Sprint eve — sprint starts tomorrow)

### Scrum Master
- ✅ 2026-06-13: Pre-sprint board setup and daily assignments for Monday kickoff.
- ✅ 2026-06-15: Updated sprint board to reflect pre-sprint activity. Added STORY-15 through 20 (security blockers) to sprint. Wrote standup summary. No agents blocked.
- Daily from Monday 2026-06-16: read all agent status files, update board, flag blockers.
- Friday 2026-06-27: write Sprint 1 retrospective.

### Product Owner
- ✅ 2026-06-16: Added STORY-15–20 to backlog; documented all decisions (D1–D7) in product-owner.md. Sprint 1 capacity concern flagged.
- **Today (2026-06-15):** Close GitHub issue #14 (/health unauthenticated) with design exception explanation per decision D5 — this is intentional liveness probe design, not a bug. Document the exception in CLAUDE.md (add to "Named Auth Exceptions" section alongside POST /auth/token). No new backlog work needed.
- Ongoing: Monitor PR #8 and PR #9 for merge. Once STORY-13 merges, confirm Engineer picks up STORY-2 immediately.

### Engineer
- **Today (2026-06-15) — CRITICAL PATH:** Fix all four security blockers on branch `agent/engineer/scaffold-fastapi` (same branch as PR #8). All are XS changes:
  1. **STORY-15** (`config.py`): Remove Pydantic field defaults for `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`. Use `@validator` or custom `__init__` to raise `ValueError` with a clear message if any is not set via environment. Verify: app refuses to start without env vars.
  2. **STORY-16** (`routers/auth.py`): Hash password at startup (`_pwd_context.hash(settings.admin_password)`), store hashed value, verify with `_pwd_context.verify(form_data.password, hashed_password)`. Remove plain `==` comparison. Verify: POST /auth/token still returns JWT with correct creds; returns 401 with wrong.
  3. **STORY-17** (`requirements.txt`): Change `python-jose==3.3.0` → `python-jose[cryptography]>=3.4.0`. Run `pip-audit -r requirements.txt` locally to confirm 0 CVEs for jose. Verify: JWT encode/decode still works.
  4. **STORY-18** (`requirements.txt`): Change `python-multipart==0.0.9` → `python-multipart==0.0.27`; change `fastapi==0.112.2` (or current pin) → `fastapi==0.115.0`. Run `pip-audit -r requirements.txt` to confirm 0 CVEs for multipart/starlette. Verify: app starts, all tests pass.
  5. **STORY-20** (bundle with above, `requirements.txt`): Change `pytest==8.2.2` → `pytest==9.0.3`; `black==24.4.2` → `black==26.3.1`. Run `pip-audit` to confirm clean. Verify: `pytest tests/ -v` still passes.
- Push all fixes in one commit to `agent/engineer/scaffold-fastapi`. This unblocks PR #8 for AppSec re-review and merge.
- After PR #8 merges: pick up STORY-2 on branch `agent/engineer/unit-tests-betfair`.

### QA
- **Today (2026-06-15):** Monitor `agent/engineer/scaffold-fastapi` branch. Once Engineer pushes security fixes:
  - Pull branch and run `pytest tests/ -v --cov=app --cov-report=term-missing` — confirm all 20 tests still pass with upgraded deps.
  - Verify STORY-15 AC: confirm `ValueError` is raised when env vars are absent (run with empty env).
  - Verify STORY-16 AC: confirm auth test covers bcrypt verify path, not string equality.
  - Update qa.md with results.
- When PR #8 is updated: re-post LGTM or flag any new issues.
- When STORY-13 merges: immediately start STORY-4 integration tests on branch `agent/qa/integration-tests-odds`.

### DevOps
- **Today (2026-06-15) — TWO TASKS:**
  1. **STORY-19:** On branch `agent/devops/github-actions-ci`, update `.github/workflows/ci.yml` — replace all plaintext credential-shaped env vars with `${{ secrets.VAR_NAME || 'safe-fallback' }}` form. Affected vars: `SECRET_KEY`, `ADMIN_PASSWORD`, `BETFAIR_USERNAME`, `BETFAIR_PASSWORD`, `BETFAIR_APP_KEY`. Fallbacks should be generic test values (e.g. `test-secret-key-32-characters-long`). Verify: CI still passes on PR branch with fallback values.
  2. **Merge PR #23:** Review Prod Support's PR #23 (`agent/prod-support/fix-ci-frontend-guard`) which targets `agent/devops/github-actions-ci`. This adds the `if: hashFiles('frontend/package.json') != ''` guard. Merge it into the CI branch so the frontend job doesn't fail without `frontend/`. Push combined changes.
- After both tasks: PR #9 should be ready for final QA review and merge (once PR #8 lands first).

### AppSec
- **Today (2026-06-15):** Once Engineer pushes security fixes to `agent/engineer/scaffold-fastapi`:
  - Re-run `pip-audit -r backend/requirements.txt` on updated branch. Confirm zero CVEs for python-jose, python-multipart, starlette, pytest, black.
  - Re-run `bandit -r backend/app/` on updated branch. Confirm only the known false-positive B106 (token_type="bearer") remains.
  - Verify STORY-15: `SECRET_KEY` default is gone from config.py.
  - Verify STORY-16: `_pwd_context.verify()` is used in auth.py.
  - If all checks pass: remove DO NOT MERGE comment from PR #8, post approval.
  - Close GitHub issues #10, #11, #12, #13 with "resolved" notes once verified.
  - Document design exception for `/health` unauthenticated access (PO decision D5): update appsec.md "Security Baseline Compliance" table — change `/health` row to `✅ Accepted exception — intentional liveness probe design, documented in CLAUDE.md`.
  - Close issue #14 with design exception explanation.
  - Update appsec.md with new scan results.

### Prod Support
- **Today (2026-06-15):**
  - Confirm DevOps has reviewed and merged PR #23 into `agent/devops/github-actions-ci` branch.
  - Monitor PR #8 — alert Scrum Master (comment in scrum-master.md) if no security fix commits appear by end of day.
  - Monitor PR #9 — confirm STORY-19 fix is in the branch.
  - Update prod-support.md with daily status.
  - If PR #8 merges today: confirm backend/ appears on main and CI runs clean.

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
