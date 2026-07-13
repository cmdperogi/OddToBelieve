# Product Backlog

**Project:** OddToBelieve — FastAPI + React/Vite odds aggregation dashboard (Betfair Exchange + The Odds API)  
**PO:** Product Owner Agent  
**Last refined:** 2026-07-13

---

## Priority 1 — Bugs / Blockers

*Sprint 3 carry-overs. PRs #52 (STORY-7) and #53 (STORY-14) have all gates cleared (QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅) since 2026-07-09. DevOps missed the Sprint 2 merge deadline (2026-07-10). Both must merge on Sprint 3 Day 1 (today, 2026-07-13). Merge order: PR #52 first, then PR #53.*

---

### [STORY-7] Add rate limit guard to OddsApiService
**As a** developer, **I want** the OddsApiService to halt polling when quota is low **so that** the 500 req/month hard limit is never breached.  
**Status:** PR #52 open — **ALL GATES CLEAR ✅** (QA LGTM 2026-07-08, AppSec CLEAR 2026-07-09, CI GREEN). **DevOps merge OVERDUE since 2026-07-10. Merge TODAY (Sprint 3 Day 1).**  
**Note:** ⚠️ This guard is a safety net, not the primary monthly budget control — `ODDS_API_POLL_INTERVAL_MINUTES=360` (STORY-21b) is the primary control. Mandatory before STORY-21b starts.  
**⚠️ Rate limit budget check:** At 60-min polling, OddsApiService makes 720 calls/month — 44% over the 500 req/month cap. This guard (threshold < 50 remaining) prevents the tail from exhausting. STORY-21b's 360-min default interval (120 calls/month) is the real protection.  
**Acceptance criteria:**
- Given `x-requests-remaining < 50` in a response header, When the APScheduler job calls `OddsApiService`, Then the HTTP request is NOT made and a `WARNING` is logged with the current remaining count
- Given `x-requests-remaining >= 50`, When the scheduler calls `OddsApiService`, Then the HTTP request proceeds normally
- Given the app has just started and no Odds API response has been received yet, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": null, "guard_active": false}` (startup state — no header seen)
- Given the guard has fired at least once in this process lifetime, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": true}`
- Given the guard has fired previously and a subsequent response shows `x-requests-remaining >= 50`, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": false}` (guard auto-deactivates on recovery)
- Given any test in this suite runs, Then no real HTTP requests are made to `api.the-odds-api.com`  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #40  
**Depends on:** STORY-3 ✅

---

### [STORY-14] Scaffold React/Vite frontend project
**As a** developer, **I want** the frontend project scaffolded **so that** the team can implement and test UI components.  
**Status:** PR #53 open — **ALL GATES CLEAR ✅** (QA LGTM 2026-07-08, AppSec CLEAR 2026-07-09, CI GREEN). **DevOps merge OVERDUE since 2026-07-10. Merge TODAY (Sprint 3 Day 1), after PR #52.**  
**Acceptance criteria:**
- Given the repo has no `frontend/` directory, When the scaffold is complete, Then `frontend/` exists with the structure from CLAUDE.md (`src/pages/`, `src/components/`, `src/hooks/`, `src/api/`)
- Given the scaffold is complete, When `cd frontend && npm run dev` is run, Then the app serves on port 5173 without errors
- Given the scaffold is complete, When `npm run build` is run, Then the build completes with no errors
- Given the scaffold is complete, When `npm run lint` is run, Then zero lint errors are reported
- Given the scaffold is complete, When a `.env.local` file is added with `VITE_API_BASE_URL=http://localhost:8000`, When `npm run dev` is run, Then the API base URL is read from the env variable (no hardcoded `localhost:8000` in source files)
- Given the scaffold is complete, When `frontend/` is inspected, Then TypeScript (`tsconfig.json`) is configured — all component files use `.tsx` extension, not `.jsx`
- Given the scaffold includes a placeholder home page at `/`, When the user navigates to `http://localhost:5173`, Then a placeholder message (e.g. "OddToBelieve") is visible — not a generic Vite default starter page
- Given the scaffolded app's HTML `<head>` is inspected, Then the `<title>` tag reads "OddToBelieve" — not "Vite + React" or any other default  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #7  
**Blocks:** STORY-6, STORY-8, STORY-9, STORY-22, STORY-23a, STORY-23b, STORY-12b

