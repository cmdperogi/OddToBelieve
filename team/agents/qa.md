# QA — Status

**Last updated:** 2026-06-18

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

---

### PR #26 — feat: BetfairClient unit tests [STORY-2] (`agent/engineer/unit-tests-betfair`)

#### 2026-06-17 (review)
- **Verdict:** LGTM ✅ — posted as PR comment (self-approve blocked for same-account PRs)
- **Tests run:** 40/40 passed (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`)
  - 9 new BetfairClient unit tests + 31 existing
- **Coverage:** `app/services/betfair.py` 0% → 100%; overall 67% → 82%
- **STORY-2 AC verification:**
  - ✅ AC1 — `test_login_success_stores_and_returns_session_token`: token stored in `_session_token` and returned
  - ✅ AC2 — `test_post_403_reauthenticates_and_retries_exactly_once`: exactly 3 HTTP calls (initial→403, re-auth login, retry)
  - ✅ AC3 — `test_login_fail_status_raises_runtime_error` + `test_login_error_field_included_in_runtime_error`
  - ✅ AC4 — `test_list_events_returns_correct_keys_and_values` + empty + missing-fields variants; all 4 keys mapped
  - ✅ AC5 — entire suite patches `app.services.betfair.httpx.AsyncClient`; zero real HTTP calls
- **Quality checklist:**
  - ✅ Type annotations throughout (`str | None`, `list[str]`, `list[dict[str, Any]]`)
  - ✅ All BetfairClient methods are `async def`
  - ✅ Credentials never in assertions, fixtures, or log output
- **Non-blocking:** StarletteDeprecationWarning about httpx/httpx2 is a system-level package conflict, not introduced by this PR
- **Merge dependency:** Needs rebase onto main after PR #8 merges. Merge order: PR #8 → PR #26

---

### PR #28 — feat: OddsApiService unit tests [STORY-3] (`agent/engineer/unit-tests-oddsapi`)

#### 2026-06-18 (review)
- **Verdict:** LGTM ✅ — posted as PR comment (self-approve blocked — same account)
- **Tests run:** 56/56 passed (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`)
  - 16 new OddsApiService unit tests + 40 previously passing tests
- **Coverage:** `app/services/odds_api.py` 0% → 100%; overall 82% → 90%
- **STORY-3 AC verification:**
  - ✅ AC1 — `test_quota_guard_blocks_*` (4 tests): guard blocks HTTP call and logs WARNING when `_requests_remaining < 50`, tested at 49, 0, 1, and general below-threshold
  - ✅ AC2 — `test_fetch_proceeds_*` (6 tests): fetch proceeds when `remaining >= 50` or `None`; `x-requests-remaining` header updates internal state; absent header leaves state unchanged
  - ✅ AC3 — `test_fetch_returns_parsed_*` (4 tests): full bookmaker/market/outcome structure verified, multi-event case, empty list case
  - ✅ AC4 — `test_no_real_http_calls_reach_odds_api` + `test_quota_guard_prevents_any_http_call_when_low`: `httpx.AsyncClient` patched at `app.services.odds_api.httpx.AsyncClient`; Odds API key never in assertions; 0 real HTTP calls
- **Quality checklist:**
  - ✅ Type annotations throughout (`str | None`, `tuple[MagicMock, MagicMock]`, `list`)
  - ✅ All test functions are `async def`
  - ✅ URL path and query params (`regions`, `markets`) verified via `call_args` introspection
  - ✅ Patch target correct: `app.services.odds_api.httpx.AsyncClient`
- **Merge dependency:** PR #8 → PR #26 → PR #28. Merge order must be respected.

---

## STORY-4 Integration Tests — `agent/qa/integration-tests-odds` (2026-06-17)

**Branch pushed:** `agent/qa/integration-tests-odds` (based on `agent/engineer/scaffold-fastapi`)
**Tests:** 16/16 passing (up from 11 — added 5 schema-shape tests)
**File:** `backend/tests/integration/test_odds_endpoints.py`

New tests added 2026-06-17:
- `test_list_events_event_schema_shape` — verifies `source_id`, `start_time`, `markets` in list response
- `test_get_event_schema_shape` — verifies all EventSchema fields in detail response
- `test_list_markets_market_schema_shape` — verifies `id`, `market_type`, `odds` in markets list
- `test_list_markets_odds_schema_shape` — verifies all OddsSchema fields (`id`, `bookmaker`, `selection`, `value`, `fetched_at`)
- `test_list_events_returns_multiple_events` — multi-sport/source fixture covers list-all behaviour

All 5 STORY-4 ACs now fully covered with explicit schema-field assertions.
**Awaiting PR #8 merge** before this branch can be merged to main.

## STORY-4 PR Opened (2026-06-18)

**PR #31 opened as draft:** `agent/qa/integration-tests-odds` → `main`
- URL: https://github.com/cmdperogi/OddToBelieve/pull/31
- Tests: 16/16 passing (verified 2026-06-18)
- Opened as draft because PR #8 has not yet merged; merge dependency documented in PR body
- Review can proceed in advance of the merge

---

## Test Coverage Notes (2026-06-18 — 56 tests on PR #28 branch)

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
| `app/services/betfair.py` | 100% | All paths covered by PR #26 (9 unit tests) |
| `app/services/odds_api.py` | 100% | All paths covered by PR #28 (16 unit tests) |

**Overall: 90% — up from 82% after PR #28 OddsApiService unit tests**

---

## Recurring Issues / Patterns Noticed

- **`pytest-cov` not in `requirements.txt`**: Added by QA in initial review. Always verify test tooling deps appear in `requirements.txt`.
- **Duplicate deps**: `httpx` appeared twice in initial `requirements.txt` — cleaned up.
- **Frontend CI jobs need existence guards**: Until `frontend/` is scaffolded, frontend CI steps must use `if: hashFiles('frontend/package.json') != ''` guard. DevOps applied this correctly via PR #23.
- **DB session isolation in tests**: Always use the `db_session` fixture (wraps `_TestingSessionLocal`) when seeding integration test data.
- **Merge order critical for CI**: PR #8 must land before PR #9; PR #8 must land before PR #26; PR #26 must land before PR #28.
- **`pytest` on PATH is not the project's Python**: `/root/.local/bin/pytest` is a `uv tool` install in its own isolated venv — it never sees `pip install -r requirements.txt`. Always run `python3 -m pytest ...`, not bare `pytest`.
- **Self-approve blocked on same-account PRs**: GitHub blocks `gh pr review --approve` when the PR author and reviewer share the same account. Post LGTM as a PR comment instead.
- **asyncio_mode = "auto"**: All `async def test_*` functions run as coroutines without `@pytest.mark.asyncio` — this is configured in `pyproject.toml`.
- **Stacked PRs need explicit merge-order documentation**: PR #28 stacks on PR #26 which stacks on PR #8. Document the chain in each PR body and QA LGTM comment to prevent out-of-order merges that break CI.

## Next Up

- **STORY-4** (`agent/qa/integration-tests-odds`): Draft PR #31 open. Merge blocked until PR #8 lands. Mark PR ready-for-review immediately when PR #8 merges.
- **STORY-3 QA**: PR #28 LGTM posted. Needs rebase onto PR #26 and then main once PR #8 → PR #26 merge chain completes.
- **AppSec gate**: PR #8 formal re-scan is the only sprint blocker. Sprint goal at risk if AppSec does not post results by 2026-06-19.
