"""Historia 4 · Invitación (distribución del referente Rimberio). Capas para Canva + PDF editable."""
import asyncio, math
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
FONTS = (HERE.parent / "canva/fonts-ticket.css").read_text()
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
C = {"bg": "#5C7891", "paper": "#F3F1EA", "ink": "#2E3A46", "line": "#8FA3B6", "accent": "#5C7891"}

# Ticket con bordes festoneados arriba y abajo
TX, TW, TY, TH, R = 64, 952, 1120, 560, 14
def ticket_path():
    n = TW // (2*R); d = f"M {TX} {TY}"
    d += f" a {R} {R} 0 0 1 {2*R} 0" * n
    d += f" L {TX+TW} {TY+TH}"
    d += f" a {R} {R} 0 0 1 {-2*R} 0" * n
    return d + " Z"
# Sello festoneado
BX, BY, BR = 838, 905, 165
def seal_path(cx, cy, r, n=30, bump=9):
    pts = []
    for i in range(n*8):
        a = 2*math.pi*i/(n*8); rr = r + bump*abs(math.cos(n*a/2))
        pts.append(f"{cx+rr*math.cos(a):.1f} {cy+rr*math.sin(a):.1f}")
    return "M " + " L ".join(pts) + " Z"

def seal_svg():
    return f'''<svg id="seal" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0">
      <defs><path id="arc" d="M {BX-118} {BY+8} A 118 118 0 0 1 {BX+118} {BY+8}"/></defs>
      <g transform="rotate(-10 {BX} {BY})">
        <path d="{seal_path(BX, BY, BR)}" fill="{C['paper']}"/>
        <circle cx="{BX}" cy="{BY}" r="{BR-16}" fill="none" stroke="{C['ink']}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round" opacity=".6"/>
        <text font-family="Archivo" font-weight="600" font-size="40" fill="{C['ink']}" letter-spacing="1"><textPath href="#arc" startOffset="50%" text-anchor="middle">Pinta tu</textPath></text>
        <g transform="translate({BX-44} {BY-22})" fill="{C['accent']}">
          <path d="M 0 0 H 70 V 34 Q 70 62 42 62 H 28 Q 0 62 0 34 Z"/>
          <path d="M 68 10 Q 96 10 96 28 Q 96 46 66 46" fill="none" stroke="{C['accent']}" stroke-width="9"/>
        </g>
        <text x="{BX}" y="{BY+92}" text-anchor="middle" font-family="Archivo Black" font-size="50" fill="{C['ink']}" letter-spacing="1">VAJILLA</text>
      </g></svg>'''

