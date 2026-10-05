# NewFinera service model

Maps NewFinera's actual service lines to the workflow that delivers each one.
Every workflow ends the same way: a review-ready output, never a lodgment,
filing or payment. An authorised human (NewFinera's registered agent, or the
client) decides and lodges.

## Service lines

### 1. Bookkeeping & Systems Setup (from $350/month)

Chart of accounts configuration, monthly reconciliations, record-keeping in
Xero or MYOB, and cleanup projects for backlogged books.

| Step | Tool |
|---|---|
| Parse the client's Xero/MYOB export | `xero-exports` skill (report conventions, CSV parsing traps) |
| Bank & control account reconciliation | `month-end-close` skill |
| Backlog cleanup, tracing every line to source | `workpaper-tie-out` skill |
| AU-specific bookkeeping treatment | `openaccountants` guide: `australia-bookkeeping.md` |

### 2. BAS preparation (recurring, monthly or quarterly)

Not listed as a separate line on the site but implied by "accurate
record-keeping" — every bookkeeping client on a GST registration needs this.

| Step | Tool |
|---|---|
| Build the BAS workpaper, tie 1A − 1B to the GST control account | `bas-preparation` skill |
| GST treatment references | `openaccountants` guides: `australia-gst.md`, `au-gst-bas.md`, `au-gst-property.md` |
| Payroll-linked labels (W1-W4) if the client runs payroll | `bas-preparation` skill, sourced from the payroll activity summary, never GL wages expense |

### 3. Virtual CFO & Management Accounts (from $750/month)

Monthly financial statements, cash flow forecasting, budget analysis, KPI
dashboards.

| Step | Tool |
|---|---|
| Monthly financial statements | `month-end-close` skill, `openaccountants` guide `australia-financial-statements.md` |
| Cash flow forecasting | `cashflow-forecast-13week` skill (receipts from debtor history, ATO obligation timing) |
| Annual/period-end statement pack | `year-end-workpapers` skill (lead schedules, movement analysis, analytical review) |
| Budget/KPI analytical review | `month-end-close` skill's P&L variance step |

### 4. Specialist add-ons (available, not yet offered on the site)

If NewFinera takes on construction/contracting clients, the accounting-skills
package already covers that vertical: `progress-claim-preparation`,
`retention-schedule`, `wip-over-under-billing`, `contract-cost-tracking`,
`plant-and-equipment-costing`, `fuel-tax-credits`. Payroll-adjacent
compliance work (`stp-finalisation`, `div7a-compliance`, `fbt-annual-workflow`,
`payroll-tax-contractors`, `contractor-super-tpar`, `coal-lsl-levy`) is also
available the moment a client needs it — none of it requires new tooling,
just the relevant skill invoked.

### 5. Client Reporting Dashboard (product)

A sellable deliverable, not just an internal report: a tailored, branded
dashboard built from each client's reconciliation data. It's the concrete
form of the "KPI dashboards" already promised under Virtual CFO & Management
Accounts — and can also be sold standalone, to a client who only wants the
dashboard without the full monthly engagement.

**Two implementations, pick by what the client needs:**

- `product/dashboard/` — the React build (Vite + TypeScript + Tailwind +
  Recharts). Use this by default: it compiles at build time, so there's no
  runtime CDN dependency and no risk of a script failing to load for the
  client. Populate `src/components/dashboard/*Card.tsx` with that client's
  real figures per the checklist below, run `pnpm run build`, and confirm it
  completes with zero TypeScript errors before delivery. See
  `product/dashboard/README.md`.
- `docs/templates/client-dashboard-template.html` — a static HTML/CSS/SVG
  fallback for a one-off delivery where standing up the React project isn't
  worth it. Fill every bracketed placeholder and example number from the
  client's workpaper.

Either way: never ship with template example data still in place, and never
commit a filled-in copy (with real client figures) to this repo — it's a
client deliverable, handed off or published for that client only, per
`CLAUDE.md`'s data-handling rule.

**Tailoring checklist per client:**

| What varies | Examples |
|---|---|
| KPI tiles | Revenue measure, volume metric, and risk metric depend on the business — an e-commerce client wants refund rate; a contracting client wants WIP over/under-billing |
| Breakdown chart | Product/service line, cost centre, project, or whatever dimension the client's business actually segments by |
| Channel/source reconciliation | Payment gateways for e-commerce; progress claims and retentions for contracting; bank accounts for a simple services business |
| Jurisdiction/compliance flag | Only included when a real exception is found in that client's data — never a placeholder risk claim |

