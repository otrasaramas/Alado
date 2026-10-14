import asyncio, json, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
FONTS = (HERE.parent / "canva/fonts-tyc.css").read_text()
st = json.loads(Path(sys.argv[1]).read_text())
OUT = Path(sys.argv[2])

rates = {r["id"]: r for r in st["rates"]}
def money(n): return "$" + f"{n:,.0f}".replace(",", ".")
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def price(it): r = rates.get(it["rate"]); return r["price"] if r and isinstance(r.get("price"), (int, float)) else None
def sec_total(sec):
    t = tbd = 0
    for it in sec["items"]:
        p = price(it)
        if p is None:
            if it["qty"] > 0: tbd += 1
        else: t += p * it["qty"]
    return t, tbd
grand = sum(sec_total(s)[0] for s in st["sections"]); grand_tbd = sum(sec_total(s)[1] for s in st["sections"])
TBD = '<span class="tbd">Por definir</span>'

def table(sec):
    rows = ""
    for it in sec["items"]:
        p = price(it); r = rates.get(it["rate"])
        date = TBD if (not it["date"] or "definir" in it["date"].lower()) else esc(it["date"])
        rows += (f'<tr><td>{esc(it["piece"])}</td><td class="fmt">{esc(r["name"] if r else "")}</td><td class="nw">{date}</td>'
                 f'<td class="num">{it["qty"]}</td><td class="num">{money(p) if p is not None else TBD}</td>'
                 f'<td class="num">{money(p*it["qty"]) if p is not None else "—"}</td></tr>')
    t, tbd = sec_total(sec)
    extra = f' <span class="tbd">+ {tbd} por definir</span>' if tbd else ""
    return (f'<section class="block"><h2>{esc(sec["name"])}<span class="sub">{money(t)}{extra}</span></h2>'
            f'<table><thead><tr><th>Pieza</th><th>Formato</th><th>Publica</th><th class="num">Cant.</th><th class="num">Valor unit.</th><th class="num">Subtotal</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></section>')

