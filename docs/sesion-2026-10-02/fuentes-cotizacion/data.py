"""Fuente única: piezas de Alado Bride y Alado & Co. (oct 2026 – ene 2027)."""
from datetime import date
D = lambda m, d: date(2027 if m == 1 else 2026, m, d)

RATES = [  # formato, tarifa (None = por definir), nota
    ("Video", 200000, "Grabado y editado"),
    ("Carrusel", 170000, ""),
    ("Historias", 120000, "Set de historias"),
    ("Pieza gráfica", 120000, "Por confirmar: hoy igual al set de historias"),
    ("Gestión de taller", None, "Por definir"),
    ("Campaña de fotos", None, "Por definir"),
]

# linea, proyecto, pieza, formato, graba, publica, cantidad, nota
ITEMS = [
 ("Bride", "Alado Bride", "Alejo como artista", "Video", None, None, 1, "Una pieza sobre Alejo"),
 ("Bride", "Alado Bride", "La atención en el taller: Lola y las chicas", "Video", None, None, 1, "Fecha con Andrés"),
 ("Bride", "Alado Bride", "7 claves del vestido perfecto", "Video", None, None, 1, "Con Alejo"),
 ("Bride", "Alado Bride", "7 claves del traje perfecto", "Video", None, None, 1, "Con Alejo"),
 ("Bride", "Alado Bride", "Agenda abierta hasta el 11 de diciembre", "Pieza gráfica", None, D(11,30), 1, ""),
 ("Bride", "Alado Bride", "Notas de Alejo: novias 2027", "Carrusel", None, D(1,5), 1, ""),

 ("Alado & Co.", "Taller de pintura cerámica", "Video promocional con Andrés", "Video", D(10,6), D(10,8), 1, ""),
 ("Alado & Co.", "Taller de pintura cerámica", "Invitación", "Pieza gráfica", None, D(10,7), 1, ""),
 ("Alado & Co.", "Taller de pintura cerámica", "Gestión y organización del taller", "Gestión de taller", None, D(10,17), 1, "Hasta el día del taller"),
 ("Alado & Co.", "Taller de pintura cerámica", "Video del taller", "Video", D(10,17), D(10,19), 1, "Sale 2 días después"),
 ("Alado & Co.", "Grabación de Navidad", "Campaña de fotos de textil hogar", "Campaña de fotos", D(10,22), D(10,27), 1, ""),
 ("Alado & Co.", "Grabación de Navidad", "Video de Navidad", "Video", D(10,22), D(10,29), 1, ""),
 ("Alado & Co.", "Grabación de Navidad", "Video de textil hogar", "Video", D(10,22), D(11,3), 1, ""),
 ("Alado & Co.", "Grabación de Navidad", "Video de la receta", "Video", D(10,22), D(11,21), 1, ""),
 ("Alado & Co.", "La tienda", "Montando la tienda", "Video", D(10,23), D(10,24), 1, ""),
 ("Alado & Co.", "La tela", "Video en el taller de los Pérez", "Video", None, None, 1, "Fecha por confirmar"),
]

# Opcionales del taller de cerámica (cantidad 0: suman solo si no van en gestión)
OPTIONAL = [
 ("Alado & Co.", "Taller de pintura cerámica", "Post de confirmación de cupo", "Pieza gráfica", None, D(10,13), 0, "¿Dentro de gestión o aparte?"),
 ("Alado & Co.", "Taller de pintura cerámica", "Términos y condiciones (PDF)", "Pieza gráfica", None, None, 0, "¿Dentro de gestión o aparte?"),
 ("Alado & Co.", "Taller de pintura cerámica", "Carrusel «Cómo participar» (si se publica)", "Carrusel", None, None, 0, "Hay texto; falta diseño"),
]

# Eventos y grabaciones para el calendario (no cotizados aparte)
EVENTS = [
 (D(10,6), "Grabación", "Alado & Co.", "Video de Andrés para el taller"),
 (D(10,17), "Evento", "Alado & Co.", "Taller de pintura cerámica · Montesereno"),
 (D(10,22), "Grabación", "Alado & Co.", "Día de Navidad: fotos de textil hogar, Navidad, receta"),
 (D(10,23), "Grabación", "Alado & Co.", "Montaje de la tienda en El Retiro"),
 (D(11,27), "Evento", "Alado", "Lanzamiento Alado × Entrelazos y pasarela"),
 (D(12,12), "Evento", "Alado & Co.", "Taller de pintura textil (kimono)"),
]
UNDATED_EXTRA = []
