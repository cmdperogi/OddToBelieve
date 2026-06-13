# AppSec — Status

**Last updated:** 2026-06-13 (Mon/Thu scheduled scan)

## Last Scan

### Bandit (SAST)
- **Run against:** `backend/app/` (PR #8 branch: `agent/engineer/scaffold-fastapi`)
- **Result:** 1 issue — Low/Medium confidence
  - B106 false positive: `token_type="bearer"` in `routers/auth.py:37` flagged as hardcoded password. This is the standard OAuth2 token type string, not a credential.

### pip-audit (Dependency CVEs)
- **Run against:** `backend/requirements.txt` (PR #8 branch)
- **Result:** 15 vulnerabilities in 5 packages

| Package | Version | CVEs | Fix Version |
|---|---|---|---|
| python-jose | 3.3.0 | PYSEC-2024-232, PYSEC-2024-233, PYSEC-2025-185 | 3.4.0 |
| python-multipart | 0.0.9 | CVE-2024-53981, CVE-2026-24486, CVE-2026-40347, CVE-2026-42561 | 0.0.27 |
| starlette | 0.37.2 | PYSEC-2026-161, CVE-2024-47874, CVE-2025-54121 | 1.0.1 |
| pytest | 8.2.2 | CVE-2025-71176 | 9.0.3 |
| black | 24.4.2 | CVE-2026-32274 | 26.3.1 |

## Open Security Issues

| # | Title | Severity | PR | Status |
|---|---|---|---|---|
| [#10](https://github.com/cmdperogi/OddToBelieve/issues/10) | Hardcoded default SECRET_KEY and admin credentials in config.py | CRITICAL | #8 | Open |
| [#11](https://github.com/cmdperogi/OddToBelieve/issues/11) | python-jose 3.3.0 has 3 CVEs — JWT authentication at risk | HIGH | #8 | Open |
| [#12](https://github.com/cmdperogi/OddToBelieve/issues/12) | python-multipart 0.0.9 and starlette 0.37.2 have multiple CVEs | HIGH | #8 | Open |
| [#13](https://github.com/cmdperogi/OddToBelieve/issues/13) | Admin password compared as plain text — bcrypt imported but unused | HIGH | #8 | Open |
| [#14](https://github.com/cmdperogi/OddToBelieve/issues/14) | /health route missing UserDep — violates auth baseline | LOW | #8 | Open |
| [#15](https://github.com/cmdperogi/OddToBelieve/issues/15) | pytest 8.2.2 (CVE-2025-71176) and black 24.4.2 (CVE-2026-32274) — dev dep CVEs | LOW | #8 | Open |
| [#16](https://github.com/cmdperogi/OddToBelieve/issues/16) | CI workflow hardcodes Betfair test credentials in YAML | LOW | #9 | Open |

## PRs Reviewed

### PR #8 — feat: scaffold FastAPI backend [`agent/engineer/scaffold-fastapi`]
- **Outcome:** DO NOT MERGE — blocking comment posted
- **Blocking findings:** #10 (CRITICAL), #11 (HIGH), #12 (HIGH), #13 (HIGH)
- **Non-blocking:** #14, #15 (LOW)
- **Clean checks:**
  - No raw SQL strings or f-strings in queries (SQLAlchemy ORM used throughout)
  - No JWT or Betfair credentials in logs or responses
  - CORS correctly set to `allow_origins=["http://localhost:5173"]`
  - All `/odds/*` routes correctly use `UserDep`
  - Betfair credentials read from env via pydantic-settings (not hardcoded)

### PR #9 — chore: add GitHub Actions CI [`agent/devops/github-actions-ci`]
- **Outcome:** Non-blocking comment posted (Issue #16 LOW)
- **Clean checks:**
  - No real credentials committed (all values are test placeholders)
  - No new runtime dependencies introduced
  - BETFAIR env vars are test-only values, not production credentials

## Security Baseline Compliance

| Baseline Rule | Status |
|---|---|
| JWT HS256, SECRET_KEY from env only | ❌ Default fallback in config.py (#10) |
| All routes except POST /auth/token use UserDep | ❌ /health unprotected (#14) |
| SQLAlchemy ORM only — no raw SQL | ✅ |
| Betfair credentials from env only, never in logs/responses | ✅ (runtime) / ⚠️ test YAML (#16) |
| CORS: allow_origins=["http://localhost:5173"] only | ✅ |