rates_rows = "".join(f'<tr><td>{esc(r["name"])}</td><td class="num">{money(r["price"]) if isinstance(r.get("price"), (int, float)) else TBD}</td><td>{esc(r.get("note",""))}</td></tr>' for r in st["rates"])
summary = "".join(f'<div><span>{esc(s["name"])}</span><b>{money(sec_total(s)[0])}</b></div>' for s in st["sections"])
pending = f'<p class="pending">+ {grand_tbd} {"pieza" if grand_tbd == 1 else "piezas"} por definir</p>' if grand_tbd else ""

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Cotización · Contenido para Alado</title><style>{FONTS}
@page {{ size: A4; margin: 14mm 0 14mm; }}
@page :first {{ margin-top: 0; }}
:root {{ --ink:#1F2A33; --muted:#5E6B76; --rule:#D5DCE2; --blue:#5C7891; --soft:#E9EEF3; --warn:#8F520F; --paper:#FFFFFF; }}
html, body {{ margin:0; background:var(--paper); }}
body {{ font-family:'Archivo'; color:var(--ink); font-size:9.6pt; line-height:1.42; font-variant-numeric:lining-nums tabular-nums; font-feature-settings:'lnum' 1, 'tnum' 1; }}
.pad {{ padding:0 16mm; }}
header {{ background:var(--blue); color:#F3F1EA; padding:13mm 16mm 9mm; display:flex; justify-content:space-between; align-items:flex-end; gap:10mm; }}
.brand {{ font-weight:600; font-size:13pt; margin:0 0 5mm; }}
.kicker {{ font-weight:600; font-size:8pt; letter-spacing:1.6px; margin:0 0 1.5mm; opacity:.9; }}
h1 {{ font-family:'Playfair Display'; font-weight:400; font-size:30pt; line-height:1; margin:0; }}
h1 em {{ font-style:italic; }}
.total {{ text-align:right; white-space:nowrap; }}
.total .l {{ font-weight:600; font-size:8pt; letter-spacing:1.6px; opacity:.9; }}
.total .v {{ font-family:'Playfair Display'; font-size:28pt; line-height:1; margin-top:2mm; }}
.total .pending {{ margin:2mm 0 0; font-size:8.5pt; font-weight:600; color:#FBE7C2; }}
.meta {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:4mm; margin:6mm 0 0; padding-bottom:4mm; border-bottom:1.5px solid var(--ink); }}
.meta small {{ display:block; font-weight:600; font-size:7pt; letter-spacing:1.3px; color:var(--muted); }}
.meta b {{ font-weight:500; }}
.summary {{ display:grid; grid-template-columns:repeat({len(st["sections"])}, 1fr); gap:4mm; margin:5mm 0 2mm; }}
.summary div {{ background:var(--soft); border-radius:2mm; padding:3mm 4mm; }}
.summary span {{ display:block; font-size:8.5pt; color:var(--muted); }}
.summary b {{ font-size:13pt; font-weight:600; }}
.block {{ margin-top:5.5mm; }}
.rates {{ break-before:page; margin-top:0; }}
h2 {{ font-family:'Playfair Display'; font-weight:400; font-size:16pt; margin:0 0 2mm; display:flex; justify-content:space-between; align-items:baseline; break-after:avoid; }}
h2 .sub {{ font-family:'Archivo'; font-size:9.5pt; font-weight:600; }}
table {{ width:100%; border-collapse:collapse; }}
thead {{ display:table-header-group; }}
tr {{ break-inside:avoid; }}
th {{ text-align:left; font-weight:600; font-size:7pt; letter-spacing:1px; text-transform:uppercase; color:var(--muted); padding:2mm 2mm; border-bottom:1px solid var(--ink); white-space:nowrap; }}
td {{ padding:1.7mm 2mm; border-bottom:1px solid var(--rule); vertical-align:top; }}
.num {{ text-align:right; white-space:nowrap; }}
.nw {{ white-space:nowrap; }}
.fmt {{ color:var(--muted); white-space:nowrap; }}
.tbd {{ color:var(--warn); font-weight:600; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:7mm; break-inside:avoid; }}
.cols h3 {{ font-family:'Playfair Display'; font-weight:400; font-size:14pt; margin:0 0 2mm; }}
.cols ul {{ margin:0; padding-left:4.5mm; }}
.cols li {{ margin-bottom:1.2mm; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid var(--rule); font-size:8pt; color:var(--muted); }}
</style></head><body>
<header><div><p class="brand">{esc(st["preparedBy"])} · Contenido y diseño</p><p class="kicker">COTIZACIÓN</p><h1>Contenido para <em>Alado</em></h1></div>
<div class="total"><div class="l">TOTAL</div><div class="v">{money(grand)}</div>{pending}</div></header>
<div class="pad">
<div class="meta"><div><small>PARA</small><b>{esc(st["client"])}</b></div><div><small>PERIODO</small><b>{esc(st["period"])}</b></div><div><small>PREPARADA POR</small><b>{esc(st["preparedBy"])}</b></div><div><small>FECHA</small><b>{esc(st["date"])}</b></div></div>
{"".join(table(s) for s in st["sections"])}
<section class="block rates"><h2>Tarifas</h2><table><thead><tr><th>Formato</th><th class="num">Valor</th><th>Incluye</th></tr></thead><tbody>{rates_rows}</tbody></table></section>
<div class="cols"><div><h3>Condiciones</h3><ul>{"".join(f"<li>{esc(c)}</li>" for c in st["conditions"])}</ul></div><div><h3>Notas</h3><ul>{"".join(f"<li>{esc(n)}</li>" for n in st["notes"])}</ul></div></div>
<p class="foot">Valores en pesos colombianos. Las piezas «por definir» se suman al total cuando tengan tarifa.</p>
</div></body></html>"""
(HERE / "_cot.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page()
        await pg.goto(f"file://{(HERE/'_cot.html').resolve()}"); await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(OUT), format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
print("total", money(grand), "por definir", grand_tbd)