**What stays fixed across every client**: the visual system (palette,
typography, layout), the tie-out discipline (every figure traces to the
workpaper, 0 unexplained variance), and the prep-only footer. That
consistency is what makes it a product line instead of a one-off design
exercise each time.

## Engagement lifecycle

1. **Intake.** Fill in `docs/templates/client-finance-officer-brief.md` for
   the client (business name, type, country, top goals), plus entity type,
   GST registration basis (cash/accruals), lodgment cycle, prior-period
   figures, and which system the client uses (Xero or MYOB). No automated
   onboarding/KYB tool is in this pipeline — intake is manual for now (see
   `docs/TOOLS.md` for why Ballerine was set aside).
2. **Data collection.** The client (or NewFinera, with their login) exports
   the relevant reports — Activity Statement, trial balance, GL detail,
   payroll summary. The `xero-exports` skill handles Xero's report quirks;
   apply the same care to MYOB exports even though it isn't Xero-specific.
3. **Processing.** Route to the skill matching the service line above.
   Every skill in this pipeline verifies current ATO rates, thresholds and
   labels at ato.gov.au at the time of use — never from memory — and stops
   to ask rather than guess when a figure can't be verified.
4. **Review.** Every workpaper carries an exceptions list and a blank
   reviewer sign-off line. Unresolved exceptions go to the reviewer, not
   smoothed over.
5. **Delivery.** The signed-off workpaper goes to the client or to
   NewFinera's registered agent for lodgment. This pipeline never lodges,
   files, or pays on the client's behalf. Where the engagement includes the
   Client Reporting Dashboard product, this step also means filling
   `docs/templates/client-dashboard-template.html` from the same reconciled
   figures and handing over the published dashboard alongside the workpaper.

## Data handling

Real client data — exports, workpapers, names, ABNs, TFNs, bank details —
never goes into this repository. Generated client output belongs in
NewFinera's firm-approved secure storage, not a `git`-tracked folder. See
`CLAUDE.md` for the enforced boundary.

## Future expansion

The model is built so a new field is additive — a new skill or guide slotted
in, not a rewrite. Three expansion axes, in the order they're likely to come
up:

1. **New AU specialisms, no new tooling needed.** `openaccountants`'
   Australia folder already carries guides NewFinera doesn't offer yet:
   `au-smsf.md`, `au-crypto-tax.md`, `au-rd-incentive.md`,
   `au-small-business-cgt.md`, `au-nonresident-cgt.md`,
   `au-deceased-estates.md`, `au-land-tax.md`. Turning one into an offered
   service is a matter of adding a row to `SERVICE-MODEL.md`, not building
   anything — the guide and, where one exists, the workflow skill are
   already in the toolkit.
2. **Other jurisdictions.** `openaccountants` covers 232 jurisdictions, not
   just Australia — matching newfinera.com's own AU/UK/US/Pakistan/UAE
   calculator pages. Expanding a service line to another country means
   pointing the same workflow skills at that jurisdiction's guide folder
   under `skills/international/<country>/` in the openaccountants repo (or
   its `packages/<country>/` bundle), and re-checking which AU-specific
   assumptions in the accounting-skills workflows (BAS labels, ATO
   references) need a jurisdiction-specific equivalent before reuse.
3. **Personal finance / broader business finance.** `openaccountant/skills`
   (44 skills, personal/business/shared) is available but not wired into any
   current service line — it's the natural source if NewFinera adds personal
   tax or broader SME financial-planning services beyond bookkeeping and
   Virtual CFO work.

Whichever axis, the engagement lifecycle above doesn't change: intake, data
collection, processing through the matching skill, review, delivery. Only the
skill/guide selected in step 3 changes.

## Explicitly out of scope, for now

- **Xero live API integration** (`xero-agent-toolkit`) — needs a Xero
  Developer Custom Connection (Client ID/Secret); no budget allocated yet.
  The manual-export pipeline above covers the same ground without it.
- **AML/KYC tooling** (evaluated: Ballerine) — a KYB/onboarding platform, not
  an accounting tool; shelved as not relevant to the current service lines.
