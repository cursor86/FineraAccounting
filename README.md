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
| [`docs/REPORTING-STANDARDS.md`](docs/REPORTING-STANDARDS.md) | Current AU financial reporting framework (AASB 1060 Tier 2, AASB S2 climate disclosure phase-in) — checked against primary sources, re-verify before relying on it |
| [`docs/templates/client-finance-officer-brief.md`](docs/templates/client-finance-officer-brief.md) | Fill-in persona/intake template run at the start of every new client engagement |
| [`docs/templates/3-statement-model-template.xlsx`](docs/templates/3-statement-model-template.xlsx) | Give it one tagged trial balance, get P&L, Balance Sheet, Cash Flow, and Dashboard KPIs — the ready-to-sell intake-to-output engine |
| [`tools/dashboard_from_model.py`](tools/dashboard_from_model.py) | Turns a filled 3-statement model into the client's web dashboard (one self-contained HTML page); refuses to build while a tie-out check fails |
| [`docs/templates/client-dashboard-template.html`](docs/templates/client-dashboard-template.html) | The Client Reporting Dashboard product — fill in per client, see `SERVICE-MODEL.md` §5 |
| [`CLAUDE.md`](CLAUDE.md) | Operating rules for any agent (Claude Code or otherwise) working in this repo |

## Status, in one line

Manual-data pipeline is ready to run today. Xero's live API is intentionally
out of scope for now (no budget for API access) — clients' Xero/MYOB exports
are the input instead. AML/KYC tooling was evaluated (Ballerine) and shelved —
not a fit for a bookkeeping/Virtual CFO practice at this stage.
