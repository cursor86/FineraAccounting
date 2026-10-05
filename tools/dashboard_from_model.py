#!/usr/bin/env python3
"""Build a client's web dashboard from a filled 3-statement model.

Reads docs/templates/3-statement-model-template.xlsx (filled for one client) and
writes a single self-contained HTML page: headline cards, charts, KPIs, the
three statements and the accountant's notes. Every figure comes from the
workbook's own computed cells, so the page and the model never disagree.

Usage:
  python3 tools/dashboard_from_model.py CLIENT.xlsx -o OUT.html \
      [--notes notes.txt] [--prepared-by "Name, ACCA"] [--brand "Rizz Digital Solutions"] [--draft]

  --notes   plain-text file, one action per line, shown as "What this means".
            Without it the page lists auto-generated discussion points marked
            for review.
  --draft   allow output when a tie-out check fails (adds a red DRAFT banner).

Write OUT.html to the firm's secure client storage, never into this repo
(see CLAUDE.md). The page is prep-only and carries a blank reviewer sign-off.
"""
import argparse, html, math, sys
from datetime import date
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("Needs openpyxl: pip install openpyxl")

TB, PL, BS, CF, DB, MO = "Trial Balance Input", "P&L", "Balance Sheet", "Cash Flow", "Dashboard", "Monthly (optional)"
EXPECT = {(PL, "A5"): "Revenue", (PL, "A17"): "Net Profit", (BS, "A10"): "TOTAL ASSETS",
          (CF, "A10"): "Net Cash from Operating Activities", (DB, "A10"): "Current Ratio"}


def read_values(path):
    """Cached values if Excel/Sheets saved them, else compute with pycel."""
    wb = load_workbook(path, data_only=True)
    for (sheet, cell), label in EXPECT.items():
        got = (wb[sheet][cell].value or "").strip()
        if got != label:
            sys.exit(f"{path}: {sheet}!{cell} reads {got!r}, expected {label!r}. Is this the 3-statement model template?")
    if wb[PL]["C17"].value is not None:
        return lambda s, c: wb[s][c].value
    try:
        from pycel import ExcelCompiler
    except ImportError:
        sys.exit("The workbook has no saved results. Open it in Excel or Google Sheets, save, and run again "
                 "(or pip install pycel to compute them here).")
    xl = ExcelCompiler(filename=str(path)); raw = load_workbook(path)
    def get(s, c):
        v = raw[s][c].value
        return xl.evaluate(f"'{s}'!{c}") if isinstance(v, str) and v.startswith("=") else v
    return get


def num(v):
    return float(v) if isinstance(v, (int, float)) else None


def money(v, short=False):
    if v is None: return "–"
    a = abs(v)
    if short and a >= 1_000_000: s = f"${a/1_000_000:.1f}m"
    elif short and a >= 10_000: s = f"${a/1000:.0f}k"
    else: s = f"${a:,.0f}"
    return f"({s})" if v < 0 else s


def pct(v, dp=1):
    return "–" if v is None else f"{v*100:.{dp}f}%"


def change(cur, prior, kind="pct"):
    """Return (text, css) for a change badge."""
    if cur is None or prior is None: return "", "flat"
    if kind == "pp":
        d = (cur - prior) * 100
        return f"{d:+.1f} pts vs prior", "up" if d > 0 else "down" if d < 0 else "flat"
    if prior == 0: return "", "flat"
    d = (cur - prior) / abs(prior)
    return f"{d*100:+.0f}% vs prior", "up" if d > 0 else "down" if d < 0 else "flat"


