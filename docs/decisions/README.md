# Decision Records

Lightweight ADRs (Architecture Decision Records) for this project — one file per significant
decision, numbered sequentially. Each covers context, the decision itself, and consequences /
open questions.

This folder exists because Daniel is the **single engineer** on this project (BRD §12,
single-engineer bus-factor risk). Writing decisions down means the team — and future-you —
doesn't need to re-derive them, and gives the PM/sponsor a paper trail for phase-gate reviews.

## Index

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-event-bus-and-datastore.md) | Event bus & data store: Redis + TimescaleDB via Docker | Decided — VPS/homelab question open |

## Format for new entries

```markdown
# NNNN — Title

**Status:** Proposed / Decided / Superseded
**Date:** YYYY-MM-DD
**Owner:** Name
**Related:** Epic/story IDs, BRD section, Jira ticket

## Context
Why this decision is needed.

## Decision
What was decided.

## Consequences
Resulting changes, follow-ups, or open questions.
```
