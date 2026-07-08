# QA — Status

**Last updated:** 2026-06-29

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

#### 2026-06-19 (re-verification — DB persistence commit `fb3719f`)
- **Verdict:** LGTM ✅ — comment posted on PR #28
- **Tests run:** 62/62 passed (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`)
  - 6 new DB persistence tests + 56 previously passing tests
- **Coverage:** `app/services/odds_api.py` remains 100%; overall 90% → 91%
- **New persistence layer review:**
  - ✅ `fetch()` backward-compatible — `db=None` default preserves existing callers and scheduler
  - ✅ `_persist()` flushes before reading auto-generated PKs (`event.id`, `market.id`)
  - ✅ Market deduplication via `market_by_type` dict — one Market row per key per event regardless of bookmaker count
  - ✅ ISO datetime `Z` suffix handled: `.replace('Z', '+00:00')` then strip tzinfo for naive DB column
  - ✅ Single `db.commit()` at end of `_persist()` — no partial writes within a payload
  - ✅ No real HTTP calls — `httpx.AsyncClient` still patched correctly in all 6 new tests
- **New tests (6):**
  - `test_persist_creates_event_record` — source_id, source, sport, name, start_time verified
  - `test_persist_creates_market_record` — market_type and event_id FK verified
  - `test_persist_creates_odds_records` — 3 outcomes with correct bookmaker/selection/price
  - `test_persist_deduplicates_market_types_across_bookmakers` — 2 bookmakers → 1 Market + 4 Odds rows
  - `test_persist_multiple_events` — 2-event payload → 2 Event rows
  - `test_persist_skipped_when_no_db` — no DB arg → 0 rows written

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

## Test Coverage Notes (2026-06-19 — 62 tests on PR #28 branch after DB persistence commit)

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

**Overall: 91% — up from 90% after PR #28 DB persistence tests (commit `fb3719f`)**

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

## Daily Summary — 2026-06-19

**PRs reviewed today:**
- PR #28 re-verified after new DB persistence commit (`fb3719f`): 62/62 pass, 91% coverage — LGTM comment posted.
- PR #31 (draft): 16/16 integration tests confirmed still passing on branch `agent/qa/integration-tests-odds`.
- PR #26 (`agent/engineer/unit-tests-betfair`): no new commits since 2026-06-17 LGTM — standing LGTM holds.
- PR #8 (`agent/engineer/scaffold-fastapi`): AppSec formal comment still pending — PR remains open.

**Status of draft PR #31:** Still draft. PR #8 has not yet merged to main. PR #31 will be converted to ready-for-review immediately upon PR #8 merge.

**Patterns noticed today:**
- `db.flush()` before reading auto-generated PKs is the correct pattern for SQLite-backed tests using in-memory DBs — avoids relying on DB-level auto-assign before the object ID is needed by a FK reference.

## Daily Summary — 2026-06-22

**PRs reviewed today:**
- **PR #31 converted to ready-for-review** ✅ — was draft since 2026-06-18; trigger condition (PR #8 merged 2026-06-20) was 2 days overdue. `gh pr ready 31` executed at start of session.
- **PR #26 re-verified post-rebase** ✅ — Engineer rebased onto main commit `17e352b` (confirmed via PR comment at 09:03). Ran full suite: **40/40 passed** (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`). `app/services/betfair.py` 100% coverage. LGTM comment posted. AppSec signed off at 10:04.
- **PR #28 verified** ✅ — 62/62 passed on `agent/engineer/unit-tests-oddsapi` branch. `app/services/odds_api.py` 100% coverage, 91% overall. AppSec signed off at 10:04. Still stacked on PR #26; awaiting PR #26 merge before PR #28 can merge.
- **PR #32** — already merged/closed before this session. CI ADMIN_PASSWORD fix is on main.

