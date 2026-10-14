# Genera cotizacion-taller-ceramica.xlsx (versión sencilla).
# Uso: python3 build_taller_ceramica.py <salida.xlsx>
# Luego: soffice --headless --calc --convert-to xlsx --outdir <carpeta> <salida.xlsx>
# para guardar los valores calculados (así el archivo muestra cifras en cualquier visor).
import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

OUT = sys.argv[1]
wb = Workbook(); ws = wb.active; ws.title = "Taller cerámica"
for col, w in zip("ABCD", [40, 12, 15, 15]):
    ws.column_dimensions[col].width = w

GREEN = PatternFill("solid", fgColor="1B3A2B"); YEL = PatternFill("solid", fgColor="FFFF00"); TOT = PatternFill("solid", fgColor="EFE6D5")
BOX = Border(*(Side(style="thin"),) * 4)
MONEY = "$#,##0"; NUM = "0"; PCT = "0%"


def cell(ref, value, fmt=None, bold=False, fill=None, color=None, box=True):
    c = ws[ref]; c.value = value; c.font = Font(name="Arial", bold=bold, color=color)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if box: c.border = BOX
    return c


def edit(ref, value, fmt):
    return cell(ref, value, fmt, bold=True, fill=YEL, color="0000FF")


def section(row, text):
    ws.merge_cells(f"A{row}:D{row}")
    cell(f"A{row}", text, bold=True, fill=GREEN, color="FFFFFF", box=False)


cell("A1", "Taller de pintura en cerámica · 17 de octubre", bold=True, box=False).font = Font(name="Arial", bold=True, size=14)
cell("A2", "En casa. Cambia las celdas amarillas y lo demás se calcula solo.", color="555555", box=False)

section(4, "DATOS")
for r, text, value, fmt in [(5, "Personas", 15, NUM), (6, "Precio del cupo", 230000, MONEY), (7, "Piezas de repuesto", 0.2, PCT)]:
    cell(f"A{r}", text, box=False); edit(f"B{r}", value, fmt)

section(9, "GASTOS")
for col, h in zip("ABCD", ["Qué", "Cantidad", "Valor", "Total"]):
    c = cell(f"{col}10", h, bold=True, fill=TOT); c.alignment = Alignment(horizontal="center")
GASTOS = [  # (qué, cantidad, valor; la cantidad en número se puede editar)
    ("Pocillos (con repuesto)", "=ROUNDUP(B5*4*(1+B7),0)", 3200),
    ("Platos (con repuesto)", "=ROUNDUP(B5*4*(1+B7),0)", 2200),
    ("Quema (8 piezas por persona)", "=B5*8", 3000),
    ("Pigmentos", "=B5", 6000),
    ("Materiales (lista de compras)", 1, 250000),
    ("Delantales", "=B5", 20000),
    ("Empaque", "=B5", 2000),
    ("Comida", "=B5", 16000),
    ("Lizeth (horas)", 5, 9000),
    ("Otros: transporte, flores", 1, 190000),
    ("Contenido del taller", 1, 690000),
]
first = 11
for i, (what, qty, value) in enumerate(GASTOS):
    r = first + i
    cell(f"A{r}", what)
    if isinstance(qty, str):
        cell(f"B{r}", qty, NUM)
    else:
        edit(f"B{r}", qty, NUM)
    edit(f"C{r}", value, MONEY)
    cell(f"D{r}", f"=B{r}*C{r}", MONEY)
last = first + len(GASTOS) - 1
tot = last + 1
cell(f"A{tot}", "TOTAL GASTOS", bold=True); cell(f"D{tot}", f"=SUM(D{first}:D{last})", MONEY, bold=True, fill=TOT)

section(tot + 2, "CUENTA")
CUENTA = [
    ("Ingresos (personas × cupo)", "=B5*B6", MONEY, False),
    ("Gastos", f"=D{tot}", MONEY, False),
    ("GANANCIA", f"=B{tot + 3}-B{tot + 4}", MONEY, True),
    ("Ganancia por persona", f"=B{tot + 5}/B5", MONEY, False),
    ("Margen", f"=IF(B{tot + 3}>0,B{tot + 5}/B{tot + 3},0)", PCT, False),
]
for i, (text, f, fmt, strong) in enumerate(CUENTA):
    r = tot + 3 + i
    cell(f"A{r}", text, bold=strong, box=False); cell(f"B{r}", f, fmt, bold=strong, fill=TOT if strong else None)

wb.save(OUT)