---

## Priority 2 — Sprint 3 Stories

*Sprint 3: 2026-07-13 → 2026-07-24. Ordered by dependency chain: Betfair scheduler + datetime fix (Day 1) → OddsApiService persistence restore (Day 2, after STORY-7 merges) → Odds API scheduler (depends on 21a + 7 + 25) → Frontend login (after STORY-14 merges).*

---

### [STORY-21a] Add APScheduler — Betfair background polling job
**As a** developer, **I want** an APScheduler job to poll Betfair on a configured interval **so that** the database stays fresh without manual triggering.  
**Note:** Split from STORY-21 (PO decision D17, 2026-06-29). STORY-21b (Odds API job) must not start until this story merges. Original GitHub issue: #33 (closed). **NOW UNBLOCKED — STORY-3 merged 2026-07-03.**  
**Acceptance criteria:**
- Given the app starts, When the scheduler initialises, Then a Betfair poll job is registered at `BETFAIR_POLL_INTERVAL_MINUTES` (default: 60 min)
- Given a Betfair poll cycle runs, When `BetfairClient.list_events()` returns events, Then `Event`, `Market`, and `Odds` records are upserted in SQLite with `source="betfair"` — new records are inserted, changed prices are updated (no duplicate rows)
- Given a Betfair poll cycle runs and the event already exists in the DB, When the upsert runs, Then the existing record is updated rather than duplicated — the upsert key is `(source_id, source)` where `source_id` is the Betfair event ID returned by `BetfairClient.list_events()`
- Given a Betfair poll cycle runs and `Market` and `Odds` rows exist for a known event, When the cycle writes new prices, Then existing `Odds` rows for that event's markets are deleted before new ones are inserted (refresh pattern — stale prices must not accumulate)
- Given a Betfair poll cycle runs and `BetfairClient.list_events()` returns an empty list, When the cycle completes, Then no rows are inserted or deleted and an `INFO` log is emitted with event count 0 (empty result is not an error)
- Given Betfair re-auth fails during a poll cycle, When the exception is raised, Then the error is logged without credentials or session tokens and the scheduler continues — the process does NOT crash
- Given any test in this story runs, Then no real Betfair API calls are made; `BetfairClient` is mocked  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #41  
**Depends on:** STORY-2 ✅, STORY-3 ✅

---

### [STORY-24] Fix datetime.utcnow() deprecation in auth.py and db/models.py
**As a** developer, **I want** deprecated `datetime.utcnow()` calls replaced with timezone-aware equivalents **so that** the codebase is forward-compatible with Python 3.12+ before any runtime upgrade.  
**Note:** Flagged in 4+ prod-support audit runs. Non-breaking on Python 3.11 (current runtime). XS estimate — two-file change.  
**Acceptance criteria:**
- Given `auth.py` is inspected, When the JWT expiry is calculated, Then `datetime.now(timezone.utc)` is used in place of `datetime.utcnow()`
- Given `db/models.py` is inspected, When the `created_at` column default is read, Then `lambda: datetime.now(timezone.utc)` is used as the `default=` callable — not `datetime.utcnow` (bare function reference) and not the deprecated call; the lambda form ensures a fresh call per row rather than capturing a single datetime at import time
- Given `python3 -m pytest tests/` is run after the fix, When all tests execute, Then all tests pass (no regressions)
- Given `python -W error::DeprecationWarning -m pytest tests/`, When tests run, Then no `DeprecationWarning` is emitted from the changed files  
**Owner:** Engineer  
**Estimate:** XS  
**GitHub Issue:** #51  
**Depends on:** STORY-13 ✅

---

