# Product Backlog

**Project:** OddToBelieve — FastAPI + React/Vite odds aggregation dashboard (Betfair Exchange + The Odds API)  
**PO:** Product Owner Agent  
**Last refined:** 2026-06-22

---

## Priority 1 — Bugs / Blockers

*No active blockers as of 2026-06-22. STORY-15 through STORY-20 (all Sprint 1 security fixes) are resolved, verified, and moved to Done. PR #8 is security-clear; sole remaining gate is AppSec formal approval comment.*

---

## Priority 2 — Sprint-Ready Stories

*Sprint 1 stories in progress, plus stories that become sprint-ready on completion of the current merge cascade.*

### [STORY-13] Scaffold FastAPI backend project ⚠️ SPRINT-1 PREREQUISITE
**As a** developer, **I want** the backend project scaffolded with the correct directory structure and dependencies **so that** the team can implement and test services without environment friction.  
**Status:** PR #8 open — security-clear; awaiting AppSec formal approval comment before merge.  
**Acceptance criteria:**
- Given the repo has no backend/ directory, When the scaffold is complete, Then `backend/` exists with the layout defined in CLAUDE.md (`app/`, `tests/unit/`, `tests/integration/`, `requirements.txt`)
- Given the scaffold is in place, When `cd backend && uvicorn app.main:app --reload` is run, Then the server starts on port 8000 with no import errors
- Given the scaffold is in place, When GET /docs is accessed, Then the OpenAPI schema page loads
- Given the scaffold is in place, When `ruff check . --fix && black .` is run from `backend/`, Then zero lint errors are reported
- Given the scaffold is in place, When `pytest tests/ -v` is run, Then the test runner initialises without import errors (even if no test files exist yet)  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #1  
**Blocks:** STORY-2, STORY-3, STORY-4, STORY-5, STORY-10, STORY-11

---

### [STORY-1] Set up GitHub Actions CI pipeline
**As a** developer, **I want** CI to run on every PR **so that** broken code is caught before merge.  
**Status:** PR #9 open — code-complete; merge blocked on PR #8 (CI backend job needs `backend/` on main).  
**Acceptance criteria:**
- Given a PR is opened, When CI runs, Then backend lint (`ruff`) + `pytest` pass
- Given a PR is opened, When CI runs, Then frontend lint (`npm run lint`) + build (`npm run build`) pass
- Given any test fails, When CI finishes, Then the PR is blocked from merge  
**Owner:** DevOps  
**Estimate:** S  
**GitHub Issue:** #2

---

### [STORY-2] Implement BetfairClient + unit tests (TDD)
**As a** developer, **I want** `BetfairClient` implemented with unit tests **so that** auth, session management, and retry logic are verified without hitting the real API.  
**Status:** PR #26 open — QA LGTM (9 unit tests, 40/40 pass, 100% coverage); needs rebase onto main once PR #8 merges.  
**Acceptance criteria:**
- Given a successful login response, When `_login()` is called, Then the session token is stored in memory and returned
- Given a 403 response on the first request, When `_post()` is called, Then it re-authenticates and retries exactly once
- Given a non-SUCCESS login status, When `_login()` is called, Then a `RuntimeError` is raised
- Given `BetfairClient.list_events(sport_ids=["1", "7"])` is called, When the response is mocked, Then a list of event dicts is returned with `id`, `name`, `sport`, `start_time`
- Given any test in this suite runs, Then no real HTTP requests are made (all Betfair endpoints must be mocked)
- ⚠️ Betfair credentials must never appear in test output, log output, or fixtures  
**Owner:** Engineer + QA  
**Estimate:** M  
**GitHub Issue:** #3  
**Depends on:** STORY-13

---

