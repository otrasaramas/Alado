import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "cotiz2"))
from data import ITEMS, EVENTS, UNDATED_EXTRA

LINE = {"Bride": "bride", "Alado & Co.": "co", "Alado": "alado"}
FMT = {"Video": "Video", "Carrusel": "Carrusel", "Historias": "Historias", "Pieza gráfica": "Gráfica", "Campaña de fotos": "Fotos"}
entries, undated = [], []
for linea, proy, pieza, fmt, graba, pub, qty, note in ITEMS:
    if fmt == "Gestión de taller": continue
    if "Lilo" in pieza:
        from datetime import timedelta
        for k in range(qty):
            d = pub + timedelta(days=7*k)
            entries.append({"d": d.isoformat(), "k": "pub", "l": LINE[linea], "f": FMT[fmt], "t": f"Lilo · parte {k+1}", "p": proy,
                            "n": "Por confirmar" if k else "Grabada el 6 oct", "tent": k > 0})
        continue
    if pub is None or pub == "asap":
        undated.append({"l": LINE[linea], "f": FMT[fmt], "t": pieza, "p": proy, "n": "Lo antes posible" if pub == "asap" else note})
        continue
    entries.append({"d": pub.isoformat(), "k": "pub", "l": LINE[linea], "f": FMT[fmt], "t": pieza, "p": proy, "n": note, "tent": False})
for d, kind, linea, title in EVENTS:
    entries.append({"d": d.isoformat(), "k": "grab" if kind == "Grabación" else "evento", "l": LINE[linea], "f": "Graba" if kind == "Grabación" else "Evento", "t": title, "p": "", "n": "", "tent": False})
for linea, title, note in UNDATED_EXTRA:
    undated.append({"l": LINE[linea], "f": "Video", "t": title, "p": "", "n": note})
entries.sort(key=lambda e: (e["d"], {"evento": 0, "grab": 1, "pub": 2}[e["k"]]))

tpl = (Path(__file__).parent / "template.html").read_text()
out = tpl.replace("/*DATA*/null", json.dumps({"entries": entries, "undated": undated}, ensure_ascii=False))
(Path(__file__).parent / "calendario-alado.html").write_text(out)
print(len(entries), "entradas,", len(undated), "sin fecha")