def collect(get):
    g = lambda s, c: num(get(s, c))
    d = {"name": str(get(TB, "B4") or "Client").strip("[]"), "period": str(get(TB, "D4") or ""),
         "entity": str(get(TB, "B6") or ""), "gst": str(get(TB, "D6") or ""),
         "uncat": int(g(TB, "B3") or 0)}
    d["pl"] = {k: (g(PL, f"B{r}"), g(PL, f"C{r}")) for k, r in
               dict(rev=5, cogs=6, gp=7, opex=9, dep=10, ebit=11, int=13, pbt=14, tax=16, np=17, gm=20, nm=21).items()}
    d["bs"] = {k: (g(BS, f"B{r}"), g(BS, f"C{r}")) for k, r in
               dict(cash=6, oca=7, tca=8, nca=9, ta=10, cl=13, ncl=14, tl=15, sc=18, draw=19, re=20, te=21, tle=23, chk=25).items()}
    d["bs_labels"] = {k: str(get(BS, f"A{r}") or "").strip() for k, r in dict(sc=18, draw=19).items()}
    d["bs_status"] = str(get(BS, "A26") or ""); d["bs_note"] = str(get(BS, "A28") or "")
    d["cf"] = {k: g(CF, f"B{r}") for k, r in
               dict(np=6, dep=7, oca=8, cl=9, op=10, capex=13, inv=14, sc=17, draw=18, ncl=19, fin=20, net=22, open=23, close=24, close_bs=25, chk=27).items()}
    d["cf_status"] = str(get(CF, "A28") or "")
    d["kpi"] = {k: (g(DB, f"B{r}"), g(DB, f"C{r}")) for k, r in
                dict(growth=7, gm=8, nm=9, cr=10, cashr=11, de=12).items()}
    months = []
    try:  # older copies of the model have no Monthly tab
        for r in range(5, 17):
            m, rv, npv, cash = get(MO, f"A{r}"), g(MO, f"B{r}"), g(MO, f"C{r}"), g(MO, f"D{r}")
            if m and rv is not None:
                months.append((str(m), rv, npv, cash))
    except KeyError:
        pass
    d["months"] = months
    d["ties"] = (d["bs"]["chk"][0] is not None and abs(d["bs"]["chk"][0]) < 1 and abs(d["bs"]["chk"][1]) < 1
                 and d["cf"]["chk"] is not None and abs(d["cf"]["chk"]) < 1 and d["uncat"] == 0)
    return d


# ---------- charts (inline SVG, no scripts) ----------
BLUE, SKY, GREEN, RED, AMBER, GREY = "#5d87ff", "#49beff", "#13deb9", "#fa896b", "#ffae1f", "#e5eaef"


def bar_chart(labels, series, height=280):
    """Grouped bars. series = [(name, colour, values)]."""
    W, H, L, B, T = 640, height, 56, 34, 16
    vals = [v for _, _, vs in series for v in vs if v is not None]
    top = max(vals + [0]); low = min(vals + [0])
    raw = max(top - low, 1) / 4; unit = 10 ** math.floor(math.log10(raw))
    step = next(m * unit for m in (1, 2, 2.5, 5, 10) if m * unit >= raw)
    top = math.ceil(top / step) * step or step; low = -math.ceil(-low / step) * step if low < 0 else 0
    y = lambda v: T + (top - v) / (top - low) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(", ".join(n for n, _, _ in series))} by period">']
    for i in range(int(round((top - low) / step)) + 1):
        v = low + step * i
        out.append(f'<line x1="{L}" x2="{W}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#eef1f6" stroke-dasharray="4 4"/>'
                   f'<text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" class="ax">{money(v, True)}</text>')
    n, k = len(labels), len(series); slot = (W - L) / n; bw = min(14, slot * 0.7 / k)
    for i, lab in enumerate(labels):
        cx = L + slot * (i + 0.5)
        for j, (name, col, vs) in enumerate(series):
            v = vs[i]
            if v is None: continue
            x = cx - bw * k / 2 - (k - 1) * 2 + j * (bw + 4)
            y0, y1 = sorted((y(0), y(v)))
            out.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{max(y1-y0,1):.1f}" rx="{bw/2:.1f}" fill="{col}">'
                       f'<title>{html.escape(lab)} · {html.escape(name)}: {money(v)}</title></rect>')
        out.append(f'<text x="{cx:.1f}" y="{H-12}" text-anchor="middle" class="ax">{html.escape(lab)}</text>')
    if low < 0:
        out.append(f'<line x1="{L}" x2="{W}" y1="{y(0):.1f}" y2="{y(0):.1f}" stroke="#c9d2de"/>')
    return "".join(out) + "</svg>"


