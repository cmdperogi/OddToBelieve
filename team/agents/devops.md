# DevOps — Status

**Last updated:** 2026-06-15

## CI Status
- GitHub Actions: **PR OPEN — STORY-19 fix applied + frontend guard merged in**
- PR: https://github.com/cmdperogi/OddToBelieve/pull/9
- Branch: `agent/devops/github-actions-ci`
- Latest commit: `89d5422` — STORY-19 credential secrets + PR #23 frontend guard

## Last Changes

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
