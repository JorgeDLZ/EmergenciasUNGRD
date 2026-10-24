# Epic 02: Etapa 1 — Interfaz completa con datos de ejemplo

> Al terminar este epic el sitio tiene todas sus páginas: guía de estilo, metodología, panel de
> resultados con gráficas accesibles, login simulado, simulador con motor de ejemplo y "Mis
> simulaciones". Todo con datos de ejemplo, listo para conectar los resultados reales en la etapa 3.

| | |
|---|---|
| **Epic id** | `02-etapa-1-interfaz` |
| **Tasks** | `E2-T1` … `E2-T7` (pasos 7 a 13 del plan) |
| **Depends on** | `01-etapa-0-montaje` |
| **Unlocks** | nada en este plan (etapas 2 y 3 se planifican aparte) |
| **Parallel with** | dentro del epic hay dos carriles sin archivos en común: **Persona A** `E2-T1 → E2-T2 → E2-T3` (`web/views.py`, CSS, gráficas) y **Persona B** `E2-T4 → E2-T5 → E2-T6` (`web/views_app.py`, acceso, simulador). `E2-T7` los une al final |

No necesitas ningún otro archivo para completar este epic. Todo lo de abajo se repite aquí a propósito.

---

## Stack

Django 6.1 · Python 3.14 (mínimo 3.12) · plantillas de Django · CSS propio con tokens (sin
compilación) · Chart.js 4.5.1 desde cdnjs (con hash de integridad) · sin base de datos en uso ·
sesión en cookie firmada · Render (Free). Gestor de paquetes: `pip` con `requirements.txt`,
`requirements-dev.txt` y `requirements-ml.txt` (este último no lo usa la web). Versiones exactas en
esos archivos. Python fijado en `.python-version`. **Las rutas viven en `app.py`** (raíz,
`ROOT_URLCONF = "app"`); ya existen todas desde `E1-T4` y este epic no agrega ni renombra ninguna.

| Tarea | Comando |
|---|---|
| Servidor local | `sh scripts/py app.py` → http://127.0.0.1:8000/ (la guía de estilo en /styleguide/) |
| Lint | `sh scripts/py -m ruff check .` |
| Formato | `sh scripts/py -m ruff format --check .` (corregir: `sh scripts/py -m ruff format .`) |
| Pruebas, un archivo | `sh scripts/py -m pytest tests/test_acceso.py` |
| Pruebas, todas | `sh scripts/py -m pytest` |

Todos los comandos se ejecutan **desde la raíz del proyecto**. `sh scripts/py` usa el Python de
`.venv` en Git Bash y en Linux/macOS (en PowerShell: activa `.venv` y usa `python`).

**Gate:** `sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check . && sh scripts/py -m pytest`
pasa antes de marcar cualquier tarea de este epic como hecha.

No hay servicios que levantar. Ninguna prueba usa red: Chart.js se carga en el navegador, no en las pruebas.

## Directory subtree

```
app.py                                   # existe · solo lectura (rutas ya definidas)
web/
  views.py                               # Persona A · E2-T1, E2-T2, E2-T3 lo reemplazan entero (literal)
  views_app.py                           # Persona B · E2-T4, E2-T5, E2-T6 lo reemplazan entero (literal)
  auth_demo.py                           # NUEVO en E2-T4 (literal) · login simulado
  context_processors.py                  # E2-T4 lo reemplaza (literal) · agrega `usuario`
  simulacion_demo.py                     # NUEVO en E2-T5 (literal) · motor de ejemplo
  datos.py, data/mock/*.json             # existen · solo lectura
  templates/web/
    base.html                            # existe · solo lectura salvo correcciones de E2-T7
    styleguide.html                      # NUEVO en E2-T1
    metodologia.html                     # NUEVO en E2-T2
    resultados.html                      # NUEVO en E2-T3
    acceso.html                          # NUEVO en E2-T4 · login y registro
    app/simulador.html                   # NUEVO en E2-T5
    app/simulaciones.html                # NUEVO en E2-T6
    app/simulacion_detalle.html          # NUEVO en E2-T6
  static/web/
    css/components.css                   # existe · E2-T1 lo amplía
    css/pages/metodologia.css            # NUEVO en E2-T2
    css/pages/resultados.css             # NUEVO en E2-T3
    js/graficas.js                       # NUEVO en E2-T3
    js/simulador.js                      # NUEVO en E2-T5
tests/
  test_styleguide.py · test_metodologia.py · test_resultados.py · test_acceso.py
  test_simulador.py · test_simulaciones.py · test_accesibilidad.py   # todos literales
```

Todo lo que está fuera de este árbol queda fuera del alcance del epic. Si una tarea parece
requerir editar otro archivo, detente e informa.

## Data model touched here

Sin tablas. La sesión (cookie firmada) guarda, bajo la clave `cauce_usuario_demo`, el diccionario
`{"correo": str en minúsculas, "nombre": str}`. Los datos de las páginas se leen con `web.datos`:

| Fuente | Lo que usa este epic |
|---|---|
| `datos.resultados()` | `metricas` (4: nombre, unidad, mejor, valores por política), `recompensa_por_episodio`, `sensibilidad_presupuesto`, `politicas` |
| `datos.perfiles()` | `perfiles` (nombre, descripcion, n_eventos), `puntos` (x, y, perfil), `ejes` |
| `datos.simulaciones()` / `datos.simulacion(id)` | lista y detalle de simulaciones guardadas de ejemplo |

## Contracts

**Consumed** — ya existen, no se reconstruyen:

| From | Interface | Guarantee |
|---|---|---|
| `01-etapa-0-montaje` | nombres de ruta en `app.py`: `inicio`, `metodologia`, `resultados`, `styleguide`, `health`, `login`, `registro`, `salir`, `simulador`, `api_simular`, `simulaciones`, `simulacion_detalle` | no cambian |
| `01-etapa-0-montaje` | `web.datos.resultados()`, `perfiles()` → `dict`; `simulaciones()` → `list[dict]`; `simulacion(id)` → `dict \| None`; `POLITICAS` | datos validados contra el contrato |
| `01-etapa-0-montaje` | `web/templates/web/base.html` con bloques `titulo`, `estilos`, `contenido`, `scripts` y las variables `sitio` y `usuario` | la cabecera muestra al usuario si `usuario` no es None |
| `01-etapa-0-montaje` | `tokens.css`, `base.css`, `components.css` (botones, etiqueta, tarjetas, stat, insignia, cabecera, menú móvil, pie) | `tests/test_estilos.py` en verde |

**Produced** — las etapas 2 y 3 dependen exactamente de estas firmas:

| Export | Signature | Used by |
|---|---|---|
| `web/auth_demo.py` → `get_current_user` | `(request) -> dict \| None` | etapa 2 (se reemplaza su interior por `django.contrib.auth`) |
| `web/auth_demo.py` → `login_requerido` | decorador; página → 302 a `/login/?next=…`; ruta `/app/api/…` → 401 JSON | toda vista bajo `/app/` |
| `web/simulacion_demo.py` → `simular` | `(presupuesto: int, recursos: int, emergencias: int, semilla: int) -> dict` con `fuente`, `parametros`, `politicas.{uniforme,reglas,rl}.{necesidades_atendidas_pct, emergencias_sin_recursos, costo_total_mcop}` y `asignacion[]` (`municipio`, `evento`, `gravedad`, una cantidad por política) | etapa 3 (el agente Q-learning conserva firma y salida) |
| `POST /app/api/simular/` | cuerpo JSON con los 4 parámetros → 200 con la salida de `simular`; 400 `{"error": {"codigo": "parametro_invalido", "mensaje"}}`; 401 `no_autenticado`; 403 sin CSRF; 405 con GET | `web/static/web/js/simulador.js` |

## Conventions that bite in this area

- **`@require_POST` va encima de `@login_requerido`** en `api_simular`: un GET debe recibir 405
  aunque no haya sesión (lo exige `tests/test_rutas.py` desde la etapa 0).
- **La sesión solo se lee con `get_current_user()`**; nunca `request.session[...]` en vistas o plantillas.
- **Los datos para JavaScript van con `json_script`** (`{{ resultados|json_script:"datos-resultados" }}`), nunca con `{{ variable|safe }}` dentro de un `<script>`.
- **Chart.js no conoce `var(--…)`**: `graficas.js` lee cada token con `getComputedStyle(document.documentElement).getPropertyValue('--serie-rl').trim()`.
- **El color nunca va solo** en una gráfica: uniforme discontinua (`borderDash: [6, 4]`), reglas continua, RL continua y gruesa (`borderWidth: 3`), y cada gráfica tiene su tabla en `<details>`.
- **Persona A no toca `views_app.py` ni Persona B `views.py`.** Cada uno reemplaza su archivo entero con la versión literal de su tarea.
- **`tests/test_estilos.py` sigue vigente**: el CSS nuevo usa solo `var(--…)`, sin sombras, radios ≤ 16px y pesos 400/500.

Reglas completas: `CLAUDE.md`. Reglas por área: `.claude/rules/*.md` (en la raíz desde el Bootstrap).

---

## Tasks

En el mismo orden que `tasks.json`. Ese orden es el de construcción: de arriba abajo, sin
reordenar. Con dos personas, A toma `E2-T1`–`E2-T3` y B toma `E2-T4`–`E2-T6` en paralelo.

### `E2-T1` — Componentes de la etapa 1 y guía de estilo

**Depends on:** `E1-T6` · **Priority:** p1 — metadato para recortes de alcance, no un orden