def page(mode="full"):
    """mode: full (preview) | ph (solo fondo) | seal (solo sello) | pdf (fondo y sello como imagen, resto vivo)"""
    ph = seal = rest = ""
    if mode in ("full", "ph"):
        ph = f'''<svg width="1080" height="1920" style="position:absolute;left:0;top:0">
          <defs><filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="7"/>
          <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.15"/></filter>
          <linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset=".45" stop-color="#000" stop-opacity="0"/></linearGradient></defs>
          <rect width="1080" height="1920" fill="{C['bg']}"/><rect width="1080" height="1920" filter="url(#g)" opacity=".2"/>
          <rect width="1080" height="1920" fill="url(#sh)"/>
          <text x="300" y="920" text-anchor="middle" font-family="Archivo" font-weight="600" font-size="30" letter-spacing="6" fill="{C['paper']}" opacity=".75">TU FOTO DE FONDO</text></svg>'''
    elif mode == "pdf":
        ph = '<img src="capa-fondo-foto.png" style="position:absolute;left:0;top:0;width:1080px;height:1920px">'
    if mode in ("full", "seal"): seal = seal_svg()
    elif mode == "pdf": seal = '<img src="capa-sello.png" style="position:absolute;left:0;top:0;width:1080px;height:1920px">'
    if mode in ("full", "pdf"):
        L = f"position:absolute;margin:0;color:{C['ink']};font-family:Archivo"
        cw = TW/3
        rest = f'''
        <p style="{L};left:64px;top:225px;color:{C['paper']};font-weight:600;font-size:64px;letter-spacing:-1px;line-height:1">Alado &amp; Co.</p>
        <p style="{L};left:66px;top:312px;color:{C['paper']};font-weight:500;font-size:32px;letter-spacing:3px;line-height:1">TE INVITA A UNA TARDE DE</p>
        <p id="title" style="{L};left:56px;top:372px;color:{C['paper']};font-family:'Archivo Black';font-size:170px;line-height:.92;letter-spacing:-2px">PINTURA<br>CERÁMICA</p>
        <svg width="1080" height="1920" style="position:absolute;left:0;top:0">
          <path d="{ticket_path()}" fill="{C['paper']}"/>
          <g stroke="{C['line']}" stroke-width="2">
            <line x1="{TX+cw:.0f}" y1="{TY+50}" x2="{TX+cw:.0f}" y2="{TY+250}"/><line x1="{TX+2*cw:.0f}" y1="{TY+50}" x2="{TX+2*cw:.0f}" y2="{TY+250}"/>
            <line x1="{TX+40}" y1="{TY+290}" x2="{TX+TW-40}" y2="{TY+290}"/><line x1="{TX+40}" y1="{TY+400}" x2="{TX+TW-40}" y2="{TY+400}"/>
            <line x1="{TX+TW/2:.0f}" y1="{TY+420}" x2="{TX+TW/2:.0f}" y2="{TY+530}"/>
          </g></svg>
        <p style="{L};left:{TX}px;width:{cw:.0f}px;top:{TY+124}px;text-align:center;font-weight:600;font-size:46px;letter-spacing:3px;line-height:1">SÁBADO</p>
        <p style="{L};left:{TX+cw:.0f}px;width:{cw:.0f}px;top:{TY+58}px;text-align:center;font-weight:700;font-size:112px;letter-spacing:-2px;line-height:1">17</p>
        <p style="{L};left:{TX+cw:.0f}px;width:{cw:.0f}px;top:{TY+184}px;text-align:center;font-weight:600;font-size:38px;letter-spacing:3px;line-height:1">OCTUBRE</p>
        <p style="{L};left:{TX+2*cw:.0f}px;width:{cw:.0f}px;top:{TY+102}px;text-align:center;font-weight:600;font-size:50px;letter-spacing:0;line-height:1.05">2 – 6<br>P. M.</p>
        <p style="{L};left:{TX}px;width:{TW}px;top:{TY+322}px;text-align:center;font-weight:600;font-size:46px;letter-spacing:0;line-height:1">Montesereno · El Retiro</p>
        <p style="{L};left:{TX}px;width:{TW/2:.0f}px;top:{TY+428}px;text-align:center;font-weight:600;font-size:24px;letter-spacing:3px;line-height:1">POR PERSONA</p>
        <p style="{L};left:{TX}px;width:{TW/2:.0f}px;top:{TY+464}px;text-align:center;font-weight:700;font-size:58px;letter-spacing:-1px;line-height:1">$230.000</p>
        <p style="{L};left:{TX+TW/2:.0f}px;width:{TW/2:.0f}px;top:{TY+428}px;text-align:center;font-weight:600;font-size:22px;letter-spacing:3px;line-height:1">RESERVAS POR WHATSAPP</p>
        <p style="{L};left:{TX+TW/2:.0f}px;width:{TW/2:.0f}px;top:{TY+468}px;text-align:center;font-weight:600;font-size:46px;letter-spacing:0;line-height:1">[número]</p>'''
    bg = C['bg'] if mode == "full" else "transparent"
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FONTS}
      html,body{{margin:0;padding:0;background:transparent}}</style></head>
      <body><div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:{bg}">{ph}{seal}{rest}</div></body></html>'''

FIT = """() => { const t=document.getElementById('title'); if(!t) return 0;
  let s=170; t.style.fontSize=s+'px'; t.style.whiteSpace='nowrap';
  while (t.scrollWidth > 968 && s>80) { s-=1; t.style.fontSize=s+'px'; } return s; }"""

async def shot(b, html, png=None, pdf=None, transparent=False):
    f = OUT/"_tmp.html"; f.write_text(html)
    pg = await b.new_page(viewport={"width":1080,"height":1920})
    await pg.goto(f"file://{f.resolve()}"); await pg.evaluate("document.fonts.ready")
    s = await pg.evaluate(FIT); await pg.wait_for_timeout(200)
    if png: await pg.screenshot(path=str(png), omit_background=transparent)
    if pdf: await pg.pdf(path=str(pdf), width="1080px", height="1920px", print_background=True, page_ranges="1")
    await pg.close(); return s

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        print("title px", await shot(b, page("full"), png=OUT/"preview.png"))
        await shot(b, page("ph"), png=OUT/"capa-fondo-foto.png")
        await shot(b, page("seal"), png=OUT/"capa-sello.png", transparent=True)
        await shot(b, page("pdf"), pdf=OUT/"historia-invitacion.pdf")
        await b.close()
if __name__ == "__main__": asyncio.run(main())