def line_chart(labels, values, colour=SKY, height=150):
    W, H, P = 320, height, 14
    vs = [v for v in values if v is not None]
    if len(vs) < 2: return ""
    hi, lo = max(vs), min(vs + [0]); span = (hi - lo) or 1
    pts = [(P + i * (W - 2 * P) / (len(values) - 1), P + (hi - v) / span * (H - 2 * P - 16)) for i, v in enumerate(values)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    area = d + f" L{pts[-1][0]:.1f},{H-16} L{pts[0][0]:.1f},{H-16} Z"
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cash at month end">'
            f'<path d="{area}" fill="{colour}" opacity=".12"/><path d="{d}" fill="none" stroke="{colour}" stroke-width="2.5"/>'
            f'<text x="{P}" y="{H-2}" class="ax">{html.escape(labels[0])}</text>'
            f'<text x="{W-P}" y="{H-2}" class="ax" text-anchor="end">{html.escape(labels[-1])}</text></svg>')


def donut(parts, size=150):
    """parts = [(label, value, colour)] — values >= 0."""
    tot = sum(v for _, v, _ in parts if v and v > 0) or 1
    r, c = 52, 2 * math.pi * 52; off = 0; segs = []
    for lab, v, col in parts:
        if not v or v <= 0: continue
        ln = v / tot * c
        segs.append(f'<circle r="{r}" cx="75" cy="75" fill="none" stroke="{col}" stroke-width="20" '
                    f'stroke-dasharray="{ln:.2f} {c-ln:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 75 75)">'
                    f'<title>{html.escape(lab)}: {money(v)}</title></circle>')
        off += ln
    return f'<svg viewBox="0 0 150 150" width="{size}" height="{size}" role="img" aria-label="Where revenue went">{"".join(segs)}</svg>'


# ---------- notes ----------
def auto_notes(d):
    pl, bs, kpi = d["pl"], d["bs"], d["kpi"]; n = []
    g = kpi["growth"][1]
    if g is not None:
        n.append(f"Revenue {'grew' if g >= 0 else 'fell'} {abs(g)*100:.0f}% to {money(pl['rev'][1])}. "
                 + ("Check the drivers: price, volume or new customers." if g >= 0 else "Look at which customers or services dropped."))
    gm0, gm1 = pl["gm"]
    if gm0 is not None and gm1 is not None and abs(gm1 - gm0) >= 0.01:
        n.append(f"Gross margin moved from {pct(gm0)} to {pct(gm1)}. "
                 + ("Supplier costs or pricing are working in your favour." if gm1 > gm0 else "Review supplier prices and your own pricing."))
    cr = kpi["cr"][1]
    if cr is not None:
        n.append(f"Current ratio is {cr:.1f}x: "
                 + ("short-term bills are well covered." if cr >= 1.5 else "short-term bills are only just covered, so watch cash timing." if cr >= 1 else "short-term bills exceed short-term assets, so plan cash carefully."))
    net = d["cf"]["net"]
    if net is not None:
        n.append(f"Cash {'rose' if net >= 0 else 'fell'} by {money(abs(net))} to {money(bs['cash'][1])}, after "
                 f"{money(abs(d['cf']['capex'] or 0))} on equipment and {money(abs(d['cf']['draw'] or 0))} paid to owners.")
    return n[:4]


