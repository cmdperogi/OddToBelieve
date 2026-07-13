# AppSec — Status

**Last updated:** 2026-07-13 (Mon/Thu scheduled scan)

## Last Scan

### Bandit (SAST)
- **Run against:** `backend/app/` (main)
- **Result:** 1 issue — Low/Medium confidence
  - B106 false positive: `token_type="bearer"` in `routers/auth.py:40` flagged as hardcoded password. This is the standard OAuth2 token type string, not a credential. Known false positive — no action required.
- **No change from prior cycle.**

### pip-audit (Dependency CVEs)
- **Run against:** `backend/requirements.txt` (main)
- **Result:** ⚠️ **1 vulnerability found**
  - `ecdsa 0.19.2` — PYSEC-2026-1325 (Minerva timing attack on P-256 curve)
  - **Severity:** LOW — ecdsa is a transitive dep of `python-jose[cryptography]`; application uses HS256 only; no ECDSA signing surfaces exposed
  - **Fix versions:** None available — unchanged from prior cycle
  - **Tracking:** Issue #54 remains open (accepted risk)

### PRs scanned this cycle

| PR | Branch | Status | Verdict |
|---|---|---|---|
| (none) | — | All PRs closed/merged | No review actions required |

**Note:** PR #28 (`agent/engineer/unit-tests-oddsapi`) shows as merged on GitHub (2026-07-03) but its commits (`_persist()` method in `odds_api.py`, `test_odds_api_service.py`) are not present in the tip of `origin/main`. The merge commit (c5fa096) exists only in `agent/engineer/unit-tests-betfair`. The security review for those changes remains SECURITY CLEAR from the 2026-06-22 cycle; no blocking findings were identified then and the code is unchanged. The discrepancy is a git history anomaly — the feature code passes all security baseline checks regardless of which branch it lands in.

### Issues opened this cycle
None.

### Issues closed this cycle
None — issue #54 (ecdsa CVE) remains open: pip-audit confirms no fix version is available.

## Open Security Issues

