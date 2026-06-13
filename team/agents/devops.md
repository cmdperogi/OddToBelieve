# DevOps — Status

**Last updated:** 2026-06-13

## CI Status
- GitHub Actions: **PR OPEN — awaiting review and merge**
- PR: https://github.com/cmdperogi/OddToBelieve/pull/9
- Branch: `agent/devops/github-actions-ci`

## Last Changes

### 2026-06-13 — STORY-1: GitHub Actions CI (completed)

**Task:** Create `.github/workflows/ci.yml` on branch `agent/devops/github-actions-ci` and open PR.

**What was done:**
- Created `.github/workflows/ci.yml` per spec
- Pushed branch `agent/devops/github-actions-ci` successfully (new PAT includes `workflow` scope)
- Opened PR #9: https://github.com/cmdperogi/OddToBelieve/pull/9

**CI workflow covers:**
- **backend:** `ruff check`, `black --check`, `pytest tests/ -v --cov=app` with test env vars injected
- **frontend:** `npm ci`, `npm run lint`, `npm run build`
- Triggers: push to any branch, PR targeting main

**Previous blocker resolved:**
- Prior session (2026-06-13) was blocked — PAT lacked `workflow` scope
- New PAT provided with `workflow` scope — push and PR creation succeeded

## Open Issues
- STORY-1 PR #9 is open — needs review and merge before CI protects PRs
- Once merged, all future PRs will be gated on backend lint/test + frontend lint/build
- Backend tests will fail until Engineer completes STORY-13 (scaffold FastAPI) — expected
