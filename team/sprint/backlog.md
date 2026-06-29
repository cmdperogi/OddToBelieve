# Product Backlog

**Project:** OddToBelieve — FastAPI + React/Vite odds aggregation dashboard (Betfair Exchange + The Odds API)  
**PO:** Product Owner Agent  
**Last refined:** 2026-06-29

---

## Priority 1 — Bugs / Blockers

### Sprint 1 Carry-Overs — MUST MERGE BEFORE ANY SPRINT 2 FEATURE WORK

*Sprint 1 ended 2026-06-27. STORY-3 (PR #28) and STORY-4 (PR #31) did NOT merge by sprint end. They carry into Sprint 2 as the highest-priority items. QA must re-verify PR #28 today; DevOps must merge PR #28 then PR #31 immediately after. STORY-7 and STORY-21a both depend on STORY-3 — no new backend feature work starts until both carry-over PRs land on main.*

---

### [STORY-3] Implement OddsApiService + unit tests (TDD) ⬅ SPRINT 1 CARRY-OVER
**As a** developer, **I want** `OddsApiService` implemented with unit tests **so that** the rate-limit guard and response parsing are verified.  
**Status:** PR #28 open — rebased 2026-06-25 (62/62 passing, 91% coverage); AppSec CLEAR. QA must re-verify final rebase HEAD (`9641eb2`+`2ed2ce2` on `090413e`); DevOps merges immediately on QA LGTM.  
**Note:** ⚠️ The Odds API has a hard limit of **500 req/month** — tests must never make real HTTP calls.  
**Acceptance criteria:**
- Given `x-requests-remaining < 50` in a mocked response header, When `OddsApiService.fetch()` is called, Then the HTTP request is NOT made and a `WARNING` is logged with the remaining count
- Given `x-requests-remaining >= 50`, When `OddsApiService.fetch()` is called, Then the HTTP request proceeds normally
- Given a valid Odds API response payload, When odds are parsed, Then `Event`, `Market`, and `Odds` records are created with correct field values
- Given any test in this suite runs, Then no real HTTP requests are made to `api.the-odds-api.com`  
**Owner:** Engineer + QA  
**Estimate:** S  
**GitHub Issue:** #4  
**Depends on:** STORY-13 ✅

---

### [STORY-4] Write integration tests for /odds/* endpoints ⬅ SPRINT 1 CARRY-OVER
**As a** developer, **I want** integration tests for the odds endpoints **so that** auth enforcement and response shapes are verified.  
**Status:** PR #31 open — all gates CLEAR (CI GREEN ✅, QA LGTM 2026-06-23 ✅, AppSec CLEAR ✅). Merge immediately after PR #28.  
**Acceptance criteria:**
- Given no auth token, When `GET /odds/events` is called, Then HTTP 401 is returned
- Given a valid JWT token, When `GET /odds/events` is called, Then a list conforming to `EventSchema` is returned
- Given an invalid `event_id`, When `GET /odds/events/{id}` is called, Then HTTP 404 is returned
- Given a valid `event_id`, When `GET /odds/events/{id}/markets` is called, Then a list conforming to `MarketSchema` is returned
- Given the integration test suite runs, Then no real Betfair or Odds API calls are made (services mocked or DB seeded with fixtures)  
**Owner:** QA  
**Estimate:** S  
**GitHub Issue:** #5  
**Depends on:** STORY-13 ✅

---

## Priority 2 — Sprint 2 Stories

*Sprint 2 starts 2026-06-29. Ordered by dependency chain: health → logging → rate guard → scheduler (Betfair first, then Odds API) → frontend scaffold. STORY-7 and STORY-21a are blocked on STORY-3 merging.*

---

### [STORY-10] Add /health endpoint
**As a** developer, **I want** a `/health` endpoint **so that** uptime and database connectivity can be confirmed without authenticating.  
**Note:** XS estimate — first Sprint 2 backend task. Safe to start in parallel with STORY-11 immediately after carry-over PRs merge.  
**Acceptance criteria:**
- Given the backend is running, When `GET /health` is called with no auth token, Then HTTP 200 is returned with `{"status": "ok"}`
- Given the SQLite database file is reachable, When `GET /health` is called, Then the response body includes `{"db": "ok"}`
- Given the database file is missing or locked, When `GET /health` is called, Then the response body includes `{"db": "error"}` and the HTTP status is still 200 (liveness semantics — a 500 here would break monitoring tools)
- Given the endpoint is inspected, When the route definition is read, Then no `UserDep` or auth dependency is applied — this is the named public exception (PO decision D5)
- Given `GET /health` is called in any state, When the response is received, Then `Content-Type: application/json` is present in the response headers  
**Owner:** Engineer  
**Estimate:** XS  
**GitHub Issue:** #38  
**Depends on:** STORY-13 ✅

---

### [STORY-11] Add structured logging
**As a** developer, **I want** structured logs **so that** errors and warnings are easy to trace during local development.  
**Note:** Safe to develop in parallel with STORY-10. No inter-dependency between them.  
**Acceptance criteria:**
- Given any poll cycle completes, When the scheduler runs, Then an `INFO` log is emitted with sport name and event count
- Given the rate-limit guard fires, When `OddsApiService` skips a request, Then a `WARNING` log is emitted with the remaining request count
- Given any Betfair or Odds API call fails, When the exception is caught, Then an `ERROR` log is emitted with context but without credentials or session tokens
- Given `LOG_LEVEL=DEBUG` is set in the environment, When the app starts, Then `DEBUG`-level messages are emitted
- Given any log message is emitted at `WARNING` or higher, When the logger formats the message, Then the output includes the module name to aid debugging
- ⚠️ Betfair session tokens and The Odds API key must never appear in log output at any level  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #39  
**Depends on:** STORY-13 ✅

---

### [STORY-7] Add rate limit guard to OddsApiService
**As a** developer, **I want** the OddsApiService to halt polling when quota is low **so that** the 500 req/month hard limit is never breached.  
**Note:** ⚠️ This guard is a safety net, not the primary monthly budget control — `ODDS_API_POLL_INTERVAL_MINUTES=360` (STORY-21b) is the primary control. Mandatory before STORY-21b starts.  
**⚠️ Rate limit budget check:** At 60-min polling, OddsApiService makes 720 calls/month — 44% over the 500 req/month cap. This guard (threshold < 50 remaining) prevents the tail from exhausting. STORY-21b's 360-min default interval (120 calls/month) is the real protection.  
**Acceptance criteria:**
- Given `x-requests-remaining < 50`, When the APScheduler job calls `OddsApiService`, Then the HTTP request is NOT made and a `WARNING` is logged with the current remaining count
- Given `x-requests-remaining >= 50`, When the scheduler calls `OddsApiService`, Then the HTTP request proceeds normally
- Given the guard has fired at least once in this process lifetime, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": true}`
- Given the guard has never fired, When `GET /odds/api-status` is called, Then the response includes `{"requests_remaining": <n>, "guard_active": false}`
- Given the guard was active (`x-requests-remaining < 50`), When a subsequent response header shows `x-requests-remaining >= 50`, Then the guard deactivates and `GET /odds/api-status` returns `{"guard_active": false}`  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #40  
**Depends on:** STORY-3

---

### [STORY-21a] Add APScheduler — Betfair background polling job
**As a** developer, **I want** an APScheduler job to poll Betfair on a configured interval **so that** the database stays fresh without manual triggering.  
**Note:** Split from STORY-21 (PO decision D17, 2026-06-29). STORY-21b (Odds API job) must not start until this story merges. Original GitHub issue: #33.  
**Acceptance criteria:**
- Given the app starts, When the scheduler initialises, Then a Betfair poll job is registered at `BETFAIR_POLL_INTERVAL_MINUTES` (default: 60 min)
- Given a Betfair poll cycle runs, When `BetfairClient.list_events()` returns events, Then `Event`, `Market`, and `Odds` records are upserted in SQLite with `source="betfair"` — new records are inserted, changed prices are updated (no duplicate rows)
- Given a Betfair poll cycle runs and the event already exists in the DB, When the upsert runs, Then the existing record is updated rather than duplicated (idempotent on `source_id`)
- Given Betfair re-auth fails during a poll cycle, When the exception is raised, Then the error is logged without credentials or session tokens and the scheduler continues — the process does NOT crash
- Given any test in this story runs, Then no real Betfair API calls are made; `BetfairClient` is mocked  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #41  
**Depends on:** STORY-2 ✅, STORY-3

---

### [STORY-21b] Add APScheduler — Odds API background polling job
**As a** developer, **I want** an APScheduler job to poll The Odds API on a configured interval **so that** the database stays fresh without exhausting the 500 req/month cap.  
**Note:** Split from STORY-21 (PO decision D17, 2026-06-29). ⚠️ `ODDS_API_POLL_INTERVAL_MINUTES` must default to **360 min (6h)** — this gives 120 calls/month against the 500 req/month hard cap. Do not lower this default without explicit PO sign-off and rate-limit recalculation. Original GitHub issue: #33.  
**⚠️ The Odds API has a hard limit of 500 req/month.** Default 360 min = 120 req/month (safe). At 60 min it would be 720 req/month (over cap).  
**Acceptance criteria:**
- Given the app starts, When the scheduler initialises, Then an Odds API poll job is registered at `ODDS_API_POLL_INTERVAL_MINUTES` (default: 360 min), independent of `BETFAIR_POLL_INTERVAL_MINUTES`
- Given an Odds API poll cycle runs, When `OddsApiService.fetch()` returns data, Then `Event`, `Market`, and `Odds` records are upserted in SQLite with `source="odds_api"`
- Given the OddsApiService rate guard is active (`x-requests-remaining < 50`), When the Odds API scheduler job runs, Then `OddsApiService.fetch()` is NOT called; a `WARNING` is logged; Betfair polling is unaffected and continues on its own schedule
- Given Betfair polling is running and the Odds API guard fires, When the next `BETFAIR_POLL_INTERVAL_MINUTES` elapses, Then the Betfair job runs normally — the two schedules are fully independent
- Given any test in this story runs, Then no real Betfair or Odds API calls are made; both services are mocked  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #42  
**Depends on:** STORY-21a, STORY-7

---

### [STORY-14] Scaffold React/Vite frontend project
**As a** developer, **I want** the frontend project scaffolded **so that** the team can implement and test UI components.  
**Note:** All frontend stories (STORY-6, 8, 9, 22, 23, 12b) are blocked on this. Safe to develop in parallel with STORY-21a/21b by a separate developer.  
**Acceptance criteria:**
- Given the repo has no `frontend/` directory, When the scaffold is complete, Then `frontend/` exists with the structure from CLAUDE.md (`src/pages/`, `src/components/`, `src/hooks/`, `src/api/`)
- Given the scaffold is complete, When `cd frontend && npm run dev` is run, Then the app serves on port 5173 without errors
- Given the scaffold is complete, When `npm run build` is run, Then the build completes with no errors
- Given the scaffold is complete, When `npm run lint` is run, Then zero lint errors are reported
- Given the scaffold is complete, When a `.env.local` file is added with `VITE_API_BASE_URL=http://localhost:8000`, When `npm run dev` is run, Then the API base URL is read from the env variable (no hardcoded `localhost:8000` in source files)
- Given the scaffold is complete, When `frontend/` is inspected, Then TypeScript (`tsconfig.json`) is configured — all component files use `.tsx` extension, not `.jsx`
- Given the scaffold includes a placeholder home page at `/`, When the user navigates to `http://localhost:5173`, Then a placeholder message (e.g. "OddToBelieve") is visible — not a generic Vite default starter page  
**Owner:** Engineer  
**Estimate:** S  
**GitHub Issue:** #7  
**Blocks:** STORY-6, STORY-8, STORY-9, STORY-22, STORY-23, STORY-12b

---

## Priority 3 — Backlog

*Sprint 2+ scope. Ordered by: reliability > UX > new features. Frontend stories are all blocked on STORY-14.*

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
**Depends on:** STORY-14, STORY-22, STORY-4

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
**GitHub Issue:** #43  
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
**GitHub Issue:** #44  
**Depends on:** STORY-14

---

### [STORY-9] Frontend loading states and error handling
**As a** user, **I want** clear loading and error states **so that** I know what is happening when data is slow or unavailable.  
**Note:** STORY-23 covers loading/error states for the main OddsTable. This story covers the global error boundary and app-level patterns.  
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
**Depends on:** STORY-2 ✅, STORY-3, STORY-21b

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

### [STORY-2] Implement BetfairClient + unit tests (TDD) — RESOLVED
**Resolved:** PR #26 merged 2026-06-23. 40/40 tests passing, 100% coverage. **GitHub Issue:** #3 (close overdue — action for Prod Support).

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
