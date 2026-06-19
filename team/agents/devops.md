# DevOps — Status

**Last updated:** 2026-06-19

## CI Status

- GitHub Actions: **PR #9 open on `agent/devops/github-actions-ci` — code-complete, QA LGTM, awaiting merge after PR #8**
- PR: https://github.com/cmdperogi/OddToBelieve/pull/9
- Branch: `agent/devops/github-actions-ci`
- Latest commit: `789c6f7` — fix: move frontend guard to step level (hashFiles() unavailable at job if)
- `.github/workflows/ci.yml` does not exist on `main` yet — it ships with PR #9, held behind PR #8 (merge order: PR #8 → PR #9, backend job needs `backend/` on main)
- **Recent CI runs (all on PR #9 branch):** All 7 runs failing — current failure at `pip install -r backend/requirements.txt` (exit code 1). This is **expected and not a workflow bug**: `backend/` does not exist on the CI branch (it lives on PR #8). Frontend job passes (guarded by step-level `frontend/package.json` check). CI will pass on main once PR #8 → PR #9 merge cascade completes.

## PR #8 Merge Readiness (2026-06-19 check)

| Check | Status |
|-------|--------|
| `mergeable` | MERGEABLE |
| `mergeStateStatus` | CLEAN |
| AppSec re-scan | ✅ SECURITY CLEAR (2026-06-18, 0 CVEs) |
| QA sign-off | ✅ LGTM — 31/31 tests passing |
| STORY-15/16/17/18/20 | ✅ All resolved |
| AppSec formal approval comment | **PENDING** — sole remaining gate |

**PR #8 is ready to merge.** Waiting only on AppSec posting formal approval comment.

## Last Changes

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

Monitoring PR #8 (`agent/engineer/scaffold-fastapi`). **The moment PR #8 merges to main, merge PR #9 immediately.** Merge order is critical: PR #8 → PR #9 so that `backend/` exists when the CI backend job runs. After merge, verify CI run on main passes and update this file.

## Open Issues

- **PR #9 waiting on PR #8** — sole dependency; PR #9 is fully ready
- **AppSec formal comment on PR #8** is the sole sprint merge gate (scan is done, result is CLEAR — comment is an administrative formality)
- AppSec BLOCKED flag lifted 2026-06-19 (issues #12, #20, #24, #27 closed by Prod Support)
- CI workflow parse error fixed 2026-06-18 (commit `789c6f7`) — confirmed working (frontend job passes; backend job fails only due to missing `backend/` on CI branch, not a workflow bug)
