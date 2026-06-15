# AppSec — Status

**Last updated:** 2026-06-15 (Mon/Thu scheduled scan)

## Last Scan

### Bandit (SAST)
- **Run against:** `backend/app/` (PR #8 branch: `agent/engineer/scaffold-fastapi`)
- **Result:** 1 issue — Low/Medium confidence
  - B106 false positive: `token_type="bearer"` in `routers/auth.py:40` flagged as hardcoded password. This is the standard OAuth2 token type string, not a credential. Known false positive — no action required.

### pip-audit (Dependency CVEs)
- **Run against:** `backend/requirements.txt` (PR #8 branch: `agent/engineer/scaffold-fastapi`)
- **Result:** 4 vulnerabilities in 1 package (significant improvement from 15 in 5 packages last scan)

| Package | Version | CVEs | Fix Version | Notes |
|---|---|---|---|---|
| starlette | 0.38.6 | PYSEC-2026-161, CVE-2024-47874, CVE-2025-54121 | 0.47.2 / 1.0.1 | Transitive dep via fastapi==0.115.0 |

**Resolved since last scan (2026-06-13):**
- python-jose 3.3.0 → >=3.4.0 ✅ (zero CVEs)
- python-multipart 0.0.9 → 0.0.27 ✅ (zero CVEs)
- pytest 8.2.2 → 9.0.3 ✅ (zero CVEs)
- black 24.4.2 → 26.3.1 ✅ (zero CVEs)

## Open Security Issues

| # | Title | Severity | PR | Status |
|---|---|---|---|---|
| [#12](https://github.com/cmdperogi/OddToBelieve/issues/12) | python-multipart 0.0.9 and starlette 0.37.2 have multiple CVEs | HIGH | #8 | Open (multipart resolved; starlette 0.38.6 still vulnerable — see #25) |
| [#20](https://github.com/cmdperogi/OddToBelieve/issues/20) | [STORY-18] Upgrade python-multipart and fastapi to CVE-free versions | HIGH | #8 | Open (starlette transitive dep still vulnerable) |
| [#25](https://github.com/cmdperogi/OddToBelieve/issues/25) | starlette 0.38.6 has 3 CVEs — fastapi 0.115.0 transitive dep still vulnerable | HIGH | #8 | Open — NEW this scan |

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

## PRs Reviewed

### PR #8 — feat: scaffold FastAPI backend [`agent/engineer/scaffold-fastapi`]
- **Outcome:** DO NOT MERGE — starlette 0.38.6 CVEs still blocking (issue #25)
- **Blocking findings:** #25 (HIGH) — starlette 0.38.6 transitive CVEs
- **Resolved since last review:** #10 (CRITICAL), #11 (HIGH), #13 (HIGH), #15 (LOW)
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
- **Outcome:** Clean — ready to merge after PR #8 lands
- **Resolved since last review:** #16, #21 (CI credential secrets pattern applied)
- **Clean checks:**
  - All credential-shaped vars use `${{ secrets.VAR || 'safe-fallback' }}` ✅
  - Frontend job guard present: `if: hashFiles('frontend/package.json') != ''` ✅
  - No new runtime dependencies introduced ✅

## Security Baseline Compliance

| Baseline Rule | Status |
|---|---|
| JWT HS256, SECRET_KEY from env only | ✅ No defaults; env required |
| All routes except POST /auth/token use UserDep | ✅ Accepted exception: /health (PO decision D5 — intentional liveness probe, documented in sprint notes) |
| SQLAlchemy ORM only — no raw SQL | ✅ |
| Betfair credentials from env only, never in logs/responses | ✅ |
| CORS: allow_origins=["http://localhost:5173"] only | ✅ |
| Dependencies free of known CVEs | ❌ starlette 0.38.6 (3 CVEs) — issue #25 — blocks PR #8 merge |
