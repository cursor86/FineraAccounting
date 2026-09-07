# Toolkit

What's assembled, what each piece is for, and its current status. Mirrors the
architecture reviewed in-session; kept here so it travels with the repo.

| Component | Source | Role | Status |
|---|---|---|---|
| Accounting workflow skills | `ryanduguid/australian-accounting-skills` | 19 Claude skills encoding AU practice workflows — BAS, month-end close, STP, Div 7A, year-end packs, contracting specialisms | **Live** — loaded as Claude Skills |
| AU tax knowledge | `openaccountants/openaccountants` | Accountant-reviewed reference guides; 29 AU topics inside a 232-jurisdiction library. Supplies the facts the workflow skills cite | **Available** — cloned read-only |
| General finance skills | `openaccountant/skills` | 44 broader personal/business finance skills, not AU-specific | **Available, secondary** — use outside the AU practice scope, not the default path |
| Xero live API connection | `XeroAPI/xero-agent-toolkit` | Reference agents (LangChain, OpenAI Agents SDK, Google ADK) pulling live Xero data via the Xero MCP Server | **Deferred** — needs a Xero Developer Custom Connection app; no budget allocated. Manual exports substitute for it |
| Client onboarding / KYB | `ballerine-io/ballerine` | Identity verification, case management for onboarding | **Shelved** — evaluated, not a fit for the current service lines |

## Why Xero's live API is deferred, not abandoned

The manual-export pipeline (client sends Activity Statement / trial balance /
GL detail; `xero-exports` skill parses it) covers every service line in
`SERVICE-MODEL.md` today. Wiring the live API later removes a manual step,
it doesn't unlock a new capability — so it's picked up when there's budget
for a Xero Developer Custom Connection app (Client ID/Secret), not before.

## Why Ballerine was set aside

Ballerine solves client *onboarding* (identity verification, KYB) — a
different problem from bookkeeping and management accounts. It's worth
revisiting only if manual client onboarding becomes an actual bottleneck,
which isn't the case at NewFinera's current scale.