### [STORY-3] Implement OddsApiService + unit tests (TDD)
**As a** developer, **I want** `OddsApiService` implemented with unit tests **so that** the rate-limit guard and response parsing are verified.  
**Status:** PR #28 open — QA LGTM (16 unit tests, 56/56 pass, 90% coverage); stacked on PR #26; DB persistence (`Event`/`Market`/`Odds` records) in progress on branch. This is in STORY-3 scope per AC 3 — no new story needed.  
**Note:** ⚠️ The Odds API has a hard limit of **500 req/month** — tests must never make real HTTP calls.  
**Acceptance criteria:**
- Given `x-requests-remaining < 50` in a mocked response header, When `OddsApiService.fetch()` is called, Then the HTTP request is NOT made and a `WARNING` is logged with the remaining count
- Given `x-requests-remaining >= 50`, When `OddsApiService.fetch()` is called, Then the HTTP request proceeds normally
- Given a valid Odds API response payload, When odds are parsed, Then `Event`, `Market`, and `Odds` records are created with correct field values
- Given any test in this suite runs, Then no real HTTP requests are made to `api.the-odds-api.com`  
**Owner:** Engineer + QA  
**Estimate:** S  
**GitHub Issue:** #4  
**Depends on:** STORY-13

---

### [STORY-4] Write integration tests for /odds/* endpoints
**As a** developer, **I want** integration tests for the odds endpoints **so that** auth enforcement and response shapes are verified.  
**Status:** Draft PR #31 open (16/16 tests passing, all 5 ACs covered). QA converts from draft immediately when PR #8 merges.  
**Acceptance criteria:**
- Given no auth token, When `GET /odds/events` is called, Then HTTP 401 is returned
- Given a valid JWT token, When `GET /odds/events` is called, Then a list conforming to `EventSchema` is returned
- Given an invalid `event_id`, When `GET /odds/events/{id}` is called, Then HTTP 404 is returned
- Given a valid `event_id`, When `GET /odds/events/{id}/markets` is called, Then a list conforming to `MarketSchema` is returned
- Given the integration test suite runs, Then no real Betfair or Odds API calls are made (services mocked or DB seeded with fixtures)  
**Owner:** QA  
**Estimate:** S  
**GitHub Issue:** #5  
**Depends on:** STORY-13

---

### [STORY-5] AppSec baseline scan
**As a** security engineer, **I want** a Bandit + pip-audit baseline run **so that** existing vulnerabilities are documented before feature work begins.  
**Status:** Pre-scan complete on PR #8 branch (security-clear). Formal STORY-5 run on main post-merge.  
**Acceptance criteria:**
- Given `backend/app/` exists, When Bandit is run against it, Then findings are recorded in `team/agents/appsec.md`
- Given `backend/requirements.txt` exists, When pip-audit runs against it, Then dependency CVEs are recorded in `team/agents/appsec.md`
- Given any HIGH or CRITICAL finding is identified, Then a GitHub issue is opened for each one with the finding details  
**Owner:** AppSec  
**Estimate:** XS  
**GitHub Issue:** #6  
**Depends on:** STORY-13

---

### [STORY-10] Add /health endpoint
**As a** developer, **I want** a `/health` endpoint **so that** uptime and database connectivity can be confirmed without authenticating.  
**Note:** Moved to P2 — sprint-ready the moment PR #8 merges to main. XS estimate; can be picked up as the first backend task in Sprint 2.  
**Acceptance criteria:**
- Given the backend is running, When `GET /health` is called with no auth token, Then HTTP 200 is returned with `{"status": "ok"}`
- Given the SQLite database file is reachable, When `GET /health` is called, Then the response body includes `{"db": "ok"}`
- Given the database file is missing or locked, When `GET /health` is called, Then the response body includes `{"db": "error"}` and the HTTP status is still 200 (liveness semantics — a 500 here would break monitoring tools)
- Given the endpoint is inspected, When the route definition is read, Then no `UserDep` or auth dependency is applied — this is the named public exception (PO decision D5)  
**Owner:** Engineer  
**Estimate:** XS  
**GitHub Issue:** none — create at sprint planning  
**Depends on:** STORY-13

---

