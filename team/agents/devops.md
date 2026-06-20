# DevOps — Status

**Last updated:** 2026-06-20

## CI Status

- GitHub Actions: **`.github/workflows/ci.yml` is on `main`** — PR #9 merged 2026-06-20T21:25:46Z
- First CI run on main (run 27884339327): **backend ✗ / frontend ✓**
  - Backend failure: pytest 2 failures + 11 errors, all 401 Unauthorized
  - Root cause: `ADMIN_PASSWORD || 'test-password'` in CI overrides `conftest.py` `setdefault("ADMIN_PASSWORD", "changeme")` — tests authenticate with hardcoded `"changeme"` → mismatch
  - **Fix PR open: [#32](https://github.com/cmdperogi/OddToBelieve/pull/32)** — branch `agent/devops/fix-ci-admin-password` — changes fallback from `'test-password'` to `'changeme'`
  - Local verification with `ADMIN_PASSWORD=changeme`: **31/31 tests pass**
- Frontend job: ✅ skipped (no `frontend/package.json` on main yet — guard working correctly)

## PR #8 Merge Status

**MERGED** — 2026-06-20T21:22:55Z ✅

## PR #9 Merge Status

**MERGED** — 2026-06-20T21:25:46Z ✅ (immediately after PR #8 per sprint merge order)

## PR #32 — fix: align CI ADMIN_PASSWORD fallback

**OPEN** — https://github.com/cmdperogi/OddToBelieve/pull/32
Branch: `agent/devops/fix-ci-admin-password`
One-line change: `ADMIN_PASSWORD || 'test-password'` → `ADMIN_PASSWORD || 'changeme'`
Local test result: 31/31 pass. Awaiting CI run and merge.

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

## Current Action

**Awaiting PR #32 merge** — one-line fix to align `ADMIN_PASSWORD` CI fallback with test fixtures. Once merged, CI backend job should go green on main (31 tests, 67% coverage). Frontend CI will activate once frontend is scaffolded.

## Open Issues

- **PR #32** (`agent/devops/fix-ci-admin-password`) — CI `ADMIN_PASSWORD` mismatch fix; ready to merge
- Frontend CI steps skipped (by design) — activate automatically once `frontend/package.json` exists on main
- `app/services/betfair.py` and `app/services/odds_api.py` at 0% coverage — covered by PRs #26/#28 (pending rebase onto updated main)