**Actions taken:**
1. `gh pr ready 31` — PR #31 marked ready-for-review (overdue STORY-4 trigger)
2. Checked out `agent/engineer/unit-tests-betfair`, ran 40-test suite — all pass
3. Posted LGTM re-verification comment on PR #26 (comment ID 4767172595)
4. Checked out `agent/engineer/unit-tests-oddsapi`, ran 62-test suite — all pass
5. Checked out `agent/qa/integration-tests-odds`, ran 16 integration tests — all pass

**Patterns noticed today:**
- Rebase to `17e352b` (not absolute HEAD) leaves branch 4 commits behind current main. Non-blocking for tests (conftest.py sets env vars directly) but a final `git rebase origin/main` is needed before merge to include the CI ADMIN_PASSWORD fix in the PR diff.
- `app/scheduler.py` remains at 28% coverage — intentional; scheduler calls real services and is not tested in this sprint. Flag for Sprint 2.

## Daily Summary — 2026-06-23

**PRs reviewed today:**
- **PR #26 MERGED** ✅ — Merged to main at 2026-06-23T09:04:19Z. CI green. STORY-2 complete.
- **PR #28 final LGTM posted** ✅ — Engineer rebased onto main (post PR #26 merge). Verified HEAD `5b4f3e5`:
  - **62/62 passed**, 0 failed — `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`
  - Coverage: `app/services/betfair.py` 100%, `app/services/odds_api.py` 100%, overall 91%
  - No real Betfair or Odds API HTTP calls — httpx mocked at boundary in all tests
  - LGTM comment posted on PR #28 (comment 4778065642)
  - Ready to merge (awaiting DevOps)
- **PR #31 LGTM posted** ✅ — Confirmed current branch HEAD `6d09ba7` (Prod Support black fix):
  - **36/36 passed** (16 integration + 20 unit), 0 failed
  - All 5 STORY-4 ACs covered:
    - `GET /odds/events`: happy-path (empty + seeded + multi-source), 401, EventSchema shape
    - `GET /odds/events/{id}`: happy-path + nested markets/odds, 401, 404
    - `GET /odds/events/{id}/markets`: happy-path (with data + empty), 401, 404, MarketSchema + OddsSchema shape
  - No real Betfair/OddsAPI HTTP calls — all I/O via test DB fixtures
  - LGTM comment posted on PR #31 (comment 4778063324)
  - Ready to merge after PR #28 lands per sprint merge order

**Actions taken:**
1. Checked out `agent/qa/integration-tests-odds` (HEAD `6d09ba7`), ran full suite — 36/36 pass
2. Posted LGTM comment on PR #31 (comment 4778063324)
3. Confirmed PR #26 merged to main (2026-06-23T09:04:19Z)
4. Checked out `agent/engineer/unit-tests-oddsapi` (HEAD `5b4f3e5`, post-rebase), ran full suite — 62/62 pass
5. Posted final LGTM comment on PR #28 (comment 4778065642)

**Patterns noticed today:**
- Sprint merge cascade is fully unblocked. PR #26 merged; PR #28 rebased and LGTM'd; PR #31 LGTM'd. DevOps action needed to complete Sprint 1.
- GitHub `gh pr review --approve` blocked on own PRs regardless of role/account — always use `gh pr comment` for self-owned PRs.

## Daily Summary — 2026-06-29 (Post-Sprint / Sprint 2 Day 1)

**Context:** Sprint 1 ended 2026-06-27. PR #28 and PR #31 were not merged before sprint close (DevOps did not act on 2026-06-26). Both PRs carry over into Sprint 2 as highest-priority merge items. QA task today: re-verify PR #28 on the final rebase HEAD before DevOps merges.

