"""Historias del taller, estilo ticket: 1 Invitación, 2 Qué incluye. PDF (2 pág.) + PPTX + capas."""
import asyncio, json, math, re
from pathlib import Path
from playwright.async_api import async_playwright
import pymupdf

HERE = Path(__file__).parent
FONTS = (HERE.parent / "canva/fonts-ticket.css").read_text()
OUT = HERE / "out2"; OUT.mkdir(exist_ok=True)
C = {"bg": "#5C7891", "paper": "#F3F1EA", "ink": "#2E3A46", "line": "#8FA3B6", "accent": "#5C7891"}
TX, TW, R = 64, 952, 14

def ticket_path(ty, th):
    n = TW // (2*R)
    return (f"M {TX} {ty}" + f" a {R} {R} 0 0 1 {2*R} 0"*n + f" L {TX+TW} {ty+th}" + f" a {R} {R} 0 0 1 {-2*R} 0"*n + " Z")

def seal_svg(bx, by, br, top, bottom, rot=-10, tsize=40):
    pts = []
    n = 30
    for i in range(n*8):
        a = 2*math.pi*i/(n*8); rr = br + 9*abs(math.cos(n*a/2))
        pts.append(f"{bx+rr*math.cos(a):.1f} {by+rr*math.sin(a):.1f}")
    k = br/165; ar = 118*k
    return f'''<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0">
      <defs><path id="arc" d="M {bx-ar:.1f} {by+8*k:.1f} A {ar:.1f} {ar:.1f} 0 0 1 {bx+ar:.1f} {by+8*k:.1f}"/></defs>
      <g transform="rotate({rot} {bx} {by})">
        <path d="M {' L '.join(pts)} Z" fill="{C['paper']}"/>
        <circle cx="{bx}" cy="{by}" r="{br-16}" fill="none" stroke="{C['ink']}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round" opacity=".6"/>
        <text font-family="Archivo" font-weight="600" font-size="{tsize*k:.0f}" fill="{C['ink']}" letter-spacing="1"><textPath href="#arc" startOffset="50%" text-anchor="middle">{top}</textPath></text>
        <g transform="translate({bx-44*k:.1f} {by-22*k:.1f}) scale({k:.3f})" fill="{C['accent']}">
          <path d="M 0 0 H 70 V 34 Q 70 62 42 62 H 28 Q 0 62 0 34 Z"/>
          <path d="M 68 10 Q 96 10 96 28 Q 96 46 66 46" fill="none" stroke="{C['accent']}" stroke-width="9"/></g>
        <text x="{bx}" y="{by+92*k:.1f}" text-anchor="middle" font-family="Archivo Black" font-size="{50*k:.0f}" fill="{C['ink']}" letter-spacing="1">{bottom}</text>
      </g></svg>'''

PHOTO = f'''<svg width="1080" height="1920" style="position:absolute;left:0;top:0">
  <defs><filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="7"/>
  <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.15"/></filter>
  <linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset=".45" stop-color="#000" stop-opacity="0"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="{C['bg']}"/><rect width="1080" height="1920" filter="url(#g)" opacity=".2"/>
  <rect width="1080" height="1920" fill="url(#sh)"/></svg>'''

L = f"position:absolute;margin:0;color:{C['ink']};font-family:Archivo;white-space:nowrap"
def P(x, y, txt, size, weight=600, w=None, align="left", ls=0, lh=1, color=None, fam=None, fit=None):
    st = f"{L};left:{x:.0f}px;top:{y:.0f}px;font-weight:{weight};font-size:{size}px;letter-spacing:{ls}px;line-height:{lh};text-align:{align}"
    if w: st += f";width:{w:.0f}px"
    if color: st += f";color:{color}"
    if fam: st += f";font-family:'{fam}'"
    return f'<p class="t"{f" data-fit={fit}" if fit else ""} style="{st}">{txt}</p>'

def header(sub, title):
    return (P(64, 225, "Alado &amp; Co.", 64, 600, ls=-1, color=C['paper']) +
            P(66, 312, sub, 32, 500, ls=3, color=C['paper']) +
            P(56, 372, title, 170, 400, ls=-2, lh=.92, color=C['paper'], fam="Archivo Black", fit=968))

