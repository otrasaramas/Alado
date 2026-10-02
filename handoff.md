# Handoff — Sesión Alado

> Resumen para retomar el trabajo en otra sesión. Fecha de cierre: **2026-10-02**.

## 1. Objetivo
Construir el **cerebro de marca de Alado** para el Codex de Andrés y la **estrategia de contenido** (redes, Navidad y Bride), y **consolidar todo en el repositorio `otrasaramas/alado`**.

## 2. Estado en el que termina esta sesión
- **Cerebro de marca v3.0 — COMPLETO y consolidado** en `otrasaramas/alado`. Integra ADN, tono de voz, arquetipo (Creador/Sabio-mentor), personas de cliente, ecosistema digital/recorrido de venta, y la investigación del portafolio (colecciones, método, identidad visual, línea de hogar).
- **Export condensado para Codex listo:** `docs/ALADO-CODEX.md`.
- **Estrategia de contenido lista:** redes (Bride + sostenimiento), Navidad (3 drops), 30 ideas de reels y plan semanal de Bride.
- **Todo movido a `otrasaramas/alado`** y **borrado de `pendientes-bot1`**.
- Quedan solo pulidos menores (ver próximos pasos).

## 3. Archivos y cambios

**En `otrasaramas/alado` (rama `main`):**
- `docs/ALADO-CODEX.md` — **export condensado para pegar en Codex** (empezar por aquí).
- `docs/cerebro-de-marca.md` — cerebro de marca extenso (v3.0).
- `docs/estrategia-redes.md` — estrategia de Instagram (campaña Bride hasta el 12 dic + sostenimiento general).
- `docs/estrategia-navidad-y-bride.md` — Navidad (3 drops, calendario, 30 reels), plan semanal de Bride.
- `docs/assets/` — guía de rodaje backstage + sticker de ruta a la tienda (png/svg).
- `README.md` y `CLAUDE.md` — actualizados para apuntar primero al Codex.
- (Ya existían, de otra sesión) `docs/alado-portafolio.md` + 337 imágenes + `docs/alado-imagenes.csv` + `docs/textos-fuente/` — catálogo visual / investigación del portafolio.

**En `otrasaramas/pendientes-bot1` (rama `claude/nice-cerf-3zlu1w`):**
- **Eliminados** los 6 archivos de Alado que estaban ahí (cerebro, resumen ChatGPT, estrategia, guía de rodaje, sticker png/svg). Solo quedaron los archivos propios del bot (`index.js`, `Procfile`, etc.), que no son de Alado.

## 4. Intentos fallidos / fricciones
- **Red restringida:** el entorno bloquea sitios externos. No se pudo abrir el **portafolio Wix** ni los **links de prensa**. *Workaround:* Sara subió imágenes al chat, y la investigación completa se encontró ya hecha en el repo `otrasaramas/alado`.
- **Confusión de repositorios:** `pendientes-bot1` se renombró/movió a `sara-general` (su `main` sigue en un commit de julio). El trabajo de Alado **no** estaba ahí: estaba en un repo aparte, `otrasaramas/alado`, ubicado con `list_repos`.
- **Rama `claude/fervent-cannon-6ta0ww`:** nunca estuvo publicada en el remoto esperado; el contenido vivía en `otrasaramas/alado` (main).
- **SVG→PNG:** no había convertidor instalado; se instaló `cairosvg` para generar el sticker.
- **Push intermitente:** un push falló por el proxy de git caído temporalmente; se resolvió al reintentar.

## 5. Próximos pasos
- **Pulir el cerebro de marca:** códigos hex exactos de la paleta, nombres de las tipografías, y **vetar la lista de palabras "que ama" Alado** (quedó pendiente de Sara).
- **Guiones de reels:** desarrollar plano por plano los prioritarios — "La casa se viste de Navidad", "Bodegón que cobra vida", "Regala Alado"; y el reel de la tienda (23 oct).
- **Bride:** armar el contenido del **Destacado fijo "Bride"** (proceso · vestidos · cómo agendar).
- **Taller de cerámica (17 oct):** definir modalidad (**pintura en frío vs. esmalte+quema**) y cupos; se ofreció una **hoja de cálculo de cotización** con fórmulas (pendiente de hacer).
- **Producción de Navidad:** grabar el **16 oct** (fotos + b-roll de los 3 drops) y el **23 oct** (reel de la tienda vestida). **Pre-producir y PROGRAMAR los reels evergreen antes del 12 dic**, porque el equipo está de vacaciones del **12 dic al 12 ene** — ese contenido debe llevar a la **web (Shopify)**, sin depender del equipo.

---
*Punto de entrada para la próxima sesión: `docs/ALADO-CODEX.md` (marca) y `docs/estrategia-navidad-y-bride.md` (contenido inmediato).*

---
## Actualización 2026-10-02 (sesión de 4 tareas)
- **Hecho:** cotización del taller de cerámica (Excel simple), estrategia de Bride (privacidad, figurín enmarcado, escalera de voz de Alejo, tendencias con criterio) y plan de contenido 5 oct → 1 dic con presupuesto.
- **Decisión tomada:** Alado sí habla de tendencias, con criterio propio (Alejo); ya está en `docs/cerebro-de-marca.md` y `docs/ALADO-CODEX.md`.
- **Corrección:** las vacaciones son del **12 dic al 12 ene** (antes decía 11).
- **Archivos nuevos en `docs/sesion-2026-10-02/`:** `05-plan-contenido-oct-dic.md`, `presupuesto-contenido-oct-dic.xlsx`, `datos-presentacion-contenido.json` (base para la presentación en artifact).
- **Pendiente:** Tarea 3 (contenido Alado ropa), Tarea 4 (guion de invitación al taller, P02 del plan), confirmar tarifa de historias y los estimados de gastos reembolsables, y construir la presentación a partir del JSON.

## Presentación (2026-10-03)
- Deck de la propuesta para Andrés y Alejo (18 diapositivas, estética Alado): https://claude.ai/artifact/2vozp4t8Th8AHpuqBa5ypx (privado hasta que Sara lo comparta).
- Se construyó con el calendario final de `docs/sesion-2026-10-02/datos-presentacion-contenido.json`: 13 reels, 5 carruseles, 8 sets de historias; opciones $2.910.000 / $4.920.000 / $6.060.000.
- Por confirmar antes de presentar: tarifa de sets de historias ($180.000) y los gastos reembolsables estimados ($640.000).
