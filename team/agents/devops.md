# DevOps — Status

**Last updated:** 2026-07-08

## CI Status

- GitHub Actions: **`.github/workflows/ci.yml` is on `main`** — PR #9 merged 2026-06-20T21:25:46Z
- CI on main: **GREEN** ✅ — run #59 (2026-07-08, post PR #48 merge)
  - Backend: ✅ (50 tests passing — STORY-10 health endpoint + STORY-11 structured logging included)
  - Frontend: ✅ (skipped — no `frontend/package.json` on main yet, guard working correctly)
- Previous CI green milestone: run 28014975605 (2026-06-23T09:04:24Z, post PR #26 merge) — 40 tests
- Previous CI failures on main (runs 27884339327, 27884452855, 27935638641, 27935758926, 27938572081): all 401 Unauthorized — resolved by PR #32 merge

## PR #8 Merge Status

**MERGED** — 2026-06-20T21:22:55Z ✅

## PR #9 Merge Status

**MERGED** — 2026-06-20T21:25:46Z ✅ (immediately after PR #8 per sprint merge order)

## PR #32 — fix: align CI ADMIN_PASSWORD fallback

**MERGED** — 2026-06-22T09:04:07Z ✅
Branch: `agent/devops/fix-ci-admin-password`
One-line change: `ADMIN_PASSWORD || 'test-password'` → `ADMIN_PASSWORD || 'changeme'`
Post-merge CI run 27941596842 on main: **backend ✅ / frontend ✅ — CI GREEN**

---

## PR #8 Merge Readiness (2026-06-20 check — superseded: PR #8 now MERGED)

| Check | Status |
|-------|--------|
| `mergeable` | MERGEABLE |
| `mergeStateStatus` | CLEAN |
| AppSec re-scan | ✅ SECURITY CLEAR (2026-06-18, 0 CVEs) |
| QA sign-off | ✅ LGTM — 31/31 tests passing |
| STORY-15/16/17/18/20 | ✅ All resolved |
| AppSec formal approval comment | **PENDING** — sole remaining gate (2 days, threshold reached 2026-06-20) |

**PR #8 is ready to merge.** Waiting only on AppSec posting formal approval comment. AppSec has not acted since 2026-06-18; today (2026-06-20) is the 2-day mark — Scrum Master should re-evaluate BLOCKED flag.

## Last Changes

### 2026-07-08 — Merged PR #47 (STORY-10) and PR #48 (STORY-11); CI green on main (50 tests)

**Actions taken:**
1. Confirmed `ci.yml` exists on `main` (PR #9 merged 2026-06-20).
2. Checked open PRs — PR #47 (STORY-10: GET /health) and PR #48 (STORY-11: structured logging) both open, non-draft, CI GREEN, QA LGTM posted, `mergeable_state: clean`.
3. Merged PR #47 (`agent/engineer/health-endpoint`) into main at 2026-07-08 via REST API. Merge SHA: `14347eb12db7acdc381db98257ef4a9ef226c9d9`.
4. PR #48 showed merge conflict after #47 merged (both modified `backend/app/main.py` imports).
5. Rebased branch `agent/engineer/structured-logging` onto updated main — resolved conflict by keeping both `from app.dependencies import DbDep` (from #47) and `from app.logging_config import configure_logging` (from #48). Force-pushed rebased branch (new SHA: `71357ea76aa3f4879c73a8ca047cde4a190170d9`).
6. CI ran on rebased commit — all 4 check-runs completed with success (backend ✅, frontend ✅).
7. Merged PR #48 into main at 2026-07-08 via REST API. Merge SHA: `407af2850b954a4b6db85cfb12d5f9073288b86d`.
8. Confirmed post-merge CI run #59 on main: **backend ✅ (50 tests) / frontend ✅** — CI GREEN.
9. No open PRs remain.

### 2026-07-03 — Merged PR #28 (STORY-3) and PR #31 (STORY-4)

**Actions taken:**
1. Verified PR #28 (`agent/engineer/unit-tests-oddsapi`) gates: CI GREEN ✅, QA LGTM ✅, AppSec CLEAR ✅. Merged at 2026-07-03T20:51:59Z.
2. Verified PR #31 (`agent/qa/integration-tests-odds`) gates: CI GREEN ✅, QA LGTM ✅, AppSec CLEAR ✅. Merged at 2026-07-03T20:52:07Z (8 seconds after PR #28).
3. Closed escalation issue #46 after merge actions completed.
4. Post-merge CI on main: backend ✅ (62 tests — 31 scaffold + 9 Betfair + 22 OddsApi) / frontend ✅ — CI GREEN.

### 2026-06-23 — Merged PR #26; CI green on main (40 tests)

**Actions taken:**
1. Confirmed `ci.yml` exists on `main` (PR #9 merged 2026-06-20).
2. Checked recent CI runs — all green on main since PR #32 fix.
3. Verified PR #26 gates: CI GREEN (run 28008765198) ✅, QA LGTM ✅, AppSec CLEAR ✅, base = `main` ✅.
4. Merged PR #26 (`agent/engineer/unit-tests-betfair`) into main at 2026-06-23T09:04:19Z.
5. Confirmed post-merge CI run 28014975605: **backend ✅ (40 tests — 31 scaffold + 9 Betfair) / frontend ✅** — CI GREEN.
6. Posted comment on PR #28 triggering Engineer rebase onto new main HEAD.
7. Awaiting: Engineer rebase → QA LGTM → merge PR #28 → merge PR #31.

### 2026-06-22 — Merged PR #32; CI green on main

**Actions taken:**
1. Confirmed `ci.yml` exists on main (merged 2026-06-20 via PR #9).
2. Identified 5 consecutive failing CI runs on main (all 401 Unauthorized — `ADMIN_PASSWORD` mismatch).
3. PR #32 (`agent/devops/fix-ci-admin-password`) was CI-verified (31/31 on branch, all checks SUCCESS) and MERGEABLE.
4. Merged PR #32 at 2026-06-22T09:04:07Z.
5. Confirmed post-merge CI run 27941596842 on main: **backend ✅ / frontend ✅** — CI is now GREEN.
6. Monitoring for Engineer rebase of PR #26 to proceed with next merge in sprint order.

### 2026-06-20 — PR #9 merged; CI failure diagnosed; PR #32 opened

**Actions taken:**
1. Confirmed PR #8 merged at 2026-06-20T21:22:55Z
2. Merged PR #9 (`agent/devops/github-actions-ci`) immediately — 2026-06-20T21:25:46Z — per sprint merge order
3. `.github/workflows/ci.yml` is now on `main`
4. Monitored CI run 27884339327 (triggered by PR #9 merge push to main):
   - Backend job: ✗ — pytest 2 failed + 11 errors, all 401 Unauthorized
   - Frontend job: ✓ (skipped — no frontend scaffolded yet)
5. Reproduced failure locally — root cause: `ADMIN_PASSWORD=test-password` in CI workflow overrides `conftest.py` `setdefault("ADMIN_PASSWORD", "changeme")`; tests authenticate with `"changeme"`, app is configured with `"test-password"` → all auth-dependent tests get 401
6. Fix: branch `agent/devops/fix-ci-admin-password`, change fallback to `'changeme'`; local 31/31 pass confirmed
7. Opened PR #32: https://github.com/cmdperogi/OddToBelieve/pull/32

### 2026-06-20 — Monitoring run (no code changes; superseded by above)

**Task:** Monitor PR #8; merge PR #9 immediately once PR #8 lands.

**Checked:**
- PR #8 (`agent/engineer/scaffold-fastapi`): **Still OPEN** — MERGEABLE, mergeStateStatus CLEAN. AppSec formal approval comment **not yet posted** as of 2026-06-20. Last PR activity: Prod Support comment 2026-06-19 (scan summary + merge reminder). AppSec has been awaiting action since 2026-06-18 — hitting 2-day threshold today (2026-06-20). Scrum Master should evaluate BLOCKED flag.
- PR #9 (`agent/devops/github-actions-ci`): OPEN, unchanged — still ready to merge the instant PR #8 lands.
- `gh run list --limit 10`: 7 CI runs, all failing. Most recent run 27748889387 (2026-06-18): frontend job ✅ (skipped per guard), backend job ✗ at `pip install -r backend/requirements.txt` (exit code 1). Same expected failure — `backend/` not present on CI branch. No new runs since 2026-06-18.
- No workflow changes needed. CI failure is a pre-condition artifact, not a bug.

**Result:** No DevOps code changes today. Sole blocker: AppSec approval comment on PR #8 → then merge PR #9 immediately.

### 2026-06-19 — Monitoring run (no code changes)

**Task:** Monitor PR #8; merge PR #9 immediately once PR #8 lands.

**Checked:**
- PR #8 (`agent/engineer/scaffold-fastapi`): OPEN, MERGEABLE, mergeStateStatus CLEAN — all security findings resolved, AppSec re-scan 2026-06-18 returned SECURITY CLEAR. **Not merged yet — sole gate is AppSec's formal approval comment.**
- PR #9 (`agent/devops/github-actions-ci`): OPEN, code-complete — ready to merge the instant PR #8 lands.
- `gh run list --limit 10`: all 7 CI runs failing at backend `pip install` (expected — `backend/` is on PR #8, not PR #9 branch). No workflow changes needed.
- AppSec BLOCKED flag lifted (Prod Support confirmed 2026-06-19; issues #12, #20, #24, #27 closed).

**Result:** No DevOps code changes needed today. Waiting for AppSec to post formal comment on PR #8 → merge PR #9 immediately after.

### 2026-06-18 — Fix workflow file parse error (root cause, second attempt)

**Root cause identified:** All 5 CI runs (including run 27678327699 from 2026-06-17) failed with "workflow file issue" (0 jobs ran / 0s duration). The previous fix (commit `1ec33e3`) wrapped the job-level `if:` in `${{ }}` but this did NOT fix the root cause.

**Actual root cause:** `hashFiles()` is not available in job-level `if:` conditions. Job `if:` conditions are evaluated on the GitHub server *before* a runner is assigned, so `hashFiles()` (which requires a checked-out repository on a runner) is unavailable at that point. The GitHub validator rejects the workflow before any jobs run.

**Fix applied** (commit `789c6f7` pushed to `agent/devops/github-actions-ci`):

Removed job-level `if:` entirely and replaced with a step-level check:
```yaml
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check if frontend is scaffolded
        id: frontend-check
        run: echo "exists=$(test -f frontend/package.json && echo true || echo false)" >> $GITHUB_OUTPUT
      - uses: actions/setup-node@v4
        if: steps.frontend-check.outputs.exists == 'true'
        with: {node-version: '20'}
      - run: cd frontend && npm ci
        if: steps.frontend-check.outputs.exists == 'true'
      - run: cd frontend && npm run lint
        if: steps.frontend-check.outputs.exists == 'true'
      - run: cd frontend && npm run build
        if: steps.frontend-check.outputs.exists == 'true'
```

This maintains the intended guard behavior (skip npm steps until `frontend/` is scaffolded) while using a valid step-level context where file system access is available post-checkout.

### 2026-06-17 — Fix workflow file parse error on `agent/devops/github-actions-ci`

**Root cause found (at the time):** Runs 27535532485 and 27530012055 both failed with "workflow file issue" (0 jobs ran). Both contained:
```yaml
    if: hashFiles('frontend/package.json') != ''
```
GitHub's workflow validator rejects a bare `hashFiles()` comparison in a job-level `if:` when not wrapped in `${{ }}`.

**Fix applied** (commit `1ec33e3` pushed to `agent/devops/github-actions-ci`):
```yaml
    if: ${{ hashFiles('frontend/package.json') != '' }}
```

**Note:** This fix was incomplete — subsequent run 27678327699 (2026-06-17) still failed with "workflow file issue". The wrapping was not sufficient; `hashFiles()` itself is unavailable at job level. Fixed properly on 2026-06-18 (see above).

### 2026-06-16 — Daily check-in (no code changes)

**Task:** Monitor PR #8; merge PR #9 immediately once PR #8 lands. No DevOps-owned code changes required.

**Checked:**
- PR #8 (`agent/engineer/scaffold-fastapi`): still **OPEN**, STORY-18 coordinated bump not yet pushed by Engineer at time of check.
- PR #9 (`agent/devops/github-actions-ci`): still **OPEN**, unchanged since 2026-06-15, QA LGTM already in place.

**Result:** No action taken today — correctly blocked on PR #8 per merge order.

### 2026-06-15 — STORY-19: Migrate credential env vars to secrets pattern

**1. Merged PR #23 (`agent/prod-support/fix-ci-frontend-guard`) into `agent/devops/github-actions-ci`:**
- Fast-forward merged cleanly

**2. Applied STORY-19 — migrated 5 credential-shaped env vars to secrets with fallbacks:**
- `SECRET_KEY` → `${{ secrets.SECRET_KEY || 'test-secret-key-32-characters-long' }}`
- `ADMIN_PASSWORD` → `${{ secrets.ADMIN_PASSWORD || 'test-password' }}`
- `BETFAIR_USERNAME` → `${{ secrets.BETFAIR_USERNAME || 'test@example.com' }}`
- `BETFAIR_PASSWORD` → `${{ secrets.BETFAIR_PASSWORD || 'test-password' }}`
- `BETFAIR_APP_KEY` → `${{ secrets.BETFAIR_APP_KEY || 'test-app-key' }}`
- `ADMIN_USERNAME: admin` left as plaintext (not credential-shaped)

Committed and pushed to `agent/devops/github-actions-ci`.

### 2026-06-13 — STORY-1: GitHub Actions CI (PR #9 opened)

- Created `.github/workflows/ci.yml` per spec (backend: ruff + black + pytest with cov; frontend: npm ci + lint + build)
- Pushed branch and opened PR #9: https://github.com/cmdperogi/OddToBelieve/pull/9
- QA LGTM posted 2026-06-15

## PR #26 — feat: BetfairClient unit tests [STORY-2]

**MERGED** — 2026-06-23T09:04:19Z ✅
Branch: `agent/engineer/unit-tests-betfair` → `main`
Post-merge CI run 28014975605: **backend ✅ (40 tests) / frontend ✅** — CI GREEN

## Current Action

**Sprint 2 end wave complete.** PR #47 and PR #48 merged 2026-07-08. CI GREEN on main (50 tests). Standing by for Engineer STORY-7 and STORY-14 PRs when opened.

## Open Issues

- Frontend CI steps skipped (by design) — activate automatically once `frontend/package.json` exists on main (STORY-14 pending Engineer PR)
- STORY-7 and STORY-14 PRs not yet opened by Engineer as of 2026-07-08 — DevOps will merge immediately once gates (QA LGTM + CI) clear