# ---------- page ----------
CSS = """
:root{--pri:#5d87ff;--pri-l:#ecf2ff;--sec:#49beff;--ok:#13deb9;--ok-l:#e6fffa;--bad:#fa896b;--bad-l:#fdede8;--warn:#ffae1f;--warn-l:#fef5e5;
--ink:#2a3547;--mute:#5a6a85;--line:#e5eaef;--bg:#f4f7fb;--card:#fff}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 14px/1.55 'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
.app{display:grid;grid-template-columns:250px 1fr;min-height:100vh}
aside{background:#fff;border-right:1px solid var(--line);padding:24px 18px;position:sticky;top:0;height:100vh}
.logo{font-weight:700;font-size:18px;display:flex;gap:10px;align-items:center;margin-bottom:26px}
.logo i{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--pri),var(--sec));display:block}
.navh{font-size:11px;font-weight:700;letter-spacing:.08em;color:var(--ink);margin:18px 8px 8px;text-transform:uppercase}
nav a{display:block;padding:10px 14px;border-radius:7px;color:var(--mute);text-decoration:none;font-weight:500}
nav a:hover,nav a.on{background:var(--pri);color:#fff}
.client{margin-top:26px;padding:14px;border-radius:10px;background:var(--pri-l);font-size:12.5px;color:var(--mute)}
.client b{display:block;color:var(--ink);font-size:14px}
main{padding:24px 28px 40px;min-width:0}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:22px}
.top h1{margin:0;font-size:22px}.top p{margin:2px 0 0;color:var(--mute)}
.pill{padding:6px 12px;border-radius:99px;font-weight:600;font-size:12.5px}
.pill.ok{background:var(--ok-l);color:#0b9e85}.pill.bad{background:var(--bad-l);color:#c2410c}
.grid{display:grid;gap:20px}.g4{grid-template-columns:repeat(4,1fr)}.g21{grid-template-columns:2fr 1fr}.g3{grid-template-columns:repeat(3,1fr)}.g11{grid-template-columns:1fr 1fr}
.card{background:var(--card);border-radius:12px;box-shadow:0 2px 6px rgba(37,83,185,.06),0 0 0 1px rgba(229,234,239,.6);padding:22px 24px;min-width:0}
.card h2{font-size:17px;margin:0 0 4px}.card .sub{color:var(--mute);margin:0 0 14px;font-size:13px}
.stat .lab{color:var(--mute);font-weight:500}.stat .val{font-size:24px;font-weight:700;margin:6px 0}
.chg{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:600;color:var(--mute)}
.chg i{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:12px}
.chg.up i{background:var(--ok-l);color:#0b9e85}.chg.down i{background:var(--bad-l);color:#c2410c}.chg.flat i{background:var(--line)}
.legend{display:flex;gap:16px;color:var(--mute);font-size:12.5px;margin-bottom:6px}.legend b{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
svg{display:block;width:100%;height:auto}svg .ax{fill:#7c8fac;font-size:11px;font-family:inherit}
.donut{display:flex;align-items:center;gap:16px}.donut svg{width:150px;flex:none}
.dl{list-style:none;margin:0;padding:0;font-size:13px}.dl li{display:flex;justify-content:space-between;gap:10px;padding:4px 0}.dl b{font-weight:600}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}
table{width:100%;border-collapse:collapse;font-size:13px}th{font-size:11.5px;color:var(--mute);font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid var(--line)}
th:first-child{text-align:left}td{padding:7px 0;border-bottom:1px solid #f1f4f8;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td:first-child{text-align:left;white-space:normal;color:var(--mute)}tr.s td{font-weight:600;color:var(--ink)}tr.t td{font-weight:700;color:var(--pri);border-top:1px solid var(--line);border-bottom:0}
.kpi{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.k{border:1px solid var(--line);border-radius:10px;padding:14px}.k .n{font-size:12.5px;color:var(--mute);font-weight:500}.k .v{font-size:20px;font-weight:700;margin:2px 0}
.k .p{font-size:12px;color:var(--mute)}
.notes ol{margin:0;padding-left:20px}.notes li{margin-bottom:10px}
.flag{background:var(--warn-l);color:#92400e;border-radius:8px;padding:10px 14px;font-size:13px;margin-top:12px}
.draft{background:var(--bad);color:#fff;font-weight:700;text-align:center;padding:10px;border-radius:10px;margin-bottom:18px}
footer{color:var(--mute);font-size:12px;margin-top:24px;line-height:1.7}
.sign{display:flex;gap:30px;flex-wrap:wrap;margin-top:10px}.sign span{border-bottom:1px solid #c9d2de;min-width:220px;display:inline-block;padding-bottom:2px}
@media(max-width:1100px){.g4{grid-template-columns:repeat(2,1fr)}.g21,.g3,.g11{grid-template-columns:1fr}}
@media(max-width:820px){.app{grid-template-columns:minmax(0,1fr)}aside{position:static;height:auto;padding:16px;min-width:0}nav{display:flex;gap:6px;overflow-x:auto}nav a{white-space:nowrap}.navh,.client{display:none}.logo{margin-bottom:12px}
main{padding:16px}.kpi{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.g4,.kpi{grid-template-columns:1fr}.donut{flex-direction:column;align-items:flex-start}}
@media print{aside{display:none}.app{display:block}.card{break-inside:avoid;box-shadow:none;border:1px solid var(--line)}}
"""


