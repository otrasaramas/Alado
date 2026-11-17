import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
FONTS = (HERE / "inter-local.css").read_text()
OUT = Path(sys.argv[1])
def money(n): return "$" + f"{n:,.0f}".replace(",", ".")
def F(t): return f'<span class="fill">{t}</span>'

NUM = "03"; FECHA_DIA = "17 de noviembre"; FECHA_ANIO = "de 2026"
ITEMS = [  # título, descripción, fecha, cantidad (texto), cant, unitario
 ("Video de la tienda de El Retiro", "Día completo de grabación en El Retiro, edición y entrega", "28/10", "1", 1, 200000),
 ("Video con material de Alado", "Edición, música y texto sobre material suministrado por Alado", "13/11", "1", 1, 140000),
 ("Fotografías de producto", "Sesión en la tienda de El Retiro, selección y corrección de color", "28/10", "124", 124, 4000),
 ("Set de historias de Instagram", "Set producido con fotografías propias y material de Alado", "13/11", "1 set", 1, 120000),
]
total = sum(c * v for *_, c, v in ITEMS)
WORDS = "NOVECIENTOS CINCUENTA Y SEIS MIL PESOS M/CTE"
assert total == 956000
rows = "".join(f'<tr><td class="n">{i}</td><td><div class="t">{t}</div><div class="d">{d}</div></td><td>{f}</td><td class="c">{q}</td><td class="r">{money(v)}</td><td class="r">{money(c*v)}</td></tr>' for i, (t, d, f, q, c, v) in enumerate(ITEMS, 1))

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Cuenta de cobro No. {NUM}</title><style>{FONTS}
@page {{ size: Letter; margin: 0; }}
:root {{ --ink:#1b1b1b; --gray:#6b6762; --rust:#a4452c; --beige:#f5f0eb; --rule:#d9d5d0; }}
html, body {{ margin:0; background:#fff; }}
body {{ font-family:'Inter'; color:var(--ink); font-size:11pt; line-height:1.4; }}
.page {{ padding:9mm 19mm 0; zoom:.89; }}
.top {{ display:flex; justify-content:space-between; align-items:flex-end; padding-bottom:5mm; border-bottom:2px solid var(--ink); }}
h1 {{ margin:0; font-weight:700; font-size:31pt; letter-spacing:.3px; line-height:1; }}
.num small {{ display:block; text-align:right; font-weight:500; font-size:8.5pt; letter-spacing:2px; color:var(--gray); }}
.num b {{ display:block; text-align:right; font-weight:600; font-size:19pt; margin-top:1mm; }}
.date {{ margin:3mm 0 6mm; font-size:12pt; color:var(--gray); }}
.date b {{ font-weight:600; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:9mm; }}
.box {{ background:var(--beige); border-radius:2mm; padding:4mm 6mm 4mm; }}
.box small {{ display:block; color:var(--rust); font-weight:600; font-size:9pt; letter-spacing:1.8px; margin-bottom:2.5mm; }}
.box b {{ display:block; font-weight:600; font-size:14.5pt; }}
.box span {{ font-size:12.5pt; }}
.lead {{ margin:5mm 0 5mm; font-size:11.5pt; line-height:1.5; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ text-align:left; font-weight:500; font-size:8.5pt; letter-spacing:1.5px; color:var(--gray); padding:0 2mm 3mm; border-bottom:2px solid var(--ink); text-transform:uppercase; }}
th.c, td.c {{ text-align:center; }} th.r, td.r {{ text-align:right; white-space:nowrap; }}
td {{ padding:2.4mm 2mm; border-bottom:1px solid var(--rule); vertical-align:top; font-size:11.5pt; }}
td.n {{ color:var(--rust); font-weight:600; width:8mm; }}
.t {{ font-weight:600; font-size:12.5pt; }}
.d {{ color:var(--gray); font-size:10.5pt; margin-top:.8mm; }}
.sum {{ margin:3mm 0 0 auto; width:80mm; }}
.sum .row {{ display:flex; justify-content:space-between; padding:2mm 2mm; font-size:12pt; }}
.sum .tot {{ border-top:2px solid var(--ink); margin-top:3mm; padding-top:4mm; font-weight:700; font-size:15pt; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:9mm; margin-top:5mm; }}
.cols h3 {{ margin:0 0 3mm; color:var(--rust); font-weight:600; font-size:9.5pt; letter-spacing:1.8px; }}
.kv {{ display:grid; grid-template-columns:34mm 1fr; row-gap:1.6mm; font-size:11.5pt; }}
.kv span {{ color:var(--gray); }}
.decl p {{ margin:0 0 2.2mm; color:var(--gray); font-size:10pt; line-height:1.5; }}
.sign {{ margin-top:7mm; }}
.line {{ width:80mm; border-top:1px solid var(--ink); margin-top:9mm; }}
.sign b {{ display:block; font-weight:600; font-size:12.5pt; margin-top:3mm; }}
.sign span {{ display:block; color:var(--gray); font-size:11pt; }}
.fill {{ background:#fbe7a1; padding:0 1mm; }}
</style></head><body><div class="page">
<div class="top"><h1>CUENTA DE COBRO</h1><div class="num"><small>NÚMERO</small><b>No. {NUM}</b></div></div>
<div class="date"><b>{FECHA_DIA}</b> {FECHA_ANIO}</div>
<div class="two">
 <div class="box"><small>COBRAR A</small><b>Alado Diseño S.A.S</b><span>NIT 900290813</span></div>
 <div class="box"><small>DEBE A</small><b>Sara Castrillón Chaparro</b><span>C.C. 1001367866</span></div>
</div>
<p class="lead">La suma de <b>{WORDS} ({money(total)})</b>, por concepto de prestación de servicios de producción de contenido audiovisual y gráfico para la marca Alado, según el siguiente desglose:</p>
<table><thead><tr><th>#</th><th>Descripción</th><th>Fecha</th><th class="c">Cant.</th><th class="r">Valor unit.</th><th class="r">Total</th></tr></thead><tbody>{rows}</tbody></table>
<div class="sum"><div class="row"><span>Subtotal</span><span>{money(total)}</span></div><div class="row tot"><span>Total a pagar</span><span>{money(total)}</span></div></div>
<div class="cols">
 <div><h3>DATOS PARA EL PAGO</h3><div class="kv"><span>Banco</span><div>Bancolombia</div><span>Tipo de cuenta</span><div>Ahorros</div><span>Número</span><div>69300004996</div><span>Titular</span><div>Sara Castrillón Chaparro</div></div>
  <div class="sign">Atentamente,<div class="line"></div><b>Sara Castrillón Chaparro</b><span>C.C 1001367866</span><span>Cel: 3234031224</span></div></div>
 <div class="decl"><h3>DECLARACIONES</h3>
  <p>Manifiesto bajo la gravedad de juramento que no soy responsable del impuesto sobre las ventas (IVA), por cumplir los requisitos del parágrafo 3 del artículo 437 del Estatuto Tributario.</p>
  <p>Por lo anterior, no estoy obligada a expedir factura electrónica de venta.</p>
  <p>Los servicios descritos fueron prestados de manera independiente, sin vínculo laboral.</p></div>
</div>
</div></body></html>"""
(HERE / "_c3.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(); await pg.goto(f"file://{(HERE/'_c3.html').resolve()}"); await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(OUT), format="Letter", print_background=True)
        await b.close()
asyncio.run(main())
print("total", money(total))
