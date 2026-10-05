# NewFinera Client Dashboard

The React build of the Client Reporting Dashboard product (see
`../../docs/SERVICE-MODEL.md` §5). Forked from
[Daaviddev/vite-dashboard-starter](https://github.com/Daaviddev/vite-dashboard-starter)
(Vite + React + TypeScript + Tailwind + Radix/shadcn + Zustand), with Recharts
added for the charts.

This replaces the earlier Artifact-based attempt at the same layout, which
hit unreliable external-CDN script loading (React/Tailwind/Chart.js all
loaded at runtime from a `<script src>`) in that sandbox. This project
compiles everything at build time instead — no runtime CDN dependency, no
loading-order risk.

## Status

`src/pages/DashboardHome.tsx` currently renders the five-card layout from the
original spec — donut, multi-series trend line, semi-circular gauge with
ecosystem badges, bullet-target progress bars with a mini bar chart, and a
KPI list with radial loaders — all populated with clearly-labelled
**illustrative sample data**. It is a layout demonstration, not yet wired to
a real client's reconciled figures.

## Using it for a real client

1. `pnpm install`
2. Replace the sample data in each `src/components/dashboard/*Card.tsx` file
   with that client's actual figures, per the tailoring checklist in
   `../../docs/SERVICE-MODEL.md` §5 (what varies per client vs. what stays
   fixed).
3. `pnpm run build` — must complete with zero TypeScript errors before
   delivery.
4. Never commit a client-specific build of this project back into this
   shared template; per `../../CLAUDE.md`, real client data stays out of
   this repository. Deploy or export the built client version separately.

## Development

```bash
pnpm install
pnpm run dev      # local dev server
pnpm run build    # production build, outputs to docs/ (gitignored)
pnpm run lint
```

## Known issue fixed from upstream

The starter's `tsconfig.json` used a `baseUrl` + `paths` combination that a
newer TypeScript release rejects (`error TS5102: Option 'baseUrl' has been
removed`). Fixed here by dropping `baseUrl` and keeping `paths` with
`./src/*`-style relative entries, per the compiler's own suggested fix.
