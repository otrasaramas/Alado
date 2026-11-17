import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
FONTS = (HERE / "fonts-local.css").read_text()
OUT = Path(sys.argv[1])
def money(n): return "$" + f"{n:,.0f}".replace(",", ".")
def F(t): return f'<span class="fill">{t}</span>'

ITEMS = [
 ("Video de la tienda de El Retiro", "Un día completo de grabación en El Retiro, edición y entrega.", 1, 200000),
 ("Video editado con material de Alado", "Edición, música y texto sobre el material suministrado por Alado. Sin grabación.", 1, 140000),
 ("Fotografías de producto", "Sesión de fotografía de producto con la cámara de Alado, selección y corrección de color. 124 fotografías editadas entregadas.", 124, 4000),
 ("Set de historias de Instagram", "Un set producido con fotografías propias y material de Alado.", 1, 120000),
]
total = sum(q * v for *_, q, v in ITEMS)
rows = "".join(f'<tr><td><b>{t}</b><div class="d">{d}</div></td><td class="num">{q}</td><td class="num">{money(v)}</td><td class="num">{money(q*v)}</td></tr>' for t, d, q, v in ITEMS)

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Cuenta de cobro</title><style>{FONTS}
@page {{ size: A4; margin: 0; }}
:root {{ --ink:#1F2A33; --muted:#5E6B76; --rule:#D5DCE2; --blue:#5C7891; --soft:#E9EEF3; }}
html, body {{ margin:0; background:#fff; }}
body {{ font-family:'Archivo'; color:var(--ink); font-size:10pt; line-height:1.45; font-variant-numeric:lining-nums tabular-nums; font-feature-settings:'lnum' 1, 'tnum' 1; }}
header {{ background:var(--blue); color:#F3F1EA; padding:14mm 17mm 9mm; display:flex; justify-content:space-between; align-items:flex-end; }}
h1 {{ font-family:'Archivo Black'; font-weight:400; font-size:24pt; line-height:1; margin:0; letter-spacing:.5px; }}
.k {{ font-weight:600; font-size:8pt; letter-spacing:1.6px; margin:0 0 2mm; opacity:.9; }}
.no {{ text-align:right; font-weight:600; font-size:9.5pt; line-height:1.6; }}
.pad {{ padding:0 17mm; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:8mm; }}
.box small {{ display:block; font-weight:600; font-size:7pt; letter-spacing:1.3px; color:var(--muted); margin-bottom:1.5mm; }}
.box b {{ font-weight:600; }}
.box {{ border-top:1.5px solid var(--ink); padding-top:3mm; }}
h2 {{ font-family:'Playfair Display'; font-weight:400; font-size:14pt; margin:6mm 0 2mm; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ text-align:left; font-weight:600; font-size:7pt; letter-spacing:1px; text-transform:uppercase; color:var(--muted); padding:2mm 2mm; border-bottom:1px solid var(--ink); }}
td {{ padding:3mm 2mm; border-bottom:1px solid var(--rule); vertical-align:top; }}
.d {{ color:var(--muted); font-size:9pt; margin-top:.8mm; }}
.num {{ text-align:right; white-space:nowrap; }}
.tot td {{ border-bottom:0; font-size:12pt; font-weight:700; padding-top:4mm; }}
.words {{ background:var(--soft); border-radius:2mm; padding:3.5mm 4mm; margin-top:3mm; font-size:9.5pt; }}
.pay {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 8mm; margin-top:2mm; }}
.sign {{ margin-top:14mm; width:78mm; border-top:1px solid var(--ink); padding-top:2mm; font-size:9pt; }}
.note {{ margin-top:5mm; font-size:8.5pt; color:var(--muted); }}
.fill {{ background:#FBE7A1; color:var(--ink); padding:0 1mm; font-weight:500; }}
</style></head><body>
<header><div><p class="k">CUENTA DE COBRO</p><h1>Contenido para Alado</h1></div>
<div class="no">N.º {F("[consecutivo]")}<br>{F("[Ciudad]")}, 17 de noviembre de 2026</div></header>
<div class="pad">
<div class="two">
 <div class="box"><small>DEBE A</small><b>{F("[Nombre completo]")}</b><br>C.C. {F("[cédula]")}<br>{F("[Dirección o ciudad]")} · {F("[teléfono]")}</div>
 <div class="box"><small>CLIENTE</small><b>{F("[Razón social de Alado]")}</b><br>NIT {F("[NIT]")}</div>
</div>
<h2>Por concepto de</h2>
<p style="margin:0 0 3mm">Servicios de creación de contenido para Alado &amp; Co., campaña de Navidad en la tienda de El Retiro.</p>
<table><thead><tr><th>Servicio</th><th class="num">Cant.</th><th class="num">Valor unit.</th><th class="num">Subtotal</th></tr></thead>
<tbody>{rows}<tr class="tot"><td>Total a pagar</td><td></td><td></td><td class="num">{money(total)}</td></tr></tbody></table>
<div class="words">Son: <b>novecientos cincuenta y seis mil pesos moneda corriente.</b><br>Abonos recibidos: {F("[$ 0]")} · Saldo a pagar: {F("[" + money(total) + "]")}</div>
<h2>Forma de pago</h2>
<div class="pay"><div><small style="color:var(--muted);font-weight:600;letter-spacing:1px;font-size:7pt">BANCO Y TIPO DE CUENTA</small><br>{F("[Banco · ahorros / corriente]")}</div>
<div><small style="color:var(--muted);font-weight:600;letter-spacing:1px;font-size:7pt">NÚMERO DE CUENTA</small><br>{F("[número]")}</div>
<div><small style="color:var(--muted);font-weight:600;letter-spacing:1px;font-size:7pt">TITULAR</small><br>{F("[nombre y cédula]")}</div>
<div><small style="color:var(--muted);font-weight:600;letter-spacing:1px;font-size:7pt">PAGO</small><br>{F("[fecha acordada]")}</div></div>
<div class="sign">{F("[Nombre completo]")}<br>C.C. {F("[cédula]")}</div>
<p class="note">{F("[Confirmar con tu contador antes de enviar:]")} persona natural no responsable de IVA y no obligada a expedir factura de venta.</p>
</div></body></html>"""
(HERE / "_c.html").write_text(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(); await pg.goto(f"file://{(HERE/'_c.html').resolve()}"); await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(OUT), format="A4", print_background=True)
        await b.close()
asyncio.run(main())
print("total", money(total))