### [STORY-11] Add structured logging
**As a** developer, **I want** structured logs **so that** errors and warnings are easy to trace during local development.  
**Note:** Moved to P2 — sprint-ready when PR #8 merges. Can be picked up alongside STORY-10 in Sprint 2.  
**Acceptance criteria:**
- Given any poll cycle completes, When the scheduler runs, Then an `INFO` log is emitted with sport name and event count
- Given the rate-limit guard fires, When `OddsApiService` skips a request, Then a `WARNING` log is emitted with the remaining request count
- Given any Betfair or Odds API call fails, When the exception is caught, Then an `ERROR` log is emitted with context but without credentials or session tokens
- Given `LOG_LEVEL=DEBUG` is set in the environment, When the app starts, Then `DEBUG`-level messages are emitted
- ⚠️ Betfair session tokens and The Odds API key must never appear in log output at any level  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** none — create at sprint planning  
**Depends on:** STORY-13

---

### [STORY-7] Add rate limit guard to OddsApiService
**As a** developer, **I want** the OddsApiService to halt polling when quota is low **so that** the 500 req/month hard limit is never breached.  
**Note:** Moved to P2 — sprint-ready when STORY-3 merges. ⚠️ This guard is mandatory before enabling the scheduler (STORY-21). The scheduler must call this guard on every Odds API invocation.  
**⚠️ Rate limit budget check:** At 60 min default poll interval, OddsApiService would make 720 calls/month — 44% over the 500 req/month cap. The guard prevents exhausting the last 50 requests but cannot prevent the monthly cap being hit. STORY-21 (scheduler) addresses this by using a separate, longer Odds API interval (default: 360 min = 120/month). This guard is a safety net, not the primary control.  
**Acceptance criteria:**
- Given `x-requests-remaining < 50`, When the APScheduler job calls `OddsApiService`, Then the HTTP request is NOT made and a `WARNING` is logged with the current remaining count
- Given `x-requests-remaining >= 50`, When the scheduler calls `OddsApiService`, Then the HTTP request proceeds normally
- Given the guard has fired at least once in this process lifetime, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": true}`
- Given the guard has never fired, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": false}`  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** none — create at sprint planning  
**Depends on:** STORY-3

---

### [STORY-21] Add APScheduler background polling job
**As a** developer, **I want** an APScheduler job to poll Betfair and (where quota allows) The Odds API on a configured interval **so that** the database stays fresh without manual triggering.  
**Note:** Sprint-ready when STORY-2 and STORY-3 merge. ⚠️ Critical rate limit constraint — see below.  
**⚠️ The Odds API rate limit: 500 req/month hard cap.** At the `ODDS_POLL_INTERVAL_MINUTES` default of 60 min, OddsApiService would make 720 calls/month (60 × 24 × 30 ÷ 60 = 720) — 44% over budget. This story introduces a separate `ODDS_API_POLL_INTERVAL_MINUTES` environment variable defaulting to **360 min (6h)**, giving a safe 120 calls/month. The existing rate guard (STORY-7) remains the safety net but must not be the primary control for monthly budget.  
**Acceptance criteria:**
- Given the app starts, When the scheduler initialises, Then a Betfair poll job is registered at `BETFAIR_POLL_INTERVAL_MINUTES` (default: 60) and an Odds API poll job is registered at `ODDS_API_POLL_INTERVAL_MINUTES` (default: 360); the two intervals are independent
- Given a Betfair poll cycle runs, When `BetfairClient.list_events()` returns data, Then `Event`, `Market`, and `Odds` records are upserted in the database with `source="betfair"`
- Given an Odds API poll cycle runs, When `OddsApiService.fetch()` returns data, Then `Event`, `Market`, and `Odds` records are upserted in the database with `source="odds_api"`
- Given the OddsApiService rate guard is active (`x-requests-remaining < 50`), When the Odds API scheduler job runs, Then `OddsApiService.fetch()` is NOT called; a `WARNING` is logged; Betfair polling is unaffected and continues on its own schedule
- Given Betfair re-auth fails during a poll cycle, When the exception is raised, Then the error is logged (without credentials or session tokens) and the scheduler continues — the process does NOT crash
- Given any test in this story runs, Then no real Betfair or Odds API calls are made; both services are mocked  
**Owner:** Engineer  
**Estimate:** M  
**GitHub Issue:** #33  
**Depends on:** STORY-2 (BetfairClient), STORY-3 (OddsApiService)