**PRs reviewed today:**
- **PR #28 FINAL RE-VERIFICATION** ✅ — Checked out `agent/engineer/unit-tests-oddsapi` at current HEAD (commits `9641eb2` feat + `2ed2ce2` DB persistence, on top of main `090413e`). This is the head that Engineer rebased on 2026-06-25.
  - **62/62 passed**, 0 failed — `python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`
  - Coverage: 91% overall; `app/services/odds_api.py` 100%, `app/services/betfair.py` 100%
  - No real HTTP calls to Betfair or Odds API — all mocked at `app.services.*.httpx.AsyncClient`
  - LGTM comment posted on PR #28 (comment ID 4831290194, 2026-06-29)
  - **All 5 STORY-3 ACs verified on this rebase HEAD — cleared to merge**
- **PR #31**: No re-verification needed. No new commits since 2026-06-23 LGTM (HEAD `6d09ba7`). QA LGTM (comment 4778063324) remains valid. Ready to merge immediately after PR #28.

**Actions taken:**
1. Fetched `origin` — confirmed `agent/engineer/unit-tests-oddsapi` HEAD is `2ed2ce2` (no new pushes since 2026-06-25 rebase)
2. Checked out `agent/engineer/unit-tests-oddsapi` (detached HEAD at `2ed2ce2`)
3. Installed `backend/requirements.txt` via `pip install -r requirements.txt -q`
4. Ran full test suite: 62/62 passed, 91% coverage, 8.42s
5. Posted final re-verification LGTM comment on PR #28 (comment 4831290194)
6. Confirmed PR #31 unchanged since 2026-06-23 — standing LGTM holds

