# AppSec — Status

**Last updated:** 2026-06-18 (Mon/Thu scheduled scan)

## Last Scan

### Bandit (SAST)
- **Run against:** `backend/app/` (PR #8 branch: `agent/engineer/scaffold-fastapi`)
- **Result:** 1 issue — Low/Medium confidence
  - B106 false positive: `token_type="bearer"` in `routers/auth.py:40` flagged as hardcoded password. This is the standard OAuth2 token type string, not a credential. Known false positive — no action required.

### pip-audit (Dependency CVEs)
- **Run against:** `backend/requirements.txt` (PR #8 branch: `agent/engineer/scaffold-fastapi`)
- **Result:** ✅ **CLEAN — No known vulnerabilities found**

**Resolved since last scan (2026-06-15):**
- starlette 0.38.6 → 1.3.1 ✅ (via fastapi==0.137.1; PYSEC-2026-161, CVE-2024-47874, CVE-2025-54121 all resolved)

### New PRs scanned this cycle

| PR | Branch | New security findings |
|---|---|---|
| #26 | `agent/engineer/unit-tests-betfair` | None |
| #28 | `agent/engineer/unit-tests-oddsapi` | None |

## Open Security Issues

| # | Title | Severity | PR | Status |
|---|---|---|---|---|
| [#12](https://github.com/cmdperogi/OddToBelieve/issues/12) | python-multipart 0.0.9 and starlette 0.37.2 have multiple CVEs | HIGH | #8 | Resolved in current requirements; awaiting formal close |
| [#20](https://github.com/cmdperogi/OddToBelieve/issues/20) | [STORY-18] Upgrade python-multipart and fastapi to CVE-free versions | HIGH | #8 | Resolved in current requirements; awaiting formal close |

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
- **Outcome:** ✅ Clean — no security issues
- **Clean checks:**
  - All Betfair HTTP calls fully mocked — no real network requests ✅
  - No Betfair credentials referenced in test assertions or log output ✅
  - Mock session tokens ("stale-token", "valid-token") are test fixtures only ✅
  - `conftest.py` uses `os.environ.setdefault()` with test-only placeholder values ✅
  - No new runtime dependencies introduced ✅

### PR #28 — feat: OddsApiService unit tests [`agent/engineer/unit-tests-oddsapi`]
- **Outcome:** ✅ Clean — no security issues
- **Clean checks:**
  - All Odds API HTTP calls fully mocked — no real network requests ✅
  - API key never referenced in assertions or log output ✅
  - Quota guard behavior tested correctly (no API calls when remaining < 50) ✅
  - App code identical to PR #8 — no new security surface introduced ✅
  - No new runtime dependencies introduced ✅

## Security Baseline Compliance

| Baseline Rule | Status |
|---|---|
| JWT HS256, SECRET_KEY from env only | ✅ No defaults; env required |
| All routes except POST /auth/token use UserDep | ✅ Accepted exception: /health (PO decision D5 — intentional liveness probe) |
| SQLAlchemy ORM only — no raw SQL | ✅ |
| Betfair credentials from env only, never in logs/responses | ✅ |
| CORS: allow_origins=["http://localhost:5173"] only | ✅ |
| Dependencies free of known CVEs | ✅ pip-audit clean — starlette 1.3.1 via fastapi 0.137.1 |