Amplía `components.css` con los componentes que necesitan formularios, tablas, alertas,
gráficas y el simulador, y crea `/styleguide/` (solo con `DEBUG`) como catálogo vivo que el
equipo consulta antes de maquetar. `views.py` es literal.

**Files**
- `web/views.py` — reemplazo completo
- `web/templates/web/styleguide.html` — nuevo
- `web/static/web/css/components.css` — ampliar (agregar al final; no borrar lo existente)
- `tests/test_styleguide.py` — nuevo (literal)

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from web import datos

SECCIONES_STYLEGUIDE = [
    "botones", "tarjetas", "cifras", "etiquetas", "formularios", "tablas", "alertas",
]  # fmt: skip


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    """Página provisional: base.html muestra "Próximamente" en su bloque de contenido."""
    return render(request, "web/base.html", {"titulo": titulo})


def inicio(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/inicio.html",
        {"titulo": "Inicio", "resumen": datos.resultados()["resumen"]},
    )


def metodologia(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Metodología")


def resultados(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Resultados")


def styleguide(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        raise Http404("La guía de estilo solo existe en desarrollo")
    return render(
        request,
        "web/styleguide.html",
        {"titulo": "Guía de estilo", "secciones": SECCIONES_STYLEGUIDE},
    )


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**Agrega a `components.css`:**

| Clase | Especificación |
|---|---|
| `.campo` | bloque con `display: grid; gap: var(--esp-2)`; su `label` en `--texto-pequeno` y `--color-texto-enfasis`; su `input`/`select` con `min-height: 44px`, `padding: var(--esp-3)`, `background: var(--color-abismo)`, `color: var(--color-titulo)`, `border: 1px solid var(--color-borde-control)`, `border-radius: var(--radio-pequeno)`, `font: inherit`; `[aria-invalid="true"]` → `border-color: var(--color-error)` |
| `.campo-error` | `color: var(--color-error)`; `font-size: var(--texto-pequeno)`; `margin: 0` |
| `.ayuda` | `color: var(--color-texto)`; `font-size: var(--texto-pequeno)` |
| `.deslizador` | para `input[type="range"]`: `width: 100%`, `accent-color: var(--color-aqua)`, `min-height: 44px`; acompañado de un `<output>` con el valor en `--color-cifra` |
| `.tabla` | `width: 100%`; `border-collapse: collapse`; celdas con `padding: var(--esp-3)` y `border-bottom: 1px solid var(--color-borde)`; `th` en `--color-texto-enfasis`, `--texto-pequeno`, mayúsculas con `--tracking-etiqueta`; números alineados a la derecha con `font-variant-numeric: tabular-nums`; envoltorio `.tabla-desplazable` con `overflow-x: auto` para móvil |
| `.alerta` | `padding: var(--esp-4)`; `border-radius: var(--radio-pequeno)`; `border: 1px solid var(--color-borde-control)`; `background: var(--color-abismo)` |
| `.alerta-error` / `.alerta-aviso` / `.alerta-exito` | igual que `.alerta` con `border-color` y color de título en `--color-error` / `--color-aviso` / `--color-exito` |
| `.dividido` | rejilla de 1 columna; desde 1024px `grid-template-columns: minmax(280px, 360px) 1fr` con `gap: var(--esp-8)` (panel de controles + resultados) |
| `.panel-grafica` | `background: var(--fondo-grafica)`; `border-radius: var(--radio-tarjeta)`; `padding: var(--relleno-tarjeta)`; contiene `h3`, el `<canvas>` (alto 320px, ancho 100%) y el `<details>` con la tabla |
| `.estado-vacio` | centrado, `padding: var(--esp-16) var(--esp-6)`, `border: 1px dashed var(--color-borde-control)`, `border-radius: var(--radio-tarjeta)` |
| `.cargando` | `opacity: 0.6`; `pointer-events: none` (resultado mientras responde la API) |

**`web/templates/web/styleguide.html`** — extiende `web/base.html`; `<h1>Guía de estilo</h1>` y,
por cada nombre de `secciones`, `<section id="{{ nombre }}" class="seccion contenedor">` con su
`<h2>` y ejemplos reales: **botones** (`.boton-primario`, `.boton-secundario`, `.boton-icono` con
`aria-label`), **tarjetas** (`.tarjeta`, `.tarjeta-hundida`), **cifras** (un `.stat` con su
`.stat-etiqueta`), **etiquetas** (`.etiqueta`, `.insignia-demo`), **formularios** (un `.campo`
normal con `<label for="id_ejemplo">` + `<input id="id_ejemplo" name="ejemplo">`, uno en error con
`aria-invalid="true"`, `aria-describedby` y su `.campo-error`, y un `.deslizador` con
`<label for="id_deslizador_ejemplo">`), **tablas** (una `.tabla` de 3 filas con `<th scope="col">`)
y **alertas** (las tres variantes). Bajo cada ejemplo, `<code>` con el nombre de la clase. Un
único `<h1>` en toda la página.

**`tests/test_styleguide.py`** (contenido literal completo):

```python
"""Paso 7: la guía de estilo muestra cada componente y solo existe en desarrollo."""

from pathlib import Path

from django.urls import reverse

CSS = Path(__file__).resolve().parent.parent / "web" / "static" / "web" / "css"

SECCIONES = ["botones", "tarjetas", "cifras", "etiquetas", "formularios", "tablas", "alertas"]
COMPONENTES_NUEVOS = [
    ".campo", ".campo-error", ".deslizador", ".tabla", ".alerta", ".alerta-error",
    ".dividido", ".panel-grafica", ".estado-vacio",
]  # fmt: skip


def test_styleguide_muestra_todas_las_secciones_en_desarrollo(client, settings):
    settings.DEBUG = True
    respuesta = client.get(reverse("styleguide"))
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    for seccion in SECCIONES:
        assert f'id="{seccion}"' in html
    assert 'class="boton-primario"' in html
    assert 'class="stat"' in html


def test_styleguide_es_404_en_produccion(client, settings):
    settings.DEBUG = False
    assert client.get(reverse("styleguide")).status_code == 404


def test_components_css_define_los_componentes_de_la_etapa_1():
    componentes = (CSS / "components.css").read_text(encoding="utf-8")
    faltantes = [c for c in COMPONENTES_NUEVOS if c not in componentes]
    assert faltantes == []
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN DEBUG es True y llega un GET a /styleguide/ THE SYSTEM SHALL responder 200 con secciones de id botones, tarjetas, cifras, etiquetas, formularios, tablas y alertas, incluyendo un ejemplo class="boton-primario" y uno class="stat".
2. WHEN DEBUG es False y llega un GET a /styleguide/ THE SYSTEM SHALL responder 404.
3. WHEN se revisa components.css THE SYSTEM SHALL definir .campo, .campo-error, .deslizador, .tabla, .alerta, .alerta-error, .dividido, .panel-grafica y .estado-vacio, y seguir cumpliendo todas las reglas de tests/test_estilos.py.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_styleguide.py tests/test_estilos.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T1: Componentes de la etapa 1 y guía de estilo"
git tag step-07-styleguide
```

Si la siguiente tarea sale mal: `git reset --hard step-07-styleguide` y repetirla.

### `E2-T2` — Página de metodología

**Depends on:** `E2-T1` · **Priority:** p1

Explica, para el docente, de dónde salen los datos, cómo se agrupan, cómo se formula el problema
de RL y qué no promete el proyecto. El contenido viene de `docs/contexto_proyecto_rl_emergencias.md`
y de los perfiles de `perfiles.json`. `views.py` es literal.

**Files**
- `web/views.py` — reemplazo completo
- `web/templates/web/metodologia.html` — nuevo
- `web/static/web/css/pages/metodologia.css` — nuevo
- `tests/test_metodologia.py` — nuevo (literal)

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from web import datos

# Formulación del problema de RL (docs/contexto_proyecto_rl_emergencias.md, sección 6).
FORMULACION = [
    ("Agente", "Sistema que asigna los recursos de respuesta."),
    ("Entorno", "Simulación de varios municipios con emergencias simultáneas."),
    ("Estado", "Eventos pendientes, gravedad estimada, recursos disponibles y tiempo."),
    ("Acciones", "Asignar una unidad de recurso a una emergencia, priorizarla o reservar."),
    ("Recompensa", "Premia las necesidades atendidas; penaliza demoras, faltantes y costos."),
    ("Restricciones", "Presupuesto, inventario de recursos y capacidad de atención."),
    ("Episodio", "Un escenario simulado de emergencia con un horizonte de tiempo definido."),
]

SECCIONES_STYLEGUIDE = [
    "botones", "tarjetas", "cifras", "etiquetas", "formularios", "tablas", "alertas",
]  # fmt: skip


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    """Página provisional: base.html muestra "Próximamente" en su bloque de contenido."""
    return render(request, "web/base.html", {"titulo": titulo})


def inicio(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/inicio.html",
        {"titulo": "Inicio", "resumen": datos.resultados()["resumen"]},
    )


def metodologia(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/metodologia.html",
        {"titulo": "Metodología", "perfiles": datos.perfiles(), "formulacion": FORMULACION},
    )


def resultados(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Resultados")


def styleguide(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        raise Http404("La guía de estilo solo existe en desarrollo")
    return render(
        request,
        "web/styleguide.html",
        {"titulo": "Guía de estilo", "secciones": SECCIONES_STYLEGUIDE},
    )


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**`web/templates/web/metodologia.html`** — extiende `web/base.html` y carga
`web/css/pages/metodologia.css` en `estilos`. Encabezado: `<p class="etiqueta">Metodología</p>` y
`<h1>Metodología</h1>` con el párrafo
`<p>Cómo pasamos de los registros históricos de la UNGRD a una simulación donde un agente aprende a repartir recursos limitados.</p>`.
Luego un índice (`<nav aria-label="En esta página">` con enlaces a `#datos`, `#kmeans`,
`#formulacion`, `#limitaciones`) y cuatro secciones, cada una `<section id="…" class="seccion contenedor">` con su `<h2>`:

1. `id="datos"` · **Los datos** — `<p>Usamos Emergencias UNGRD V2, publicado por la Unidad Nacional para la Gestión del Riesgo de Desastres en Datos Abiertos Colombia: tipo de evento, fecha, ubicación, personas afectadas y daños reportados.</p>` y una `.tabla` "Verificación inicial" con 4 filas: número de registros, periodo cubierto, proporción de registros completos, disponibilidad de cada variable; segunda columna "Se verifica al descargar el archivo" (sin inventar cifras).
2. `id="kmeans"` · **Perfiles de emergencia (K-means)** — un párrafo que explica que K-means es un componente complementario, y una rejilla de `.tarjeta` por cada `perfil` de `perfiles.perfiles` con `<h3>{{ perfil.nombre }}</h3>`, `<p>{{ perfil.descripcion }}</p>` y `<p class="stat-etiqueta">{{ perfil.n_eventos }} eventos</p>`. Debajo, la lista de precauciones: no tratar códigos de municipio como cantidades, normalizar antes de agrupar, excluir variables conocidas solo después de atender la emergencia.
3. `id="formulacion"` · **Formulación del problema de RL** — `<table class="tabla">` con `<thead>` (`Elemento`, `Propuesta`) y una fila por cada par de `formulacion`: `<tr><th scope="row">{{ elemento }}</th><td>{{ descripcion }}</td></tr>`. Debajo, las tres estrategias comparadas (uniforme, basada en reglas, RL) como `<ol>`.
4. `id="limitaciones"` · **Lo que este proyecto no es** — `.alerta.alerta-aviso` con: `<p>Es una simulación, no la realidad: los resultados no son recomendaciones operativas para la UNGRD. Tampoco es un modelo predictivo: no pronostica dónde ni cuándo ocurrirá un desastre.</p>` y una `<ul>` con: supuestos explícitos de recursos, dependencia de la calidad del dato, sin información futura, escala inicial reducida.

**`metodologia.css`** — solo `var(--…)`: índice como fila de enlaces con `gap: var(--esp-4)` que
pasa a columna en móvil; rejilla de perfiles 1 → 2 (≥768px) → 4 (≥1024px) columnas con `gap: var(--esp-5)`.

**`tests/test_metodologia.py`** (contenido literal completo):

```python
"""Paso 8: la metodología explica datos, K-means, la formulación de RL y sus límites."""

from django.urls import reverse

from web import datos

FORMULACION = [
    "Agente", "Entorno", "Estado", "Acciones", "Recompensa", "Restricciones", "Episodio",
]  # fmt: skip


def _html(client) -> str:
    respuesta = client.get(reverse("metodologia"))
    assert respuesta.status_code == 200
    return respuesta.content.decode()


def test_metodologia_tiene_sus_cuatro_secciones(client):
    html = _html(client)
    for seccion in ("datos", "kmeans", "formulacion", "limitaciones"):
        assert f'<section id="{seccion}"' in html
    assert "Emergencias UNGRD V2" in html


def test_tabla_de_formulacion_tiene_los_siete_elementos(client):
    html = _html(client)
    for elemento in FORMULACION:
        assert f'<th scope="row">{elemento}</th>' in html


def test_metodologia_lista_los_perfiles_de_kmeans(client):
    html = _html(client)
    for perfil in datos.perfiles()["perfiles"]:
        assert perfil["nombre"] in html


def test_metodologia_declara_que_es_una_simulacion(client):
    html = _html(client)
    assert "no es un modelo predictivo" in html.lower()
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN llega un GET a /metodologia/ THE SYSTEM SHALL responder 200 con `<section id="datos"`, `<section id="kmeans"`, `<section id="formulacion"` y `<section id="limitaciones"`, y el texto "Emergencias UNGRD V2".
2. WHEN llega un GET a /metodologia/ THE SYSTEM SHALL mostrar celdas `<th scope="row">` para Agente, Entorno, Estado, Acciones, Recompensa, Restricciones y Episodio.
3. WHEN llega un GET a /metodologia/ THE SYSTEM SHALL mostrar el `nombre` de cada perfil de perfiles.json y la frase "no es un modelo predictivo".

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_metodologia.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T2: Página de metodología"
git tag step-08-metodologia
```

Si la siguiente tarea sale mal: `git reset --hard step-08-metodologia` y repetirla.

### `E2-T3` — Panel de resultados con Chart.js

**Depends on:** `E2-T2` · **Priority:** p1

El panel que responde la pregunta de investigación: cuatro indicadores (uno por métrica) y cuatro
gráficas (comparación de métricas, recompensa por episodio, sensibilidad al presupuesto,
perfiles de K-means), cada una con descripción para lectores de pantalla y tabla alternativa.
`views.py` es literal; la plantilla, el CSS y `graficas.js` los escribes tú.

**Files**
- `web/views.py` — reemplazo completo
- `web/templates/web/resultados.html` — nuevo
- `web/static/web/js/graficas.js` — nuevo
- `web/static/web/css/pages/resultados.css` — nuevo
- `tests/test_resultados.py` — nuevo (literal)

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from web import datos

# Formulación del problema de RL (docs/contexto_proyecto_rl_emergencias.md, sección 6).
FORMULACION = [
    ("Agente", "Sistema que asigna los recursos de respuesta."),
    ("Entorno", "Simulación de varios municipios con emergencias simultáneas."),
    ("Estado", "Eventos pendientes, gravedad estimada, recursos disponibles y tiempo."),
    ("Acciones", "Asignar una unidad de recurso a una emergencia, priorizarla o reservar."),
    ("Recompensa", "Premia las necesidades atendidas; penaliza demoras, faltantes y costos."),
    ("Restricciones", "Presupuesto, inventario de recursos y capacidad de atención."),
    ("Episodio", "Un escenario simulado de emergencia con un horizonte de tiempo definido."),
]

SECCIONES_STYLEGUIDE = [
    "botones", "tarjetas", "cifras", "etiquetas", "formularios", "tablas", "alertas",
]  # fmt: skip


def inicio(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/inicio.html",
        {"titulo": "Inicio", "resumen": datos.resultados()["resumen"]},
    )


def metodologia(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/metodologia.html",
        {"titulo": "Metodología", "perfiles": datos.perfiles(), "formulacion": FORMULACION},
    )


def resultados(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/resultados.html",
        {"titulo": "Resultados", "resultados": datos.resultados(), "perfiles": datos.perfiles()},
    )


def styleguide(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        raise Http404("La guía de estilo solo existe en desarrollo")
    return render(
        request,
        "web/styleguide.html",
        {"titulo": "Guía de estilo", "secciones": SECCIONES_STYLEGUIDE},
    )


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**`web/templates/web/resultados.html`** — extiende `web/base.html`, carga
`web/css/pages/resultados.css` en `estilos`. En `contenido`:

1. Encabezado: `<p class="etiqueta">Resultados</p>`, `<h1>Resultados de la simulación</h1>`,
   `<p>Comparamos tres estrategias sobre los mismos escenarios simulados: una regla uniforme, una basada en prioridades y un agente de aprendizaje por refuerzo.</p>`.
2. **Indicadores** — rejilla 1 → 2 → 4 columnas; por cada `metrica` de `resultados.metricas`:
   `<div class="tarjeta"><p class="etiqueta">{{ metrica.nombre }}</p><p class="stat">{{ metrica.valores.rl }}</p><p class="stat-etiqueta">{{ metrica.unidad }} con el agente RL · reglas: {{ metrica.valores.reglas }} · uniforme: {{ metrica.valores.uniforme }}</p></div>`.
   Exactamente un `class="stat"` por métrica (la prueba los cuenta).
3. **Cuatro `.panel-grafica`** (rejilla 1 → 2 columnas), cada uno con `<h3>`, el canvas y un
   `<details><summary>Ver los datos en tabla</summary><div class="tabla-desplazable"><table class="tabla">…</table></div></details>`:
   - `<canvas id="grafica-metricas" role="img" aria-label="Barras agrupadas: necesidades atendidas, tiempo hasta la atención, costo y emergencias sin recursos para las tres políticas">` — tabla: filas = métricas, columnas = políticas.
   - `<canvas id="grafica-recompensa" role="img" aria-label="Líneas: recompensa acumulada por episodio de entrenamiento para cada política">` — tabla: episodio y una columna por política.
   - `<canvas id="grafica-sensibilidad" role="img" aria-label="Líneas: porcentaje de necesidades atendidas según el presupuesto disponible">` — tabla: presupuesto % y una columna por política.
   - `<canvas id="grafica-perfiles" role="img" aria-label="Dispersión: emergencias agrupadas en perfiles de K-means según personas afectadas y viviendas dañadas">` — tabla: perfil, nombre, número de eventos.
4. Al final del bloque, `{{ resultados|json_script:"datos-resultados" }}{{ perfiles|json_script:"datos-perfiles" }}`.

En `{% block scripts %}`, **en este orden**:
`<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js" integrity="sha512-WoViKhKD4qI2WruSZqv9+kvM4WfFhUMQCLN4QlDTt5aU56fLQy2gYoxWIqlEnXqJy/+Ac5q/hk1oWfqnMDhwMA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>`
y luego `<script src="{% static 'web/js/graficas.js' %}" defer></script>`.

**`web/static/web/js/graficas.js`** — sin otras dependencias:
- `const token = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();`
- Lee los datos con `JSON.parse(document.getElementById('datos-resultados').textContent)` (y `datos-perfiles`).
- Estilo por política: uniforme → `token('--serie-uniforme')` con `borderDash: [6, 4]` (y barras con transparencia 60%); reglas → `token('--serie-reglas')`; RL → `token('--serie-rl')` con `borderWidth: 3`. Los nombres de leyenda salen de `resultados.politicas`.
- Defaults: `Chart.defaults.color = token('--color-texto')`, `Chart.defaults.font.family = token('--fuente')`, `Chart.defaults.borderColor = token('--rejilla-grafica')`; animaciones apagadas si `matchMedia('(prefers-reduced-motion: reduce)').matches` (`animation: false`).
- **grafica-metricas**: barras agrupadas; como las métricas tienen unidades distintas, normaliza cada métrica a 0–100 respecto de su máximo y muestra el valor real en el tooltip con su unidad.
- **grafica-recompensa** y **grafica-sensibilidad**: líneas con un dataset por política.
- **grafica-perfiles**: dispersión con un dataset por perfil, colores `--perfil-0` … `--perfil-3` y `pointStyle` distinto por perfil (`circle`, `triangle`, `rect`, `rectRot`); ejes con los textos de `perfiles.ejes`.
- Todas: `responsive: true`, `maintainAspectRatio: false`, leyenda abajo.
- Si `window.Chart` no existe (CDN bloqueado), no lanza error: deja las tablas visibles abriendo los `<details>` (`details.open = true`).

**`resultados.css`** — solo `var(--…)`: rejillas de indicadores y paneles con `gap: var(--esp-5)`; contenedor del canvas con `position: relative; height: 320px`.

**`tests/test_resultados.py`** (contenido literal completo):

```python
"""Paso 9: el panel de resultados dibuja 4 gráficas accesibles a partir del contrato."""

from pathlib import Path

from django.urls import reverse

from web import datos

JS = Path(__file__).resolve().parent.parent / "web" / "static" / "web" / "js"
GRAFICAS = ["grafica-metricas", "grafica-recompensa", "grafica-sensibilidad", "grafica-perfiles"]
CHART_JS = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js"
SRI_CHART_JS = (
    "sha512-WoViKhKD4qI2WruSZqv9+kvM4WfFhUMQCLN4QlDTt5aU56fLQy2gYoxWIqlEnXqJy/"
    "+Ac5q/hk1oWfqnMDhwMA=="
)


def _html(client) -> str:
    respuesta = client.get(reverse("resultados"))
    assert respuesta.status_code == 200
    return respuesta.content.decode()


def test_resultados_expone_los_datos_como_json_script(client):
    html = _html(client)
    assert '<script id="datos-resultados" type="application/json">' in html
    assert '<script id="datos-perfiles" type="application/json">' in html


def test_cada_grafica_es_accesible_y_tiene_tabla_alternativa(client):
    html = _html(client)
    for grafica in GRAFICAS:
        assert f'<canvas id="{grafica}" role="img" aria-label="' in html
    assert html.count("<details") >= len(GRAFICAS)
    assert html.count("<table") >= len(GRAFICAS)


def test_indicadores_por_metrica(client):
    html = _html(client)
    assert html.count('class="stat"') == len(datos.resultados()["metricas"])
    for metrica in datos.resultados()["metricas"]:
        assert metrica["nombre"] in html


def test_chart_js_fijado_con_integridad(client):
    html = _html(client)
    assert f'src="{CHART_JS}"' in html
    assert f'integrity="{SRI_CHART_JS}"' in html
    assert 'crossorigin="anonymous"' in html
    assert "web/js/graficas.js" in html


def test_graficas_js_usa_los_tokens_y_respeta_movimiento_reducido():
    codigo = (JS / "graficas.js").read_text(encoding="utf-8")
    for token in ("--serie-uniforme", "--serie-reglas", "--serie-rl", "--fondo-grafica"):
        assert token in codigo
    assert "prefers-reduced-motion" in codigo
    assert "borderDash" in codigo
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN llega un GET a /resultados/ THE SYSTEM SHALL incrustar los datos con `<script id="datos-resultados" type="application/json">` y `<script id="datos-perfiles" type="application/json">`.
2. WHEN llega un GET a /resultados/ THE SYSTEM SHALL mostrar los canvas grafica-metricas, grafica-recompensa, grafica-sensibilidad y grafica-perfiles, cada uno con role="img" y aria-label no vacío, y al menos 4 <details> con una <table> de los mismos datos.
3. WHEN llega un GET a /resultados/ THE SYSTEM SHALL mostrar un class="stat" por cada métrica de resultados.json, con el `nombre` de cada métrica.
4. WHEN llega un GET a /resultados/ THE SYSTEM SHALL cargar Chart.js 4.5.1 desde cdnjs con su hash de integridad sha512 y crossorigin="anonymous", y después web/js/graficas.js.
5. WHEN se lee web/js/graficas.js THE SYSTEM SHALL usar --serie-uniforme, --serie-reglas, --serie-rl y --fondo-grafica, comprobar prefers-reduced-motion y usar borderDash.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_resultados.py tests/test_estilos.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T3: Panel de resultados con Chart.js"
git tag step-09-resultados
```

Si la siguiente tarea sale mal: `git reset --hard step-09-resultados` y repetirla.

### `E2-T4` — Login simulado que protege la app

**Depends on:** `E1-T6` · **Priority:** p1

Login y registro sin contraseñas reales ni base de datos: cualquier correo con formato válido
entra y el usuario vive en la sesión. Todo pasa por `web/auth_demo.py`, el punto donde la etapa 2
conecta `django.contrib.auth` sin tocar nada más. Además protege todas las páginas bajo `/app/`.
`auth_demo.py`, `context_processors.py` y `views_app.py` son literales; `acceso.html` lo escribes tú.

**Files**
- `web/auth_demo.py` — nuevo
- `web/context_processors.py` — reemplazo completo
- `web/views_app.py` — reemplazo completo
- `web/templates/web/acceso.html` — nuevo
- `tests/test_acceso.py` — nuevo (literal)

**`web/auth_demo.py`** (contenido literal completo):

```python
"""Login SIMULADO de la etapa 1: sin contraseñas ni base de datos.

Cualquier correo con formato válido entra; la clave se ignora a propósito. El usuario vive en
la sesión (cookie firmada). Toda la aplicación pregunta por el usuario SOLO a través de
`get_current_user()` y protege vistas SOLO con `login_requerido`. En la etapa 2 se reemplaza
el interior de estas funciones por `django.contrib.auth` y nada más cambia.
"""

from collections.abc import Callable
from functools import wraps
from urllib.parse import urlencode

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

CLAVE_SESION = "cauce_usuario_demo"
DESTINO_POR_DEFECTO = "simulador"


def correo_valido(correo: str) -> bool:
    try:
        validate_email(correo)
    except ValidationError:
        return False
    return True


def get_current_user(request: HttpRequest) -> dict | None:
    """El usuario actual como {"correo", "nombre"}, o None si nadie inició sesión."""
    sesion = getattr(request, "session", None)  # peticiones sin middleware (p. ej. RequestFactory)
    return sesion.get(CLAVE_SESION) if sesion is not None else None


def iniciar_sesion_demo(request: HttpRequest, correo: str, nombre: str = "") -> dict:
    correo = correo.strip().lower()
    if not correo_valido(correo):
        raise ValueError("correo inválido")
    request.session.cycle_key()
    usuario = {"correo": correo, "nombre": nombre.strip() or correo.split("@")[0]}
    request.session[CLAVE_SESION] = usuario
    return usuario


def cerrar_sesion(request: HttpRequest) -> None:
    request.session.flush()


def destino_seguro(request: HttpRequest, siguiente: str | None) -> str:
    """A dónde ir después de entrar. Nunca a otro dominio (evita redirecciones abiertas)."""
    if siguiente and url_has_allowed_host_and_scheme(
        siguiente, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return siguiente
    return reverse(DESTINO_POR_DEFECTO)


def login_requerido(vista: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """Página: redirige a /login/?next=<ruta>. API (/app/api/…): responde 401 en JSON."""

    @wraps(vista)
    def envoltura(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if get_current_user(request) is not None:
            return vista(request, *args, **kwargs)
        if request.path.startswith("/app/api/"):
            return JsonResponse(
                {"error": {"codigo": "no_autenticado", "mensaje": "Inicia sesión para continuar"}},
                status=401,
            )
        return redirect(f"{reverse('login')}?{urlencode({'next': request.get_full_path()})}")

    return envoltura
```

**`web/context_processors.py`** (contenido literal completo):

```python
"""Variables disponibles en todas las plantillas."""

from django.conf import settings
from django.http import HttpRequest

from web.auth_demo import get_current_user


def sitio(request: HttpRequest) -> dict:
    return {
        "sitio": {
            "nombre": "Cauce",
            "subtitulo": "Asignación inteligente de recursos ante emergencias",
            "datos_demo": settings.CAUCE_DATOS_DEMO,
        },
        "usuario": get_current_user(request),
    }
```

**`web/views_app.py`** (contenido literal completo):

```python
"""Vistas de acceso (login simulado) y de la aplicación (simulador, simulaciones)."""

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from web.auth_demo import (
    cerrar_sesion,
    correo_valido,
    destino_seguro,
    iniciar_sesion_demo,
    login_requerido,
)


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    return render(request, "web/base.html", {"titulo": titulo})


def _acceso(request: HttpRequest, modo: str) -> HttpResponse:
    """Login y registro comparten plantilla. Cualquier correo válido entra (modo demostración)."""
    error = ""
    correo = request.POST.get("correo", "")
    nombre = request.POST.get("nombre", "")
    if request.method == "POST":
        if correo_valido(correo.strip()):
            iniciar_sesion_demo(request, correo, nombre)
            return redirect(destino_seguro(request, request.GET.get("next")))
        error = "Escribe un correo válido, por ejemplo nombre@dominio.co"
    titulo = "Iniciar sesión" if modo == "login" else "Crear cuenta"
    return render(
        request,
        "web/acceso.html",
        {"titulo": titulo, "modo": modo, "error": error, "correo": correo, "nombre": nombre},
    )


def login(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "login")


def registro(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "registro")


@require_POST
def salir(request: HttpRequest) -> HttpResponse:
    cerrar_sesion(request)
    return redirect("inicio")


@login_requerido
def simulador(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Simulador")


@require_POST
def api_simular(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {"error": {"codigo": "no_implementado", "mensaje": "El simulador llega en el paso 11"}},
        status=501,
    )


@login_requerido
def simulaciones(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Mis simulaciones")


@login_requerido
def simulacion_detalle(request: HttpRequest, sim_id: str) -> HttpResponse:
    return _proximamente(request, "Simulación")
```

**`web/templates/web/acceso.html`** — una plantilla para los dos modos (`modo` es `"login"` o
`"registro"`). Extiende `web/base.html`; en `contenido`, una `<section class="seccion contenedor">`
con una `.tarjeta` centrada de máx. 440px:

1. `<p class="etiqueta">Cauce</p>` y `<h1>{{ titulo }}</h1>`.
2. `<div class="alerta alerta-aviso" role="note"><p><strong>Modo demostración:</strong> no hay contraseñas ni base de datos todavía. Cualquier correo con formato válido entra.</p></div>`.
3. `<form method="post" novalidate>` con `{% csrf_token %}` y, en este orden:
   - solo si `modo == "registro"`: `.campo` con `<label for="id_nombre">Nombre</label>` y `<input type="text" name="nombre" id="id_nombre" value="{{ nombre }}" autocomplete="name">`;
   - `.campo` con `<label for="id_correo">Correo</label>` y exactamente `<input type="email" name="correo" id="id_correo" value="{{ correo }}" autocomplete="email" required` más, **si hay `error`**, ` aria-invalid="true" aria-describedby="error-correo"`, y `>`; si hay error, debajo `<p id="error-correo" class="campo-error">{{ error }}</p>`;
   - `.campo` con `<label for="id_clave">Clave</label>` y `<input type="password" name="clave" id="id_clave" autocomplete="{% if modo == 'registro' %}new-password{% else %}current-password{% endif %}">` y `<p class="ayuda">En modo demostración la clave no se verifica.</p>`;
   - `<button type="submit" class="boton-primario">{% if modo == 'registro' %}Crear cuenta{% else %}Entrar{% endif %}</button>`.
4. Enlace al otro modo: en login `¿No tienes cuenta? <a href="{% url 'registro' %}">Crear cuenta</a>`; en registro `¿Ya tienes cuenta? <a href="{% url 'login' %}">Iniciar sesión</a>`. Si la URL trae `next`, consérvalo en ese enlace (`?next={{ request.GET.next|urlencode }}`).

Nunca bloquear pegar (sin `onpaste`) ni pedir confirmar la clave: el gestor de contraseñas debe funcionar.

**`tests/test_acceso.py`** (contenido literal completo):

```python
"""Paso 10: login simulado; protege la app sin contraseñas ni base de datos."""

from django.urls import reverse

from web.auth_demo import CLAVE_SESION


def test_formulario_de_login_es_accesible(client):
    respuesta = client.get(reverse("login"))
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    assert 'method="post"' in html
    assert '<label for="id_correo"' in html
    assert 'type="email" name="correo" id="id_correo"' in html
    assert 'autocomplete="current-password"' in html
    assert "onpaste" not in html
    assert "Modo demostración" in html


def test_cualquier_correo_valido_entra_y_va_al_simulador(client):
    respuesta = client.post(reverse("login"), {"correo": "Ana@Ejemplo.co", "clave": "x"})
    assert respuesta.status_code == 302
    assert respuesta["Location"] == reverse("simulador")
    assert client.session[CLAVE_SESION]["correo"] == "ana@ejemplo.co"


def test_correo_invalido_muestra_error_junto_al_campo(client):
    respuesta = client.post(reverse("login"), {"correo": "no-es-correo", "clave": ""})
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    assert "Escribe un correo válido" in html
    assert 'aria-invalid="true"' in html
    assert CLAVE_SESION not in client.session


def test_next_interno_se_respeta_y_externo_se_ignora(client):
    interno = client.post(
        reverse("login") + "?next=/app/simulaciones/", {"correo": "a@b.co", "clave": ""}
    )
    assert interno["Location"] == "/app/simulaciones/"
    client.post(reverse("salir"))
    externo = client.post(
        reverse("login") + "?next=https://malicioso.example/", {"correo": "a@b.co", "clave": ""}
    )
    assert externo["Location"] == reverse("simulador")


def test_app_protegida_y_cabecera_muestra_al_usuario(client):
    anonimo = client.get(reverse("simulador"))
    assert anonimo.status_code == 302
    assert anonimo["Location"] == f"{reverse('login')}?next=%2Fapp%2Fsimulador%2F"
    client.post(reverse("registro"), {"nombre": "Ana Gómez", "correo": "ana@b.co", "clave": "x"})
    html = client.get(reverse("simulador")).content.decode()
    assert "Ana Gómez" in html
    assert f'action="{reverse("salir")}"' in html


def test_salir_borra_la_sesion(client):
    client.post(reverse("login"), {"correo": "a@b.co", "clave": ""})
    respuesta = client.post(reverse("salir"))
    assert respuesta["Location"] == reverse("inicio")
    assert CLAVE_SESION not in client.session
    assert client.get(reverse("simulador")).status_code == 302
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN llega un GET a /login/ THE SYSTEM SHALL mostrar un formulario POST con <label for="id_correo">, un input email name="correo" id="id_correo", un input de clave con autocomplete="current-password", sin atributo onpaste, y el texto "Modo demostración".
2. WHEN /login/ recibe un POST con cualquier correo válido THE SYSTEM SHALL guardar {correo en minúsculas, nombre} en la sesión y redirigir con 302 a /app/simulador/.
3. WHEN /login/ recibe un POST con un correo inválido THE SYSTEM SHALL responder 200 con "Escribe un correo válido" y aria-invalid="true" en el campo, sin crear usuario en la sesión.
4. WHEN el POST de login trae ?next=/app/simulaciones/ THE SYSTEM SHALL redirigir ahí, y WHEN next apunta a otro dominio SHALL redirigir a /app/simulador/.
5. WHEN un visitante anónimo pide /app/simulador/ THE SYSTEM SHALL redirigir con 302 a /login/?next=%2Fapp%2Fsimulador%2F, y WHEN hay sesión SHALL mostrar en la cabecera el nombre del usuario y un formulario que envía a /salir/.
6. WHEN /salir/ recibe un POST THE SYSTEM SHALL vaciar la sesión y redirigir a /.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_acceso.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T4: Login simulado que protege la app"
git tag step-10-login-demo
```

Si la siguiente tarea sale mal: `git reset --hard step-10-login-demo` y repetirla.

### `E2-T5` — Simulador con motor de ejemplo y API JSON

**Depends on:** `E2-T4` · **Priority:** p1

El corazón interactivo: el usuario mueve presupuesto, recursos, número de emergencias y semilla, y
ve cómo reparte cada estrategia. Hoy responde un motor de **ejemplo** determinista
(`simulacion_demo.py`) con la misma firma y salida que tendrá el agente Q-learning en la etapa 3.
La página llama a la API con `fetch` y anuncia el resultado a lectores de pantalla.
`simulacion_demo.py` y `views_app.py` son literales; la plantilla y el JS los escribes tú.

**Files**
- `web/simulacion_demo.py` — nuevo
- `web/views_app.py` — reemplazo completo
- `web/templates/web/app/simulador.html` — nuevo
- `web/static/web/js/simulador.js` — nuevo
- `tests/test_simulador.py` — nuevo (literal)

**`web/simulacion_demo.py`** (contenido literal completo):

```python
"""Motor de simulación de EJEMPLO (etapa 1).

No hay agente real todavía: genera resultados creíbles y deterministas a partir de la semilla,
con el MISMO formato que devolverá el agente Q-learning en la etapa 3. Para conectarlo, se
reemplaza el interior de `simular()` conservando su firma y su salida.
"""

import random

from web.datos import POLITICAS

LIMITES = {
    "presupuesto": (50, 150),  # % del presupuesto de referencia
    "recursos": (5, 50),  # unidades de recurso disponibles
    "emergencias": (3, 12),  # emergencias simultáneas en el escenario
    "semilla": (0, 9999),
}

MUNICIPIOS = [
    ("Mocoa (Putumayo)", "Avenida torrencial"),
    ("Quibdó (Chocó)", "Inundación"),
    ("Salgar (Antioquia)", "Avenida torrencial"),
    ("Gramalote (Norte de Santander)", "Movimiento en masa"),
    ("Montería (Córdoba)", "Inundación"),
    ("San Andrés (San Andrés)", "Vendaval"),
    ("Riohacha (La Guajira)", "Sequía"),
    ("Popayán (Cauca)", "Movimiento en masa"),
    ("Neiva (Huila)", "Incendio forestal"),
    ("Magangué (Bolívar)", "Inundación"),
    ("Pasto (Nariño)", "Actividad volcánica"),
    ("Yopal (Casanare)", "Incendio forestal"),
]


def validar_parametros(parametros: dict) -> dict[str, int]:
    """Convierte y valida los cuatro parámetros. Lanza ValueError con un mensaje en español."""
    limpios: dict[str, int] = {}
    for nombre, (minimo, maximo) in LIMITES.items():
        try:
            valor = int(parametros[nombre])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"'{nombre}' es obligatorio y debe ser un número entero") from None
        if not minimo <= valor <= maximo:
            raise ValueError(f"'{nombre}' debe estar entre {minimo} y {maximo}")
        limpios[nombre] = valor
    return limpios


def _repartir(total: int, pesos: list[float]) -> list[int]:
    """Reparte `total` unidades enteras en proporción a `pesos` (método del mayor residuo)."""
    suma = sum(pesos)
    exactas = [total * peso / suma for peso in pesos]
    enteras = [int(valor) for valor in exactas]
    sobrantes = total - sum(enteras)
    orden = sorted(range(len(pesos)), key=lambda i: exactas[i] - enteras[i], reverse=True)
    for i in orden[:sobrantes]:
        enteras[i] += 1
    return enteras


def simular(presupuesto: int, recursos: int, emergencias: int, semilla: int) -> dict:
    parametros = validar_parametros(
        {
            "presupuesto": presupuesto,
            "recursos": recursos,
            "emergencias": emergencias,
            "semilla": semilla,
        }
    )
    azar = random.Random(semilla)
    cobertura = min(1.0, (presupuesto / 100) * (recursos / (emergencias * 2.5)))
    base = 30 + 45 * cobertura
    atendidas = {
        "uniforme": round(base + azar.uniform(-3, 3), 1),
        "reglas": round(min(99.0, base + 9 + azar.uniform(-3, 3)), 1),
        "rl": round(min(99.5, base + 19 + azar.uniform(-3, 3)), 1),
    }
    sin_recursos = {
        politica: max(0, round(emergencias * (1 - atendidas[politica] / 100) * 0.9))
        for politica in POLITICAS
    }
    costo_base = recursos * 38.0 * presupuesto / 100
    costo = {
        "uniforme": round(costo_base * 1.08, 1),
        "reglas": round(costo_base * 1.04, 1),
        "rl": round(costo_base, 1),
    }
    escenario = azar.sample(MUNICIPIOS, emergencias)
    gravedades = [round(azar.uniform(0.2, 1.0), 2) for _ in escenario]
    por_reglas = _repartir(recursos, gravedades)
    por_rl = _repartir(recursos, [g**2 for g in gravedades])
    asignacion = [
        {
            "municipio": municipio,
            "evento": evento,
            "gravedad": gravedad,
            "uniforme": recursos // emergencias,
            "reglas": por_reglas[i],
            "rl": por_rl[i],
        }
        for i, ((municipio, evento), gravedad) in enumerate(zip(escenario, gravedades, strict=True))
    ]
    asignacion.sort(key=lambda fila: fila["gravedad"], reverse=True)
    return {
        "fuente": "datos_de_ejemplo",
        "parametros": parametros,
        "politicas": {
            politica: {
                "necesidades_atendidas_pct": atendidas[politica],
                "emergencias_sin_recursos": sin_recursos[politica],
                "costo_total_mcop": costo[politica],
            }
            for politica in POLITICAS
        },
        "asignacion": asignacion,
    }
```

**`web/views_app.py`** (contenido literal completo):

```python
"""Vistas de acceso (login simulado) y de la aplicación (simulador, simulaciones)."""

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from web.auth_demo import (
    cerrar_sesion,
    correo_valido,
    destino_seguro,
    iniciar_sesion_demo,
    login_requerido,
)
from web.simulacion_demo import LIMITES, simular


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    return render(request, "web/base.html", {"titulo": titulo})


def _acceso(request: HttpRequest, modo: str) -> HttpResponse:
    """Login y registro comparten plantilla. Cualquier correo válido entra (modo demostración)."""
    error = ""
    correo = request.POST.get("correo", "")
    nombre = request.POST.get("nombre", "")
    if request.method == "POST":
        if correo_valido(correo.strip()):
            iniciar_sesion_demo(request, correo, nombre)
            return redirect(destino_seguro(request, request.GET.get("next")))
        error = "Escribe un correo válido, por ejemplo nombre@dominio.co"
    titulo = "Iniciar sesión" if modo == "login" else "Crear cuenta"
    return render(
        request,
        "web/acceso.html",
        {"titulo": titulo, "modo": modo, "error": error, "correo": correo, "nombre": nombre},
    )


def login(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "login")


def registro(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "registro")


@require_POST
def salir(request: HttpRequest) -> HttpResponse:
    cerrar_sesion(request)
    return redirect("inicio")


@login_requerido
def simulador(request: HttpRequest) -> HttpResponse:
    return render(request, "web/app/simulador.html", {"titulo": "Simulador", "limites": LIMITES})


@require_POST  # va primero: un GET recibe 405 aunque no haya sesión
@login_requerido
def api_simular(request: HttpRequest) -> JsonResponse:
    try:
        parametros = json.loads(request.body or b"{}")
        if not isinstance(parametros, dict):
            raise ValueError("el cuerpo debe ser un objeto JSON")
        resultado = simular(**{clave: parametros.get(clave) for clave in LIMITES})
    except (json.JSONDecodeError, ValueError) as error:
        return JsonResponse(
            {"error": {"codigo": "parametro_invalido", "mensaje": str(error)}}, status=400
        )
    return JsonResponse(resultado)


@login_requerido
def simulaciones(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Mis simulaciones")


@login_requerido
def simulacion_detalle(request: HttpRequest, sim_id: str) -> HttpResponse:
    return _proximamente(request, "Simulación")
```

**`web/templates/web/app/simulador.html`** — extiende `web/base.html`; carga
`<script src="{% static 'web/js/simulador.js' %}" defer></script>` en `scripts`. En `contenido`:

1. `<section class="seccion contenedor">` con `<p class="etiqueta">Simulador</p>`, `<h1>Simulador de asignación</h1>`,
   `<p>Elige un escenario y compara cuántos recursos asigna cada estrategia a cada municipio.</p>`.
2. `<div class="dividido">`:
   - **Controles**: `<form id="form-simulador" class="tarjeta" data-api="{% url 'api_simular' %}">` con
     `{% csrf_token %}` y cuatro `.campo`, uno por parámetro, con estos textos y rangos (de `limites`):
     `presupuesto` "Presupuesto disponible (%)" `type="range"` 50–150 paso 5, valor inicial 100;
     `recursos` "Unidades de recurso" `type="range"` 5–50, inicial 20;
     `emergencias` "Emergencias simultáneas" `type="range"` 3–12, inicial 8;
     `semilla` "Semilla del escenario" `type="number"` 0–9999, inicial 42.
     Cada uno exactamente como `<label for="id_{{ nombre }}">…</label>` + `<input … name="{{ nombre }}" id="id_{{ nombre }}" …>`; los `range` con clase `.deslizador` y un `<output for="id_{{ nombre }}">` con el valor actual.
     Botón `<button type="submit" class="boton-primario">Simular</button>`.
   - **Resultados**: `<div id="resultado-simulacion" aria-live="polite" class="tarjeta">` con, al
     inicio, `<p>Ajusta los controles y pulsa <strong>Simular</strong>.</p>`.

**`web/static/web/js/simulador.js`** — sin dependencias:
- Actualiza cada `<output>` en el evento `input` de su control.
- En `submit`: `preventDefault()`; arma `{presupuesto, recursos, emergencias, semilla}` como enteros; marca `#resultado-simulacion` con `.cargando` y `aria-busy="true"`; hace `fetch(form.dataset.api, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value}, body: JSON.stringify(datos)})`.
- **200**: pinta (con `document.createElement`, nunca `innerHTML` con datos) tres `.stat` con `necesidades_atendidas_pct` por política y sus nombres, y una `.tabla` dentro de `.tabla-desplazable` con columnas Municipio, Evento, Gravedad, Uniforme, Reglas, RL (una fila por `asignacion`); encabezado de sección "Resultado (datos de ejemplo)".
- **400**: muestra `.alerta.alerta-error` con `error.mensaje`. **401**: redirige a `/login/?next=` + la ruta actual. Error de red: `.alerta.alerta-error` "No se pudo contactar el servidor. Intenta de nuevo."
- Siempre al final: quita `.cargando` y `aria-busy`, y mueve el foco al encabezado del resultado (`tabindex="-1"`).

**`tests/test_simulador.py`** (contenido literal completo):

```python
"""Paso 11: simulador con motor de ejemplo y API JSON protegida."""

import json

import pytest
from django.test import Client
from django.urls import reverse

from web.datos import POLITICAS
from web.simulacion_demo import simular

VALIDOS = {"presupuesto": 100, "recursos": 20, "emergencias": 8, "semilla": 42}


@pytest.fixture
def con_sesion(client):
    client.post(reverse("login"), {"correo": "equipo@cauce.co", "clave": ""})
    return client


def test_motor_es_determinista_por_semilla():
    assert simular(**VALIDOS) == simular(**VALIDOS)
    assert simular(**VALIDOS) != simular(**{**VALIDOS, "semilla": 43})


@pytest.mark.parametrize("semilla", [0, 7, 42, 2026, 9999])
def test_motor_respeta_inventario_y_ordena_politicas(semilla):
    resultado = simular(**{**VALIDOS, "semilla": semilla})
    assert resultado["fuente"] == "datos_de_ejemplo"
    assert len(resultado["asignacion"]) == VALIDOS["emergencias"]
    for politica in POLITICAS:
        asignado = sum(fila[politica] for fila in resultado["asignacion"])
        assert asignado <= VALIDOS["recursos"]
    atendidas = {p: v["necesidades_atendidas_pct"] for p, v in resultado["politicas"].items()}
    assert atendidas["rl"] > atendidas["reglas"] > atendidas["uniforme"]


@pytest.mark.parametrize(
    "cambio", [{"presupuesto": 10}, {"recursos": 99}, {"emergencias": 0}, {"semilla": "x"}]
)
def test_motor_rechaza_parametros_fuera_de_rango(cambio):
    with pytest.raises(ValueError):
        simular(**{**VALIDOS, **cambio})


def test_api_sin_sesion_responde_401(client):
    respuesta = client.post(
        reverse("api_simular"), json.dumps(VALIDOS), content_type="application/json"
    )
    assert respuesta.status_code == 401
    assert respuesta.json()["error"]["codigo"] == "no_autenticado"


def test_api_con_sesion_devuelve_el_formato_del_motor(con_sesion):
    respuesta = con_sesion.post(
        reverse("api_simular"), json.dumps(VALIDOS), content_type="application/json"
    )
    assert respuesta.status_code == 200
    assert respuesta.json() == simular(**VALIDOS)


def test_api_con_parametro_invalido_responde_400(con_sesion):
    respuesta = con_sesion.post(
        reverse("api_simular"),
        json.dumps({**VALIDOS, "recursos": 500}),
        content_type="application/json",
    )
    assert respuesta.status_code == 400
    assert respuesta.json()["error"]["codigo"] == "parametro_invalido"


def test_api_exige_token_csrf():
    cliente = Client(enforce_csrf_checks=True)
    cliente.post(reverse("login"), {"correo": "a@b.co", "clave": ""})
    respuesta = cliente.post(
        reverse("api_simular"), json.dumps(VALIDOS), content_type="application/json"
    )
    assert respuesta.status_code == 403


def test_pagina_del_simulador_tiene_controles_con_etiqueta_y_region_viva(con_sesion):
    html = con_sesion.get(reverse("simulador")).content.decode()
    for nombre in VALIDOS:
        assert f'<label for="id_{nombre}"' in html
        assert f'name="{nombre}" id="id_{nombre}"' in html
    assert 'id="resultado-simulacion" aria-live="polite"' in html
    assert "web/js/simulador.js" in html
    assert "csrfmiddlewaretoken" in html
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se llama `simular()` dos veces con los mismos parámetros THE SYSTEM SHALL devolver resultados idénticos, y otra semilla SHALL cambiar el resultado.
2. WHEN `simular()` se ejecuta con las semillas 0, 7, 42, 2026 y 9999 THE SYSTEM SHALL asignar como máximo `recursos` unidades por política, devolver una fila por emergencia y ordenar necesidades_atendidas_pct como rl > reglas > uniforme.
3. WHEN un parámetro sale de presupuesto 50-150, recursos 5-50, emergencias 3-12 o semilla 0-9999, o no es entero THE SYSTEM SHALL lanzar ValueError, y la API SHALL responder 400 con error.codigo "parametro_invalido".
4. WHEN llega un POST a /app/api/simular/ sin sesión THE SYSTEM SHALL responder 401 con error.codigo "no_autenticado"; con sesión y JSON válido SHALL responder 200 con exactamente `simular(**parametros)`; sin token CSRF con verificación activa SHALL responder 403.
5. WHEN un usuario con sesión abre /app/simulador/ THE SYSTEM SHALL mostrar los campos con etiqueta presupuesto, recursos, emergencias y semilla (ids id_<nombre>), una región `id="resultado-simulacion" aria-live="polite"`, un token CSRF y web/js/simulador.js.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_simulador.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T5: Simulador con motor de ejemplo y API JSON"
git tag step-11-simulador
```

Si la siguiente tarea sale mal: `git reset --hard step-11-simulador` y repetirla.

### `E2-T6` — Mis simulaciones: lista, detalle y estado vacío

**Depends on:** `E2-T5` · **Priority:** p1

La lista de escenarios guardados (hoy, los de ejemplo de `simulaciones.json`) y su detalle. Guardar
simulaciones nuevas queda para la etapa 2, cuando haya base de datos. `views_app.py` es literal.

**Files**
- `web/views_app.py` — reemplazo completo
- `web/templates/web/app/simulaciones.html` — nuevo
- `web/templates/web/app/simulacion_detalle.html` — nuevo
- `tests/test_simulaciones.py` — nuevo (literal)

**`web/views_app.py`** (contenido literal completo):

```python
"""Vistas de acceso (login simulado) y de la aplicación (simulador, simulaciones)."""

import json

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from web import datos
from web.auth_demo import (
    cerrar_sesion,
    correo_valido,
    destino_seguro,
    iniciar_sesion_demo,
    login_requerido,
)
from web.simulacion_demo import LIMITES, simular


def _acceso(request: HttpRequest, modo: str) -> HttpResponse:
    """Login y registro comparten plantilla. Cualquier correo válido entra (modo demostración)."""
    error = ""
    correo = request.POST.get("correo", "")
    nombre = request.POST.get("nombre", "")
    if request.method == "POST":
        if correo_valido(correo.strip()):
            iniciar_sesion_demo(request, correo, nombre)
            return redirect(destino_seguro(request, request.GET.get("next")))
        error = "Escribe un correo válido, por ejemplo nombre@dominio.co"
    titulo = "Iniciar sesión" if modo == "login" else "Crear cuenta"
    return render(
        request,
        "web/acceso.html",
        {"titulo": titulo, "modo": modo, "error": error, "correo": correo, "nombre": nombre},
    )


def login(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "login")


def registro(request: HttpRequest) -> HttpResponse:
    return _acceso(request, "registro")


@require_POST
def salir(request: HttpRequest) -> HttpResponse:
    cerrar_sesion(request)
    return redirect("inicio")


@login_requerido
def simulador(request: HttpRequest) -> HttpResponse:
    return render(request, "web/app/simulador.html", {"titulo": "Simulador", "limites": LIMITES})


@require_POST  # va primero: un GET recibe 405 aunque no haya sesión
@login_requerido
def api_simular(request: HttpRequest) -> JsonResponse:
    try:
        parametros = json.loads(request.body or b"{}")
        if not isinstance(parametros, dict):
            raise ValueError("el cuerpo debe ser un objeto JSON")
        resultado = simular(**{clave: parametros.get(clave) for clave in LIMITES})
    except (json.JSONDecodeError, ValueError) as error:
        return JsonResponse(
            {"error": {"codigo": "parametro_invalido", "mensaje": str(error)}}, status=400
        )
    return JsonResponse(resultado)


@login_requerido
def simulaciones(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/app/simulaciones.html",
        {"titulo": "Mis simulaciones", "simulaciones": datos.simulaciones()},
    )


@login_requerido
def simulacion_detalle(request: HttpRequest, sim_id: str) -> HttpResponse:
    sim = datos.simulacion(sim_id)
    if sim is None:
        raise Http404("Simulación no encontrada")
    return render(request, "web/app/simulacion_detalle.html", {"titulo": sim["nombre"], "sim": sim})
```

**`web/templates/web/app/simulaciones.html`** — extiende `web/base.html`. `<section class="seccion contenedor">` con `<p class="etiqueta">Aplicación</p>`, `<h1>Mis simulaciones</h1>` y:
- `{% for sim in simulaciones %}` una rejilla de `.tarjeta` (1 → 2 → 3 columnas) con `<h2>{{ sim.nombre }}</h2>` (usa el tamaño de `h3` vía clase), `<p class="stat-etiqueta">{{ sim.fecha }}</p>`, un resumen `RL: {{ sim.resultado.necesidades_atendidas_pct.rl }} % atendidas` y `<a class="boton-secundario" href="{% url 'simulacion_detalle' sim.id %}">Ver detalle</a>`;
- `{% empty %}` `<div class="estado-vacio"><p>Aún no hay simulaciones guardadas.</p><a class="boton-primario" href="{% url 'simulador' %}">Ir al simulador</a></div>`;
- debajo, una `.alerta` de nota: "Guardar simulaciones propias llegará cuando el proyecto tenga base de datos (etapa 2)."

**`web/templates/web/app/simulacion_detalle.html`** — extiende `web/base.html`.
`<p class="etiqueta">Simulación · {{ sim.fecha }}</p>`, `<h1>{{ sim.nombre }}</h1>`, una `.tabla`
"Parámetros" (`<th scope="row">` presupuesto, recursos, emergencias, semilla y su valor), una
`.tabla` "Resultado" con filas = métricas de `sim.resultado` y columnas = Uniforme, Reglas, RL, y
`<a href="{% url 'simulaciones' %}">Volver a mis simulaciones</a>`.

**`tests/test_simulaciones.py`** (contenido literal completo):

```python
"""Paso 12: "Mis simulaciones" lista, detalla y maneja el estado vacío."""

import pytest
from django.urls import reverse

from web import datos


@pytest.fixture
def con_sesion(client):
    client.post(reverse("login"), {"correo": "equipo@cauce.co", "clave": ""})
    return client


def test_lista_enlaza_cada_simulacion(con_sesion):
    respuesta = con_sesion.get(reverse("simulaciones"))
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    for sim in datos.simulaciones():
        assert sim["nombre"] in html
        assert f'href="{reverse("simulacion_detalle", args=[sim["id"]])}"' in html


def test_detalle_muestra_parametros_y_resultado(con_sesion):
    sim = datos.simulaciones()[0]
    respuesta = con_sesion.get(reverse("simulacion_detalle", args=[sim["id"]]))
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    assert sim["nombre"] in html
    assert "<table" in html
    for valor in sim["parametros"].values():
        assert str(valor) in html


def test_detalle_inexistente_es_404(con_sesion):
    assert con_sesion.get(reverse("simulacion_detalle", args=["no-existe"])).status_code == 404


def test_estado_vacio_invita_a_simular(con_sesion, monkeypatch):
    monkeypatch.setattr("web.views_app.datos.simulaciones", lambda: [])
    html = con_sesion.get(reverse("simulaciones")).content.decode()
    assert "Aún no hay simulaciones guardadas" in html
    assert f'href="{reverse("simulador")}"' in html


def test_simulaciones_requiere_sesion(client):
    respuesta = client.get(reverse("simulaciones"))
    assert respuesta.status_code == 302
    assert respuesta["Location"].startswith(reverse("login"))
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN un usuario con sesión abre /app/simulaciones/ THE SYSTEM SHALL listar cada simulación de simulaciones.json por su `nombre` con un enlace a /app/simulaciones/<id>/.
2. WHEN un usuario con sesión abre /app/simulaciones/<id>/ con un id existente THE SYSTEM SHALL responder 200 con el nombre, una <table> y cada valor de los parámetros; con un id inexistente SHALL responder 404.
3. WHEN no hay simulaciones THE SYSTEM SHALL mostrar "Aún no hay simulaciones guardadas" y un enlace a /app/simulador/.
4. WHEN un visitante anónimo abre /app/simulaciones/ THE SYSTEM SHALL redirigir con 302 a una URL que empieza por /login/.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_simulaciones.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T6: Mis simulaciones: lista, detalle y estado vacío"
git tag step-12-simulaciones
```

Si la siguiente tarea sale mal: `git reset --hard step-12-simulaciones` y repetirla.

### `E2-T7` — Revisión automática de accesibilidad

**Depends on:** `E2-T3`, `E2-T6` · **Priority:** p1

Una prueba recorre todas las páginas HTML (públicas, de la app con sesión, detalle, 404 y guía de
estilo) y verifica lo que se puede decidir sin navegador: un `<h1>`, sin estilos ni manejadores en
línea, `alt` en imágenes, canvas descritos, campos con etiqueta, enlaces externos seguros y zoom
permitido. Si falla, **se corrigen las plantillas**, nunca la prueba.

**Files**
- `tests/test_accesibilidad.py` — nuevo (literal)
- `web/templates/**/*.html` — solo correcciones que pida la prueba

**`tests/test_accesibilidad.py`** (contenido literal completo):

```python
"""Paso 13: revisión automática de accesibilidad sobre todas las páginas HTML."""

from html.parser import HTMLParser

import pytest
from django.urls import reverse

from web import datos

PUBLICAS = ["inicio", "metodologia", "resultados", "login", "registro"]
DE_LA_APP = ["simulador", "simulaciones"]


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.etiquetas: list[tuple[str, dict]] = []
        self.labels_for: set[str] = set()
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        atributos = {k: (v or "") for k, v in attrs}
        self.etiquetas.append((tag, atributos))
        if tag == "label" and "for" in atributos:
            self.labels_for.add(atributos["for"])
        if tag == "h1":
            self.h1 += 1


def _inspeccionar(html: str) -> Inspector:
    inspector = Inspector()
    inspector.feed(html)
    return inspector


def _revisar(html: str) -> None:
    pagina = _inspeccionar(html)
    assert pagina.h1 == 1, "debe haber exactamente un <h1>"
    for tag, attrs in pagina.etiquetas:
        assert "style" not in attrs, f"estilo en línea en <{tag}>"
        assert not any(a.startswith("on") for a in attrs), f"manejador en línea en <{tag}>"
        if tag == "img":
            assert "alt" in attrs, "imagen sin alt"
        if tag == "canvas":
            assert attrs.get("aria-hidden") == "true" or (
                attrs.get("role") == "img" and attrs.get("aria-label")
            ), "canvas sin descripción"
        if tag == "a" and attrs.get("target") == "_blank":
            assert "noopener" in attrs.get("rel", ""), "target=_blank sin rel=noopener"
        if tag == "input" and attrs.get("type") not in ("hidden", "submit", "button"):
            assert attrs.get("id") in pagina.labels_for, f"campo sin <label>: {attrs}"
        if tag == "meta" and attrs.get("name") == "viewport":
            assert "user-scalable=no" not in attrs.get("content", "")
            assert "maximum-scale=1" not in attrs.get("content", "")


@pytest.fixture
def con_sesion(client):
    client.post(reverse("login"), {"correo": "equipo@cauce.co", "clave": ""})
    return client


@pytest.mark.parametrize("nombre", PUBLICAS)
def test_paginas_publicas_accesibles(client, nombre):
    _revisar(client.get(reverse(nombre)).content.decode())


@pytest.mark.parametrize("nombre", DE_LA_APP)
def test_paginas_de_la_app_accesibles(con_sesion, nombre):
    _revisar(con_sesion.get(reverse(nombre)).content.decode())


def test_detalle_de_simulacion_accesible(con_sesion):
    sim_id = datos.simulaciones()[0]["id"]
    _revisar(con_sesion.get(reverse("simulacion_detalle", args=[sim_id])).content.decode())


def test_paginas_de_error_accesibles(client):
    _revisar(client.get("/pagina-que-no-existe/").content.decode())


def test_styleguide_accesible(client, settings):
    settings.DEBUG = True
    _revisar(client.get(reverse("styleguide")).content.decode())
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se analizan todas las páginas públicas, las de la app con sesión, un detalle de simulación, la página 404 y la guía de estilo (con DEBUG) THE SYSTEM SHALL encontrar exactamente un <h1> en cada una.
2. WHEN se analizan esas páginas THE SYSTEM SHALL no encontrar atributos style en línea ni manejadores on* en línea en ningún elemento.
3. WHEN se analizan esas páginas THE SYSTEM SHALL encontrar alt en cada <img>, role="img" con aria-label (o aria-hidden="true") en cada <canvas>, rel="noopener" en cada enlace target="_blank" y un <label for> para cada <input> visible.
4. WHEN se analiza la meta viewport THE SYSTEM SHALL no contener user-scalable=no ni maximum-scale=1.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_accesibilidad.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E2-T7: Revisión automática de accesibilidad"
git tag step-13-accesibilidad
```

Si la siguiente tarea sale mal: `git reset --hard step-13-accesibilidad` y repetirla.

---

## Epic acceptance

El epic está hecho cuando las siete tareas están `done` **y**:

1. **WHEN** un usuario anónimo recorre inicio → simulador **THE SYSTEM SHALL** llevarlo a `/login/?next=…`, y tras entrar con cualquier correo válido SHALL volver al simulador, donde `POST /app/api/simular/` responde 200 (cubierto por `test_acceso.py` y `test_simulador.py`).
2. **WHEN** la suite completa corre desde la raíz **THE SYSTEM SHALL** terminar con código 0, 0 fallas y 0 advertencias, y ruff limpio, incluyendo `tests/test_estilos.py` sobre todo el CSS nuevo.

```bash
sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check . && sh scripts/py -m pytest
sh scripts/py -m pytest tests/test_accesibilidad.py tests/test_estilos.py
```

Revisión manual antes de la presentación (no bloquea tareas): recorrer el sitio solo con teclado,
probarlo a 375px y a 1440px de ancho, y abrir /resultados/ con la red del navegador bloqueando
cdnjs para ver las tablas alternativas.

## Pitfalls

- **Escribir `request.session["cauce_usuario_demo"]` en una vista** — rompe el punto de reemplazo de la etapa 2. Usa `get_current_user()`.
- **Invertir los decoradores de `api_simular`** — `@login_requerido` encima convierte el GET anónimo en 401 y rompe `tests/test_rutas.py`.
- **Pintar el resultado con `innerHTML`** usando datos de la API — usa `textContent` / `createElement`.
- **Colores de Chart.js escritos en hex en `graficas.js`** — lee los tokens; si cambia la paleta, cambia en un solo lugar.
- **Una prueba que falla por la página 404 o la guía de estilo en `E2-T7`** — corrige `404.html` o `styleguide.html`; están dentro del glob de la tarea.

## Before moving on

- [ ] Las siete tareas están `done` en `tasks.json`; ninguna quedó `in_progress`.
- [ ] Pasaron todos los comandos `verify` de cada tarea, no solo el primero.
- [ ] Ningún comando `verify` se editó ni se saltó.
- [ ] Cada tarea tiene su etiqueta: `git tag -l 'step-*'` lista de `step-07-styleguide` a `step-13-accesibilidad` (y las seis de la etapa 0).
- [ ] El gate pasa limpio desde la raíz.
- [ ] Existen los contratos "Produced" con las firmas indicadas.
- [ ] Ningún archivo fuera del árbol del epic se modificó.
- [ ] `.env.example` sin cambios (este epic no agrega variables de entorno).
- [ ] Un commit por tarea, con el prefijo de su id y seguido de su etiqueta.