| # | Title | Severity | Status |
|---|---|---|---|
| [#54](https://github.com/cmdperogi/OddToBelieve/issues/54) | ecdsa 0.19.2 PYSEC-2026-1325 — Minerva timing attack (transitive dep, no fix available) | LOW | Accepted risk; monitor for upstream fix |

## Resolved Issues (closed this scan)

| # | Title | Severity | Resolution |
|---|---|---|---|
| [#10](https://github.com/cmdperogi/OddToBelieve/issues/10) | Hardcoded default SECRET_KEY and admin credentials in config.py | CRITICAL | ✅ Closed — config.py has no defaults; validators enforce env vars |
| [#11](https://github.com/cmdperogi/OddToBelieve/issues/11) | python-jose 3.3.0 has 3 CVEs | HIGH | ✅ Closed — pinned >=3.4.0; zero CVEs confirmed |
| [#13](https://github.com/cmdperogi/OddToBelieve/issues/13) | Admin password compared as plain text | HIGH | ✅ Closed — bcrypt hash at startup + verify on login |
| [#14](https://github.com/cmdperogi/OddToBelieve/issues/14) | /health route missing UserDep | LOW | ✅ Closed — accepted design exception (PO decision D5); intentional liveness probe |
| [#15](https://github.com/cmdperogi/OddToBelieve/issues/15) | pytest/black dev dep CVEs | LOW | ✅ Closed — pinned pytest==9.0.3, black==26.3.1 |
| [#16](https://github.com/cmdperogi/OddToBelieve/issues/16) | CI workflow hardcodes Betfair test credentials | LOW | ✅ Closed — ci.yml uses secrets pattern with fallbacks |
| [#17](https://github.com/cmdperogi/OddToBelieve/issues/17) | [STORY-15] Fix hardcoded credential defaults | HIGH | ✅ Closed — same fix as #10 |
| [#18](https://github.com/cmdperogi/OddToBelieve/issues/18) | [STORY-16] Fix plain-text password comparison | HIGH | ✅ Closed — same fix as #13 |
| [#19](https://github.com/cmdperogi/OddToBelieve/issues/19) | [STORY-17] Fix python-jose CVEs | HIGH | ✅ Closed — same fix as #11 |
| [#21](https://github.com/cmdperogi/OddToBelieve/issues/21) | [STORY-19] Migrate CI credentials to secrets pattern | MEDIUM | ✅ Closed — same fix as #16 |
| [#22](https://github.com/cmdperogi/OddToBelieve/issues/22) | [STORY-20] Upgrade dev deps — fix pytest and black CVEs | LOW | ✅ Closed — same fix as #15 |
| [#12](https://github.com/cmdperogi/OddToBelieve/issues/12) | python-multipart 0.0.9 and starlette 0.37.2 have multiple CVEs | HIGH | ✅ Confirmed closed — requirements upgraded; pip-audit clean |
| [#20](https://github.com/cmdperogi/OddToBelieve/issues/20) | [STORY-18] Upgrade python-multipart and fastapi to CVE-free versions | HIGH | ✅ Confirmed closed — fastapi==0.137.1, python-multipart==0.0.31 |
| [#25](https://github.com/cmdperogi/OddToBelieve/issues/25) | starlette 0.38.6 has 3 CVEs — fastapi 0.115.0 transitive dep | HIGH | ✅ Resolved — fastapi==0.137.1 pulls starlette==1.3.1; pip-audit clean |
| [#29](https://github.com/cmdperogi/OddToBelieve/issues/29) | /health endpoint lacks UserDep authentication | LOW | ✅ Closed — duplicate of #14; PO D5 exception still applies |
| [#30](https://github.com/cmdperogi/OddToBelieve/issues/30) | CI workflow falls back to plaintext hardcoded credentials when secrets unset | LOW | ✅ Closed — duplicate of #16; team accepted fallback pattern for local-only app |

## PRs Reviewed

### PR #8 — feat: scaffold FastAPI backend [`agent/engineer/scaffold-fastapi`]
- **Outcome:** ✅ **SECURITY CLEAR** — starlette CVE resolved; no blocking findings
- **Resolved since last review:** #25 (HIGH) — starlette now 1.3.1 via fastapi 0.137.1
- **Non-blocking / accepted exceptions:** #14 (design exception — PO D5)
- **Clean checks:**
  - No raw SQL strings or f-strings in queries (SQLAlchemy ORM throughout) ✅
  - No JWT or Betfair credentials in logs or responses ✅
  - CORS correctly set to `allow_origins=["http://localhost:5173"]` ✅
  - All `/odds/*` routes correctly use `UserDep` ✅
  - Betfair credentials read from env via pydantic-settings ✅
  - SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD — no defaults, env required ✅
  - Admin password bcrypt-hashed at startup; `verify()` used on login ✅

### PR #9 — chore: add GitHub Actions CI [`agent/devops/github-actions-ci`]
- **Outcome:** ✅ Clean — ready to merge after PR #8 lands
- **Clean checks:**
  - All credential-shaped vars use `${{ secrets.VAR || 'safe-fallback' }}` ✅
  - Frontend job guard present (step-level) ✅
  - No new runtime dependencies introduced ✅

### PR #26 — feat: BetfairClient unit tests [`agent/engineer/unit-tests-betfair`]
- **Reviewed:** 2026-06-22
- **Outcome:** ✅ **SECURITY CLEAR** — AppSec sign-off comment posted
- **Clean checks:**
  - All Betfair HTTP calls fully mocked — no real network requests ✅
  - No Betfair credentials referenced in test assertions or log output ✅
  - Mock session tokens ("stale-token", "valid-token") are test fixtures only ✅
  - `betfair.py` reads credentials exclusively from settings.betfair_username/password/app_key ✅
  - 403 re-auth path logs only status ("Betfair 403 — re-authenticating"), never token values ✅
  - `conftest.py` uses `os.environ.setdefault()` with test-only placeholder values ✅
  - No new runtime dependencies introduced ✅

### PR #28 — feat: OddsApiService unit tests [`agent/engineer/unit-tests-oddsapi`]
- **Reviewed:** 2026-06-22
- **Outcome:** ✅ **SECURITY CLEAR** — AppSec sign-off comment posted
- **Clean checks:**
  - All Odds API HTTP calls fully mocked — no real network requests ✅
  - API key never referenced in assertions or log output ✅
  - `_persist()` method in odds_api.py uses SQLAlchemy ORM exclusively (Event/Market/Odds via db.add/flush/commit) — no raw SQL ✅
  - Quota guard behavior tested correctly (no API calls when remaining < 10) ✅
  - No new runtime dependencies introduced ✅

### PR #31 — test: STORY-4 integration tests for /odds/* endpoints [`agent/qa/integration-tests-odds`] *(DRAFT)*
- **Reviewed:** 2026-06-22
- **Outcome:** ✅ **SECURITY CLEAR** — AppSec sign-off comment posted (noted DRAFT status)
- **Clean checks:**
  - No hardcoded credentials or API keys — `conftest.py` uses `os.environ.setdefault()` with test-only placeholder values (`SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`) ✅
  - No raw SQL — tests use ORM models exclusively for fixture seeding ✅
  - All `/odds/*` routes still require `UserDep`; integration tests verify 401 on every endpoint without auth ✅
  - No JWT or Betfair credentials in assertions or log output ✅
  - CORS unchanged at `allow_origins=["http://localhost:5173"]` ✅
  - No new runtime dependencies introduced; pip-audit clean ✅
  - No real HTTP calls to Betfair or Odds API — DB-seeded fixtures only ✅

### PR #52 — feat: add rate limit guard and GET /odds/api-status [STORY-7] [`agent/engineer/rate-limit-guard`]
- **Reviewed:** 2026-07-09
- **Outcome:** ✅ **SECURITY CLEAR** — AppSec sign-off comment posted
- **Clean checks:**
  - New `GET /odds/api-status` endpoint uses `UserDep` ✅
  - Response exposes only `requests_remaining: int|None` and `guard_active: bool` — no credential leakage ✅
  - Quota guard logs only request count, never API key ✅
  - No raw SQL — ORM-only patterns ✅
  - No hardcoded credentials ✅
  - CORS unchanged ✅
  - No new runtime dependencies; `requirements.txt` unchanged ✅
  - Betfair/JWT credentials from env only ✅

### PR #53 — feat: scaffold React/Vite TypeScript frontend [STORY-14] [`agent/engineer/frontend-scaffold`]
- **Reviewed:** 2026-07-09
- **Outcome:** ✅ **SECURITY CLEAR** — AppSec sign-off comment posted
- **Clean checks:**
  - Frontend-only PR — no backend changes ✅
  - `src/api/config.ts` reads `import.meta.env.VITE_API_BASE_URL` only — no hardcoded URLs ✅
  - `.env.local.example` contains no real credentials (template only) ✅
  - `.gitignore` covers `*.local` — prevents committing `.env.local` ✅
  - No CORS changes ✅
  - `requirements.txt` unchanged ✅

### Cycle 2026-07-13 — No open PRs
- **PRs reviewed:** 0 (GitHub confirmed 0 open PRs)
- **Bandit:** unchanged — 1 LOW false positive (B106, known)
- **pip-audit:** unchanged — ecdsa 0.19.2 PYSEC-2026-1325, no fix available, issue #54 open
- **Open security issues:** #54 only (LOW, accepted risk)
- **Baseline compliance:** all checks pass — see table below

## Security Baseline Compliance

| Baseline Rule | Status |
|---|---|
| JWT HS256, SECRET_KEY from env only | ✅ No defaults; env required |
| All routes except POST /auth/token use UserDep | ✅ Accepted exception: /health (PO decision D5 — intentional liveness probe) |
| SQLAlchemy ORM only — no raw SQL | ✅ |
| Betfair credentials from env only, never in logs/responses | ✅ |
| CORS: allow_origins=["http://localhost:5173"] only | ✅ |
| Dependencies free of known CVEs | ⚠️ ecdsa 0.19.2 PYSEC-2026-1325 (LOW — transitive dep, HS256-only app, no fix available) — tracked in #54 |
