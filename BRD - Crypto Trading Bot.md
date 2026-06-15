# Business Requirements Document
## Multi-Venue Crypto Trading Bot (R&D Prototype)

**Version:** 1.2  
**Date:** 15 June 2026  
**Author:** Blockchain Advisors — Summer Internship 2026  
**Status:** Draft for PM Review  
**Project Jira Site:** blockchainadvisors-project1.atlassian.net

> **v1.2 changes (15/06/2026):** **PM change** — Ibraheem Akram moved to Sigalmark Market Discovery as its PM; **Muhammad F. Khurram is now CTB ★PM on a placeholder basis** (his continued involvement is unconfirmed — no comms since the first weekly meeting). §6.0 team table updated accordingly (allocation v7). All other scope unchanged from v1.1.
> **v1.1 changes (12/06/2026):** Reoriented to **DeFi-first** (CEX integration deferred to stretch scope); added **Epic 0 — Venue & Pair Selection** (formal research/selection process for chain, DEX, and trading pairs); added **Team & Suggested Assignments** (§6.0) mapped to the confirmed CTB team (allocation v6); phase timeline aligned to the actual programme window (1 Jun – 4 Aug 2026); tiny capped live-trade goal retained.

---

## 1. Executive Summary

This document defines the business and technical requirements for an R&D prototype of a multi-venue crypto trading bot. The primary goal is **learning and platform reuse**, not profit generation. Success is measured by what the prototype enables the team to understand, validate, and reuse in future phases.

Any live trading is incidental to end-to-end system validation. All live capital must be treated as expendable R&D spend, with hard-capped limits and non-negotiable safety controls.

---

## 2. Project Vision & Objectives

### 2.1 Vision
Build a modular, observable, and safely constrained trading platform for decentralized finance (DeFi) venues — architected so centralized exchanges (CEX) can plug in later — running multiple strategy types under unified risk management.

### 2.2 Objectives (Success Criteria)
The prototype is considered successful when it demonstrably:

1. Completes a **documented venue & pair selection process** (Epic 0) producing an approved choice of chain, DEX/AMM, and starting trading pairs.
2. Connects to the selected **DEX/AMM** for both market data and on-chain order execution. (CEX integration is **stretch scope** — only if DeFi path lands early.)
3. Supports **limited live trading** with hard-capped capital on a dedicated, balance-capped hot wallet.
4. Runs **three pluggable strategies** through a single interface: one rule-based, one TA-signal, and one ML-driven.
5. Enforces **risk-management rules** — position limits, max drawdown, and a global kill switch — that provably halt trading when breached.
6. Provides **real-time observability** — a dashboard or logs showing positions, P&L, signals, and executions.
7. Generates **comparative backtest/paper reports** comparing strategy behaviour, venue/pair characteristics, and platform limitations.

### 2.3 Out-of-Phase Goal
**Production readiness** is not the objective of this phase. The prototype must not manage external or significant capital.

---

## 3. Stakeholders

| Role | Responsibility |
|------|----------------|
| Project Sponsor | Budget, live-capital cap approval, go/no-go at phase gates |
| Project Manager | Planning, Jira epic/story/task breakdown, sprint coordination |
| Platform Engineer | Core architecture, data ingestion, execution abstraction |
| Strategy Developer | Strategy plugin development (rule-based, TA, ML) |
| Risk & Safety Lead | Risk subsystem, kill switch, security posture |
| DevOps / Infrastructure | Self-hosted deployment, observability stack, secret handling |

---

