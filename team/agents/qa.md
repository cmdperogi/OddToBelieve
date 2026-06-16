# QA — Status

**Last updated:** 2026-06-16

## PRs Reviewed

### PR #8 — feat: scaffold FastAPI backend [STORY-13] (`agent/engineer/scaffold-fastapi`)

#### 2026-06-13 (initial review)
- **Verdict:** LGTM (comment posted — GitHub blocked self-approve since QA pushed commits to the branch)
- **Tests run:** 20 passed, 0 failed
- **Fixes pushed to branch by QA:** pytest-cov added to requirements, duplicate httpx removed, db_session fixture added, integration tests added (STORY-4)

#### 2026-06-15 (security fixes re-review)
- **Verdict:** LGTM ✅ — review comment posted on PR
- **Tests run:** 27/27 passed (`pytest tests/ -v --cov=app --cov-report=term-missing`)
  - `tests/integration/test_odds_endpoints.py` — 11 passed
  - `tests/unit/test_scaffold.py` — 9 passed
  - `tests/unit/test_security_fixes.py` — 7 passed
- **STORY-15 AC verified:** ✅ `Settings()` with no env vars raises `ValidationError: Field required`; empty strings raise `ValueError` from `field_validator`
- **STORY-16 AC verified:** ✅ `_pwd_context.hash()` at startup, `_pwd_context.verify()` in login; `test_hashed_password_not_plaintext` confirms `$2b$` prefix
- **STORY-17 verified:** ✅ `python-jose[cryptography]>=3.4.0` in requirements
- **STORY-18 verified:** ✅ `python-multipart==0.0.27`, `fastapi==0.115.0`
- **STORY-20 verified:** ✅ `pytest==9.0.3`, `black==26.3.1`
- **Checklist:**
  - ✅ Type annotations throughout; Pydantic v2 style (`field_validator @classmethod`, `model_config` dict)
  - ✅ All route handlers are `async def`
  - ✅ 27 tests pass including happy-path, 401, 404 for every endpoint
- **Non-blocking:** starlette emits `PendingDeprecationWarning` for `python_multipart` import in its own `formparsers.py` — not fixable by us

#### 2026-06-16 (STORY-18 coordinated bump re-review)
- **Verdict:** LGTM ✅ — posted as PR comment (self-approve still blocked, same reason as 2026-06-13)
- **Tests run:** 31/31 passed (`pytest tests/ -v --cov=app --cov-report=term-missing`) — up from 27; Engineer's new `tests/unit/test_dependency_versions.py` (4 tests) pins minimum secure versions for fastapi/starlette/python-multipart/pydantic
- **Pydantic 2.7.4 → 2.9.0 bump:** No validation-error-shape breakage — `test_security_fixes.py` and `test_scaffold.py` assertions all pass unchanged, no action needed
- **Installed versions confirmed:** `fastapi==0.137.1`, `pydantic==2.13.4`, `starlette==1.3.1`, `python-multipart==0.0.31` — matches the verified chain on issue #24
- **`pip-audit -r backend/requirements.txt`:** No known vulnerabilities found (sanity-checked ahead of AppSec's formal scan)
- **Coverage:** 67% overall, unchanged from 2026-06-15 baseline (new tests cover dependency metadata only, not app code paths)
- **Environment note for future QA runs:** the `pytest` binary on PATH (`/root/.local/bin/pytest`) is a `uv tool`-installed isolated environment and does NOT see packages installed via `pip install -r requirements.txt`. Running `pytest tests/ -v ...` directly fails with `ModuleNotFoundError: No module named 'fastapi'` even right after a clean install. **Use `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing` instead** — same flags, correct interpreter.
- STORY-18 is resolved; PR #8 is otherwise unblocked from QA's side. AppSec's formal re-scan/sign-off is the only remaining step before merge.

### PR #9 — chore: add GitHub Actions CI [STORY-1] (`agent/devops/github-actions-ci`)

#### 2026-06-13 (initial review)
- **Verdict:** Changes requested — frontend job missing existence guard
- **Blocking issue:** `cd frontend && npm ci` would always fail without `frontend/`

#### 2026-06-15 (re-review)
- **Verdict:** LGTM ✅ — review comment posted on PR
- **STORY-19 verified:** ✅ All credential-shaped vars now use `${{ secrets.VAR || 'fallback' }}` pattern: `SECRET_KEY`, `ADMIN_PASSWORD`, `BETFAIR_USERNAME`, `BETFAIR_PASSWORD`, `BETFAIR_APP_KEY`
- **Frontend guard:** ✅ `if: hashFiles('frontend/package.json') != ''` prevents frontend job failure
- **Merge dependency noted in PR comment:** PR #9 branch does not include `backend/`; CI backend job will fail until PR #8 lands on main. Documented merge order: PR #8 → PR #9.

#### 2026-06-16 (status check)
- No new commits since the 2026-06-15 LGTM (`89d5422` is still HEAD). No re-review needed; standing LGTM holds.

## Test Coverage Notes (2026-06-15 — 27 tests, security fixes included)

| Module | Coverage | Notes |
|--------|----------|-------|
| `app/config.py` | 100% | All three field validators exercised by security fix tests |
| `app/routers/auth.py` | 100% | Full login happy-path + wrong-password + bcrypt path covered |
| `app/routers/odds.py` | 100% | All three endpoints covered with 401/404/happy-path |
| `app/models/schemas.py` | 100% | Validated via response serialization |
| `app/db/models.py` | 100% | Exercised by seeded integration tests |
| `app/db/database.py` | 100% | |
| `app/dependencies.py` | 73% | Lines 16-20 (get_db body), 35-37 (JWTError path) — acceptable |
| `app/main.py` | 84% | Lines 14-16 (lifespan/scheduler start) — no process-level test |
| `app/scheduler.py` | 28% | Intentional — scheduler calls real services; mock tests in STORY-2/3 |
| `app/services/betfair.py` | 0% | Intentional — mocked unit tests in STORY-2 |
| `app/services/odds_api.py` | 0% | Intentional — mocked unit tests in STORY-3 |

**Overall: 67% — up from 65%, acceptable scaffold baseline**

## Recurring Issues / Patterns Noticed

- **`pytest-cov` not in `requirements.txt`**: Added by QA in initial review. Always verify test tooling deps appear in `requirements.txt`.
- **Duplicate deps**: `httpx` appeared twice in initial `requirements.txt` — cleaned up.
- **Frontend CI jobs need existence guards**: Until `frontend/` is scaffolded, frontend CI steps must use `if: hashFiles('frontend/package.json') != ''` guard. DevOps applied this correctly via PR #23.
- **DB session isolation in tests**: Always use the `db_session` fixture (wraps `_TestingSessionLocal`) when seeding integration test data.
- **Merge order critical for CI**: The CI backend job references `backend/requirements.txt`. PR #8 must land on main before PR #9 merges, or CI will fail on the combined state.
- **`pytest` on PATH is not the project's Python**: `/root/.local/bin/pytest` is a `uv tool` install in its own isolated venv — it never sees `pip install -r requirements.txt` into the system/site Python. Always run `python3 -m pytest ...` in this environment, not bare `pytest`, or you'll get false `ModuleNotFoundError` failures that look like a broken PR but aren't.

## Next Up
- STORY-4 integration tests on `agent/qa/integration-tests-odds` are drafted and ready, but per sprint board this starts only **after STORY-13 (PR #8) merges to main**. PR #8 has not merged yet (AppSec sign-off still pending) — standing by.
