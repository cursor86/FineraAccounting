# AU financial reporting standards — current framework

What NewFinera's deliverables need to comply with, checked against primary
sources on 2026-09-07. Re-verify before relying on this for a real client —
standards move; this is a snapshot, not a live feed.

## 1. AASB 1060 — Tier 2 simplified disclosures

Almost every NewFinera client that prepares general purpose financial
statements (most small proprietary companies don't have to lodge any — see
below) will report under **Tier 2**, not Tier 1. AASB 1060 sets those
disclosure requirements: full Tier 1 recognition and measurement, reduced
disclosure.

- The compiled AASB 1060 applies to annual periods beginning on or after
  **1 January 2026**, incorporating amendments up to 19 August 2025.
- **AASB 2025-2** (Classification and Measurement of Financial Instruments —
  Tier 2 Disclosures) amends AASB 1060, effective for periods beginning on
  or after 1 January 2026 — relevant to any client holding financial
  instruments beyond plain cash/receivables/payables.
- Source: [AASB 1060, Aug 2025 compiled version](https://standards.aasb.gov.au/aasb-1060-aug-2025), checked 2026-09-07.

**Action for `year-end-workpapers` and Virtual CFO deliverables**: confirm
which tier the client reports under (most small clients: Tier 2, if they
report general purpose financial statements at all), and check the AASB 1060
compiled standard for the disclosure checklist current at the statement date
— don't reuse last year's disclosure list unchanged.

## 2. Does the client even need to lodge financial statements?

Most small proprietary companies in Australia are **not required** to
prepare or lodge financial statements at all, unless a trigger applies
(foreign control, ASIC direction, shareholder request under the Corporations
Act, or the entity is large enough to fall outside the small-company
thresholds). This determination — small vs large proprietary company — comes
before AASB 1060 even becomes relevant, and the size thresholds themselves
change periodically. Verify current thresholds at asic.gov.au or the
Corporations Act before assuming a client is exempt.

## 3. AASB S2 — mandatory climate-related financial disclosure

New regime, phased in by entity size ("Group"). Relevant to check against
every client, even though most of NewFinera's bookkeeping/Virtual CFO client
base is very unlikely to be large enough to be caught:

| Group | First reporting period | Status as at 2026-09-07 |
|---|---|---|
| Group 1 | Periods starting on/after 1 January 2025 | Already reporting |
| Group 2 | Periods starting on/after 1 July 2026 | About to start |
| Group 3 | Periods starting on/after 1 July 2027 | Not yet started |

A 1-year relief applies to Scope 3 emissions reporting (mandatory from each
group's *second* reporting period, not its first).

**Action**: the Group thresholds themselves (revenue, assets, employee
count) are not reproduced here — verify current thresholds directly against
AASB/Treasury guidance per client before concluding a client is in or out of
scope. Don't assume every small client is automatically excluded; check.

Sources: search results summarizing
[Anthesis Group's AASB S2 guide](https://www.anthesisgroup.com/au/insights/asrs-and-aasb-s2-a-guide-to-mandatory-climate-reporting-in-australia/)
and [Carbon Impact's Group 2 coverage](https://carbonimpacthq.com/journal/australia-aasb-s2-group-2-climate-reporting-2026),
checked 2026-09-07 — re-verify against aasb.gov.au / standards.aasb.gov.au
directly before relying on this for a specific client, per this repo's
verification discipline.

## How this plugs into the existing workflow

Nothing here replaces the `ryanduguid/australian-accounting-skills` skills —
`year-end-workpapers`, `bas-preparation`, `month-end-close`, etc. still do the
mechanical work, and their own rule stands: never state a rate, threshold, or
requirement from memory, verify live per engagement. This file exists so the
*current shape* of the reporting framework (Tier 2/AASB 1060, the S2 phase-in)
is visible at the repo level, not just inside each skill's own citations —
useful when scoping a new engagement, before any skill runs.
