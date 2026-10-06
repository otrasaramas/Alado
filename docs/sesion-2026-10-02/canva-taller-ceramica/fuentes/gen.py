"""Historia 4 · Ventana (referente Cläj). Genera capas PNG, preview, PDF y PPTX para Canva."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
FONTS = (HERE.parent / "canva/fonts-ttf-local.css").read_text()
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

THEMES = {
  "azul":  {"bg": "#5C7891", "fg": "#ECEFF1", "title": "#CFD6DD", "ph1": "#B8B0A3", "ph2": "#8C857A"},
  "crema": {"bg": "#F3F1EA", "fg": "#3D3B37", "title": "#3D3B37", "ph1": "#CFC8BC", "ph2": "#A39C90"},
}
# Vasija en caja 760x800, escalada y centrada
VASE = ("M 280 0 H 480 V 70 C 600 80 740 140 755 300 C 770 440 700 580 590 660 L 590 800 H 170 "
        "L 170 660 C 60 580 -10 440 5 300 C 20 140 160 80 280 70 Z")
S = 0.925; VW, VH = 760*S, 800*S; VX, VY = (1080-VW)/2, 455
VT = f"translate({VX:.1f} {VY}) scale({S})"

def page(theme, layers=("ph","win","text"), img_src=None):
    t = THEMES[theme]
    ph = win = text = ""
    if "ph" in layers:
        if img_src:
            ph = f'<img id="ph" src="{img_src["ph"]}" style="position:absolute;left:{VX:.1f}px;top:{VY}px;width:{VW:.1f}px;height:{VH:.1f}px">'
        else:
            ph = f'''<div id="ph" style="position:absolute;left:{VX:.1f}px;top:{VY}px;width:{VW:.1f}px;height:{VH:.1f}px;
              background:radial-gradient(ellipse at 40% 35%, {t["ph1"]}, {t["ph2"]});display:flex;align-items:center;justify-content:center">
              <span style="font-family:Archivo;font-weight:600;font-size:30px;letter-spacing:6px;color:#F3F1EA;opacity:.85">TU FOTO AQUÍ</span></div>'''
    if "win" in layers:
        if img_src:
            win = f'<img id="win" src="{img_src["win"]}" style="position:absolute;left:0;top:0;width:1080px;height:1920px">'
        else:
            win = f'''<svg id="win" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0">
              <defs>
                <filter id="grain" x="0" y="0" width="100%" height="100%">
                  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" stitchTiles="stitch"/>
                  <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.15"/>
                </filter>
                <filter id="grain2" x="0" y="0" width="100%" height="100%">
                  <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="21" stitchTiles="stitch"/>
                  <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.1"/>
                </filter>
                <mask id="m"><rect width="1080" height="1920" fill="#fff"/><path d="{VASE}" transform="{VT}" fill="#000"/></mask>
              </defs>
              <g mask="url(#m)">
                <rect width="1080" height="1920" fill="{t["bg"]}"/>
                <rect width="1080" height="1920" filter="url(#grain)" opacity="0.22"/>
                <rect width="1080" height="1920" filter="url(#grain2)" opacity="0.22"/>
              </g>
            </svg>'''
    if "text" in layers:
        sm = f'font-family:Archivo;font-weight:500;color:{t["fg"]};letter-spacing:-1.2px;line-height:1.02;margin:0'
        text = f'''
        <div id="t-labels" style="position:absolute;left:64px;top:235px;font-size:40px;{sm}">Fecha<br>Hora<br>Lugar<br>Valor</div>
        <div id="t-values" style="position:absolute;right:64px;top:235px;text-align:right;font-size:40px;{sm}">Sábado 17 de octubre<br>1 – 4 p. m.<br>El Retiro<br>$230.000</div>
        <div id="t-title1" style="position:absolute;left:214px;top:1238px;font-family:'Playfair Display';font-weight:400;font-size:118px;line-height:1;letter-spacing:3px;color:{t["title"]}">PINTURA</div>
        <div id="t-tag" style="position:absolute;left:0;top:1310px;font-family:'Playfair Display';font-style:italic;font-weight:400;font-size:26px;line-height:1;color:{t["title"]}">taller de una tarde</div>
        <div id="t-title2" style="position:absolute;left:214px;top:1356px;font-family:'Playfair Display';font-weight:400;font-size:118px;line-height:1;letter-spacing:3px;color:{t["title"]}">CERÁMICA</div>
        <div id="t-left" style="position:absolute;left:64px;top:1556px;font-size:50px;{sm};letter-spacing:-2px;line-height:.98">TALLER<br>ALADO &amp; CO.</div>
        <div id="t-right" style="position:absolute;right:64px;top:1556px;text-align:right;font-size:50px;{sm};letter-spacing:-2px;line-height:.98">RESERVAS<br>ABIERTAS</div>'''
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FONTS}
      html,body{{margin:0;padding:0;background:transparent;font-variant-numeric:lining-nums}}</style></head>
      <body><div id="root" style="width:1080px;height:1920px;position:relative;overflow:hidden;background:{"transparent" if layers!=("ph","win","text") else THEMES[theme]["bg"]}">
      {ph}{win}{text}</div></body></html>'''

FIX = """() => {
  // centra el bloque del título y pega el tagline a la derecha de PINTURA
  const t1=document.getElementById('t-title1'), t2=document.getElementById('t-title2'), tg=document.getElementById('t-tag');
  if(!t1) return;
  const w=Math.max(t1.offsetWidth,t2.offsetWidth), x=Math.round((1080-w)/2);
  t1.style.left=x+'px'; t2.style.left=x+'px';
  tg.style.left=(x+t1.offsetWidth+18)+'px';
  tg.style.top=(t1.offsetTop+t1.offsetHeight-tg.offsetHeight-22)+'px';
}"""
MEASURE = """() => [...document.querySelectorAll('[id^=t-]')].map(e=>{const r=e.getBoundingClientRect(), cs=getComputedStyle(e);
  return {id:e.id, x:r.left, y:r.top, w:r.width, h:r.height, lines:e.innerText.split('\\n'), size:parseFloat(cs.fontSize),
  family:cs.fontFamily.replace(/['"]/g,''), weight:cs.fontWeight, italic:cs.fontStyle==='italic', align:cs.textAlign,
  spacing:parseFloat(cs.letterSpacing)||0, lh:parseFloat(cs.lineHeight)||parseFloat(cs.fontSize), color:cs.color}})"""

async def shot(b, html, path, transparent=False, pdf=None, measure=False, clip=None):
    f = OUT / "_tmp.html"; f.write_text(html)
    pg = await b.new_page(viewport={"width":1080,"height":1920})
    await pg.goto(f"file://{f.resolve()}"); await pg.evaluate("document.fonts.ready")
    await pg.evaluate(FIX); await pg.wait_for_timeout(300)
    if path: await pg.screenshot(path=str(path), omit_background=transparent, clip=clip)
    if pdf: await pg.pdf(path=str(pdf), width="1080px", height="1920px", print_background=True, page_ranges="1")
    m = await pg.evaluate(MEASURE) if measure else None
    await pg.close(); return m

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for th in THEMES:
            await shot(b, page(th), OUT/f"preview-{th}.png")
            await shot(b, page(th, ("win",)), OUT/f"capa-fondo-ventana-{th}.png", transparent=True)
            await shot(b, page(th, ("ph",)), OUT/f"capa-foto-ejemplo-{th}.png", transparent=True, clip={"x":VX,"y":VY,"width":VW,"height":VH})
        # PDF editable: capas como imágenes + texto real
        for th in THEMES:
            src = {"ph": f"capa-foto-ejemplo-{th}.png", "win": f"capa-fondo-ventana-{th}.png"}
            m = await shot(b, page(th, img_src=src), None, pdf=OUT/f"historia-ventana-{th}.pdf", measure=True)
            (OUT/f"medidas-{th}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
        await b.close()
asyncio.run(main())
