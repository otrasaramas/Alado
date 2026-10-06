import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
FONTS = (HERE.parent/"canva/fonts-tyc.css").read_text()

def F(t): return f'<span class="fill">{t}</span>'   # dato por completar

SECTIONS = [
 ("Qué incluye", f"""<ul>
  <li>4 pocillos y 4 platos para pintar: tu juego de café para cuatro.</li>
  <li>Pigmentos, pinceles, materiales y delantal.</li>
  <li>Guía y acompañamiento de Andrés, Alejo y Lizeth durante toda la tarde.</li>
  <li>La quema de tus piezas.</li>
  <li>Vino, café, bebidas sin alcohol y bocados para la tarde (no es un almuerzo).</li>
  <li>Parqueadero y espacio cubierto.</li></ul>
  <p>Llega a las 2:00 p. m. para empezar a tiempo y ven con ropa cómoda.</p>"""),
 ("Valor y reserva", f"""<p>El valor del taller es de <b>$230.000 por persona</b>. Tu cupo queda separado cuando recibimos el anticipo del <b>50% ($115.000)</b> y nos envías el comprobante por WhatsApp. El saldo de $115.000 se paga el día del taller.</p>
  <p>Hay 18 cupos y se asignan en orden de pago.</p>"""),
 ("Cancelación y cambio de nombre", f"""<p>Las piezas y los materiales se compran para cada participante. Por eso, si cancelas tu asistencia, te devolvemos el <b>80% del valor pagado</b>.</p>
  <p>Si no puedes asistir, también puedes <b>ceder tu cupo a otra persona</b>. Solo avísanos su nombre hasta el viernes 16 de octubre.</p>
  <p>Si por fuerza mayor Alado debe cancelar o cambiar la fecha, te proponemos una nueva fecha o te devolvemos el 100% de lo pagado.</p>"""),
 ("Alergias y alimentación", """<p>Te agradecemos contarnos al reservar si tienes alguna alergia o restricción alimentaria, para tenerla en cuenta.</p>"""),
 ("Acompañantes", """<p>Cada participante puede venir con <b>un (1) acompañante</b>. El acompañante asiste como invitado: no participa en la actividad de pintura ni en el servicio de alimentos y bebidas incluido en el taller.</p>"""),
 ("Edad mínima", """<p>La edad mínima para participar es de <b>13 años</b>. Los menores de edad asisten con un adulto responsable y no consumen bebidas alcohólicas.</p>"""),
 ("La cerámica es un proceso incierto", """<p>En la quema, la cerámica tiene vida propia: los colores pueden cambiar de tono y una pieza puede agrietarse o romperse. No podemos garantizar el resultado de cada pieza después de la quema.</p>
  <p>Tendremos algunas piezas de repuesto en la mesa por si alguna se daña durante la tarde o no sale como esperabas.</p>"""),
 ("Entrega de las piezas", f"""<p>Después del taller llevamos tus piezas a la quema. Te avisamos por WhatsApp cuando estén listas, <b>aproximadamente 2 a 3 semanas después del taller</b>. Puedes recogerlas en:</p>
  <ul><li><b>Taller Alado</b>, en Itagüí.</li><li><b>Tienda Alado</b>, en El Retiro.</li></ul>
  <p>Te enviamos la dirección y el horario con el aviso.</p>"""),
 ("Fotos y video", """<p>Durante la tarde tomaremos fotos y video para las redes de Alado. Si prefieres no aparecer, cuéntanos y lo respetamos.</p>"""),
]

