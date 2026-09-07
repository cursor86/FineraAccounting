# Reporting standards

Which AU financial reporting framework applies to a client's statement pack,
and how climate disclosure phases in. Feeds the `year-end-workpapers` and
`month-end-close` skills' output — it does not replace either skill's own
process, only tells it which framework's disclosure set to assemble against.

## AASB 1060 Tier 2 — the default framework

Most NewFinera clients (small proprietary companies, small
not-for-profits, entities preparing special purpose reports that a
lender or the constitution requires to move to general purpose) sit in
**Tier 2 — Simplified Disclosures**, reported under AASB 1060. Tier 1
(full IFRS-equivalent disclosure) only applies to for-profit private
sector entities with public accountability, or public sector entities
required onto full IFRS — neither is expected in this client base;
confirm per-entity before assuming Tier 2.

| Step | Tool |
|---|---|
| Determine Tier 1 vs Tier 2 eligibility for the entity | `openaccountants` guide `australia-financial-statements.md`; re-verify against the current AASB 1060 standard, not from memory |
| Build the statement pack against the Tier 2 disclosure checklist | `year-end-workpapers` skill |
| Confirm which disclosures Tier 2 removes relative to full IFRS (e.g. segment reporting, most financial instrument disclosures) before treating something as "missing" | `openaccountants` guide, re-verified at time of use |

AASB 1060 is a disclosure standard, not a recognition-and-measurement one —
it still points to the applicable AASB standards (e.g. AASB 15, AASB 16) for
how a transaction is recognised and measured. Simplification is in what's
disclosed about it, not how it's accounted for.

## AASB S2 — climate-related financial disclosure phase-in

AASB S2 introduces mandatory climate disclosure for entities that meet the
size/reporting thresholds under the Australian Sustainability Reporting
Standards regime, phased in by group over several years starting with the
largest entities. It sits alongside AASB 1060, not instead of it — a Tier 2
statement pack for a client that crosses an AASB S2 threshold gets both the
Tier 2 financial statement disclosures and a separate sustainability report.

| Step | Tool |
|---|---|
| Check whether a client meets the current AASB S2 group/threshold test for its first applicable year | `openaccountants` guide (AU financial statements / sustainability reporting); verify the live thresholds and start dates at the authoritative source — AASB S2 phase-in dates are legislated, not stable across memory |
| If in scope, scope the climate disclosure as a distinct deliverable from the statement pack | `year-end-workpapers` skill, extended rather than folded into the existing lead schedules |
| If not yet in scope but approaching a threshold | Note the trigger and expected year in the client's engagement file so intake catches it before the threshold year, not after |

Given NewFinera's current client base (small proprietary companies,
Virtual CFO clients), AASB S2 is not expected to be in scope for most
engagements yet — but the phase-in schedule brings progressively smaller
entity groups in each year, so this check belongs in intake going forward,
not just at year-end.

## Data handling

Same boundary as everywhere else in this repo: the disclosure checklists
and framework logic above live here; a client's actual statement pack,
trial balance or sustainability data does not. See
[`SERVICE-MODEL.md`](SERVICE-MODEL.md#data-handling) and
[`../CLAUDE.md`](../CLAUDE.md).
