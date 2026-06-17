# DevOps — Status

**Last updated:** 2026-06-17

## CI Status

- GitHub Actions: **PR #9 open on `agent/devops/github-actions-ci` — workflow parse error fixed, QA LGTM**
- PR: https://github.com/cmdperogi/OddToBelieve/pull/9
- Branch: `agent/devops/github-actions-ci`
- Latest commit: `1ec33e3` — fix workflow file parse error (job-level `if:` must use `${{ }}`)
- `.github/workflows/ci.yml` does not exist on `main` yet — it ships with PR #9, held behind PR #8 (merge order: PR #8 → PR #9, backend job needs `backend/` on main)

## Last Changes

### 2026-06-17 — Fix workflow file parse error on `agent/devops/github-actions-ci`

**Root cause found:** Runs 27535532485 and 27530012055 both failed with "workflow file issue" (0 jobs ran). Both contained:
```yaml
    if: hashFiles('frontend/package.json') != ''
```
GitHub's workflow validator rejects a bare `hashFiles()` comparison in a job-level `if:` when not wrapped in `${{ }}`.

**Fix applied** (commit `1ec33e3` pushed to `agent/devops/github-actions-ci`):
```yaml
    if: ${{ hashFiles('frontend/package.json') != '' }}
```

**Note on earlier run failures (27482213479, 27482213022):** backend job failed on `pip install -r backend/requirements.txt` and frontend job failed on `npm ci` — expected until PR #8 merges `backend/` and `frontend/` to main.

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

Monitoring PR #8 (`agent/engineer/scaffold-fastapi`). **The moment PR #8 merges to main, merge PR #9 immediately.** Merge order is critical: PR #8 → PR #9 so that `backend/` exists when the CI backend job runs.

## Open Issues

- PR #9 is waiting on PR #8 (sole dependency)
- PR #8 is waiting on AppSec formal re-scan (STORY-18 fix applied 2026-06-16; QA LGTM confirmed 31/31 tests, 0 CVEs)
- **AppSec re-scan is the sole sprint blocker** — if AppSec does not complete today (2026-06-17), sprint goal is at risk
