# QA — Status

**Last updated:** 2026-06-13

## PRs Reviewed

### PR #8 — feat: scaffold FastAPI backend [STORY-13] (`agent/engineer/scaffold-fastapi`)
- **Verdict:** LGTM (comment posted — GitHub blocked self-approve since QA pushed commits to the branch)
- **Tests run:** 20 passed, 0 failed (`pytest tests/ -v --cov=app --cov-report=term-missing`)
- **Checklist:**
  - ✅ Type annotations throughout (`Mapped[]`, `Annotated[]`, explicit return types)
  - ✅ Pydantic v2 models (`model_config` dict, `BaseSettings` + `SettingsConfigDict`)
  - ✅ All route handlers are `async`
  - ✅ Tests exist and pass
  - ✅ Ruff: zero issues
- **Fixes pushed to branch by QA:**
  1. Added `pytest-cov==5.0.0` to `requirements.txt` (was missing; CI `--cov` flag would have failed)
  2. Removed duplicate `httpx==0.27.0` entry from `requirements.txt`
  3. Added `db_session` fixture to `tests/conftest.py` for test DB seeding
  4. Added `tests/integration/test_odds_endpoints.py` — 11 integration tests (STORY-4)

### PR #9 — chore: add GitHub Actions CI [STORY-1] (`agent/devops/github-actions-ci`)
- **Verdict:** Changes requested (comment posted — GitHub blocked self-request since QA is on main)
- **Blocking issue:** Frontend CI job (`cd frontend && npm ci`) will always fail because `frontend/` does not exist yet (STORY-14 is a future sprint). Since CI blocks merges on failure, this would prevent ALL PRs from merging. Fix: add `if: hashFiles('frontend/package.json') != ''` guard to the frontend job.
- **Note:** Merge order matters — PR #8 must merge first so `backend/` exists when CI runs.

## Test Coverage Notes (2026-06-13)

| Module | Coverage | Notes |
|--------|----------|-------|
| `app/routers/auth.py` | 100% | Full login happy-path + wrong-password covered |
| `app/routers/odds.py` | 100% | All three endpoints covered with 401/404/happy-path |
| `app/models/schemas.py` | 100% | Validated via response serialization |
| `app/db/models.py` | 100% | Exercised by seeded integration tests |
| `app/dependencies.py` | 73% | Lines 16-20 (get_db generator body), 35-37 (JWTError path) — acceptable |
| `app/main.py` | 84% | Lines 14-16 (lifespan context, scheduler start) — no test starts the server process |
| `app/scheduler.py` | 28% | Intentional — scheduler calls real services; mock tests come in STORY-2/3 |
| `app/services/betfair.py` | 0% | Intentional — mocked unit tests come in STORY-2 |
| `app/services/odds_api.py` | 0% | Intentional — mocked unit tests come in STORY-3 |

**Overall: 65% — acceptable for scaffold baseline**

## Recurring Issues / Patterns Noticed

- **`pytest-cov` not in `requirements.txt`**: The CI workflow (`pytest --cov`) requires it, but it wasn't listed. Pattern to watch: always verify that test tooling deps appear in `requirements.txt`, not just installed in the dev environment.
- **Duplicate deps**: `httpx` appeared twice in `requirements.txt`. Not a runtime bug but makes dep auditing harder.
- **Frontend CI jobs need existence guards**: Until `frontend/` is scaffolded, all frontend CI steps must be guarded with `if: hashFiles('frontend/package.json') != ''` to avoid blocking PRs.
- **DB session isolation in tests**: Direct `SessionLocal()` in fixtures hits the real DB, not the test DB. Always use the `db_session` fixture (which wraps `_TestingSessionLocal`) when seeding integration test data.
