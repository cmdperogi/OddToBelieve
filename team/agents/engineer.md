# Engineer — Status

**Last updated:** 2026-06-16

## Current Task

**STORY-18 second pass (today):** Applied the coordinated dependency bump per the verified version-compatibility chain on issue #24 (Prod Support, 2026-06-16), on branch `agent/engineer/scaffold-fastapi`:

| Package | Was | Now |
|---|---|---|
| `fastapi` | 0.115.0 | 0.137.1 |
| `pydantic` | 2.7.4 | >=2.9.0 |
| `python-multipart` | 0.0.27 | 0.0.31 |

`fastapi==0.137.1` is the first version whose `starlette` constraint (`>=0.46.0`, no upper bound) can resolve to `starlette 1.3.1`, which clears all 11 CVEs from the 2026-06-16 re-scan (7 starlette, 3 python-multipart, plus the pydantic-version conflict that made the previous single-line pin unsatisfiable).

**Verification:**
- `pip-audit -r backend/requirements.txt` → **0 vulnerabilities** (was 11)
- `pytest tests/ -v --cov=app` → **31/31 passed** (27 existing + 4 new). No breakage in `test_security_fixes.py` / `test_scaffold.py` assertions from the pydantic 2.7.4 → 2.9 validation-error-shape change.
- `ruff check . --fix && black .` → clean
- `bandit -r app/` → only the known B106 false positive remains
- Added `backend/tests/unit/test_dependency_versions.py` — regression test asserting installed fastapi/starlette/python-multipart/pydantic versions stay at or above the CVE-free floor.

Pushed to `agent/engineer/scaffold-fastapi` and posted results as a PR #8 comment for AppSec re-scan and QA re-run. This was the sole remaining blocker for PR #8.

Previously completed on this same branch (2026-06-15, still resolved/unaffected by today's change):

| Story | Fix | File(s) |
|-------|-----|---------|
| STORY-15 | Removed hardcoded defaults for `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`; fields now required with `@field_validator` raising `ValueError` if empty | `backend/app/config.py` |
| STORY-16 | Hash admin password at startup with `_pwd_context.hash()`; verify with `_pwd_context.verify()` — no more plain `==` comparison | `backend/app/routers/auth.py` |
| STORY-17 | `python-jose[cryptography]==3.3.0` → `>=3.4.0` (resolves to 3.5.0) | `backend/requirements.txt` |
| STORY-20 | `pytest==8.2.2` → `9.0.3`; `pytest-asyncio==0.23.7` → `1.4.0`; `black==24.4.2` → `26.3.1` | `backend/requirements.txt` |

Additional fixes bundled:
- Pinned `bcrypt==3.2.2` to maintain passlib 1.7.4 compatibility (bcrypt 4.x+ dropped `__about__`)
- Added `os.environ.setdefault(...)` at top of `tests/conftest.py` so required env vars are set before app import
- Added 7 new unit tests in `backend/tests/unit/test_security_fixes.py` covering STORY-15 and STORY-16 ACs

## Last PR

PR #8 — `agent/engineer/scaffold-fastapi` → main
URL: https://github.com/cmdperogi/OddToBelieve/pull/8
Status: STORY-18 coordinated bump pushed 2026-06-16; awaiting AppSec re-scan + QA re-run. All other stories on this PR (15, 16, 17, 20) remain resolved.

## Previous PR

[feat: scaffold FastAPI backend [STORY-13]](https://github.com/cmdperogi/OddToBelieve/pull/8)
Branch: `agent/engineer/scaffold-fastapi`

### What was delivered
- `backend/` created with the full layout from CLAUDE.md
- FastAPI app: JWT auth (`POST /auth/token`), odds routes (`GET /odds/events`, `/odds/events/{id}`, `/odds/events/{id}/markets`), `/health` (no auth required)
- SQLAlchemy ORM: `Event`, `Market`, `Odds` with relationships + `Base.metadata.create_all()`
- Pydantic v2 response schemas in `backend/app/models/schemas.py`
- `BetfairClient` with session-token management and 403 → re-auth retry
- `OddsApiService` with `x-requests-remaining` quota guard (threshold: 50)
- APScheduler hourly poll wired in lifespan context
- `ruff check .` + `black .` → clean
- 9 unit tests passing in `tests/unit/test_scaffold.py`
- `pytest tests/ -v` runs without import errors

## Next Task

After PR #8 merges: **STORY-2** — Implement BetfairClient + unit tests (TDD)
Branch: `agent/engineer/unit-tests-betfair` (to create once unblocked)
