# TODO — Crypto Trading Bot (Daniel's Track)

Living checklist for Daniel's work (Epics 1–4 + 6). Tied to **BRD v1.2 (15 Jun 2026)** and the
**12 Jun kickoff meeting**. Check items off as you go — this is the "document as built" mitigation
for the single-engineer risk in BRD §12.

Programme window: **1 Jun – 4 Aug 2026**. Today = Mon 15 Jun = start of **Week 3 / Phase 1**.

---

## NOW — Week 3 (15–21 Jun), Phase 1

### Action 1 — Close out infra decision (kickoff action item #5, due now)
- [ ] Confirm event bus = Redis (not NATS)
- [ ] Confirm data store = TimescaleDB via Docker (`timescale/timescaledb:latest-pg16`)
- [ ] Write decision record → `docs/decisions/0001-event-bus-and-datastore.md`
- [ ] Post summary in **Team 1 - CTB** channel to close action item #5
- [ ] Raise open question: does a VPS/homelab actually exist for always-on components? (needed from Epic 2)

### Action 2 — Epic 1: Foundation & Skeleton Architecture
- [ ] **E1-US1** — Monorepo folders (`data/`, `engine/`, `execution/`, `risk/`, `strategies/`,
      `backtest/`, `observability/`, `infra/`, `tests/`) + README explaining each
- [ ] **E1-US2** — `docker-compose.yml` (TimescaleDB + Redis + app skeleton); `docker compose up`
      runs clean with no errors
- [ ] **E1-US3** — `.env.example`, `.gitignore`, pre-commit hook blocking committed secrets
      (gitleaks)
- [ ] **E1-US4** — GitHub Actions CI: black, flake8, mypy, pytest (>80% coverage on core modules)
- [ ] Push repo to GitHub, confirm CI runs green on first PR

---

## Week 4 (22–28 Jun), Phase 2 starts
**Gate:** Epic 0 venue/pair selection must be approved before this work starts (expected end of W3 / start of W4).

- [ ] Confirm Epic 0 outcome (chain, DEX/AMM, starting pairs) — get from Bishal
- [ ] **E2-US1** — DEX/AMM pool state via RPC → normalize to `MarketState` → persist to TimescaleDB
- [ ] **E2-US3** — Paper-trading simulator (realistic fills/fees/slippage, internal P&L, no real orders)
- [ ] **E2-US4** — Data-feed health observability (last-update timestamp per feed; alert if stale >30s)
- [ ] *(Stretch, E2-US2)* CEX websocket feed for comparison — only if DeFi path is solid early
- [ ] Note: Liam on leave 19–26 Jun — don't depend on his TA research input this week

## Week 5 (29 Jun – 5 Jul), Phase 2 continued
- [ ] Finish/harden Epic 2 deliverables above
- [ ] Start sketching `MarketState` consumers for Epic 3 (strategy interface)

---

## Week 6 (6–12 Jul), Phase 3 starts
- [ ] **E3-US1** — Common strategy interface: `receive(market_state) -> Optional[Orders]`
      + example template strategy
- [ ] **E3-US2** — Rule-based strategy (staged buy/sell around configurable price range)
- [ ] **E3-US3** — TA-signal strategy (composable indicators: MA cross, RSI, Bollinger), config-tunable

## Week 7 (13–19 Jul), Phase 3 continued
**Constraint:** Live capital cap must be approved by end of this week (Affan/sponsor) — needed for Epic 4.

- [ ] **E3-US5** — Backtester: same strategy class runs in backtest and live; models fees/slippage;
      generates per-strategy report
- [ ] **E3-US6** — Baseline strategies (buy-and-hold, no-op) + Sharpe/max-drawdown/win-rate in reports
- [ ] Confirm capital cap approved (track with Affan)

---

## Week 8 (20–26 Jul), Phase 4
- [ ] **E4-US1** — `LIVE_ENABLED` flag + manual confirmation prompt, logged with timestamp + operator ID
- [ ] **E4-US2** — Hard capital cap enforced in code (reject orders exceeding cap)
- [ ] **E4-US3** — Global kill switch (<1s activation, cancels open orders, logs halt event)
- [ ] **E4-US4** — Pre-trade risk checks (position size, exposure, max drawdown, daily loss) — get
      risk parameters from Bishal
- [ ] **E4-US5** — Secure key handling (dedicated capped hot wallet, vault/env-only keys, capped
      token approvals, slippage/gas limits)
- [ ] **E4-US6** — State reconciliation on startup (no duplicate orders after restart)
- [ ] Kill-switch test, witnessed by ≥2 team members (Affan as witness per BRD)

---

## Week 9 (27 Jul – 2 Aug), Phase 5–6
- [ ] **E5-US1** — Dashboard: positions, P&L, signals, fills; auto-refresh <5s
- [ ] **E5-US2** — Structured JSON logs with trace IDs; basic metrics (Prometheus/Grafana deferred —
      lightweight custom is fine)
- [ ] **E5-US3** — Backtest/paper reports per strategy (equity curve, trade log, Sharpe, drawdown,
      benchmark comparison, parameter sensitivity)
- [ ] *(Stretch)* **Epic 6**: ML model-serving container (local GPU, REST/gRPC), ML strategy through
      same `Strategy` interface — **only if Epics 1–4 are done**

## Week 10 (3–4 Aug), Handover
- [ ] **E5-US4** — Final findings document input (strategy comparison, venue/pair findings,
      platform limitations, risk validation, recommendations) — feeds Khurram/Affan's writeup
- [ ] Final README/docs pass — make sure a stranger could pick this up
- [ ] Handover by **4 Aug**

---

## Ongoing / Always
- [ ] Weekly written status update in Team 1 - CTB (done / in progress / blocked / decisions made)
- [ ] New significant decisions → `docs/decisions/NNNN-*.md`
- [ ] No secrets ever committed (pre-commit + CI scan should catch this, but double-check)
