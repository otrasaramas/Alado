import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
FONTS = (HERE.parent/"canva/fonts-tyc.css").read_text()

ROWS = [
 ("0 – 3 s", "andres", "Andrés a cámara · Hook", "Lo que se hace con las manos se queda un poco con uno.", "Sus manos sobre las piezas en blanco. Al terminar la frase, sube la mirada a la cámara."),
 ("3 – 10 s", "andres", "Andrés a cámara · Presentación", "Soy Andrés Restrepo, cofundador y diseñador de Alado, y te invito este 17 de octubre a pintar con nosotros tu propio juego de café para cuatro.", "Plano medio, sentado a la mesa con pinceles y pocillos."),
 ("10 – 16 s", "vo", "Voz en off", "Aprenderás distintas técnicas y pinceladas para crear un patrón a tu gusto, y llevarlo a cada pieza de tu juego de café.", "Manos mostrando pinceladas distintas. Un mismo patrón en un pocillo y en un plato."),
 ("16 – 20 s", "vo", "Voz en off", "Te acompañamos todo el tiempo: aquí nadie pinta solo.", "Alejo o Lizeth inclinándose a ayudar. Una mano que guía a otra."),
 ("20 – 27 s", "vo", "Voz en off", "Será una tarde de risas, conversación y creatividad, con vino, café y algo rico para picar.", "La mesa completa, gente riendo, una copa servida, el café."),
 ("27 – 31 s", "vo", "Voz en off", "Nos vemos en Montesereno, El Retiro, de 2 a 6 de la tarde.", "Paisaje de El Retiro con luz de tarde."),
 ("31 – 39 s", "vo", "Voz en off", "El cupo tiene un valor de 230 mil pesos e incluye la quema de tus piezas, que luego recoges en El Retiro o en Itagüí.", "Piezas terminadas en fila."),
 ("39 – 44 s", "vo", "Voz en off", "Queremos que te sientas en casa: de todo lo demás nos encargamos nosotros.", "Alguien sirviendo vino. Detalle de la mesa puesta."),
 ("44 – 48 s", "andres", "Andrés a cámara · Cierre", "Te esperamos. Reserva tu cupo por WhatsApp.", "Andrés en la mesa, sonríe."),
]
rows = "".join(f'''<tr class="{c}"><td class="t">{t}</td><td><div class="who">{w}</div><div class="line">{l}</div></td><td class="img">{i}</td></tr>''' for t,c,w,l,i in ROWS)
andres = "".join(f'<li>{l}</li>' for t,c,w,l,i in ROWS if c=="andres")
vo = "<br>".join(l for t,c,w,l,i in ROWS if c=="vo")

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Guion · Reel taller de pintura cerámica</title><style>{FONTS}
@page {{ size: A4; margin: 0; }}
:root {{ --paper:#F3F1EA; --ink:#2E3A46; --blue:#5C7891; --line:#C9D2DB; --soft:#E6EAEE; }}
html,body {{ margin:0; background:var(--paper); }}
body {{ font-family:'Archivo'; font-variant-numeric:lining-nums; font-feature-settings:'lnum' 1; color:var(--ink); font-size:9.6pt; line-height:1.38; }}
.page {{ padding:12mm 15mm 10mm; height:297mm; box-sizing:border-box; position:relative; overflow:hidden; page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
header {{ background:var(--blue); color:var(--paper); margin:-12mm -15mm 5mm; padding:9mm 15mm 6mm; }}
.brand {{ font-weight:600; font-size:13pt; margin:0 0 3mm; }}
.kicker {{ font-weight:500; font-size:8pt; letter-spacing:2.2px; margin:0 0 1.5mm; }}
h1 {{ font-family:'Archivo Black'; font-weight:400; font-size:23pt; line-height:.95; margin:0 0 3mm; }}
.meta {{ display:flex; border-top:1px solid rgba(243,241,234,.45); padding-top:3mm; font-weight:600; font-size:9pt; }}
.meta div {{ flex:1; }} .meta div + div {{ border-left:1px solid rgba(243,241,234,.45); padding-left:4mm; }}
.meta small {{ display:block; font-weight:500; font-size:7pt; letter-spacing:1.8px; opacity:.85; }}
table {{ width:100%; border-collapse:collapse; }}
td {{ vertical-align:top; padding:2mm 2.5mm; border-bottom:1px solid var(--line); }}
td.t {{ width:17mm; font-weight:600; font-size:8.5pt; color:var(--blue); white-space:nowrap; }}
td.img {{ width:58mm; font-family:'Archivo'; font-size:8.3pt; color:#5A6672; }}
.who {{ font-weight:600; font-size:7.5pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--blue); margin-bottom:1mm; }}
.line {{ font-family:'Playfair Display'; font-size:11pt; line-height:1.28; }}
tr.andres td {{ background:var(--soft); }}
tr.andres .line {{ font-weight:400; }}
th {{ text-align:left; font-weight:600; font-size:7.5pt; letter-spacing:1.6px; color:#5A6672; padding:0 2.5mm 1.5mm; border-bottom:1.5px solid var(--ink); }}
h2 {{ font-weight:700; font-size:10.5pt; margin:4.5mm 0 2mm; padding-bottom:1.5mm; border-bottom:1px solid var(--line); }}
.screen {{ background:var(--blue); color:var(--paper); padding:4mm 5mm; font-weight:600; font-size:10pt; line-height:1.5; }}
.cols {{ display:flex; gap:8mm; }} .cols > div {{ flex:1; }}
ul {{ margin:0; padding-left:4.5mm; }} li {{ margin:0 0 1.2mm; }}
.big li {{ font-family:'Playfair Display'; font-size:13pt; line-height:1.35; margin-bottom:3mm; }}
.vo {{ font-family:'Playfair Display'; font-size:12.5pt; line-height:1.55; }}
.note {{ font-size:8.5pt; color:#5A6672; }}
</style></head><body>
<div class="page">
<header><p class="brand">Alado &amp; Co.</p><p class="kicker">GUION · REEL DE INVITACIÓN</p><h1>TARDE DE PINTURA CERÁMICA</h1>
<div class="meta"><div><small>FORMATO</small>Reel vertical · unos 48 s</div><div><small>A CÁMARA</small>Andrés Restrepo</div><div><small>VOZ EN OFF</small>Andrés (grabada aparte)</div></div></header>
<table><tr><th>TIEMPO</th><th>QUÉ SE DICE</th><th>QUÉ SE VE</th></tr>{rows}</table>
<h2>Texto en pantalla al cierre</h2>
<div class="screen">Sábado 17 de octubre · 2 – 6 p. m.<br>Montesereno, El Retiro · $230.000<br>Reserva por WhatsApp: 316 533 3125</div>
<p class="note" style="margin-top:3mm">Las filas grises son las que Andrés dice a cámara. El resto es voz en off sobre imágenes del taller.</p>
</div>
<div class="page">
<header><p class="brand">Alado &amp; Co.</p><p class="kicker">GUION · PARA ANDRÉS</p><h1>LO QUE DICES A CÁMARA</h1></header>
<ul class="big">{andres}</ul>
<p class="note">Si la presentación cuesta en una sola toma, se graba en dos partes y se corta después de "Alado". Versión corta: <i>"Soy Andrés, de Alado. Este 17 de octubre te invito a pintar tu propio juego de café."</i></p>
<h2>Voz en off (se graba aparte, de corrido)</h2>
<p class="vo">{vo}</p>
<h2>Para la grabación</h2>
<div class="cols"><div><ul>
<li>Luz natural de lado, cámara a la altura de los ojos, celular en vertical.</li>
<li>Micrófono de solapa. La voz en off, en un cuarto sin eco.</li>
<li>2 o 3 tomas de cada frase. Frases cortas, sin afán.</li></ul></div><div><ul>
<li>El b-roll se prepara antes del taller: mesa montada y 2 o 3 personas pintando.</li>
<li>Música con licencia, suave (jazz o acústica), bajo la voz.</li>
<li>Subtítulos en todo el video.</li></ul></div></div>
</div></body></html>"""
(HERE/"guion.html").write_text(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(); await pg.goto(f"file://{(HERE/'guion.html').resolve()}"); await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(HERE/"guion-reel-taller-andres.pdf"), format="A4", print_background=True)
        await b.close()
asyncio.run(main())
