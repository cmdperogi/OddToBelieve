# Project: OddToBelieve

Extends `~/.claude/CLAUDE.md`.

## Overview

Aggregates betting odds from Betfair Exchange and The Odds API for soccer and horse racing, displays them in a React dashboard. Single-user local app — no AWS yet.

**Type:** Fullstack (FastAPI + React/Vite)
**Database:** SQLite (local)
**Environments:** local only

## Commands

```bash
# Backend (run from backend/)
uvicorn app.main:app --reload            # http://localhost:8000
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
ruff check . --fix && black .

# Frontend (run from frontend/)
npm run dev                              # http://localhost:5173
npm run build
npm run lint

# Database
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Project Layout

```
OddToBelieve/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app factory + CORS
│   │   ├── config.py         # pydantic-settings (reads .env)
│   │   ├── dependencies.py   # get_db, get_current_user
│   │   ├── scheduler.py      # APScheduler — hourly feed polling
│   │   ├── routers/
│   │   │   ├── auth.py       # POST /auth/token
│   │   │   └── odds.py       # GET /odds/*, GET /events/*
│   │   ├── services/
│   │   │   ├── betfair.py    # Betfair Exchange API client
│   │   │   └── odds_api.py   # The Odds API client
│   │   ├── models/           # Pydantic request/response schemas
│   │   └── db/
│   │       ├── database.py   # SQLAlchemy engine + session
│   │       └── models.py     # ORM models: Event, Market, Odds
│   └── tests/
│       ├── unit/
│       └── integration/
└── frontend/
    └── src/
        ├── pages/
        ├── components/
        ├── hooks/
        └── api/              # typed fetch wrappers for the backend
```

## Environment Variables

Copy `.env.example` → `.env` and fill in values. Never commit `.env`.

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | yes | JWT signing key — `openssl rand -hex 32` |
| `ADMIN_USERNAME` | yes | Login username |
| `ADMIN_PASSWORD` | yes | Login password (hashed at startup) |
| `BETFAIR_USERNAME` | yes | Betfair account email |
| `BETFAIR_PASSWORD` | yes | Betfair account password |
| `BETFAIR_APP_KEY` | yes | From Betfair developer portal |
| `THE_ODDS_API_KEY` | no | Free tier — 500 req/month, use sparingly |
| `DATABASE_URL` | no | Default: `sqlite:///./oddtobelieve.db` |
| `ODDS_POLL_INTERVAL_MINUTES` | no | Default: `60` |

## Key External APIs

**Betfair Exchange API** (primary — free with account)
- Base: `https://api.betfair.com/exchange/betting/rest/v1.0/`
- Auth: POST login → session token → `X-Authentication` header + `X-Application` (app key)
- Soccer = Event Type `1`, Horse Racing = Event Type `7`
- Session tokens expire after ~8h of inactivity; re-auth on 403

**The Odds API** (secondary — use sparingly)
- Base: `https://api.the-odds-api.com/v4/`
- Auth: `apiKey` query param
- Always check `x-requests-remaining` response header; stop if < 50

## Data Model

- `Event` — a match or race (sport, name, start_time, source_id, source)
- `Market` — a betting market on an event (type: match_winner, over_under, win)
- `Odds` — one bookmaker's price for a selection (bookmaker, value, fetched_at)

## Overrides

- **Database:** SQLite only — use `Base.metadata.create_all()` until schema stabilises, then switch to Alembic.
- **Auth:** Single user from env vars (`ADMIN_USERNAME` / `ADMIN_PASSWORD`) — no user table needed.

## Out of Scope (ask first)

- No AWS resources — local only
- No web scraping
- Do not add new data sources without confirming API cost/rate limits
- Do not change poll interval without checking rate limit headroom
- Do not run `alembic downgrade` without confirming
