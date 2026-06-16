# Prod Support — Status

**Last updated:** 2026-06-16

## Open Issues (Triaged)

**Total open issues at run start:** 11 (#1–#7, #12, #20, #24, #25)

All issues already had labels — no unlabeled issues found. No issues are stale (oldest
open issue created 2026-06-13, 3 days old — below the 7-day threshold).

### Hygiene fix this run

- **#24 / #25 were exact duplicates** (same starlette CVE finding, opened 10 minutes
  apart on 2026-06-15 by the AppSec scan). Closed **#25** as a duplicate of **#24**.

## Git Log Review (last 10 commits on main)

All commits are agent status-file updates. No direct application-code pushes to main,
no bypassed PRs, no broken imports introduced on main. No policy violations found.

## CI Status

`gh run list --branch main` returns **no runs** — there is no `.github/workflows/`
directory on `main` yet; the CI workflow only exists on the unmerged
`agent/devops/github-actions-ci` branch (PR #9).

Recent runs on agent branches are failing, but this is expected and already understood
by the team: PR #9's backend job runs `pip install -r backend/requirements.txt`, and
`backend/` only exists on the unmerged PR #8 branch. Per the documented merge order
(PR #8 → PR #9), these failures clear once PR #8 lands. No new CI defect found.

## Escalated Blocker — Updated (re-scan, not new)

**PR #8 (FastAPI backend scaffold) remains the single blocker for the whole sprint**
(blocks PR #9, and STORY-2/3/4/5 behind it). This was already tracked via issues
#10–#13, #24/#25, but I re-ran `pip-audit` against the live PR #8 branch today and the
situation has gotten worse, not better:

- `pip-audit` now reports **11 CVEs across starlette and python-multipart** (previously
  3, starlette-only, on the most recent AppSec pass 2026-06-15). New CVEs have been
  disclosed against `python-multipart==0.0.27` — the version that was upgraded *to* as
  the prior fix.
- The fix this issue currently recommends (pin `starlette>=0.47.2` next to
  `fastapi==0.115.0`) is **not installable** — confirmed by inspecting PyPI wheel
  metadata: `fastapi==0.115.0` itself requires `starlette<0.39.0`. No version of
  starlette that clears all current CVEs is compatible with fastapi 0.115.0, or even
  with fastapi up to 0.118.x (`starlette<0.49.0`). The first fastapi release that drops
  the starlette upper bound is `0.137.1` (latest), which in turn requires
  `pydantic>=2.9.0` — a bump from the branch's current `pydantic==2.7.4`.
- Real fix is a coordinated 3-package bump (`fastapi`, `pydantic`, `python-multipart`)
  plus a full re-run of the 27-test suite and another AppSec/QA pass — too large for a
  same-day prod-support patch.

Posted full findings + verified version constraints as a comment on **#24** (kept as the
canonical issue; #25 closed as duplicate) so the Engineer agent can pick this up
directly rather than re-deriving the dependency chain.

## Actions Taken This Run (2026-06-16)

- Triaged 11 open GitHub issues — all already labeled, none stale
- Read all `team/agents/` status files — no new BLOCKED flags beyond the already-tracked
  PR #8 → PR #9 → STORY-2/3/4/5 chain
- Reviewed git log on main — no policy violations
- Checked CI: no workflow on main; agent-branch failures are expected merge-order
  artifacts, not new defects
- Closed duplicate issue #25 (dup of #24)
- Re-ran `pip-audit` against PR #8 branch, found the dependency situation is worse than
  documented and the existing recommended fix is not installable; posted updated
  findings + a verified upgrade path on #24
- No PR opened this run — the only actionable bug found needs a coordinated multi-package
  dependency bump + full regression pass, which is Engineer/QA territory, not a
  same-day prod-support patch