def page1():
    TY, TH = 1000, 690; cw = TW/3
    lines = f'''<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><path d="{ticket_path(TY,TH)}" fill="{C['paper']}"/>
      <g stroke="{C['line']}" stroke-width="2">
      <line x1="{TX+cw:.0f}" y1="{TY+50}" x2="{TX+cw:.0f}" y2="{TY+250}"/><line x1="{TX+2*cw:.0f}" y1="{TY+50}" x2="{TX+2*cw:.0f}" y2="{TY+250}"/>
      <line x1="{TX+40}" y1="{TY+290}" x2="{TX+TW-40}" y2="{TY+290}"/><line x1="{TX+40}" y1="{TY+400}" x2="{TX+TW-40}" y2="{TY+400}"/>
      <line x1="{TX+40}" y1="{TY+540}" x2="{TX+TW-40}" y2="{TY+540}"/>
      <line x1="{TX+TW/2:.0f}" y1="{TY+560}" x2="{TX+TW/2:.0f}" y2="{TY+660}"/></g></svg>'''
    text = (header("TE INVITA A UNA TARDE DE", "PINTURA<br>CERÁMICA") +
        P(64, 712, "Pinta tu propio juego<br>de café para cuatro", 44, 600, ls=-.5, lh=1.15, color=C['paper']) +
        P(TX, TY+124, "SÁBADO", 46, 600, cw, "center", 3) +
        P(TX+cw, TY+58, "17", 112, 700, cw, "center", -2) +
        P(TX+cw, TY+184, "OCTUBRE", 38, 600, cw, "center", 3) +
        P(TX+2*cw, TY+102, "2 – 6<br>P. M.", 50, 600, cw, "center", 0, 1.05) +
        P(TX, TY+322, "Montesereno · El Retiro", 46, 600, TW, "center") +
        P(TX, TY+426, "INCLUYE", 22, 600, TW, "center", 3) +
        P(TX, TY+462, "Materiales, quema, vino, café y pasabocas", 38, 600, TW, "center", -.3) +
        P(TX, TY+568, "POR PERSONA", 22, 600, TW/2, "center", 3) +
        P(TX, TY+600, "$230.000", 54, 700, TW/2, "center", -1) +
        P(TX+TW/2, TY+568, "RESERVAS POR WHATSAPP", 22, 600, TW/2, "center", 3) +
        P(TX+TW/2, TY+604, "[número]", 44, 600, TW/2, "center"))
    return {"ticket": lines, "seal": seal_svg(850, 870, 150, "Pinta tu", "VAJILLA"), "text": text}

def page2():
    TY, TH = 760, 860
    items = ["4 pocillos y 4 platos para pintar", "Pigmentos, pinceles y materiales", "La quema de tus piezas",
             "Te acompañan Andrés, Alejo y Lizeth", "Vino, café y pasabocas para la tarde"]
    rows = 118; y0 = TY + 40
    ln = "".join(f'<line x1="{TX+40}" y1="{y0+rows*(i+1)}" x2="{TX+TW-40}" y2="{y0+rows*(i+1)}"/>' for i in range(len(items)))
    yb = y0 + rows*len(items)
    lines = f'''<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><path d="{ticket_path(TY,TH)}" fill="{C['paper']}"/>
      <g stroke="{C['line']}" stroke-width="2">{ln}<line x1="{TX+TW/2:.0f}" y1="{yb+24}" x2="{TX+TW/2:.0f}" y2="{TY+TH-34}"/></g></svg>'''
    text = header("TU TARDE DE TALLER", "¿QUÉ<br>INCLUYE?")
    for i, it in enumerate(items):
        y = y0 + rows*i + 36
        text += P(TX+40, y-2, f"{i+1:02d}", 44, 400, ls=0, color=C['accent'], fam="Archivo Black")
        ph = it.startswith("[")
        text += P(TX+150, y, it, 40, 500 if ph else 600, ls=-.5, color="#6B7480" if ph else None, fit=TW-190)
    text += (P(TX, yb+40, "SÁBADO 17 DE OCTUBRE", 26, 600, TW/2, "center", 2) +
             P(TX, yb+82, "2 – 6 P. M.", 54, 700, TW/2, "center", -1) +
             P(TX+TW/2, yb+40, "POR PERSONA", 26, 600, TW/2, "center", 3) +
             P(TX+TW/2, yb+82, "$230.000", 54, 700, TW/2, "center", -1))
    return {"ticket": lines, "seal": seal_svg(842, 372, 140, "Te llevas tu", "VAJILLA", rot=8, tsize=31), "text": text}

