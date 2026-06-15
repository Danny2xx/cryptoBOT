# Crypto Trading Bot — R&D Prototype

Multi-venue (DeFi-first) crypto trading bot, built as an R&D prototype for Blockchain Advisors'
Summer Internship 2026. **Goal: learning and a reusable platform — not profit.** All live trading
is incidental, hard-capped, and gated behind explicit risk controls.

See [`BRD - Crypto Trading Bot.md`](BRD%20-%20Crypto%20Trading%20Bot.md) for the full business
requirements, [`TODO.md`](TODO.md) for the live task checklist, and
[`docs/decisions/`](docs/decisions/) for architecture decision records.

## Module boundaries

| Folder | Responsibility |
|--------|-----------------|
| `data/` | Market data ingestion — CCXT/websocket and web3/RPC clients, normalization into the shared `MarketState` format, persistence to TimescaleDB. |
| `engine/` | Strategy engine — orchestration, lifecycle, state management. Loads strategy plugins and feeds them market state. |
| `execution/` | Execution layer — abstracts venue differences (DEX on-chain swaps today, CEX REST/WS as stretch), routes orders through the risk manager. |
| `risk/` | Risk manager — position/portfolio limits, max drawdown, exposure caps, global kill switch, pre-trade checks. |
| `strategies/` | Pluggable strategy implementations (rule-based, TA-signal, ML) behind a common interface. |
| `backtest/` | Backtesting harness (replays historical data through live strategy code) and paper-trading simulator. |
| `observability/` | Structured logging, metrics, and the dashboard. |
| `infra/` | Dockerfiles and deployment configuration. |
| `tests/` | Unit and integration tests. |
| `docs/decisions/` | Architecture decision records (ADRs) — one file per significant decision. |

## Getting started

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker
Compose).

```bash
cp .env.example .env   # fill in real values — never commit .env
docker compose up -d
docker compose logs -f app
```

You should see `Redis OK` and `Postgres OK` from the app container — that confirms the skeleton
stack is wired up correctly.

## Development

```bash
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

CI (GitHub Actions) runs `black`, `flake8`, `mypy`, and `pytest` on every PR — see
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).
