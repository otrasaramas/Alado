"""Confirmación de cupo · post de feed 1080x1350, estilo ticket del taller."""
import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "ticket"))
from playwright.async_api import async_playwright
import gen2
from gen2 import C, TX, TW, ticket_path, seal_svg, P, PHOTO

HERE = Path(__file__).parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
FONTS = (HERE.parent / "canva/fonts-tyc.css").read_text()
H = 1350
TY, TH = 392, 880
CW = TW / 3
ACCOUNT = "xxxxx"

def parts():
    items = [
        "Llega a la 1:45 p. m. para empezar puntuales.",
        "Ven con ropa cómoda: los delantales los ponemos nosotros.",
        "Si tienes alguna alergia, cuéntanos antes del taller.",
        "¿Vienes con acompañante? Avísanos con anticipación.",
        "¿No puedes asistir? Cede tu cupo hasta el 16 de octubre.",
        "Tus piezas estarán listas en 2 a 3 semanas.",
    ]
    lines = f'''<svg width="1080" height="{H}" style="position:absolute;left:0;top:0"><path d="{ticket_path(TY, TH)}" fill="{C['paper']}"/>
      <g stroke="{C['line']}" stroke-width="2">
      <line x1="{TX+CW:.0f}" y1="{TY+40}" x2="{TX+CW:.0f}" y2="{TY+195}"/><line x1="{TX+2*CW:.0f}" y1="{TY+40}" x2="{TX+2*CW:.0f}" y2="{TY+195}"/>
      <line x1="{TX+40}" y1="{TY+222}" x2="{TX+TW-40}" y2="{TY+222}"/><line x1="{TX+40}" y1="{TY+310}" x2="{TX+TW-40}" y2="{TY+310}"/>
      <line x1="{TX+40}" y1="{TY+758}" x2="{TX+TW-40}" y2="{TY+758}"/>
      <line x1="{TX+TW/2:.0f}" y1="{TY+778}" x2="{TX+TW/2:.0f}" y2="{TY+858}"/></g></svg>'''
    text = (
        P(64, 62, "Alado &amp; Co.", 40, 600, ls=-.5, color=C['paper']) +
        P(66, 128, "TARDE DE PINTURA CERÁMICA", 24, 500, ls=3, color=C['paper']) +
        P(62, 176, "Tu lugar en la mesa<br>está confirmado.", 76, 400, lh=1.08, color=C['paper'], fam="Playfair Display") +
        P(TX, TY+96, "SÁBADO", 40, 600, CW, "center", 3) +
        P(TX+CW, TY+38, "17", 96, 700, CW, "center", -2) +
        P(TX+CW, TY+146, "OCTUBRE", 32, 600, CW, "center", 3) +
        P(TX+2*CW, TY+74, "2 – 6<br>P. M.", 44, 600, CW, "center", 0, 1.05) +
        P(TX, TY+246, "Montesereno · El Retiro", 40, 600, TW, "center") +
        P(TX, TY+338, "PARA TENER EN CUENTA", 22, 600, TW, "center", 3)
    )
    for i, it in enumerate(items):
        y = TY + 386 + i * 60
        text += P(TX+48, y, f"{i+1:02d}", 30, 400, color=C['accent'], fam="Archivo Black")
        text += P(TX+128, y+2, it, 28, 500, ls=-.3, fit=TW-176)
    text += (
        P(TX, TY+784, "SALDO · EL DÍA DEL TALLER", 20, 600, TW/2, "center", 2.5) +
        P(TX, TY+814, "$115.000", 48, 700, TW/2, "center", -1) +
        P(TX+TW/2, TY+784, "TRANSFERENCIA A LA CUENTA", 20, 600, TW/2, "center", 2.5) +
        P(TX+TW/2, TY+814, ACCOUNT, 48, 700, TW/2, "center", -.5) +
        P(0, 1300, "¿Preguntas? Escríbenos por WhatsApp al 316 533 3125", 22, 500, 1080, "center", .3, color=C['paper'])
    )
    seal = seal_svg(878, 232, 112, "Nos vemos el", "17 OCT", rot=8, tsize=27).replace('height="1920" viewBox="0 0 1080 1920"', f'height="{H}" viewBox="0 0 1080 {H}"')
    return {"ticket": lines, "seal": seal, "text": text}

def html(layers, fonts=FONTS):
    p = parts(); body = ""
    for k in ("photo", "ticket", "seal", "text"):
        if k not in layers: continue
        v = layers[k]
        body += v if isinstance(v, str) and v.startswith("<img") else (PHOTO if k == "photo" else p[k])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{fonts}
      html,body{{margin:0;padding:0;background:transparent;font-variant-numeric:lining-nums}}</style></head>
      <body><div style="width:1080px;height:{H}px;position:relative;overflow:hidden">{body}</div></body></html>'''

async def shot(b, doc, png=None, pdf=None, transparent=True):
    f = OUT/"_tmp.html"; f.write_text(doc)
    pg = await b.new_page(viewport={"width":1080,"height":H})
    await pg.goto(f"file://{f.resolve()}"); await pg.evaluate("document.fonts.ready"); await pg.evaluate(gen2.FIT); await pg.wait_for_timeout(200)
    if png: await pg.screenshot(path=str(png), omit_background=transparent)
    if pdf: await pg.pdf(path=str(pdf), width="1080px", height=f"{H}px", print_background=True, page_ranges="1")
    sizes = await pg.evaluate("() => [...document.querySelectorAll('[data-fit]')].map(e => e.style.fontSize)")
    await pg.close(); return sizes

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        sizes = await shot(b, html({"photo":1,"ticket":1,"seal":1,"text":1}), png=OUT/"confirmacion-cupo.png", transparent=False)
        await shot(b, html({"photo":1}), png=OUT/"capa-fondo.png", transparent=False)
        await shot(b, html({"seal":1}), png=OUT/"capa-sello.png")
        img = lambda n: f'<img src="{n}" style="position:absolute;left:0;top:0;width:1080px;height:{H}px">'
        await shot(b, html({"photo":img("capa-fondo.png"),"ticket":1,"seal":img("capa-sello.png"),"text":1}), pdf=OUT/"confirmacion-cupo.pdf")
        await b.close()
    (OUT/"fit.json").write_text(json.dumps(sizes)); print("fit", sizes)

if __name__ == "__main__": asyncio.run(main())