def html(parts, layers):
    body = ""
    for k in ("photo", "ticket", "seal", "text"):
        if k not in layers: continue
        v = layers[k]
        body += v if isinstance(v, str) and v.startswith("<img") else (PHOTO if k == "photo" else parts[k])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FONTS}
      html,body{{margin:0;padding:0;background:transparent}}</style></head>
      <body><div style="width:1080px;height:1920px;position:relative;overflow:hidden">{body}</div></body></html>'''

FIT = """() => document.querySelectorAll('[data-fit]').forEach(t => { const max=+t.dataset.fit;
  let s=parseFloat(getComputedStyle(t).fontSize); while (t.scrollWidth > max && s > 20) { s -= 1; t.style.fontSize = s+'px'; } })"""
MEASURE = """() => [...document.querySelectorAll('p.t')].map(e=>{const r=e.getBoundingClientRect(), cs=getComputedStyle(e);
  return {x:r.left, y:r.top, w:r.width, h:r.height, lines:e.innerText.split('\\n'), size:parseFloat(cs.fontSize),
  family:cs.fontFamily.split(',')[0].replace(/['"]/g,''), weight:+cs.fontWeight, align:cs.textAlign,
  spacing:parseFloat(cs.letterSpacing)||0, lh:parseFloat(cs.lineHeight)||parseFloat(cs.fontSize), color:cs.color}})"""

async def shot(b, doc, png=None, pdf=None, transparent=True, measure=False):
    f = OUT/"_tmp.html"; f.write_text(doc)
    pg = await b.new_page(viewport={"width":1080,"height":1920})
    await pg.goto(f"file://{f.resolve()}"); await pg.evaluate("document.fonts.ready"); await pg.evaluate(FIT); await pg.wait_for_timeout(200)
    if png: await pg.screenshot(path=str(png), omit_background=transparent)
    if pdf: await pg.pdf(path=str(pdf), width="1080px", height="1920px", print_background=True, page_ranges="1")
    m = await pg.evaluate(MEASURE) if measure else None
    await pg.close(); return m

async def main():
    pages = {"1-invitacion": page1(), "2-que-incluye": page2()}
    meas = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for name, parts in pages.items():
            await shot(b, html(parts, {"photo":1,"ticket":1,"seal":1,"text":1}), png=OUT/f"preview-{name}.png", transparent=False)
            await shot(b, html(parts, {"photo":1}), png=OUT/f"capa-fondo-{name}.png", transparent=False)
            await shot(b, html(parts, {"ticket":1}), png=OUT/f"capa-ticket-{name}.png")
            await shot(b, html(parts, {"seal":1}), png=OUT/f"capa-sello-{name}.png")
            imgs = {k: f'<img src="capa-{k2}-{name}.png" style="position:absolute;left:0;top:0;width:1080px;height:1920px">' for k, k2 in (("photo","fondo"),("seal","sello"))}
            meas[name] = await shot(b, html(parts, {"photo":imgs["photo"],"ticket":1,"seal":imgs["seal"],"text":1}), pdf=OUT/f"_{name}.pdf", measure=True)
        await b.close()
    doc = pymupdf.open()
    for name in pages: doc.insert_pdf(pymupdf.open(OUT/f"_{name}.pdf"))
    doc.save(OUT/"historias-taller-ceramica.pdf", garbage=3, deflate=True)
    (OUT/"medidas.json").write_text(json.dumps(meas, ensure_ascii=False, indent=1))

if __name__ == "__main__": asyncio.run(main())