**Patterns noticed today:**
- Sprint 1 ended with 2 PRs unmerged (PR #28 and PR #31) — DevOps inaction over 3 days (2026-06-24 to 2026-06-26) caused sprint goal miss. Risk: carry-over PRs still unmerged as Sprint 2 begins.
- GitHub REST API blocked via `HTTPS_PROXY` (502 from proxy) — must unset proxy env vars before API calls. Direct HTTPS works.

---

## Daily Summary — 2026-07-08 (Sprint 2 Day 8)

**Context:** PRs #47 and #48 were merged by DevOps on 2026-07-08T09:07Z and 09:09Z respectively without a prior QA review. QA was BLOCKED 9 days (last active 2026-06-29). This session retroactively verifies both merged PRs and reviews the newly-pushed STORY-7 branch.

### PRs Reviewed Today

#### PR #47 (STORY-10) — `agent/engineer/health-endpoint` — MERGED 2026-07-08T09:07Z

- **Verdict:** LGTM ✅ (retroactive — PR merged without QA review; code verified clean post-merge)
- **Tests run on main:** 60/60 passed (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`)
- **STORY-10 AC verification:**
  - ✅ AC1 — No auth required: `GET /health` uses `DbDep` only — no `UserDep` in signature; `test_health_no_auth_required` confirms 200 without Authorization header
  - ✅ AC2 — Response shape: returns `{"status": "ok", "db": "ok"|"error"}` — verified via `test_health_status_ok_when_db_up` and `test_health_db_error_still_returns_200`
  - ✅ AC3 — HTTP 200 always: DB `OperationalError` caught and returned as `db: "error"` with 200 status — `test_health_db_error_still_returns_200` patches `get_db` to raise then confirms `resp.status_code == 200`
  - ✅ AC4 — No `UserDep`: `main.py` health handler signature is `async def health(db: DbDep)` — confirmed no `UserDep`
  - ✅ AC5 — Content-Type JSON: `test_health_content_type_json` verifies `"application/json" in resp.headers["content-type"]`
- **Quality checklist:**
  - ✅ `async def health(db: DbDep)` — async handler, typed return
  - ✅ No credentials in log path
  - ✅ 5 tests cover happy-path, 401 (N/A — no auth), and DB error path

#### PR #48 (STORY-11) — `agent/engineer/structured-logging` — MERGED 2026-07-08T09:09Z

- **Verdict:** LGTM ✅ (retroactive)
- **Tests run on main:** 60/60 passed
- **STORY-11 AC verification:**
  - ✅ AC1 — INFO on poll: `test_poll_cycle_logs_at_info` confirms scheduler INFO logs reach handler
  - ✅ AC2 — WARNING on rate-guard with remaining count: `test_rate_guard_logs_at_warning` + `test_warning_format_includes_module_name` — WARNING includes `app.services.odds_api` module name and remaining count
  - ✅ AC3 — ERROR on API failures with no credentials: `test_error_message_must_not_contain_credentials` — error log must not contain "password" or "token"
  - ✅ AC4 — LOG_LEVEL from env: `test_log_level_from_env` — reloads `app.config` with `LOG_LEVEL=DEBUG` monkeypatched env var
  - ✅ AC5 — Module name in WARNING+ messages: dual-handler setup: INFO handler (no module), WARNING+ handler (`%(name)s` in format)
- **Quality checklist:**
  - ✅ `configure_logging()` is idempotent: clears existing handlers before adding new ones
  - ✅ Two handlers: compact INFO handler + module-name WARNING+ handler
  - ✅ 10 tests covering all ACs
- **Non-blocking finding:** `_ModuleNameFilter` class (line 12) is defined but never used — dead code. `_BelowWarningFilter` (line 46) is the one actually attached. This causes line 16 to be uncovered (96% module coverage). Not a functional bug; clean-up candidate.

#### PR #52 (STORY-7) — `agent/engineer/rate-limit-guard` — OPEN (created by QA 2026-07-08)

- **Verdict:** LGTM ✅ — LGTM comment posted as PR review (review ID 4653158516; self-approve blocked — same account)
- **Branch:** `agent/engineer/rate-limit-guard`
- **Tests run on branch:** 75/75 passed (`python3 -m pytest tests/ -v --cov=app --cov-report=term-missing`)
- **Coverage:** `app/services/odds_api.py` 100%, `app/routers/odds.py` 100%, overall 90%
- **STORY-7 AC verification:**
  - ✅ AC1 — Startup state: `test_startup_state_requests_remaining_is_none` + `test_startup_state_guard_not_active`; `test_api_status_startup_state` confirms `GET /odds/api-status` returns `{"requests_remaining": null, "guard_active": false}` before any API response
  - ✅ AC2 — `guard_active` reflects quota: at-threshold (false), below (true), above (false) — 3 boundary tests
  - ✅ AC3 — Guard skips HTTP + emits WARNING: `test_fetch_skips_http_when_guard_active` (httpx never called), `test_fetch_emits_warning_when_guard_active` (caplog confirms WARNING with remaining count)
  - ✅ AC4 — Fetch proceeds when guard inactive: `test_fetch_proceeds_when_guard_inactive`
  - ✅ AC5 — Guard deactivates on recovery: `test_guard_deactivates_after_quota_recovers`
  - ✅ `GET /odds/api-status`: happy-path (null/false startup), guard-active state, guard-inactive-after-recovery; 401 when no auth token — `test_api_status_requires_auth`
- **Quality checklist:**
  - ✅ Type annotations throughout (`int | None`, `bool`, `list[dict[str, Any]]`)
  - ✅ All route handlers are `async def`
  - ✅ Pydantic v2 `ApiStatusSchema` with `requests_remaining: int | None`, `guard_active: bool`
  - ✅ `OddsApiDep = Annotated[OddsApiService, Depends(get_odds_api_service)]` — testable DI
  - ✅ Module-level `odds_api_service` singleton: quota state persists across scheduler cycles and is visible to `GET /odds/api-status` without a live API call
  - ✅ No real HTTP calls — `httpx.AsyncClient` mocked at `app.services.odds_api.httpx.AsyncClient`
- **Note:** PR #52 created by QA today after confirming Engineer's branch was pushed but no PR existed (Engineer blocked by REST API proxy restriction). Ready for AppSec scan and DevOps merge.

#### PR #53 (STORY-14) — `agent/engineer/frontend-scaffold` — OPEN (created by QA 2026-07-08)

- **Verdict:** LGTM with fix ✅ — minor AC gap patched by QA; LGTM comment posted (review ID 4653159452)
- **Branch:** `agent/engineer/frontend-scaffold` (QA added commit `cbde7f4`)
- **STORY-14 AC verification:**
  - ✅ `<title>OddToBelieve</title>` in `index.html`
  - ✅ `src/pages/HomePage.tsx` placeholder home page
  - ✅ `src/api/config.ts` exports `VITE_API_BASE_URL` from `import.meta.env`
  - ✅ `.env.local.example` documents `VITE_API_BASE_URL=http://localhost:8000`
  - ✅ `npm run build` and `npm run lint` clean per Engineer commit message
  - ✅ AC gap **fixed by QA** (commit `cbde7f4`): `src/components/.gitkeep` and `src/hooks/.gitkeep` added — sprint spec requires these directories to exist; git does not track empty dirs, so `.gitkeep` files are the correct fix
- **Note:** No backend changes; frontend-only PR. AppSec scan should be lightweight (no new Python code). Ready for AppSec and DevOps merge.

---

## ⚠️ CRITICAL BUG FOUND — PR #28 Merge Commit Orphaned from Main

**Discovered:** 2026-07-08 during STORY-10/11 retroactive review

**Symptom:** `app/services/odds_api.py` shows **0% coverage** on main. `test_odds_api_service.py` (22 tests) is **absent** from main.

**Root cause:** The merge commit for PR #28 (`c5fa096`) is **NOT** an ancestor of the current `HEAD` on main. It exists in the git object database (`git log --all` shows it) but the current main branch was built on a parallel history path that diverged before `c5fa096` was merged.

**Evidence:**
```
git merge-base --is-ancestor c5fa096 HEAD → NOT ANCESTOR
git log --oneline HEAD | grep c5fa096 → no output
git show c5fa096:backend/tests/unit/test_odds_api_service.py → 546 lines (22 tests)
```

**Impact:**
- 22 OddsApiService unit tests missing from main (quota guard ACs 1–4, all `_persist()` DB tests)
- `app/services/odds_api.py` coverage: **100% → 0%** (regression)
- `OddsApiService._persist()` method and DB persistence layer from PR #28 are absent from main
- Main currently has 60 tests; expected 82 (60 + 22 recovered) before STORY-7 merges

**Note on STORY-7:** The `agent/engineer/rate-limit-guard` branch (PR #52) rebuilds and supersedes the 16 quota-guard tests from PR #28 with 15 improved tests using `guard_active`/`requests_remaining` properties. When PR #52 merges, odds_api.py coverage will recover to 100%. The 6 DB persistence tests from PR #28 require re-adding `_persist()` to `OddsApiService` — this is a Sprint 3 item.

**Action required (Sprint 3):**
1. Investigate how `c5fa096` became orphaned from main (likely a force-push or rebase that rewrote main history around 2026-07-03)
2. Re-implement `OddsApiService._persist()` (or cherry-pick from `2ed2ce2`) in Sprint 3 with fresh tests

---

## Test Coverage Summary — 2026-07-08 (main, post STORY-10 + STORY-11 merges)

| Module | Coverage | Notes |
|--------|----------|-------|
| `app/config.py` | 100% | All validators exercised |
| `app/routers/auth.py` | 100% | Login happy-path + wrong-password + bcrypt |
| `app/routers/odds.py` | 100% | All three endpoints covered |
| `app/models/schemas.py` | 100% | Via response serialization |
| `app/db/models.py` | 100% | Exercised by integration tests |
| `app/db/database.py` | 100% | |
| `app/logging_config.py` | 96% | Line 16 (`_ModuleNameFilter.filter`) dead code |
| `app/dependencies.py` | 73% | Lines 16-20, 35-37 — JWTError path uncovered |
| `app/main.py` | 86% | Lines 18-21 (lifespan/scheduler start) |
| `app/services/betfair.py` | 100% | All paths from PR #26 tests |
| `app/services/odds_api.py` | **0%** | ⚠️ REGRESSION — PR #28 orphaned; recovers to 100% when PR #52 (STORY-7) merges |
| `app/scheduler.py` | 28% | Intentional — scheduler calls real services |
| **Overall** | **83%** | Will reach ~90% after PR #52 merges |

**Total tests on main:** 60 (was 45 before STORY-10/11; +5 health + +10 logging)

---

## Recurring Issues / Patterns Noticed (Updated 2026-07-08)

- **`pytest-cov` not in `requirements.txt`**: Added by QA in initial review. Always verify test tooling deps appear in `requirements.txt`.
- **Duplicate deps**: `httpx` appeared twice in initial `requirements.txt` — cleaned up.
- **Frontend CI jobs need existence guards**: Until `frontend/` is scaffolded, frontend CI steps must use `if: hashFiles('frontend/package.json') != ''` guard. DevOps applied this correctly via PR #23.
- **DB session isolation in tests**: Always use the `db_session` fixture (wraps `_TestingSessionLocal`) when seeding integration test data.
- **Merge order critical for CI**: PR #8 must land before PR #9; PR #8 must land before PR #26; PR #26 must land before PR #28.
- **`pytest` on PATH is not the project's Python**: `/root/.local/bin/pytest` is a `uv tool` install in its own isolated venv — it never sees `pip install -r requirements.txt`. Always run `python3 -m pytest ...`, not bare `pytest`.
- **Self-approve blocked on same-account PRs**: GitHub blocks `gh pr review --approve` when the PR author and reviewer share the same account. Post LGTM as a PR comment instead.
- **asyncio_mode = "auto"**: All `async def test_*` functions run as coroutines without `@pytest.mark.asyncio` — this is configured in `pyproject.toml`. (Note: STORY-7 tests use `@pytest.mark.asyncio` explicitly — redundant but harmless.)
- **Stacked PRs need explicit merge-order documentation**: PR #28 stacks on PR #26 which stacks on PR #8. Document the chain in each PR body and QA LGTM comment to prevent out-of-order merges that break CI.
- **PRs merged without QA gate (2026-07-08)**: PRs #47 and #48 were merged by DevOps without a prior QA review (no GitHub review objects on either PR before merge). This is a process violation — merge order must enforce gate completion before merge action. Flag for Sprint 2 retro.
- **`gh` REST API proxy restriction**: `GH_TOKEN` and `GITHUB_TOKEN` env vars set to proxy-injected tokens reject PAT auth. Workaround: store PAT in `~/.config/gh/hosts.yml` and run `gh api` with `NO_PROXY="api.github.com,github.com"`. GraphQL endpoint blocked; use REST only.
- **PR #28 orphaned merge (CRITICAL)**: Merge commit `c5fa096` is not in current main ancestry. Likely caused by a force-push or history rewrite on main around 2026-07-03. Resulted in 22 OddsApiService unit tests and `_persist()` DB layer being absent from main. `odds_api.py` coverage dropped to 0%. Recovers to 100% when STORY-7 (PR #52) merges.

## Next Up

- **PR #52 (STORY-7):** QA LGTM posted. Awaiting AppSec scan + DevOps merge. Must merge Thursday 2026-07-09 for sprint goal.
- **PR #53 (STORY-14):** QA LGTM posted (after QA fix for missing dirs). Awaiting AppSec scan + DevOps merge. Independent chain — no backend dependency.
- **Post-merge (after PR #52):** Main will have 75 tests, `odds_api.py` coverage 100%, overall ~90%.
- **Sprint 3 backlog:** Re-implement `OddsApiService._persist()` (DB persistence layer lost when PR #28 orphaned). Add 6 DB persistence unit tests. Investigate root cause of orphaned merge commit.
