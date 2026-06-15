# 0001 — Event Bus & Data Store: Redis + TimescaleDB via Docker

**Status:** Decided (one open question below)
**Date:** 2026-06-15
**Owner:** Daniel Iyalekhue
**Related:** Kickoff action item #5 ("Decide TimescaleDB and Redis infrastructure before Epic 1"),
BRD v1.2 §4.2 (Component Breakdown), §11 (Dependencies), E1-US2

## Context

The BRD already specifies PostgreSQL + TimescaleDB as the data store, and lists "Redis / NATS" as
the event-bus option (§4.2). Both must run via Docker Compose alongside the app skeleton
(E1-US2). Kickoff action item #5 requires this to be confirmed and documented before Epic 1
proceeds — this record closes that item.

## Decision

- **Event bus: Redis** (not NATS) — `redis:7-alpine`.
  Reasoning: simpler to operate single-handedly, mature Python client (`redis-py`), comfortably
  meets the >1000 events/sec backtest-replay target (NFR, BRD §7) at this project's scale. NATS
  would add operational complexity with no offsetting benefit here.
- **Data store: TimescaleDB** — `timescale/timescaledb:latest-pg16` (PostgreSQL 16 + TimescaleDB
  extension). Directly matches BRD §4.2; no alternative considered.
- **Deployment, for now: local Docker Compose** on Daniel's dev machine. Both services defined in
  `docker-compose.yml` alongside the `app` service — satisfies E1-US2 ("`docker compose up` brings
  up DB, Redis, and app skeleton without errors").

## Open Question

BRD §10 (Assumptions) assumes "a self-hosted Linux VPS or homelab is available for always-on
components." From Epic 2 onward, market-data ingestion needs to run 24/7, which a laptop cannot
provide.

**Status:** unconfirmed. Raised with Laurentiu Nae / sponsor on 2026-06-15 (Team 1 - CTB channel).
If no VPS/homelab exists, this becomes a blocking risk for Epic 2 — flag to PM/sponsor with
enough lead time to provision one.

**Revisit trigger:** VPS/homelab confirmed or denied; or if Redis/TimescaleDB throughput becomes
a bottleneck under real load (unlikely at this scale).

## Consequences

- `docker-compose.yml` will define three services: `timescaledb`, `redis`, `app`.
- `.env` / `.env.example` will include: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`,
  `POSTGRES_HOST`, `POSTGRES_PORT`, `REDIS_HOST`, `REDIS_PORT`.
- Python dependencies: `redis`, `psycopg2-binary` (or `asyncpg` later if async is needed).
- If the VPS/homelab question resolves "no," escalate via weekly status update rather than
  silently absorbing the infra burden.