sec = [f'<section><h2><span class="n">{i:02d}</span>{t}</h2>{b}</section>' for i,(t,b) in enumerate(SECTIONS,1)]
secs = '<div class="col">' + "".join(sec[:4]) + '</div><div class="col">' + "".join(sec[4:]) + '</div>'
html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Términos y condiciones · Tarde de pintura cerámica</title><style>{FONTS}
@page {{ size: A4; margin: 0; }}
:root {{ --paper:#F3F1EA; --ink:#2E3A46; --blue:#5C7891; --line:#C9D2DB; }}
html,body {{ margin:0; background:var(--paper); }}
body {{ font-family:'Archivo'; font-weight:400; color:var(--ink); font-size:9.6pt; line-height:1.38; }}
.page {{ padding: 14mm 17mm 8mm; position:relative; height:297mm; box-sizing:border-box; overflow:hidden; }}
header {{ background:var(--blue); color:var(--paper); margin:-14mm -17mm 6mm; padding:11mm 17mm 7mm; }}
.brand {{ font-weight:600; font-size:14pt; letter-spacing:-.3px; margin:0 0 3mm; }}
.kicker {{ font-weight:500; font-size:8.5pt; letter-spacing:2.2px; margin:0 0 1.5mm; }}
h1 {{ font-family:'Archivo Black'; font-weight:400; font-size:25pt; line-height:.95; letter-spacing:-.5px; margin:0 0 3.5mm; }}
.meta {{ display:flex; gap:0; border-top:1px solid rgba(243,241,234,.45); padding-top:3.5mm; font-weight:600; font-size:10pt; }}
.meta div {{ flex:1; }} .meta div + div {{ border-left:1px solid rgba(243,241,234,.45); padding-left:4mm; }}
.meta small {{ display:block; font-weight:500; font-size:7.5pt; letter-spacing:1.8px; opacity:.85; margin-bottom:.6mm; }}
.intro {{ font-family:'Playfair Display'; font-style:italic; font-size:11pt; line-height:1.35; margin:0 0 4.5mm; }}
.cols {{ display:flex; gap:9mm; }} .col {{ flex:1; }}
section {{ margin:0 0 3.2mm; }}
h2 {{ font-weight:700; font-size:10.5pt; letter-spacing:.2px; margin:0 0 1.5mm; padding-bottom:1.5mm; border-bottom:1px solid var(--line); }}
h2 .n {{ font-family:'Archivo Black'; font-weight:400; color:var(--blue); margin-right:2.5mm; }}
p {{ margin:0 0 1.8mm; }} ul {{ margin:0 0 1.8mm; padding-left:4.5mm; }} li {{ margin:0 0 .8mm; }} b {{ font-weight:600; }}
.fill {{ background:#FBE7A1; padding:0 1mm; }}
footer {{ position:absolute; left:17mm; right:17mm; bottom:9mm; border-top:1px solid var(--line); padding-top:3.5mm; display:flex; justify-content:space-between; align-items:flex-end; font-size:9pt; }}
footer .ok {{ max-width:110mm; }}
footer .sig {{ font-weight:600; text-align:right; }}
</style></head><body><div class="page">
<header>
 <p class="brand">Alado &amp; Co.</p>
 <p class="kicker">TÉRMINOS Y CONDICIONES</p>
 <h1>TARDE DE PINTURA<br>CERÁMICA</h1>
 <div class="meta"><div><small>FECHA</small>Sábado 17 de octubre de 2026</div><div><small>HORA</small>2:00 – 6:00 p. m.</div><div><small>LUGAR</small>Montesereno, El Retiro</div></div>
</header>
<p class="intro">Gracias por reservar tu cupo. Esto es lo que necesitas saber para disfrutar la tarde.</p>
<div class="cols">{secs}</div>
<footer><div class="ok">Al pagar el anticipo aceptas estas condiciones. Si tienes cualquier pregunta, escríbenos por WhatsApp al <b>316 533 3125</b>.</div><div class="sig">Te esperamos.<br>Alado &amp; Co.</div></footer>
</div></body></html>"""
(HERE/"tyc.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page()
        await pg.goto(f"file://{(HERE/'tyc.html').resolve()}"); await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(HERE/"terminos-taller-pintura-ceramica.pdf"), format="A4", print_background=True)
        await b.close()
asyncio.run(main())
