# Engineer — Status

**Last updated:** 2026-07-08

## Current Tasks

### STORY-7: Rate limit guard for OddsApiService — BRANCH PUSHED ✅

**Branch:** `agent/engineer/rate-limit-guard`
**PR:** Awaiting manual creation — GitHub REST API blocked by session proxy (repository not registered). Branch pushed to `origin/agent/engineer/rate-limit-guard`. Create PR at: https://github.com/cmdperogi/OddToBelieve/pull/new/agent/engineer/rate-limit-guard

**What was done:**
- Added `guard_active: bool` property and `requests_remaining: int | None` property to `OddsApiService`
- Replaced inline guard logic with `guard_active` property call in `fetch()`
- Exposed module-level singleton `odds_api_service` so quota state persists across scheduler poll cycles and is readable by the router
- Added `ApiStatusSchema` Pydantic v2 model (`requests_remaining: int | None`, `guard_active: bool`)
- Added `GET /odds/api-status` endpoint (JWT-protected) in `backend/app/routers/odds.py` — startup state returns `{"requests_remaining": null, "guard_active": false}`
- Updated scheduler (`backend/app/scheduler.py`) to use the singleton instead of creating a new `OddsApiService()` instance per poll
- Added `get_odds_api_service()` dependency function and `OddsApiDep` annotated type in `backend/app/dependencies.py`
- Added `backend/tests/unit/test_rate_limit_guard.py` with 15 unit tests covering all 5 STORY-7 ACs
- 75/75 tests passing; 90% coverage; ruff + black clean

**All 5 STORY-7 ACs implemented:**
1. ✅ Guard skips HTTP call + emits WARNING when `requests_remaining < 50`
2. ✅ `GET /odds/api-status` returns `{"requests_remaining": null|<n>, "guard_active": false|true}`
3. ✅ Startup state (no API response yet): `{"requests_remaining": null, "guard_active": false}`
4. ✅ Guard active: `{"requests_remaining": <n>, "guard_active": true}`
5. ✅ Guard auto-deactivates when quota recovers to >= 50

---

### STORY-14: Scaffold React/Vite frontend — BRANCH PUSHED ✅

**Branch:** `agent/engineer/frontend-scaffold`
**PR:** Awaiting manual creation — GitHub REST API blocked by session proxy. Branch pushed to `origin/agent/engineer/frontend-scaffold`. Create PR at: https://github.com/cmdperogi/OddToBelieve/pull/new/agent/engineer/frontend-scaffold

**What was done:**
- Bootstrapped `frontend/` with `npm create vite@latest frontend -- --template react-ts`
- Created required directories: `src/pages/`, `src/components/`, `src/hooks/`, `src/api/`
- Set `<title>OddToBelieve</title>` in `frontend/index.html` (replaces Vite default "frontend")
- Replaced Vite default starter `App.tsx` with a minimal `HomePage` component (no Vite branding)
- Added `src/api/config.ts` exporting `API_BASE_URL = import.meta.env.VITE_API_BASE_URL` — no hardcoded localhost URLs in source
- Added `.env.local.example` documenting `VITE_API_BASE_URL=http://localhost:8000`
- `npm run build` → success (no errors)
- `npm run lint` → 0 errors
- All 8 STORY-14 ACs met

---

## Blocker: GitHub REST API

The session proxy blocks GitHub REST API calls to `cmdperogi/OddToBelieve` — both the session-injected token and the provided PAT return "GitHub access to this repository is not enabled for this session." Git push (CONNECT tunnel) works; REST API (HTTPS relay) does not. Both PRs need to be created manually by a human or by adding the repository to the session.

**Manual PR creation URLs:**
- STORY-7: https://github.com/cmdperogi/OddToBelieve/pull/new/agent/engineer/rate-limit-guard
- STORY-14: https://github.com/cmdperogi/OddToBelieve/pull/new/agent/engineer/frontend-scaffold

## Merge Readiness

| Branch | Story | Status |
|--------|-------|--------|
| `agent/engineer/rate-limit-guard` | STORY-7 | ✅ Pushed — awaiting manual PR creation + QA LGTM + AppSec CLEAR |
| `agent/engineer/frontend-scaffold` | STORY-14 | ✅ Pushed — awaiting manual PR creation + QA LGTM + AppSec CLEAR |
| [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) | STORY-10 | 🔄 Open — awaiting QA LGTM + AppSec CLEAR |
| [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) | STORY-11 | 🔄 Open — awaiting QA LGTM + AppSec CLEAR |

## Next Tasks

- **STORY-21a**: Deferred to Sprint 3 — per sprint board, insufficient time for merge cycle in Sprint 2.
- No new engineer tasks this sprint.

## Previous Tasks

- **STORY-10 (2026-07-02):** PR #47 open. 45/45 tests passing, all 5 ACs. Awaiting QA + AppSec.
- **STORY-11 (2026-07-02):** PR #48 open. 50/50 tests passing, all ACs. Awaiting QA + AppSec.
- **STORY-3 rebase (2026-06-25):** PR #28 rebased onto `090413e`. 62/62 passing, 91% coverage. All gates clear; DevOps stall blocking merge.
- **STORY-2 (merged 2026-06-23):** PR #26 merged. BetfairClient unit tests. 40/40 passing, 100% betfair.py coverage.
