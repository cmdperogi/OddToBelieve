# Product Backlog

**Project:** OddToBelieve — FastAPI + React/Vite odds aggregation dashboard (Betfair Exchange + The Odds API)  
**PO:** Product Owner Agent  
**Last refined:** 2026-06-13

---

## Priority 1 — Bugs / Blockers

*(none currently)*

---

## Priority 2 — Sprint-Ready Stories

### [STORY-1] Set up GitHub Actions CI pipeline
**As a** developer, **I want** CI to run on every PR **so that** broken code is caught before merge.  
**Acceptance criteria:**
- Given a PR is opened, When CI runs, Then backend lint + tests pass
- Given a PR is opened, When CI runs, Then frontend lint + build passes
- Given a test fails, Then the PR is blocked from merge
**Owner:** DevOps  
**Estimate:** S  
**GitHub Issue:** (to be created)

### [STORY-2] Write unit tests for BetfairClient
**As a** developer, **I want** unit tests for BetfairClient **so that** auth and retry logic is verified without hitting the real API.  
**Acceptance criteria:**
- Given a successful login response, When _login() is called, Then session token is stored
- Given a 403 response on first request, When _post() is called, Then it re-authenticates and retries once
- Given a non-SUCCESS login status, When _login() is called, Then RuntimeError is raised
**Owner:** QA / Engineer  
**Estimate:** S  
**GitHub Issue:** (to be created)

### [STORY-3] Write unit tests for OddsApiService
**As a** developer, **I want** unit tests for OddsApiService **so that** rate limit guard and response parsing are verified.  
**Acceptance criteria:**
- Given x-requests-remaining < 50, When fetch is called, Then the request is skipped and a warning is logged
- Given a valid API response, When odds are parsed, Then Event/Market/Odds records are created correctly
**Owner:** QA / Engineer  
**Estimate:** S  
**GitHub Issue:** (to be created)

### [STORY-4] Write integration tests for /odds/* endpoints
**As a** developer, **I want** integration tests for the odds endpoints **so that** auth enforcement and response shapes are verified.  
**Acceptance criteria:**
- Given no auth token, When GET /odds/events is called, Then 401 is returned
- Given a valid token, When GET /odds/events is called, Then list of EventSchema is returned
- Given an invalid event_id, When GET /odds/events/{id} is called, Then 404 is returned
- Given a valid event_id, When GET /odds/events/{id}/markets is called, Then list of MarketSchema is returned
**Owner:** QA  
**Estimate:** S  
**GitHub Issue:** (to be created)

### [STORY-5] AppSec baseline scan
**As a** security engineer, **I want** a Bandit + pip-audit baseline run **so that** existing vulnerabilities are documented.  
**Acceptance criteria:**
- Bandit scan of backend/app/ completes with findings documented
- pip-audit scan of requirements.txt completes with findings documented
- All HIGH/CRITICAL findings have GitHub issues opened
**Owner:** AppSec  
**Estimate:** XS  
**GitHub Issue:** (to be created)

---

## Priority 3 — Backlog

### [STORY-6] Add Vitest to frontend and write component tests
**As a** developer, **I want** frontend unit tests **so that** React component logic is verified.  
**Acceptance criteria:**
- Vitest is installed and runnable via `npm test`
- At least one component test exists for the odds display component
- Tests run in CI

### [STORY-7] Add rate limit guard to OddsApiService
**As a** developer, **I want** the OddsApiService to stop polling when quota is low **so that** we don't exhaust the 500 req/month limit.  
**Acceptance criteria:**
- Given x-requests-remaining < 50, When the scheduler calls the service, Then the API is not called and a warning is logged
- The remaining count is readable from a GET /odds/api-status endpoint

### [STORY-8] Add sport filter UI to React dashboard
**As a** user, **I want** to filter odds by sport (soccer / horse racing) **so that** I can focus on my sport of choice.  
**Acceptance criteria:**
- Filter buttons for Soccer and Horse Racing are visible
- Selecting a filter updates the event list without a page reload
- Filter state is preserved on page refresh (localStorage)

### [STORY-9] Frontend loading states and error handling
**As a** user, **I want** clear loading and error states **so that** I know what's happening when data is slow or unavailable.  
**Acceptance criteria:**
- A loading spinner is shown while events are fetching
- A user-friendly error message is shown if the API is unreachable
- An error boundary wraps the main dashboard

### [STORY-10] Add /health endpoint
**As a** developer, **I want** a /health endpoint **so that** uptime can be verified quickly.  
**Acceptance criteria:**
- GET /health returns 200 with `{"status": "ok"}` (no auth required)
- Response includes db connectivity check

### [STORY-11] Add structured logging
**As a** developer, **I want** structured logs **so that** errors and warnings are easy to trace.  
**Acceptance criteria:**
- All services log at appropriate levels (INFO for poll cycles, WARNING for rate limits, ERROR for failures)
- Log level is configurable via env var `LOG_LEVEL`
- No credentials or tokens appear in logs

### [STORY-12] Odds comparison view — Betfair vs Odds API
**As a** user, **I want** to see Betfair and Odds API prices side-by-side for the same event **so that** I can spot discrepancies.  
**Acceptance criteria:**
- For events that exist in both sources, odds from both are shown together
- The better price is visually highlighted

---

## Done

*(moved here when merged to main)*