### [STORY-25] Restore OddsApiService DB persistence layer
**As a** developer, **I want** `OddsApiService.fetch()` to persist events to SQLite when a DB session is provided **so that** the Odds API scheduler (STORY-21b) can write data to the database.  
**Note:** Root cause — PR #31 (STORY-4 integration tests) was branched from a pre-STORY-3 state of main. When it merged (2026-07-03), the merge resolved in favour of the STORY-4 branch tree, dropping: (1) `_persist()` method, (2) `db: Session | None = None` parameter in `fetch()`, and (3) `test_odds_api_service.py` (546 lines, ~22 tests). Confirmed via `git diff c5fa096..de55f02`. The reference implementation exists at commit `2ed2ce2` on the STORY-3 branch. **This is a prerequisite for STORY-21b.** (PO decision D31, 2026-07-13)  
**Acceptance criteria:**
- Given `backend/app/services/odds_api.py` is inspected, When the `OddsApiService.fetch()` signature is read, Then it includes `db: Session | None = None` as an optional parameter — DB persistence is opt-in, not required
- Given `OddsApiService.fetch()` is called with a `db` session and the Odds API response includes events, When the call completes, Then `Event`, `Market`, and `Odds` records are written to SQLite with `source="odds_api"` — upsert key is `(source_id, source)` to prevent duplicates across sources
- Given `OddsApiService.fetch()` is called without a `db` session (`db=None`, the default), When the call completes, Then no DB writes occur and the raw response list is returned — fully backward-compatible with all existing callers that do not pass a session
- Given an `Event` with the same `source_id` and `source="odds_api"` already exists in the DB, When `_persist()` runs, Then the existing `Event` record is updated (not duplicated) and its `Market` and `Odds` rows are refreshed (old `Odds` rows deleted, new ones inserted)
- Given `_persist()` raises a database exception, When the error is propagated to `fetch()`, Then it is logged as `ERROR` with context (no credentials, no API key) and the exception is re-raised — the caller (scheduler) decides whether to continue
- Given `backend/tests/unit/test_odds_api_service.py` is run, When all tests execute, Then the following cases pass: (a) events persisted when `db` is provided, (b) no DB write when `db=None`, (c) upsert is idempotent — second call with same `source_id` updates not duplicates, (d) `Odds` rows are refreshed (not accumulated) on second call for same event
- Given `python3 -m pytest backend/tests/` runs after the fix, When all tests execute, Then all existing tests continue to pass (no regressions)
- ⚠️ No real HTTP calls to `api.the-odds-api.com` in any test — all `httpx` calls must be mocked  
- ⚠️ The Odds API key must not appear in test fixtures, assertions, log output, or version-controlled files  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** TBD (creation blocked by session GitHub access policy — must be created manually by a team member with API access)  
**Depends on:** STORY-3 ✅, STORY-7 (merge PR #52 first — STORY-25 should build on the correct `odds_api.py` including the guard properties and singleton)

---

### [STORY-21b] Add APScheduler — Odds API background polling job
**As a** developer, **I want** an APScheduler job to poll The Odds API on a configured interval **so that** the database stays fresh without exhausting the 500 req/month cap.  
**Note:** Split from STORY-21 (PO decision D17, 2026-06-29). ⚠️ `ODDS_API_POLL_INTERVAL_MINUTES` must default to **360 min (6h)** — this gives 120 calls/month against the 500 req/month hard cap. Do not lower this default without explicit PO sign-off and rate-limit recalculation.  
**⚠️ The Odds API has a hard limit of 500 req/month.** Default 360 min = 120 req/month (safe). At 60 min it would be 720 req/month (over cap).  
**Acceptance criteria:**
- Given the app starts, When the scheduler initialises, Then an Odds API poll job is registered at `ODDS_API_POLL_INTERVAL_MINUTES` (default: 360 min), independent of `BETFAIR_POLL_INTERVAL_MINUTES`
- Given an Odds API poll cycle runs, When `OddsApiService.fetch()` returns data, Then `Event`, `Market`, and `Odds` records are upserted in SQLite with `source="odds_api"` (via the restored `_persist()` method from STORY-25)
- Given the OddsApiService rate guard is active (`x-requests-remaining < 50`), When the Odds API scheduler job runs, Then `OddsApiService.fetch()` is NOT called; a `WARNING` is logged; Betfair polling is unaffected and continues on its own schedule
- Given the OddsApiService rate guard has not yet received an API response header (startup state), When the Odds API scheduler job runs its first cycle, Then the guard behaves as inactive (`guard_active: false`) and the HTTP request proceeds normally
- Given Betfair polling is running and the Odds API guard fires, When the next `BETFAIR_POLL_INTERVAL_MINUTES` elapses, Then the Betfair job runs normally — the two schedules are fully independent
- Given the Odds API poll cycle runs and `_persist()` raises a database exception, When the error is caught by the scheduler job, Then it is logged as `ERROR` (no credentials) and the scheduler continues — the process does NOT crash
- Given any test in this story runs, Then no real Betfair or Odds API calls are made; both services are mocked  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #42  
**Depends on:** STORY-21a, STORY-7, STORY-25

---

## Priority 3 — Backlog

*Sprint 3+ scope. Ordered by: reliability > UX > new features. Frontend stories are all blocked on STORY-14 merge.*

---

### [STORY-22] Frontend login page + JWT token management
**As a** user, **I want** a login page with JWT session management **so that** I can authenticate once and use the dashboard without re-entering credentials on each page load.  
**Acceptance criteria:**
- Given the user is not authenticated, When they navigate to any protected route, Then they are redirected to `/login`
- Given valid credentials are submitted, When `POST /auth/token` responds with 200, Then the JWT is stored in React context (in-memory — NOT `localStorage` or `sessionStorage`, which are vulnerable to XSS), and the user is redirected to `/`
- Given invalid credentials are submitted, When `POST /auth/token` responds with 401, Then an inline error message is shown beneath the form — not a browser alert
- Given a JWT is in context, When any API call is made, Then the `Authorization: Bearer <token>` header is included
- Given the API returns 401 (expired or invalid token), When the error is caught by the API layer, Then the JWT is cleared from context and the user is redirected to `/login`
- Given the user clicks "Log out", When the action completes, Then the JWT is cleared from context and the user is redirected to `/login`
- Given the user closes the browser tab and reopens the app, When the app initialises, Then the user is redirected to `/login` — the JWT is NOT persisted in `localStorage` or `sessionStorage` and is gone after tab close
- Given Vitest tests run with a mock auth context, When the login form is rendered, Then the username field, password field, and submit button are visible in the DOM  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #34  
**Depends on:** STORY-14

---

### [STORY-23a] Frontend dashboard — OddsTable component + Vitest tests
**As a** developer, **I want** an `OddsTable` component that renders events from mock/fixture data **so that** the table layout and Vitest tests can be verified independently of the live backend.  
**Note:** PO decision D26 — split from original STORY-23 (M-estimate). STORY-23b covers the live API wiring.  
**Acceptance criteria:**
- Given mock event data is passed as props to `OddsTable`, When the component renders, Then each event name, sport, start time, and best available odds column are visible in the DOM
- Given an empty array is passed as props, When the component renders, Then an empty-state message is displayed — not a blank or crashed UI
- Given a loading flag is passed as a prop, When the component renders, Then a skeleton or spinner placeholder is shown in place of the table
- Given an error string is passed as a prop, When the component renders, Then a user-friendly error message is displayed — not raw JSON or a blank screen
- Given Vitest tests run for `OddsTable`, When all tests execute, Then: (a) happy-path data is visible, (b) empty-state is verified, (c) loading state is verified, (d) error state is verified — all pass
- Given `OddsTable` source is inspected, Then no hardcoded `localhost:8000` URLs appear — the component receives data as props only (no direct fetch calls in this story)  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #49  
**Depends on:** STORY-14, STORY-22  
**Blocks:** STORY-23b

---

### [STORY-23b] Frontend dashboard — wire OddsTable to GET /odds/events
**As a** user, **I want** the OddsTable wired to the live `GET /odds/events` endpoint **so that** real event data appears on the dashboard when I am authenticated.  
**Note:** PO decision D26 — split from original STORY-23 (M-estimate). STORY-23a covers the component shell with mock data.  
**Acceptance criteria:**
- Given the user is authenticated, When they navigate to `/`, Then `GET /odds/events` is called with `Authorization: Bearer <token>` header and the response data is passed to `OddsTable`
- Given `GET /odds/events` returns events, When `OddsTable` renders, Then all event names and best available odds from the API response are visible in the DOM
- Given `GET /odds/events` returns HTTP 401 (expired token), When the error is caught by the API layer, Then the JWT is cleared from context and the user is redirected to `/login`
- Given `GET /odds/events` fails (network error or 5xx), When the error is caught, Then `OddsTable` is rendered in error state — user-friendly message, not raw JSON
- Given the API call is in flight, When the component mounts, Then `OddsTable` renders in loading state — skeleton/spinner displayed
- Given Vitest tests run for the wired dashboard, When all tests execute, Then the API call is mocked (no real backend calls) and expected data appears in the DOM  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #50  
**Depends on:** STORY-23a, STORY-14, STORY-22, STORY-4 ✅

---

### [STORY-6] Wire frontend Vitest tests to CI pipeline (merge gate)
**As a** developer, **I want** frontend Vitest tests wired into the GitHub Actions CI pipeline **so that** a failing test blocks a PR from merging.  
**Note:** PO decision D30 (2026-07-13) — descoped. Vitest installation and component tests are covered by STORY-23a. This story's sole remaining value is the CI gate: ensuring `npm test` runs in CI and blocks merge on failure. Renamed from "Add Vitest to frontend and write component tests".  
**Acceptance criteria:**
- Given STORY-23a is merged and `npm test` passes locally, When a PR is opened that touches `frontend/`, Then the CI workflow runs `npm test` in the `frontend/` directory
- Given a Vitest test in `frontend/` fails, When a PR is opened with that failure, Then the CI workflow fails and merge is blocked
- Given all Vitest tests pass, When a PR is opened, Then the CI frontend test step is green and does not block merge  
**Owner:** Engineer + DevOps  
**Estimate:** XS  
**GitHub Issue:** #43  
**Depends on:** STORY-14, STORY-23a

---

### [STORY-8] Add sport filter UI to React dashboard
**As a** user, **I want** to filter odds by sport (soccer / horse racing) **so that** I can focus on my sport of choice.  
**Acceptance criteria:**
- Given the dashboard loads, When the page is displayed, Then "Soccer" and "Horse Racing" filter buttons are visible above the event list
- Given the user clicks "Soccer", When the filter is applied, Then only soccer events appear in the list without a full page reload
- Given the user clicks "Horse Racing", When the filter is applied, Then only horse racing events appear in the list without a full page reload
- Given a filter is active and the user refreshes the page, When the page loads, Then the previously selected filter is restored from `localStorage`
- Given both filters are cleared, When the view updates, Then all events from both sports are displayed  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #44  
**Depends on:** STORY-14

---

### [STORY-9] Frontend loading states and error handling
**As a** user, **I want** clear loading and error states **so that** I know what is happening when data is slow or unavailable.  
**Note:** STORY-23a/23b cover loading/error states for the main OddsTable. This story covers the global error boundary and app-level patterns.  
**Acceptance criteria:**
- Given an API call is in flight, When the events list is loading, Then a spinner or skeleton placeholder is displayed in place of stale or empty content
- Given the backend API is unreachable, When the events call fails, Then a user-friendly error message is shown (not a blank screen, raw JSON, or uncaught exception)
- Given an unexpected JavaScript error is thrown anywhere in the dashboard, When the error boundary catches it, Then a fallback UI is displayed and the error is logged to the browser console  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #45  
**Depends on:** STORY-14

---

### [STORY-12a] Backend — cross-source event matching endpoint
**As a** developer, **I want** a `GET /odds/comparison` endpoint that matches events across Betfair and The Odds API **so that** the frontend can display side-by-side pricing without making new API calls.  
**Note:** ⚠️ This endpoint serves data from the DB only — no live API calls triggered by this request. The Odds API 500 req/month limit is entirely a scheduler concern (STORY-21b).  
**Acceptance criteria:**
- Given events from both sources are stored in the database, When `GET /odds/comparison` is called with a valid JWT, Then a list of matched event objects is returned, each containing Betfair odds and Odds API odds for the same real-world event
- Given two events with the same sport, fuzzy-matched name (≥85% similarity score), and start times within 5 minutes, When the matching algorithm runs, Then they are returned as a matched pair
- Given an event exists in only one source, When the endpoint returns it, Then the response includes the single-source data with `null` for the missing source's odds field
- Given no JWT is supplied, When `GET /odds/comparison` is called, Then HTTP 401 is returned
- Given the matching algorithm runs, Then no live calls to Betfair or The Odds API are made — all data is read from the SQLite database  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #36  
**Depends on:** STORY-2 ✅, STORY-3 ✅, STORY-21b

---

### [STORY-12b] Frontend — odds comparison view
**As a** user, **I want** to see Betfair and The Odds API prices side-by-side for the same event **so that** I can spot pricing discrepancies between sources.  
**Acceptance criteria:**
- Given the user is authenticated, When they navigate to `/comparison`, Then `GET /odds/comparison` is called and matched events are displayed in a side-by-side table
- Given both sources have odds for the same selection, When the view renders, Then the better price is visually highlighted (e.g. green background or bold text)
- Given an event exists in only one source, When the table renders, Then that row shows "N/A" for the missing source with no layout breakage
- Given the `GET /odds/comparison` call is in flight, When the component mounts, Then a loading skeleton is displayed
- Given the comparison list is empty, When the view renders, Then an appropriate empty-state message is shown  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #37  
**Depends on:** STORY-12a, STORY-14, STORY-22

---

## Done

*(moved here when merged to main)*

### [STORY-10] Add /health endpoint — RESOLVED
**Resolved:** PR #47 merged 2026-07-08T09:07Z. 60/60 tests passing on main. All 5 ACs verified. **GitHub Issue:** #38 (closed).

### [STORY-11] Add structured logging — RESOLVED
**Resolved:** PR #48 merged 2026-07-08T09:09Z. 60/60 tests passing. All ACs verified. Rebase required on merge (main.py import conflict with #47). **GitHub Issue:** #39 (closed).

### [STORY-3] Implement OddsApiService + unit tests (TDD) — RESOLVED
**Resolved:** PR #28 merged 2026-07-03T20:51:59Z. 62/62 tests passing, 91% coverage. AppSec CLEAR. **GitHub Issue:** #4 (closed 2026-07-06).  
**Note:** ⚠️ The Odds API has a hard limit of **500 req/month** — all tests mock HTTP calls (no real API requests in suite).  
**Known issue:** PR #31 (STORY-4) merge dropped `_persist()` and `test_odds_api_service.py` from main. Tracked in STORY-25.

### [STORY-4] Write integration tests for /odds/* endpoints — RESOLVED
**Resolved:** PR #31 merged 2026-07-03T20:52:07Z (8 seconds after PR #28). All gates: QA LGTM ✅, AppSec CLEAR ✅, CI GREEN ✅. **GitHub Issue:** #5 (closed 2026-07-06).  
**Known issue:** PR #31 branch tree dropped STORY-3's `_persist()` and unit tests from main on merge. Tracked in STORY-25.

### [STORY-2] Implement BetfairClient + unit tests (TDD) — RESOLVED
**Resolved:** PR #26 merged 2026-06-23. 40/40 tests passing, 100% coverage. **GitHub Issue:** #3 (closed).

### [STORY-13] Scaffold FastAPI backend project — RESOLVED
**Resolved:** PR #8 merged 2026-06-20. All security findings resolved, AppSec CLEAR, QA LGTM 31/31. **GitHub Issue:** #1 (closed).

### [STORY-1] Set up GitHub Actions CI pipeline — RESOLVED
**Resolved:** PR #9 merged 2026-06-20. CI active on main. **GitHub Issue:** #2 (closed).

### [STORY-5] AppSec baseline scan — RESOLVED
**Resolved:** 2026-06-20. Bandit: B106 false positive only. pip-audit: 0 CVEs. **GitHub Issue:** #6 (closed).

### [STORY-15] Fix hardcoded credential defaults in config.py — RESOLVED
**Resolved:** PR #8 branch. `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` raise `ValueError` on startup if not set. **GitHub Issue:** #17 (closed).

### [STORY-16] Fix plain-text admin password comparison — use bcrypt — RESOLVED
**Resolved:** PR #8 branch. `_pwd_context.verify()` in place. **GitHub Issue:** #18 (closed).

### [STORY-17] Fix python-jose CVEs — upgrade to ≥3.4.0 — RESOLVED
**Resolved:** PR #8 branch. `python-jose[cryptography]>=3.4.0`, 0 CVEs. **GitHub Issue:** #19 (closed).

### [STORY-18] Upgrade python-multipart and fastapi to CVE-free versions — RESOLVED
**Resolved:** PR #8 branch. `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`, `pydantic>=2.9.0`. **GitHub Issues:** #20, #24, #25 (all closed).

### [STORY-19] Migrate CI credential-shaped env vars to GitHub Actions secrets pattern — RESOLVED
**Resolved:** PR #9 branch. All 5 credential-shaped vars use `${{ secrets.VAR || 'fallback' }}`. **GitHub Issue:** #21 (closed).

### [STORY-20] Upgrade dev dependencies — fix pytest and black CVEs — RESOLVED
**Resolved:** PR #8 branch. `pytest==9.0.3`, `black==26.3.1`. **GitHub Issue:** #22 (closed).