def stmt(rows, prior=True):
    out = ['<table><thead><tr><th></th>' + ('<th>Prior</th>' if prior else '') + '<th>Current</th></tr></thead><tbody>']
    for label, (p, c), cls in rows:
        pcol = f'<td>{money(p)}</td>' if prior else ''
        out.append(f'<tr class="{cls}"><td>{html.escape(label)}</td>{pcol}<td>{money(c)}</td></tr>')
    return "".join(out) + "</tbody></table>"


def neg(t): return tuple(None if v is None else -v for v in t)


def build(d, notes, prepared_by, brand, draft):
    pl, bs, cf, kpi = d["pl"], d["bs"], d["cf"], d["kpi"]
    e = html.escape
    cards = []
    for lab, cur, prior, kind, fmt in (("Revenue", pl["rev"][1], pl["rev"][0], "pct", money),
                                       ("Net profit", pl["np"][1], pl["np"][0], "pct", money),
                                       ("Gross margin", pl["gm"][1], pl["gm"][0], "pp", pct),
                                       ("Cash at bank", bs["cash"][1], bs["cash"][0], "pct", money)):
        txt, css = change(cur, prior, kind)
        arrow = {"up": "↑", "down": "↓", "flat": "•"}[css]
        cards.append(f'<div class="card stat"><div class="lab">{lab}</div><div class="val">{fmt(cur)}</div>'
                     f'<span class="chg {css}"><i>{arrow}</i>{e(txt) or "&nbsp;"}</span></div>')

    if d["months"]:
        labels = [m[0] for m in d["months"]]
        main_chart = (f'<h2>Revenue and profit by month</h2><p class="sub">{e(d["period"])}</p>'
                      f'<div class="legend"><span><b style="background:{BLUE}"></b>Revenue</span><span><b style="background:{SKY}"></b>Net profit</span></div>'
                      + bar_chart(labels, [("Revenue", BLUE, [m[1] for m in d["months"]]), ("Net profit", SKY, [m[2] for m in d["months"]])]))
        cash_vals = [m[3] for m in d["months"]]
        side_chart = (f'<h2>Cash at month end</h2><p class="sub">Closing balance {money(bs["cash"][1])}</p>'
                      + (line_chart(labels, cash_vals) if all(v is not None for v in cash_vals) else '<p class="sub">Monthly cash not provided.</p>'))
    else:
        labels = ["Revenue", "Gross profit", "EBIT", "Net profit"]
        main_chart = ('<h2>This period vs prior</h2><p class="sub">Annual figures from the model</p>'
                      f'<div class="legend"><span><b style="background:#c8d6ff"></b>Prior</span><span><b style="background:{BLUE}"></b>Current</span></div>'
                      + bar_chart(labels, [("Prior", "#c8d6ff", [pl[k][0] for k in ("rev", "gp", "ebit", "np")]),
                                           ("Current", BLUE, [pl[k][1] for k in ("rev", "gp", "ebit", "np")])]))
        side_chart = None

    parts = [("Cost of sales", pl["cogs"][1], BLUE), ("Operating expenses", pl["opex"][1], SKY), ("Depreciation", pl["dep"][1], "#a3b8ff"),
             ("Interest", pl["int"][1], AMBER), ("Tax", pl["tax"][1], RED), ("Net profit", max(pl["np"][1] or 0, 0), GREEN)]
    rev = pl["rev"][1] or 1
    dl = "".join(f'<li><span><i class="dot" style="background:{c}"></i>{e(l)}</span><b>{(v or 0)/rev*100:.0f}%</b></li>' for l, v, c in parts if v)
    donut_card = (f'<div class="card"><h2>Where each $1 of revenue went</h2><p class="sub">Current period</p>'
                  f'<div class="donut">{donut(parts)}<ul class="dl">{dl}</ul></div></div>')
    if side_chart is None:
        side_html, donut_slot = donut_card, ""
    else:
        side_html, donut_slot = f'<div class="card">{side_chart}</div>', donut_card

    def k(name, idx, fmt, hint):
        p, c = kpi[idx]
        prior = f"Prior {fmt(p)} · " if p is not None else ""
        return f'<div class="k"><div class="n">{name}</div><div class="v">{fmt(c)}</div><div class="p">{prior}{hint}</div></div>'
    x = lambda v: "–" if v is None else f"{v:.2f}x"
    kpis = (k("Revenue growth", "growth", lambda v: "–" if v is None else f"{v*100:+.1f}%", "vs prior period")
            + k("Gross margin", "gm", pct, "after cost of sales")
            + k("Net margin", "nm", pct, "profit per $1 of sales")
            + k("Current ratio", "cr", x, "short-term assets ÷ bills")
            + k("Cash ratio", "cashr", x, "cash ÷ short-term bills")
            + k("Debt to equity", "de", x, "liabilities ÷ equity"))

    pl_t = stmt([("Revenue", pl["rev"], ""), ("Cost of sales", neg(pl["cogs"]), ""), ("Gross profit", pl["gp"], "s"),
                 ("Operating expenses", neg(pl["opex"]), ""), ("Depreciation", neg(pl["dep"]), ""), ("EBIT", pl["ebit"], "s"),
                 ("Interest", neg(pl["int"]), ""), ("Tax", neg(pl["tax"]), ""), ("Net profit", pl["np"], "t")])
    bs_t = stmt([("Cash", bs["cash"], ""), ("Other current assets", bs["oca"], ""), ("Non-current assets", bs["nca"], ""),
                 ("Total assets", bs["ta"], "s"), ("Current liabilities", neg(bs["cl"]), ""), ("Non-current liabilities", neg(bs["ncl"]), ""),
                 (d["bs_labels"]["sc"] or "Capital", bs["sc"], ""), ("Retained earnings", bs["re"], ""), ("Total equity", bs["te"], "t")])
    c = lambda key: (None, cf[key])
    cf_t = stmt([("Net profit", c("np"), ""), ("Add back depreciation", c("dep"), ""), ("Working capital movement", (None, (cf["oca"] or 0) + (cf["cl"] or 0)), ""),
                 ("Operating cash flow", c("op"), "s"), ("Equipment & assets bought", c("inv"), "s"), ("New capital", c("sc"), ""),
                 ("Paid to owners", c("draw"), ""), ("Loans drawn / (repaid)", c("ncl"), ""), ("Financing cash flow", c("fin"), "s"),
                 ("Opening cash", c("open"), ""), ("Closing cash", c("close"), "t")], prior=False)

    note_items = notes or auto_notes(d)
    note_hint = ("Prepared by your accountant" if notes else "Auto-generated discussion points — review and replace before sending")
    flag = f'<div class="flag">{e(d["bs_note"])}</div>' if d["bs_note"] else ""
    status = ('<span class="pill ok">✓ Statements tie out</span>' if d["ties"] else '<span class="pill bad">✕ Tie-out exception</span>')
    gst = f" · GST {e(d['gst'])}" if d["gst"] else ""

    return f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{e(d['name'])} | Financial dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="app">
