# DevOps — Status

**Last updated:** 2026-06-16

## CI Status
- GitHub Actions: **PR OPEN — code-complete, QA LGTM, waiting on merge order**
- PR: https://github.com/cmdperogi/OddToBelieve/pull/9
- Branch: `agent/devops/github-actions-ci`
- Latest commit: `89d5422` — STORY-19 credential secrets + PR #23 frontend guard
- `.github/workflows/ci.yml` does not exist on `main` yet — it ships with PR #9, which is intentionally held behind PR #8 (merge order: PR #8 → PR #9, since the backend CI job needs `backend/` to exist on main).

## Last Changes

### 2026-06-16 — Daily check-in (no code changes)

**Task today (per sprint board):** Monitor PR #8; merge PR #9 immediately once PR #8 lands. No DevOps-owned code changes required unless PR #8 touches CI-related files (it doesn't).

**Checked:**
- PR #8 (`agent/engineer/scaffold-fastapi`): still **OPEN**, not merged. STORY-18 (coordinated `fastapi==0.137.1` / `pydantic>=2.9.0` / `python-multipart==0.0.31` bump) has not been pushed by Engineer yet — see issue #24 for the verified fix Prod Support posted this morning. No checks reported on the branch (expected — `ci.yml` isn't on `main` yet).
- PR #9 (`agent/devops/github-actions-ci`): still **OPEN**, unchanged since 2026-06-15, QA LGTM already in place. No new commits needed.

**Result:** No action taken today — correctly blocked on PR #8 per merge order. Will merge PR #9 as soon as PR #8 lands on main.

### 2026-06-15 — STORY-19: Migrate credential env vars to secrets pattern

**Task:** Replace all plaintext credential-shaped env vars in `ci.yml` with `${{ secrets.VAR || 'fallback' }}` pattern, and merge PR #23 (frontend guard) into the CI branch.

**What was done:**

**1. Merged PR #23 (`agent/prod-support/fix-ci-frontend-guard`) into `agent/devops/github-actions-ci`:**
- Reviewed diff — single change: `if: hashFiles('frontend/package.json') != ''` on the frontend job
- Fast-forward merged cleanly

**2. Applied STORY-19 — migrated 5 credential-shaped env vars to secrets with fallbacks:**
- `SECRET_KEY` → `${{ secrets.SECRET_KEY || 'test-secret-key-32-characters-long' }}`
- `ADMIN_PASSWORD` → `${{ secrets.ADMIN_PASSWORD || 'test-password' }}`
- `BETFAIR_USERNAME` → `${{ secrets.BETFAIR_USERNAME || 'test@example.com' }}`
- `BETFAIR_PASSWORD` → `${{ secrets.BETFAIR_PASSWORD || 'test-password' }}`
- `BETFAIR_APP_KEY` → `${{ secrets.BETFAIR_APP_KEY || 'test-app-key' }}`
- `ADMIN_USERNAME: admin` left as plaintext (not credential-shaped per sprint spec)

**Committed and pushed** to `agent/devops/github-actions-ci`.

### 2026-06-13 — STORY-1: GitHub Actions CI (completed)

**Task:** Create `.github/workflows/ci.yml` on branch `agent/devops/github-actions-ci` and open PR.

**What was done:**
- Created `.github/workflows/ci.yml` per spec
- Pushed branch `agent/devops/github-actions-ci` successfully (new PAT includes `workflow` scope)
- Opened PR #9: https://github.com/cmdperogi/OddToBelieve/pull/9

**CI workflow covers:**
- **backend:** `ruff check`, `black --check`, `pytest tests/ -v --cov=app` with test env vars injected
- **frontend:** `npm ci`, `npm run lint`, `npm run build` (guarded by `hashFiles` — skipped if no frontend/)
- Triggers: push to any branch, PR targeting main

**Previous blocker resolved:**
- Prior session (2026-06-13) was blocked — PAT lacked `workflow` scope
- New PAT provided with `workflow` scope — push and PR creation succeeded

## Open Issues
- PR #9 is ready for QA review — STORY-19 fix applied, PR #23 merged in
- PR #9 must wait for PR #8 (Engineer STORY-13) to merge first (backend/ needed for CI to pass)
- Once PR #8 merges and CI is green on PR #9, DevOps will merge PR #9 to main
