# Engineer — Status

**Last updated:** 2026-07-02

## Current Tasks

### STORY-10: Add /health endpoint — PR OPEN ✅

**Branch:** `agent/engineer/health-endpoint`
**PR:** [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) — open, awaiting QA LGTM + AppSec CLEAR

**What was done:**
- Updated `GET /health` in `backend/app/main.py` to inject `DbDep` (no `UserDep`)
- Executes `SELECT 1` to probe DB; returns `{"status": "ok", "db": "ok"|"error"}`
- HTTP 200 always returned regardless of DB state
- Updated `test_scaffold.py::test_health_no_auth` to match new response shape
- Added `backend/tests/unit/test_health_endpoint.py` with 5 targeted unit tests
- All 5 STORY-10 ACs covered; 45/45 tests pass; ruff + black clean

### STORY-11: Add structured logging — PR OPEN ✅

**Branch:** `agent/engineer/structured-logging`
**PR:** [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) — open, awaiting QA LGTM + AppSec CLEAR

**What was done:**
- Added `log_level: str = "INFO"` to `Settings` in `backend/app/config.py` (reads from `LOG_LEVEL` env var)
- Created `backend/app/logging_config.py` with `configure_logging(log_level)`:
  - INFO and below: compact format `LEVEL: message`
  - WARNING and above: includes module name `LEVEL [module.path]: message`
  - Two handlers on root logger (split at WARNING boundary)
  - Invalid log level strings fall back to INFO
- Wired `configure_logging(settings.log_level)` into app lifespan in `main.py`
- Existing log sites in `scheduler.py`, `betfair.py`, `odds_api.py` already emit at correct levels
- Added `backend/tests/unit/test_structured_logging.py` with 10 unit tests
- 50/50 tests pass; ruff + black clean

## Merge Readiness

| PR | Story | Status |
|----|-------|--------|
| [#28](https://github.com/cmdperogi/OddToBelieve/pull/28) | STORY-3 | ✅ All gates clear — awaiting DevOps merge |
| [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) | STORY-10 | 🔄 Open — awaiting QA LGTM + AppSec CLEAR |
| [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) | STORY-11 | 🔄 Open — awaiting QA LGTM + AppSec CLEAR |

## Next Tasks

- **STORY-14**: Scaffold React/Vite frontend (`agent/engineer/frontend-scaffold`) — unblocked, safe to start
- **STORY-7 / STORY-21a**: Blocked on PR #28 merging to main (DevOps stall)

## Previous Tasks

- **STORY-3 rebase (2026-06-25):** PR #28 rebased onto `090413e`. 62/62 passing, 91% coverage. All gates clear; DevOps stall blocking merge.
- **STORY-2 (merged 2026-06-23):** PR #26 merged. BetfairClient unit tests. 40/40 passing, 100% betfair.py coverage.