<aside><div class="logo"><i></i>{e(brand)}</div>
<div class="navh">Dashboard</div><nav><a class="on" href="#overview">Overview</a><a href="#kpis">Key numbers</a><a href="#statements">Statements</a><a href="#notes">What this means</a></nav>
<div class="client"><b>{e(d['name'])}</b>{e(d['entity'])}{gst}<br>{e(d['period'])}</div></aside>
<main>{'<div class="draft">DRAFT — tie-out exception, not for the client</div>' if draft and not d['ties'] else ''}
<div class="top" id="overview"><div><h1>{e(d['name'])}</h1><p>Financial dashboard · {e(d['period'])}</p></div>{status}</div>
<div class="grid g4">{''.join(cards)}</div>
<div class="grid g21" style="margin-top:20px"><div class="card">{main_chart}</div>{side_html}</div>
<div class="grid {'g21' if donut_slot else ''}" style="margin-top:20px" id="kpis"><div class="card"><h2>Key numbers</h2><p class="sub">Current period, with prior period for comparison</p><div class="kpi">{kpis}</div></div>{donut_slot}</div>
<div class="grid g3" style="margin-top:20px" id="statements">
<div class="card"><h2>Profit &amp; loss</h2><p class="sub">For the period</p>{pl_t}</div>
<div class="card"><h2>Balance sheet</h2><p class="sub">At period end</p>{bs_t}</div>
<div class="card"><h2>Cash flow</h2><p class="sub">Current period, indirect method</p>{cf_t}</div></div>
<div class="card notes" style="margin-top:20px" id="notes"><h2>What this means</h2><p class="sub">{e(note_hint)}</p>
<ol>{''.join(f'<li>{e(n)}</li>' for n in note_items)}</ol>{flag}</div>
<footer>Prepared {date.today():%d %b %Y}{(' by ' + e(prepared_by)) if prepared_by else ''} from the client's trial balance, using the 3-statement model.
Management information only: not an audit, not tax advice, and nothing here has been lodged or filed with the ATO or any other agency.
<div class="sign"><div>Reviewed by: <span>&nbsp;</span></div><div>Date: <span style="min-width:120px">&nbsp;</span></div></div></footer>
</main></div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--notes"); ap.add_argument("--prepared-by", default="")
    ap.add_argument("--brand", default="Rizz Digital Solutions"); ap.add_argument("--draft", action="store_true")
    a = ap.parse_args()
    d = collect(read_values(a.model))
    if not d["ties"] and not a.draft:
        sys.exit(f"Tie-out exception — not building a client page.\n  Balance Sheet: {d['bs_status']}\n  Cash Flow: {d['cf_status']}\n"
                 f"  Uncategorised rows: {d['uncat']}\nFix the model, or pass --draft for an internal preview.")
    notes = [l.strip() for l in Path(a.notes).read_text().splitlines() if l.strip()] if a.notes else None
    Path(a.out).write_text(build(d, notes, a.prepared_by, a.brand, a.draft), encoding="utf-8")
    print(f"Wrote {a.out}  ({d['name']}, {d['period']}, {'ties' if d['ties'] else 'DRAFT'})")


if __name__ == "__main__":
    main()
