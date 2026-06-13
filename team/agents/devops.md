# DevOps — Status

**Last updated:** 2026-06-13

## CI Status
- GitHub Actions: **BLOCKED — PAT missing `workflow` scope**

## Last Changes

### 2026-06-13 — STORY-1: GitHub Actions CI (attempted)

**Task:** Create `.github/workflows/ci.yml` on branch `agent/devops/github-actions-ci` and open PR.

**What was done:**
- Drafted full CI workflow per spec (backend: ruff + black + pytest with cov; frontend: npm ci + lint + build)
- Created local branch `agent/devops/github-actions-ci` with the commit ready
- Attempted `git push -u origin agent/devops/github-actions-ci` — **rejected by GitHub**

**Blocker:**
```
! [remote rejected] agent/devops/github-actions-ci -> agent/devops/github-actions-ci
  (refusing to allow a Personal Access Token to create or update workflow
   `.github/workflows/ci.yml` without `workflow` scope)
```

The PAT provided (`github_pat_11AW6LJDY0HxywdBlqDw8j_...`) does **not** include the `workflow` scope. GitHub enforces this at push time AND via the REST Contents API — there is no workaround without a token that has `workflow` scope.

**Resolution required:**
The repository owner must regenerate (or create a new) PAT with the `workflow` scope enabled:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Select the token used for this agent
3. Check **workflow** under "Repository permissions" or scopes
4. Update the token in the agent's environment and re-run

**CI workflow is ready** — the file content is committed locally on branch `agent/devops/github-actions-ci`. Once the token is updated, the push and PR creation will succeed immediately.

**CI workflow spec (ready to push):**
```yaml
name: CI
on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r backend/requirements.txt
      - run: cd backend && ruff check .
      - run: cd backend && black --check .
      - run: cd backend && pytest tests/ -v --cov=app --cov-report=term-missing
        env:
          SECRET_KEY: test-secret-key
          ADMIN_USERNAME: admin
          ADMIN_PASSWORD: test-password
          BETFAIR_USERNAME: test@example.com
          BETFAIR_PASSWORD: test-password
          BETFAIR_APP_KEY: test-app-key
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: {node-version: '20'}
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run build
```

## Open Issues
- **BLOCKED:** STORY-1 cannot complete until PAT is re-issued with `workflow` scope
- Note: No prior CI runs exist (`gh run list` returns empty — no workflow has ever executed in this repo)