---

## Priority 3 — Backlog

*Sprint 2 and later. Ordered by: reliability > UX > new features.*

### [STORY-14] Scaffold React/Vite frontend project
**As a** developer, **I want** the frontend project scaffolded **so that** the team can implement and test UI components.  
**Note:** Sprint 2 prerequisite. All frontend stories (STORY-6, 8, 9, 22, 23, 12b) are blocked on this. Pull into Sprint 2 immediately.  
**Acceptance criteria:**
- Given the repo has no `frontend/` directory, When the scaffold is complete, Then `frontend/` exists with the structure from CLAUDE.md (`src/pages/`, `src/components/`, `src/hooks/`, `src/api/`)
- Given the scaffold is complete, When `cd frontend && npm run dev` is run, Then the app serves on port 5173 without errors
- Given the scaffold is complete, When `npm run build` is run, Then the build completes with no errors
- Given the scaffold is complete, When `npm run lint` is run, Then zero lint errors are reported
- Given the scaffold is complete, When a `.env.local` file is added with `VITE_API_BASE_URL=http://localhost:8000`, When `npm run dev` is run, Then the API base URL is read from the env variable (no hardcoded `localhost:8000` in source files)  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #7  
**Blocks:** STORY-6, STORY-8, STORY-9, STORY-22, STORY-23, STORY-12b

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
- Given Vitest tests run with a mock auth context, When the login form is rendered, Then the username field, password field, and submit button are visible in the DOM  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #34  
**Depends on:** STORY-14

---

### [STORY-23] Frontend main dashboard — events and odds table
**As a** user, **I want** a live odds table on the dashboard **so that** I can see current events and their best available odds from both sources.  
**Acceptance criteria:**
- Given the user is authenticated, When they navigate to `/`, Then `GET /odds/events` is called and events are displayed in an `OddsTable` component
- Given events are returned, When the table renders, Then each row shows: event name, sport, start time, and best available odds across all bookmakers/sources
- Given the events list is empty (no data polled yet), When the dashboard loads, Then an empty-state message is displayed — not a blank screen or an uncaught error
- Given the `GET /odds/events` call is in flight, When the component mounts, Then a loading skeleton or spinner is displayed in place of the table
- Given the API call fails (network error or 5xx), When the error is caught, Then a user-friendly error message is displayed — not raw JSON and not a blank screen
- Given Vitest tests run with mocked API responses, When the `OddsTable` component is rendered, Then all event names and odds values from the mock data are visible in the DOM  
**Owner:** Engineer  
**Estimate:** M  
**GitHub Issue:** #35  
**Depends on:** STORY-14, STORY-22 (login/auth context), STORY-4 (integration tests confirm response shape)

---

### [STORY-6] Add Vitest to frontend and write component tests
**As a** developer, **I want** frontend unit tests **so that** React component logic is verified independently of the backend.  
**Acceptance criteria:**
- Given Vitest is installed, When `npm test` is run in `frontend/`, Then all tests execute and pass
- Given the `OddsTable` component is rendered with mock event data, When the component mounts, Then each event name and best-odds value is visible in the DOM
- Given the component is given an empty event list, When it renders, Then an empty-state message is displayed (not a blank or crashed UI)
- Given CI is configured, When a PR is opened, Then frontend tests execute in the CI workflow and block merge on failure  
**Owner:** Engineer + QA  
**Estimate:** S  
**Depends on:** STORY-14

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
**Depends on:** STORY-14

---

