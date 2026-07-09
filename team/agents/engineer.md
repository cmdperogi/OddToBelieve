# Engineer — Status

**Last updated:** 2026-07-09

## Current Tasks

### STORY-7: Rate limit guard for OddsApiService — PR #52 OPEN / AWAITING APPSEC ✅

**Branch:** `agent/engineer/rate-limit-guard`
**PR:** [#52](https://github.com/cmdperogi/OddToBelieve/pull/52)
**Status:** QA LGTM ✅ (posted 2026-07-08, review ID 4653158516) — AppSec CLEAR is the sole remaining gate.

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

### STORY-14: Scaffold React/Vite frontend — PR #53 OPEN / AWAITING APPSEC ✅

**Branch:** `agent/engineer/frontend-scaffold`
**PR:** [#53](https://github.com/cmdperogi/OddToBelieve/pull/53)
**Status:** QA LGTM ✅ (posted 2026-07-08, review ID 4653159452) — AppSec CLEAR is the sole remaining gate.

**What was done:**
- Bootstrapped `frontend/` with `npm create vite@latest frontend -- --template react-ts`
- Created required directories: `src/pages/`, `src/components/`, `src/hooks/`, `src/api/`
- Set `<title>OddToBelieve</title>` in `frontend/index.html` (replaces Vite default "frontend")
- Replaced Vite default starter `App.tsx` with a minimal `HomePage` component (no Vite branding)
- Added `src/api/config.ts` exporting `API_BASE_URL = import.meta.env.VITE_API_BASE_URL` — no hardcoded localhost URLs in source
- Added `.env.local.example` documenting `VITE_API_BASE_URL=http://localhost:8000`
- Added missing `src/components/` and `src/hooks/` `.gitkeep` placeholder dirs (QA fix applied)
- `npm run build` → success (no errors)
- `npm run lint` → 0 errors
- All 8 STORY-14 ACs met

---

## 2026-07-09 Status Check-in

- No new AppSec scan posted on PRs #52 or #53 as of today — AppSec remains BLOCKED (18 days, last active 2026-06-22).
- No Engineer code action required today per sprint board (no AppSec findings to address).
- Sprint ends TOMORROW (Friday 2026-07-10). If AppSec does not act today, PRs #52 and #53 will not merge in Sprint 2.
- STORY-21a carries to Sprint 3 — not started this sprint per plan.

## Blocker: GitHub REST API (resolved for status update; session limitation persists)

The session proxy blocks GitHub REST API calls to `cmdperogi/OddToBelieve` — both the session-injected token and the provided PAT return "GitHub access to this repository is not enabled for this session." Git push (CONNECT tunnel) works; REST API (HTTPS relay) does not. PRs #52 and #53 were created by QA on 2026-07-08.

## Merge Readiness

| Branch | Story | PR | Status |
|--------|-------|----|--------|
| `agent/engineer/rate-limit-guard` | STORY-7 | [#52](https://github.com/cmdperogi/OddToBelieve/pull/52) | QA LGTM ✅ — AppSec CLEAR pending 🔴 |
| `agent/engineer/frontend-scaffold` | STORY-14 | [#53](https://github.com/cmdperogi/OddToBelieve/pull/53) | QA LGTM ✅ — AppSec CLEAR pending 🔴 |
| [#47](https://github.com/cmdperogi/OddToBelieve/pull/47) | STORY-10 | #47 | ✅ MERGED 2026-07-08T09:07Z |
| [#48](https://github.com/cmdperogi/OddToBelieve/pull/48) | STORY-11 | #48 | ✅ MERGED 2026-07-08T09:09Z |

## Next Tasks

- **STORY-21a**: Deferred to Sprint 3 — per sprint board, top priority for Sprint 3.
- STORY-22 (frontend login) and STORY-23a (OddsTable component) unblocked once STORY-14 (PR #53) merges.
- No new engineer tasks this sprint.

## Previous Tasks

- **STORY-7 (2026-07-08):** Branch `agent/engineer/rate-limit-guard` pushed. PR #52 opened by QA. 75/75 tests passing, all 5 ACs. QA LGTM posted.
- **STORY-14 (2026-07-08):** Branch `agent/engineer/frontend-scaffold` pushed. PR #53 opened by QA (with gitkeep fix). QA LGTM posted.
- **STORY-10 (2026-07-02):** PR #47 merged 2026-07-08T09:07Z. 45/45 tests passing, all 5 ACs.
- **STORY-11 (2026-07-02):** PR #48 merged 2026-07-08T09:09Z. All ACs.
- **STORY-3 rebase (2026-06-25):** PR #28 rebased onto `090413e`. 62/62 passing, 91% coverage. All gates clear; DevOps stall blocking merge.
- **STORY-2 (merged 2026-06-23):** PR #26 merged. BetfairClient unit tests. 40/40 passing, 100% betfair.py coverage.