## 4. Project Structure & Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────┐
│  Strategy Plugins (Rule-based / TA / ML)    │
│  ——— common interface ———                   │
├─────────────────────────────────────────────┤
│  Strategy Engine                            │
│  (orchestration, state, lifecycle)            │
├─────────────────────────────────────────────┤
│  Risk Manager  │  Execution Layer            │
│  (limits,      │  (CEX REST/WS + DeFi tx)    │
│   kill switch) │                             │
├─────────────────────────────────────────────┤
│  Market Data Ingestion                        │
│  (CEX websockets, DeFi RPC/indexer)         │
├─────────────────────────────────────────────┤
│  Data Store (TimescaleDB) + Event Bus (Redis)│
├─────────────────────────────────────────────┤
│  Observability (metrics, logs, dashboard)    │
└─────────────────────────────────────────────┘
```

### 4.2 Component Breakdown

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| Market Data | CCXT + websockets, web3.py / ethers | Ingest order books, trades, candles, pool state |
| Strategy Engine | Python | Loads plugins, feeds market state, collects orders, manages lifecycle |
| Execution Layer | Python | Abstracts venue differences; routes orders through risk manager |
| Risk Manager | Python | Position/portfolio limits, max drawdown, exposure caps, kill switch |
| Backtester | vectorbt / backtrader / custom | Replays historical data through strategy interface |
| Paper Simulator | Python | Realistic fills, fees, slippage on live data without capital |
| Data Store | PostgreSQL + TimescaleDB | Time-series market data; state for positions, orders, config |
| Event Bus | Redis / NATS | Decouples data, strategy, and execution |
| ML Serving | Local GPU inference stack | Model-as-signal, kept separate from trading loop |
| Infrastructure | Docker Compose | Self-hosted on homelab / VPS |
| Observability | Prometheus + Grafana / custom dashboard | Metrics, structured logs, positions, P&L, system health |

---

## 5. Scope

### 5.1 In Scope

- **Venue & pair selection process** — criteria-driven research and selection of chain, DEX/AMM, and starting trading pairs (Epic 0).
- On-chain swaps on the selected DEX / AMM.
- Pluggable strategy framework (rule-based, TA, ML).
- Backtesting harness with historical data.
- Paper-trading simulator with realistic fills, fees, and slippage.
- Limited live trading with strict capital and risk caps.
- Risk-management subsystem and kill switch.
- Observability (metrics, logging, basic dashboard).
- Secure secret/key handling.

### 5.2 Out of Scope (This Phase)

- CEX integration (market data + execution) — **stretch scope only**, picked up if the DeFi path is solid early.
- Leveraged, margin, or derivatives trading.
- Latency-sensitive HFT or co-located execution.
- Custody or management of third-party / client funds.
- Multi-tenant or commercial deployment.
- Cross-chain bridging strategies.
- Regulatory authorisation for offering a service.

---

## 6. Functional Requirements (Epic-Ready)

### 6.0 Team & Suggested Assignments (allocation v7, 15/06/2026)

| Intern | BRD Role(s) | Suggested ownership |
|--------|-------------|---------------------|
| **Muhammad F. Khurram ★PM (placeholder)** (Accounting & Finance; fintech research; basic Excel/Python) | Project Manager + analyst | Jira epic/story breakdown, sprint coordination, phase gates; co-scores Epic 0 selection matrix; owns backtest report analysis (E3-US6, E5-US3) and final findings (E5-US4 with Affan). **Placeholder PM** — swapped in for Ibraheem Akram 15/06; his continued involvement is unconfirmed (no comms since the first weekly meeting), so confirm engagement before relying on PM deliverables. |
| **Daniel Iyalekhue** (MSc AI, BSc CS; applied AI engineer — ML, LLMs, APIs) | Platform Engineer + Strategy Developer + ML | Epics 1–3 build work (repo, Docker, data ingestion, strategy interface, backtester) and Epic 6 ML strategy. Primary (only) engineer — see bus-factor risk in §12. |
| **B M Rahidul Haq Bishal** (Accounting & Finance; active crypto/futures investor; GenAI-finance cert) | Fintech Research + Risk lead | **Leads Epic 0 venue & pair selection**; defines risk parameters (caps, drawdown, daily loss) for Epic 4; specs the rule-based and TA strategies with Liam. |
| **MD Affan Mahdeen Haque** (Mechanical Eng; blockchain + business ops) | Business Operations + Safety | Sponsor reporting, capital-cap approval tracking (Epic 4 dependency), documentation, kill-switch test witness, gas/fee cost tracking. |
| **Liam Quigley** (1st-yr Accounting; AI-in-finance interest) | TA research + reporting | TA indicator research (E3-US3 spec), backtest comparison tables, dashboard content (E5-US1 requirements). *Holiday 19–26 June — plan around Sprint 2.* |

> Assignments are suggestions for the PM to confirm at sprint planning. Capacity: 8 h/week each (~40 h/week team total); all five end **04/08/2026**.

### Epic 0: Venue & Pair Selection (NEW — runs first)
**Jira Epic Name:** `E0-Venue-Pair-Selection`  
**Goal:** A documented, criteria-driven choice of chain, DEX/AMM, and starting trading pairs, approved at a phase gate before any integration work depends on it.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E0-US1 | As a researcher, I want a selection-criteria framework so that venue choice is evidence-based, not preference-based. | Weighted scoring matrix agreed by team covering: liquidity/volume, gas & swap fees, RPC/indexer availability and cost, testnet/fork support for safe testing, SDK & docs quality (Python support), MEV exposure, and pair volatility suitability for each strategy type. |
| E0-US2 | As a researcher, I want a shortlist of candidate venues evaluated against the criteria so that the team picks from real data. | At least 4 candidates scored with current (≤2 weeks old) data from DefiLlama/CoinGecko. Starting shortlist: **Uniswap v3/v4 (Ethereum L1 + Arbitrum/Base L2)**, **PancakeSwap (BNB Chain)**, **Aerodrome (Base)**, **Raydium (Solana)**. L2/sidechain gas costs weighted heavily given the tiny live-capital cap. |
| E0-US3 | As a researcher, I want starting trading pairs selected per strategy type so that strategies are tested on suitable markets. | 2–3 pairs chosen with rationale (e.g. high-liquidity major pair for rule-based range logic; a stable pair for low-risk live validation). Liquidity depth and historical-data availability verified for each. |
| E0-US4 | As a PM, I want the selection documented and approved so that downstream epics build on a stable decision. | One-page selection report (matrix + recommendation) reviewed by sponsor; decision recorded in Jira and AGENTS.md; revisit trigger defined (e.g. liquidity collapse, RPC unreliability). |

### Epic 1: Foundation & Skeleton Architecture
**Jira Epic Name:** `E1-Foundation`  
**Goal:** Repo, config, secrets, CI, and skeleton architecture in place.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E1-US1 | As a developer, I want a monorepo with clear module boundaries so that components can evolve independently. | Repo has folders: `data/`, `engine/`, `execution/`, `risk/`, `strategies/`, `backtest/`, `observability/`, `infra/`. README explains boundaries. |
| E1-US2 | As a developer, I want Docker Compose local setup so that the full stack spins up with one command. | `docker-compose up` brings up DB, Redis, and app skeleton without errors. |
| E1-US3 | As a safety lead, I want secrets handled out-of-band so that keys never hit version control. | `.env` template exists; real secrets loaded from env/vault; pre-commit hook blocks committed secrets. |
| E1-US4 | As a PM, I want CI pipeline (lint, type-check, unit tests) so that code quality is enforced early. | GitHub Actions (or equivalent) runs on every PR: flake8/black, mypy, pytest with >80% coverage on core modules. |

### Epic 2: Market Data & Paper Trading
**Jira Epic Name:** `E2-MarketData-Paper`  
**Goal:** Connect to the selected DEX (per Epic 0); simulate trades with no capital.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E2-US1 | As a strategy developer, I want DEX/AMM pool state via RPC so that on-chain prices are available. | Reliable RPC or indexer connection to the Epic-0-selected venue; pool reserves / prices normalized to a common `MarketState` event; data persisted to TimescaleDB. |
| E2-US2 | *(Stretch)* As a strategy developer, I want real-time CEX order-book and candle data so that venue comparison is possible. | CEX websocket streams normalized to the same `MarketState` format. Only after the DeFi path is solid. |
| E2-US3 | As a safety lead, I want a paper-trading simulator so that strategies can be validated without risk. | Simulator produces realistic fills, fees, slippage; P&L tracked internally; no real orders sent. |
| E2-US4 | As a platform engineer, I want observability of data-feed health so that stale or broken feeds are detected. | Dashboard/log shows last-update timestamp per feed; alert if feed stale >30s. |

### Epic 3: Strategy Framework & Backtesting
**Jira Epic Name:** `E3-Strategies-Backtest`  
**Goal:** Pluggable strategy interface with three working strategies and reproducible backtests.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E3-US1 | As a strategy developer, I want a common strategy interface so that new strategies plug in without touching execution or risk. | Interface defined: `receive(market_state) -> Optional[Orders]`; example template strategy provided. |
| E3-US2 | As a strategy developer, I want a rule-based strategy so that simple price-range logic can be tested. | Staged buy/sell orders around a configurable price range; parameters in config. |
| E3-US3 | As a strategy developer, I want a TA-signal strategy so that indicator-driven entries/exits can be evaluated. | Composable indicators (MA cross, RSI, Bollinger); parameters tunable via config. |
| E3-US4 | As a strategy developer, I want an ML-driven strategy so that model signals can feed the same execution rails. | Model outputs target positions/orders; always passes through risk manager; guard against overfitting. |
| E3-US5 | As a researcher, I want a backtester that replays historical data through the same strategy code used live so that results are trustworthy. | Same strategy class runs in backtest and live; fees/slippage modeled; report generated per strategy. |
| E3-US6 | As a researcher, I want baseline strategies (buy-and-hold, no-op) so that strategy performance is judged against a benchmark. | Baseline strategies included in backtest reports; Sharpe, max drawdown, win rate computed. |

### Epic 4: Risk Management & First Live Trades
**Jira Epic Name:** `E4-Risk-Live`  
**Goal:** Risk controls are enforced in code; first tiny live trades execute safely.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E4-US1 | As a safety lead, I want live trading to be an explicit, deliberate switch so that it is never accidental. | Config flag `LIVE_ENABLED` plus manual confirmation prompt / signature; logged with timestamp + operator ID. |
| E4-US2 | As a safety lead, I want a hard capital cap enforced in code so that maximum loss is bounded. | Configurable max portfolio value deployed; engine rejects orders that would exceed cap. |
| E4-US3 | As a safety lead, I want a global kill switch so that all activity halts and open orders cancel on command. | One command/flag stops all strategies, cancels open orders where venue supports it, logs halt event. |
| E4-US4 | As a safety lead, I want pre-trade risk checks so that no order reaches a venue without clearing limits. | Checks: position size, total exposure, max drawdown, daily loss limit. Breach = order rejected + alert. |
| E4-US5 | As a safety lead, I want secure key handling so that compromise impact is minimized. | Dedicated hot wallet with hard-capped balance (the live-capital cap); private key in env/vault only, never in repo or logs; slippage and gas limits on every tx; unlimited token approvals forbidden (per-trade or capped approvals only). |
| E4-US6 | As a platform engineer, I want state reconciliation on startup so that duplicate orders cannot be issued after restart. | On startup, engine queries venue state, reconciles with internal DB, resumes only after match confirmed. |

### Epic 5: Observability & Reporting
**Jira Epic Name:** `E5-Observability-Reporting`  
**Goal:** Real-time visibility and documented findings.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E5-US1 | As a PM, I want a dashboard showing positions, P&L, signals, and executions so that system state is visible at a glance. | Dashboard accessible via browser; auto-refreshes; shows per-strategy and aggregate P&L, open positions, recent fills. |
| E5-US2 | As a DevOps engineer, I want structured logs and metrics so that anomalies are detectable. | JSON logs with trace IDs; Prometheus metrics for latency, error rate, drawdown, feed staleness; alerts configured. |
| E5-US3 | As a researcher, I want backtest and paper-trading reports per strategy so that comparative analysis is possible. | Report includes: equity curve, trade log, Sharpe, max drawdown, benchmark comparison, parameter sensitivity. |
| E5-US4 | As a project sponsor, I want a final findings document so that a go/no-go decision on future investment is informed. | Document covers: strategy comparison, venue/pair findings (incl. CEX-vs-DeFi if stretch reached), platform limitations, risk control validation, recommendations. |

### Epic 6: ML Serving & Model-as-Signal
**Jira Epic Name:** `E6-ML-Serving`  
**Goal:** ML strategy runs through the same platform rails.

| ID | User Story | Acceptance Criteria |
|----|-----------|---------------------|
| E6-US1 | As an ML engineer, I want model inference hosted on a local GPU so that prediction latency is acceptable. | Model serving container separate from trading loop; REST/gRPC interface for predictions. |
| E6-US2 | As a safety lead, I want ML strategy orders to pass through the same risk manager as other strategies so that model errors cannot bypass limits. | ML strategy uses identical `Strategy` interface; risk manager checks applied before every order. |

---

## 7. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Backtest replay: >1000 events/sec on standard hardware. Live signal-to-order latency: <5s (not HFT). |
| **Reliability** | 99.5% uptime for always-on components (data ingestion, risk manager). Kill switch: <1s activation. |
| **Security** | API keys in vault/env only; no secrets in logs; hot wallet balance capped; IP allowlisting; slippage/gas bounds on DeFi. |
| **Observability** | All trades, risk checks, and kill-switch events logged with trace ID; metrics scraped every 15s; dashboard refresh <5s. |
| **Portability** | Docker Compose on Linux VPS or self-hosted homelab; x86_64 target. |
| **Testability** | Every core module has unit tests; integration tests for the DEX paper path and backtest harness. |
| **Maintainability** | Modular code; strategy plugins isolated; config-driven behaviour; documented APIs. |

---

## 8. Deliverables

| # | Deliverable | Owner | Phase |
|---|-------------|-------|-------|
| 1 | Working prototype codebase (modular, documented) | Platform Engineer | All |
| 2 | Strategy plugin SDK / interface + example strategies (3) | Strategy Developer | Phase 3 |
| 3 | Backtesting and paper-trading harnesses | Strategy Developer | Phase 2–3 |
| 4 | Risk-management subsystem with kill switch | Risk & Safety Lead | Phase 3–4 |
| 5 | Observability dashboard | DevOps | Phase 2–5 |
| 6 | Backtest / paper reports per strategy | Strategy Developer | Phase 3–5 |
| 7 | Final findings & recommendations document | PM + Team | Phase 6 |
| 8 | Venue & pair selection report (Epic 0) | Fintech Research (Bishal) + PM | Phase 1 |

### 8.1 Phase Timeline (programme window: 1 Jun – 4 Aug 2026; ~7.5 weeks remaining as of 12 Jun)

| Phase | Weeks | Dates (w/c) | Focus |
|-------|-------|-------------|-------|
| 1 | W3 | 15 Jun | **Epic 0** venue & pair selection (research team) ∥ **Epic 1** repo/Docker/CI skeleton (Daniel) |
| 2 | W4–W5 | 22 Jun – 29 Jun | **Epic 2** DEX data ingestion + paper simulator. *Liam on holiday 19–26 Jun.* Epic 0 gate: selection approved end of W3/start of W4. |
| 3 | W6–W7 | 6 Jul – 13 Jul | **Epic 3** strategy interface, rule-based + TA strategies, backtests. Capital-cap approval needed by end of W7. |
| 4 | W8 | 20 Jul | **Epic 4** risk controls, kill-switch test, first tiny live trades on capped hot wallet |
| 5–6 | W9–W10 | 27 Jul – 3 Aug | **Epic 5** reports + findings doc; **Epic 6** ML strategy (Daniel, stretch if W6–W8 slip); handover by **4 Aug** |

---

## 9. Acceptance Criteria / Success Criteria Summary

- [ ] Venue & pair selection report approved at the Epic 0 phase gate.
- [ ] All 7 epics (E0–E6) have at least one closed story with passing acceptance criteria.
- [ ] Live trading is only enabled after risk controls pass a dedicated audit (code review + test).
- [ ] Backtest reports show at least 3 strategies with benchmark comparison.
- [ ] Dashboard displays real-time positions and P&L without manual refresh.
- [ ] Kill switch test documented and witnessed by at least two team members.
- [ ] No secrets committed to repo (verified by automated scan).

---

## 10. Assumptions & Constraints

### Assumptions
- Daniel Iyalekhue provides the Python/platform engineering capacity (confirmed: MSc AI, applied AI engineer). He is the **single engineer** — see bus-factor risk in §12.
- A self-hosted Linux VPS or homelab is available for always-on components.
- The DEX, chain, and pairs are chosen via the Epic 0 selection process — not pre-decided. Candidate shortlist (current as of 12/06/2026): Uniswap v3/v4 (Ethereum + Arbitrum/Base), PancakeSwap (BNB), Aerodrome (Base), Raydium (Solana). Testnet or forked-mainnet (e.g. Anvil/Hardhat fork) availability is a selection criterion so paper/integration testing needs no capital.

### Constraints
- **Budget:** Live capital cap must be set and approved before any live trade (target: end of W7, w/c 13 Jul).
- **Time:** 8h/week per intern, hard end **04/08/2026** for all five team members; phases are gated, not parallelized where dependencies exist. Liam unavailable 19–26 Jun.
- **Regulatory:** UK FCA and EU MiCA evolve quickly; any move beyond internal testing requires current legal verification.
- **Security:** DeFi MEV/sandwiching risk, failed-tx gas loss, and unlimited token approvals are explicit threats.

---

## 11. Dependencies

| Dependency | Description | Blocking For |
|------------|-------------|--------------|
| Venue & pair selection approved (Epic 0 gate) | Chain, DEX, pairs decided | Epic 2, 3, 4 |
| DeFi RPC provider / self-hosted node | On-chain data + execution | Epic 2, 4 |
| Funded, capped hot wallet | Live on-chain execution | Epic 4 |
| GPU/CPU inference host | ML model serving | Epic 6 |
| TimescaleDB + Redis infra | Data and event bus | Epic 1 |
| Live capital budget approval | Real-money trading | Epic 4 |
| CEX API account + sandbox access *(stretch)* | Venue comparison | E2-US2 only |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Single-engineer dependency (Daniel)** | Medium | Critical | Keep architecture simple; document as built; pair Khurram/Liam on Python tasks; PM reviews progress weekly and descopes early (Epic 6 first to go). |
| DeFi execution complexity dominates effort | Medium | High | Epic 0 weights SDK quality, testnet/fork support, and gas cost; test on fork/testnet before mainnet; favour an L2 with low gas to keep failed-tx losses trivial. |
| Backtest-to-live fidelity gap | High | High | Model fees/slippage conservatively; run paper before live. |
| Data quality / look-ahead bias | Medium | High | Store raw data; reproducible backtests; out-of-sample validation. |
| Live capital loss | Low (if capped) | Medium | Hard cap enforced in code; kill switch tested; treat as R&D spend. |
| Key / wallet compromise | Low | Critical | Vault-only secrets; IP allowlisting; dedicated hot wallet; limited balance. |
| Overfitting on ML strategy | High | Medium | Guard rails in risk manager; never let model trade unconstrained; walk-forward validation. |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| CEX | Centralized Exchange (e.g., Binance, Kraken) |
| DEX | Decentralized Exchange / AMM (e.g., Uniswap) |
| TA | Technical Analysis (indicator-driven trading) |
| ML | Machine Learning |
| P&L | Profit and Loss |
| MEV | Maximal Extractable Value (front-running risk on-chain) |
| Kill Switch | Emergency halt that stops all trading activity |
| Paper Trading | Simulated trading on live data with no real capital |

---

*End of Document*
