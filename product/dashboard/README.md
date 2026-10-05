# NewFinera Client Dashboard

The React build of the Client Reporting Dashboard product (see
`../../docs/SERVICE-MODEL.md` §5): Vite + React + TypeScript + Tailwind CSS +
Recharts, fully self-authored — a minimal scaffold written for this project,
not forked from any third-party template.

(An earlier version of this project was scaffolded from
[Daaviddev/vite-dashboard-starter](https://github.com/Daaviddev/vite-dashboard-starter).
That repo has no LICENSE file — "all rights reserved" by default — which is a
real risk for something NewFinera sells, so it was dropped and this scaffold
was rewritten from scratch. The five dashboard card components below were
always original work either way.)

This also replaces the earlier Artifact-based attempt at the same layout,
which hit unreliable external-CDN script loading (React/Tailwind/Chart.js
all loaded at runtime via `<script src>`) in that sandbox. Compiling
everything at build time removes that failure mode entirely.

## Status

`src/pages/DashboardHome.tsx` renders the five-card layout from the original
spec — donut, multi-series trend line, semi-circular gauge with ecosystem
badges, bullet-target progress bars with a mini bar chart, and a KPI list
with radial loaders — all populated with clearly-labelled **illustrative
sample data**. It is a layout demonstration, not yet wired to a real
client's reconciled figures.

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
pnpm run build    # production build, outputs to dist/ (gitignored)
```