### [STORY-9] Frontend loading states and error handling
**As a** user, **I want** clear loading and error states **so that** I know what is happening when data is slow or unavailable.  
**Acceptance criteria:**
- Given an API call is in flight, When the events list is loading, Then a spinner or skeleton placeholder is displayed in place of stale or empty content
- Given the backend API is unreachable, When the events call fails, Then a user-friendly error message is shown (not a blank screen, raw JSON, or uncaught exception)
- Given an unexpected JavaScript error is thrown anywhere in the dashboard, When the error boundary catches it, Then a fallback UI is displayed and the error is logged to the browser console  
**Owner:** Engineer  
**Estimate:** S  
**Depends on:** STORY-14

---

### [STORY-12a] Backend — cross-source event matching endpoint
**As a** developer, **I want** a `GET /odds/comparison` endpoint that matches events across Betfair and The Odds API **so that** the frontend can display side-by-side pricing without making new API calls.  
**Note:** Split from STORY-12 (PO decision D8, 2026-06-22). ⚠️ The comparison endpoint must serve data from the database only — no live API calls triggered by this request. The Odds API 500 req/month limit is entirely a scheduler concern (STORY-21).  
**Acceptance criteria:**
- Given events from both sources are stored in the database, When `GET /odds/comparison` is called with a valid JWT, Then a list of matched event objects is returned, each containing Betfair odds and Odds API odds for the same real-world event
- Given two events with the same sport, fuzzy-matched name (≥85% similarity score), and start times within 5 minutes, When the matching algorithm runs, Then they are returned as a matched pair
- Given an event exists in only one source, When the endpoint returns it, Then the response includes the single-source data with `null` for the missing source's odds field
- Given no JWT is supplied, When `GET /odds/comparison` is called, Then HTTP 401 is returned
- Given the matching algorithm runs, Then no live calls to Betfair or The Odds API are made — all data is read from the SQLite database  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #36  
**Depends on:** STORY-2, STORY-3, STORY-21

---

### [STORY-12b] Frontend — odds comparison view
**As a** user, **I want** to see Betfair and The Odds API prices side-by-side for the same event **so that** I can spot pricing discrepancies between sources.  
**Note:** Split from STORY-12 (PO decision D8, 2026-06-22). Depends on STORY-12a for the backend endpoint.  
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

### [STORY-15] Fix hardcoded credential defaults in config.py — RESOLVED
**Resolved:** PR #8 branch. Verified by QA + AppSec. `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` now raise `ValueError` on startup if not set. No plaintext defaults remain. **GitHub Issue:** #17 (closed).

### [STORY-16] Fix plain-text admin password comparison — use bcrypt — RESOLVED
**Resolved:** PR #8 branch. `_pwd_context.verify()` in place. **GitHub Issue:** #18 (closed).

### [STORY-17] Fix python-jose CVEs — upgrade to ≥3.4.0 — RESOLVED
**Resolved:** PR #8 branch. `python-jose[cryptography]>=3.4.0`, 0 CVEs. **GitHub Issue:** #19 (closed).

### [STORY-18] Upgrade python-multipart and fastapi to CVE-free versions — RESOLVED
**Resolved:** PR #8 branch. `fastapi==0.137.1`, `starlette==1.3.1`, `python-multipart==0.0.31`, `pydantic>=2.9.0`. AppSec re-scan 2026-06-18: SECURITY CLEAR. **GitHub Issues:** #20, #24, #25 (all closed).

### [STORY-19] Migrate CI credential-shaped env vars to GitHub Actions secrets pattern — RESOLVED
**Resolved:** PR #9 branch. All 5 credential-shaped vars use `${{ secrets.VAR || 'fallback' }}`. **GitHub Issue:** #21 (closed).

### [STORY-20] Upgrade dev dependencies — fix pytest and black CVEs — RESOLVED
**Resolved:** PR #8 branch. `pytest==9.0.3`, `black==26.3.1`. **GitHub Issue:** #22 (closed).
