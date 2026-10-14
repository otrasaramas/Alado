# Genera cotizacion-taller-ceramica.xlsx.
# Uso: python3 build_taller_ceramica.py <salida.xlsx>
# Luego: soffice --headless --calc --convert-to xlsx --outdir <carpeta> <salida.xlsx>
# para guardar los valores calculados (así el archivo muestra cifras en cualquier visor).
import sys
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

OUT = sys.argv[1]
wb = Workbook(); ws = wb.active; ws.title = "Taller cerámica"
for col, w in zip("ABCDEFG", [64, 20, 17, 17, 14, 22, 18]):
    ws.column_dimensions[col].width = w

GREEN = PatternFill("solid", fgColor="1B3A2B"); YEL = PatternFill("solid", fgColor="FFFF00"); TOT = PatternFill("solid", fgColor="EFE6D5")
BOX = Border(*(Side(style="thin"),) * 4)
MONEY = "$#,##0"; PCT = "0.0%"; NUM = "0"
GREY = "555555"


def font(**kw):
    return Font(name="Arial", **kw)


def note(row, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    ws.cell(row, 1, text).font = font(size=10, color=GREY)


def section(row, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    c = ws.cell(row, 1, text); c.font = font(bold=True, color="FFFFFF"); c.fill = GREEN


def inp(row, col, value, fmt, center=False):
    c = ws.cell(row, col, value); c.font = font(bold=True, color="0000FF"); c.fill = YEL; c.number_format = fmt; c.border = BOX
    if center:
        c.alignment = Alignment(horizontal="center")
    return c


def out(row, col, value, fmt, bold=False, fill=None):
    c = ws.cell(row, col, value); c.font = font(bold=bold); c.number_format = fmt; c.border = BOX
    if fill:
        c.fill = fill
    return c


def label(row, text, bold=False):
    ws.cell(row, 1, text).font = font(bold=bold)


def header(row, names):
    for j, h in enumerate(names, 1):
        c = ws.cell(row, j, h); c.font = font(bold=True); c.fill = TOT; c.border = BOX; c.alignment = Alignment(horizontal="center")


ws.merge_cells("A1:G1"); ws["A1"] = "Taller de pintura en cerámica · cuenta del taller"; ws["A1"].font = font(bold=True, size=14)
note(2, "Sábado 17 de octubre · 2 – 6 p. m. · Montesereno, El Retiro · esmalte + quema · 18 cupos · actualizada el 14 de octubre")
note(3, "Edita solo las celdas AMARILLAS. Todo lo demás se calcula solo.")

# ---- Datos editables -------------------------------------------------------
section(5, "EDITA ESTO")
INPUTS = [  # (fila, etiqueta, valor, formato, comentario)
    (6, "Personas confirmadas", 15, NUM, "Confirmadas al 14 de octubre. Hay 18 cupos."),
    (7, "Precio del cupo (lo que cobras)", 230000, MONEY, "Precio publicado en los términos."),
    (8, "Margen de ganancia que quieres (sobre ventas)", 0.4, PCT, "Ganancia dividida entre lo que cobras. 40% = de cada $100 cobrados, $40 son ganancia."),
    (9, "Comisión de pago online (0% si es transferencia)", 0, PCT, None),
    (10, "Imprevistos (% de las compras y pagos)", 0.05, PCT, "ESTIMADO. Se aplica a compras y pagos, no al contenido. Pon 0% si no quieres colchón."),
    (11, "Anticipo para separar el cupo", 0.5, PCT, "Según los términos: 50% para separar, el saldo el día del taller."),
    (12, "Pocillos por persona (cantidad)", 4, NUM, None),
    (13, "Precio de 1 pocillo", 3200, MONEY, "Dato de Sara."),
    (14, "Platos por persona (cantidad)", 4, NUM, None),
    (15, "Precio de 1 plato", 2200, MONEY, "Dato de Sara."),
    (16, "Piezas de repuesto (% extra que se compra)", 0.2, PCT, "Por si se dañan o se quiebran. Se redondea hacia arriba."),
    (17, "Quema (por pieza)", 3000, MONEY, "Dato de Sara: taller amigo. Solo se queman las piezas que se lleva cada persona."),
    (18, "Pigmentos (por persona)", 6000, MONEY, "Dato de Sara."),
    (19, "Empaque (por persona)", 2000, MONEY, "ESTIMADO."),
    (20, "Comida en Montesereno (por persona)", 16000, MONEY, "Dato de Sara (aproximado)."),
    (21, "Vino y bebidas, si van aparte de la comida (total)", 0, MONEY, "Si el vino no está incluido en la comida, escribe aquí lo que cueste."),
    (22, "Lizeth · horas", 5, NUM, "Dato de Sara."),
    (23, "Lizeth · valor por hora", 9000, MONEY, "Dato de Sara."),
    (24, "Pinceles, esponjas y materiales (total)", 200000, MONEY, "ESTIMADO. Son reutilizables: en el próximo taller cuestan menos."),
    (25, "Delantales (total)", 120000, MONEY, "ESTIMADO para 12 personas. Reutilizables."),
    (26, "Otros fijos: transporte, flores, promoción (total)", 190000, MONEY, "ESTIMADO."),
    (27, "Alquiler del lugar (total)", 0, MONEY, "Escribe aquí si Montesereno cobra por el espacio."),
    (28, "Contenido del taller (reel, carrusel, historias y recap)", 690000, MONEY, "Pon $0 si no se carga al taller."),
]
for r, text, value, fmt, comment in INPUTS:
    label(r, text)
    c = inp(r, 2, value, fmt)
    if comment:
        c.comment = Comment(comment, "Alado")

# ---- Presupuesto -----------------------------------------------------------
section(30, "PRESUPUESTO: LO QUE HAY QUE COMPRAR Y PAGAR")
header(31, ["Concepto", "Cantidad", "Valor unitario", "Total"])
ROWS = [  # (fila, etiqueta, cantidad, valor unitario)
    (32, "Pocillos (incluye repuesto)", "=ROUNDUP(B6*B12*(1+B16),0)", "=B13"),
    (33, "Platos (incluye repuesto)", "=ROUNDUP(B6*B14*(1+B16),0)", "=B15"),
    (34, "Quema (las piezas que se lleva cada persona)", "=B6*(B12+B14)", "=B17"),
    (36, "Pigmentos", "=B6", "=B18"),
    (37, "Pinceles, esponjas y materiales", 1, "=B24"),
    (38, "Delantales", 1, "=B25"),
    (39, "Empaque", "=B6", "=B19"),
    (41, "Comida en Montesereno", "=B6", "=B20"),
    (42, "Vino y bebidas aparte", 1, "=B21"),
    (43, "Lizeth (horas)", "=B22", "=B23"),
    (44, "Otros: transporte, flores, promoción", 1, "=B26"),
    (45, "Alquiler del lugar", 1, "=B27"),
]
for r, text, qty, unit in ROWS:
    label(r, text)
    out(r, 2, qty, NUM); out(r, 3, unit, MONEY); out(r, 4, f"=B{r}*C{r}", MONEY)
SUBTOTALS = [
    (35, "Subtotal cerámica y quema", "=SUM(D32:D34)"),
    (40, "Subtotal pintura y materiales", "=SUM(D36:D39)"),
    (46, "Subtotal compras y pagos", "=D35+D40+SUM(D41:D45)"),
]
for r, text, f in SUBTOTALS:
    label(r, text, bold=True); out(r, 4, f, MONEY, bold=True, fill=TOT)
ws["A47"] = '="Imprevistos ("&TEXT(B10,"0%")&" de las compras y pagos)"'; ws["A47"].font = font()
out(47, 4, "=D46*B10", MONEY)
label(48, "Contenido del taller"); out(48, 4, "=B28", MONEY)
label(49, "COSTO TOTAL del taller", bold=True); out(49, 4, "=D46+D47+D48", MONEY, bold=True, fill=TOT)

# ---- Resultado -------------------------------------------------------------
section(51, "RESULTADO")
RESULT = [  # (fila, etiqueta, fórmula, formato, destacado)
    (52, "Piezas que se compran (con repuesto)", "=B32+B33", NUM, False),
    (53, "Piezas que se queman", "=B34", NUM, False),
    (54, "Ingresos por cupos (precio × personas)", "=B7*B6", MONEY, False),
    (55, "Comisión de pago online", "=B54*B9", MONEY, False),
    (56, "COSTO TOTAL del taller", "=D49", MONEY, True),
    (57, "Costo por persona", "=B56/B6", MONEY, False),
    (58, "GANANCIA", "=B54-B55-B56", MONEY, True),
    (59, "MARGEN real (ganancia ÷ ingresos)", "=IF(B54>0,B58/B54,0)", PCT, True),
    (60, "Ganancia por persona", "=B58/B6", MONEY, False),
    (61, "¿Cumple el margen que quieres?", '=IF(B59>=B8,"Sí, cumple","No: está por debajo")', "@", False),
    (62, "Ganancia si el contenido no se carga al taller", "=B58+D48", MONEY, False),
    (63, "Margen si el contenido no se carga al taller", "=IF(B54>0,B62/B54,0)", PCT, False),
]
for r, text, f, fmt, strong in RESULT:
    label(r, text, bold=strong); out(r, 2, f, fmt, bold=strong, fill=TOT if strong else None)

section(65, "PLATA QUE ENTRA")
CASH = [
    (66, "Anticipo por persona", "=B7*B11", False),
    (67, "Anticipos (total)", "=B66*B6", True),
    (68, "Saldo por cobrar el día del taller", "=B54-B67", True),
]
for r, text, f, strong in CASH:
    label(r, text, bold=strong); out(r, 2, f, MONEY, bold=strong, fill=TOT if strong else None)

section(70, "CUÁNTO DEBE VALER EL CUPO")
label(71, "Precio mínimo (no pierdes ni ganas)"); out(71, 2, "=B56/(B6*(1-B9))", MONEY)
label(72, "PRECIO RECOMENDADO para tu margen (redondeado a $5.000)", bold=True)
c = out(72, 2, '=IF(1-B9-B8<=0,"Revisa el margen",ROUNDUP(B56/(B6*(1-B9-B8))/5000,0)*5000)', MONEY, bold=True); c.fill = YEL
label(73, "Diferencia con el precio que cobras hoy"); out(73, 2, '=IF(ISNUMBER(B72),B72-B7,"")', MONEY)

section(75, "PUNTO DE EQUILIBRIO")
VAR = "(D32+D33+D34+D36+D39+D41)/B6"   # lo que cuesta cada persona
FIX = "(D37+D38+D42+D43+D44+D45)"      # lo que no cambia con el número de personas
EQ = [
    (76, "Costo variable por persona (cerámica, quema, pintura, comida)", f"={VAR}", MONEY, False),
    (77, "Costos fijos (no cambian con el número de personas)", f"={FIX}", MONEY, False),
    (78, "Aporte de cada cupo a los costos fijos", "=B7*(1-B9)-B76*(1+B10)", MONEY, False),
    (79, "Personas necesarias para no perder", '=IF(B78>0,ROUNDUP((B77*(1+B10)+D48)/B78,0),"No alcanza con este precio")', NUM, True),
    (80, "Personas por encima (+) o por debajo (−) del equilibrio", '=IF(ISNUMBER(B79),B6-B79,"")', NUM, False),
]
for r, text, f, fmt, strong in EQ:
    label(r, text, bold=strong); out(r, 2, f, fmt, bold=strong, fill=TOT if strong else None)

section(82, "PRECIO DEL CUPO SEGÚN EL MARGEN QUE QUIERAS")
header(83, ["Margen", "Precio del cupo", "Ganancia total"])
for r, m in zip(range(84, 88), [0.2, 0.3, 0.4, 0.5]):
    inp(r, 1, m, PCT, center=True)
    out(r, 2, f'=IF(1-$B$9-A{r}<=0,"",ROUNDUP($B$56/($B$6*(1-$B$9-A{r}))/5000,0)*5000)', MONEY)
    out(r, 3, f'=IF(ISNUMBER(B{r}),B{r}*$B$6*(1-$B$9)-$B$56,"")', MONEY)

section(89, "SI CAMBIA EL NÚMERO DE PERSONAS")
header(90, ["Personas", "Ingresos", "Costo total", "Ganancia", "Margen", "Precio para tu margen", "¿Cubre costos?"])
for r, n in zip(range(91, 96), [10, 12, 15, 16, 18]):
    inp(r, 1, n, NUM, center=True)
    out(r, 2, f"=$B$7*A{r}", MONEY)
    cost = (f"=(ROUNDUP(A{r}*$B$12*(1+$B$16),0)*$B$13+ROUNDUP(A{r}*$B$14*(1+$B$16),0)*$B$15"
            f"+A{r}*($B$12+$B$14)*$B$17+A{r}*($B$18+$B$19+$B$20)+$B$21+$B$22*$B$23+$B$24+$B$25+$B$26+$B$27)*(1+$B$10)+$B$28")
    out(r, 3, cost, MONEY)
    out(r, 4, f"=B{r}*(1-$B$9)-C{r}", MONEY)
    out(r, 5, f"=IF(B{r}>0,D{r}/B{r},0)", PCT)
    out(r, 6, f'=IF(1-$B$9-$B$8<=0,"",ROUNDUP(C{r}/(A{r}*(1-$B$9-$B$8))/5000,0)*5000)', MONEY)
    out(r, 7, f'=IF(D{r}>=0,"Sí","No: pierdes")', "@")

note(97, "Repuestos: se compra un % extra de pocillos y platos por si se dañan o se quiebran; solo se queman las piezas que se lleva cada persona.")
note(98, "Pinceles, esponjas y delantales se compran una vez; en los próximos talleres el costo fijo baja. Los datos marcados ESTIMADO no son cotizaciones reales.")

wb.save(OUT)
