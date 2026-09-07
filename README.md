# FineraAccounting

The operating model for NewFinera's AI-assisted client work: how the tools we've
assembled turn a client's raw records into a review-ready deliverable, for
every service on [newfinera.com](https://newfinera.com).

This repo holds the **model plan**, not client data. Real client exports,
workpapers and identifiers never get committed here — see
[`docs/SERVICE-MODEL.md`](docs/SERVICE-MODEL.md#data-handling) and
[`CLAUDE.md`](CLAUDE.md).

## What's here

| File | Purpose |
|---|---|
| [`docs/SERVICE-MODEL.md`](docs/SERVICE-MODEL.md) | The client engagement model: intake → processing → review → delivery, per service line |
| [`docs/TOOLS.md`](docs/TOOLS.md) | The assembled toolkit, what each piece does, and its current status |
| [`CLAUDE.md`](CLAUDE.md) | Operating rules for any agent (Claude Code or otherwise) working in this repo |

## Status, in one line

Manual-data pipeline is ready to run today. Xero's live API is intentionally
out of scope for now (no budget for API access) — clients' Xero/MYOB exports
are the input instead. AML/KYC tooling was evaluated (Ballerine) and shelved —
not a fit for a bookkeeping/Virtual CFO practice at this stage.
