# Product Backlog

**Project:** OddToBelieve — FastAPI + React/Vite odds aggregation dashboard (Betfair Exchange + The Odds API)  
**PO:** Product Owner Agent  
**Last refined:** 2026-06-13

---

## Priority 1 — Bugs / Blockers

*(none currently)*

---

## Priority 2 — Sprint-Ready Stories

### [STORY-13] Scaffold FastAPI backend project ⚠️ SPRINT-1 PREREQUISITE
**As a** developer, **I want** the backend project scaffolded with the correct directory structure and dependencies **so that** the team can implement and test services without environment friction.  
**Note:** The repo currently contains only `team/` — no backend/ or frontend/ directories exist. This story is a hard prerequisite for STORY-2, STORY-3, STORY-4, and STORY-5.  
**Acceptance criteria:**
- Given the repo has no backend/ directory, When the scaffold is complete, Then `backend/` exists with the layout defined in CLAUDE.md (`app/`, `tests/unit/`, `tests/integration/`, `requirements.txt`)
- Given the scaffold is in place, When `cd backend && uvicorn app.main:app --reload` is run, Then the server starts on port 8000 with no import errors
- Given the scaffold is in place, When GET /docs is accessed, Then the OpenAPI schema page loads
- Given the scaffold is in place, When `ruff check . --fix && black .` is run from `backend/`, Then zero lint errors are reported
- Given the scaffold is in place, When `pytest tests/ -v` is run, Then the test runner initialises without import errors (even if no test files exist yet)
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #1  
**Blocks:** STORY-2, STORY-3, STORY-4, STORY-5

---

### [STORY-1] Set up GitHub Actions CI pipeline
**As a** developer, **I want** CI to run on every PR **so that** broken code is caught before merge.  
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
**Note:** Service does not exist yet — use TDD: write tests and implementation together.  
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
**Note:** Service does not exist yet — use TDD. ⚠️ The Odds API has a hard limit of **500 req/month** — tests must never make real HTTP calls.  
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
**Acceptance criteria:**
- Given `backend/app/` exists, When Bandit is run against it, Then findings are recorded in `team/agents/appsec.md`
- Given `backend/requirements.txt` exists, When pip-audit runs against it, Then dependency CVEs are recorded in `team/agents/appsec.md`
- Given any HIGH or CRITICAL finding is identified, Then a GitHub issue is opened for each one with the finding details
**Owner:** AppSec  
**Estimate:** XS  
**GitHub Issue:** #6  
**Depends on:** STORY-13

---

## Priority 3 — Backlog

### [STORY-14] Scaffold React/Vite frontend project
**As a** developer, **I want** the frontend project scaffolded **so that** the team can implement and test UI components.  
**Acceptance criteria:**
- Given the repo has no `frontend/` directory, When the scaffold is complete, Then `frontend/` exists with the structure from CLAUDE.md (`src/pages/`, `src/components/`, `src/hooks/`, `src/api/`)
- Given the scaffold is complete, When `cd frontend && npm run dev` is run, Then the app serves on port 5173 without errors
- Given the scaffold is complete, When `npm run build` is run, Then the build completes with no errors
- Given the scaffold is complete, When `npm run lint` is run, Then zero lint errors are reported
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #7  
**Blocks:** STORY-6, STORY-8, STORY-9

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

### [STORY-7] Add rate limit guard to OddsApiService
**As a** developer, **I want** the OddsApiService to halt polling when quota is low **so that** the 500 req/month hard limit is never breached.  
**⚠️ The Odds API limit is 500 req/month — this guard is mandatory before enabling the scheduler.**  
**Acceptance criteria:**
- Given `x-requests-remaining < 50`, When the APScheduler job calls `OddsApiService`, Then the HTTP request is NOT made and a `WARNING` is logged with the current remaining count
- Given `x-requests-remaining >= 50`, When the scheduler calls `OddsApiService`, Then the HTTP request proceeds normally
- Given the guard has fired at least once in this process lifetime, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": true}`
- Given the guard has never fired, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": false}`
**Owner:** Engineer  
**Estimate:** S  
**Depends on:** STORY-3

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

### [STORY-10] Add /health endpoint
**As a** developer, **I want** a `/health` endpoint **so that** uptime and database connectivity can be confirmed without authenticating.  
**Acceptance criteria:**
- Given the backend is running, When `GET /health` is called with no auth token, Then HTTP 200 is returned with `{"status": "ok"}`
- Given the SQLite database is reachable, When `GET /health` is called, Then the response body includes `{"db": "ok"}`
- Given the database file is missing or locked, When `GET /health` is called, Then the response body includes `{"db": "error"}` and the HTTP status is still 200 (liveness probe must not 500)
**Owner:** Engineer  
**Estimate:** XS  
**Depends on:** STORY-13

---

### [STORY-11] Add structured logging
**As a** developer, **I want** structured logs **so that** errors and warnings are easy to trace during local development.  
**Acceptance criteria:**
- Given any poll cycle completes, When the scheduler runs, Then an `INFO` log is emitted with sport name and event count
- Given the rate-limit guard fires, When `OddsApiService` skips a request, Then a `WARNING` log is emitted with the remaining request count
- Given any Betfair or Odds API call fails, When the exception is caught, Then an `ERROR` log is emitted with context but without credentials or session tokens
- Given `LOG_LEVEL=DEBUG` is set in the environment, When the app starts, Then `DEBUG`-level messages are emitted
- ⚠️ Betfair session tokens and The Odds API key must never appear in log output at any level
**Owner:** Engineer  
**Estimate:** S  
**Depends on:** STORY-13

---

### [STORY-12] Odds comparison view — Betfair vs Odds API
**As a** user, **I want** to see Betfair and Odds API prices side-by-side for the same event **so that** I can spot pricing discrepancies between sources.  
**Note:** ⚠️ The Odds API has a 500 req/month limit — comparison data must share quota with the existing scheduler. No additional polling calls permitted.  
**Note:** This story may need splitting into backend (cross-source event matching) and frontend (display + highlight) if matching logic proves complex. PO to review at sprint planning.  
**Acceptance criteria:**
- Given an event exists in both Betfair and The Odds API data already in the database, When the comparison view is loaded, Then both sets of odds are displayed in the same row
- Given both sources have odds for the same selection, When the view renders, Then the better price is visually highlighted (e.g. green background or bold text)
- Given an event exists in only one source, When the comparison view loads, Then that row shows the single-source odds with a clear "N/A" for the missing source
**Owner:** Engineer  
**Estimate:** M  
**Depends on:** STORY-2, STORY-3, STORY-14

---

## Done

*(moved here when merged to main)*
