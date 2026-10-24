# Cauce — Blueprint

> Generado por The Architect el 2026-10-24
> Forma: aplicación web con cuentas (SaaS sin cobro) · `knowledge/shapes/saas-webapp.md`
> Pista de ejecución: Python (Django) · `knowledge/runtime-tracks/python.md`
> Modo de emisión: bundle (13 pasos)
> Versión del blueprint: 1
> Versiones verificadas: 2026-10-24 — ver §11 para la procedencia de cada paquete

**Cómo leer este bundle.** `blueprint.md` (este archivo) explica el *porqué* y el diseño completo.
`tasks.json` dice *qué sigue*. `epics/01-etapa-0-montaje.md` y `epics/02-etapa-1-interfaz.md`
dicen *cómo*: traen el **contenido literal** de cada archivo de Python, de las pruebas, de los JSON
y de `tokens.css`, más la especificación exacta de cada plantilla, CSS y JS. `workspace/` se copia
a la raíz del proyecto en el Bootstrap (§10). Todo comando se ejecuta desde la raíz del proyecto
(la carpeta que contiene `docs/` y `blueprints/`).

---

## 1. Project Overview & Non-Goals

### Vision

Cauce es la página web de un proyecto universitario de aprendizaje por refuerzo (6.º semestre)
que responde **"¿quién recibe ayuda primero y en qué cantidad?"** cuando varios municipios de
Colombia enfrentan emergencias a la vez. El proyecto toma los registros históricos de la UNGRD
(Emergencias UNGRD V2, Datos Abiertos Colombia), agrupa las emergencias en perfiles con K-means y
entrena un agente (Q-learning) en una simulación propia para compararlo con una política uniforme
y otra basada en reglas, bajo restricciones de presupuesto e inventario.

La página existe para que el docente evalúe el proyecto (y después como portafolio): presenta el
problema, la metodología y los resultados con gráficas accesibles, y deja probar un simulador en
vivo detrás de un login. **Esta etapa construye solo lo visible**, con datos de ejemplo y un login
simulado, sobre un contrato de datos y una API cuyo formato ya es el definitivo: en la etapa 3 los
notebooks reemplazan los JSON y el motor de ejemplo por el agente real sin tocar las páginas.

### Users

| Persona | What they come to do | Frequency |
|---|---|---|
| Docente evaluador | Entender el problema y la metodología, ver resultados, probar el simulador | En cada revisión (pocas veces) |
| Equipo (2 estudiantes) | Construir, revisar la guía de estilo, conectar resultados reales | A diario durante un mes |
| Visitante del portafolio | Recorrer la portada y los resultados sin registrarse | Ocasional |

### Goals — v1 scope

1. El sitio está publicado en Render desde GitHub con una portada que explica el proyecto (etapa 0, hoy).
2. Metodología y resultados se pueden leer sin cuenta, con cuatro gráficas y sus tablas alternativas.
3. Un login simulado protege `/app/`: simulador (motor de ejemplo vía API JSON) y "Mis simulaciones".
4. Todo el sitio aplica el sistema de diseño de `docs/design/` corregido (§7) y pasa una revisión automática de accesibilidad.
5. Los datos entran por un contrato validado (`web/datos.py`), listo para resultados reales.

### Non-Goals — explicitly out of scope for v1

| Not building | Why not now | Revisit when |
|---|---|---|
| Login real con contraseñas y base de datos | El equipo pidió un login vacío; Django auth se conecta en `web/auth_demo.py` | Etapa 2 (semana del 4 nov), cuando el docente pida cuentas reales |
| Guardar simulaciones propias | Requiere base de datos; el disco de Render Free se borra en cada reinicio | Etapa 2, junto con la base de datos |
| Entrenar o ejecutar el agente RL real en la web | El agente aún no existe; el motor de ejemplo tiene su misma firma | Etapa 3, cuando los notebooks tengan la tabla Q |
| PyTorch / stable-baselines3 / PPO / DQN en el servidor | No caben en 512 MB de RAM del plan Free | Si se pasa a un plan pago o se sirve solo la política exportada |
| Modo claro | El sistema de diseño es oscuro por definición | Si el docente lo pide para proyectar |
| Pagos, roles, equipos u organizaciones | No hay cobro ni varios inquilinos | Nunca en este proyecto |
| Mapa geográfico de Colombia | Requiere geodatos y una librería de mapas; no está en el diseño | Etapa 3, si los datos por municipio lo justifican |
| Uso del nombre, logo o esfera de partículas de Auros | `docs/design/` se extrajo del sitio de una empresa real; se usa solo el estilo | Nunca |

**El constructor no implementa nada de esta tabla**, aunque parezca un agregado pequeño. Si un paso
parece requerirlo, es un defecto del blueprint: detente e informa.

### Success metrics

| Metric | Target | How measured |
|---|---|---|
| Sitio publicado | URL `*.onrender.com` respondiendo 200 en `/health/` hoy, 2026-10-24 | Health Check de Render en verde |
| Construcción completa de etapas 0 y 1 | 13/13 tareas `done` antes del 2026-11-03 | `tasks.json` y `git tag -l 'step-*'` |
| Calidad | Gate verde: ruff limpio, `pytest` con 0 fallas y 0 advertencias | §20.1 |
| Accesibilidad | 0 fallas en `tests/test_accesibilidad.py`; contraste ≥ 4.5:1 en todo texto | §15 |

---

## 2. Tech Stack

**Runtime track: Python.** Esta tabla nombra *decisiones*; las versiones están solo en §11.

| Layer | Choice | Why this, over what |
|---|---|---|
| Language / runtime | Python (fijado en `.python-version`, mínimo 3.12) | El proyecto es de ML en Python; el equipo ya trabaja ahí. TypeScript obligaría a un segundo servicio para el modelo |
| Framework | Django con sus plantillas; **rutas en `app.py`** | Trae sesiones, CSRF, ORM, migraciones y auth para la etapa 2. FastAPI obligaría a armar el login a mano. Flask (el `requirements.txt` original) se descartó con el usuario por la misma razón. `app.py` como tabla de rutas lo pidió el usuario |
| Styling | CSS propio con tokens (`tokens.css`) | Sin Node ni compilación: Render solo instala Python. Tailwind v4 exigiría un paso de build |
| Component layer | Clases CSS propias en `components.css` + plantillas parciales | El sistema de diseño es pequeño (≈20 componentes); una librería de componentes impondría su estética |
| Gráficas | Chart.js desde cdnjs con hash de integridad | Barras, líneas y dispersión accesibles sin build; recomendado por ui-ux-pro-max para comparar categorías y tendencias |
| Database | Ninguna en uso; SQLite declarado | La etapa 1 no persiste nada; la etapa 2 cambia el bloque `DATABASES` |
| ORM / data access | `web/datos.py` sobre JSON | Un contrato validado que los notebooks pueden reutilizar; el ORM llega con la etapa 2 |
| Auth | Login simulado en sesión firmada (`web/auth_demo.py`) | Pedido explícito del usuario; una sola función (`get_current_user`) es el punto de reemplazo por `django.contrib.auth` |
| Background work | NOT APPLICABLE — el motor de ejemplo responde en milisegundos dentro de la petición | — |
| Payments | NOT APPLICABLE — no hay cobro | — |
| File storage | NOT APPLICABLE — no se suben archivos | — |
| Email / notifications | NOT APPLICABLE — el login simulado no envía correos | — |
| Hosting | Render, Web Service plan Free, gunicorn + WhiteNoise | Elegido por el usuario; lo configura el propio equipo con los valores del README |
| Package manager | pip con `requirements.txt` (web), `requirements-dev.txt`, `requirements-ml.txt` | Pedido explícito del usuario; sin `uv.lock` para que Render no cambie de instalador |

### Compatibility check

Revisado contra `knowledge/stack-compatibility.md`: ninguna combinación conocida como mala. No hay
CSS con at-rules de un motor de utilidades (sin Tailwind), un solo proveedor de identidad (el login
simulado, luego Django auth), un solo sistema de migraciones (ninguno en la etapa 1) y el host es
un proceso de larga duración (gunicorn), adecuado para Django.

---

## 3. Directory Structure

```
UNGDR/                                  # raíz del proyecto (= raíz del repositorio)
  app.py                                # tabla ÚNICA de rutas (ROOT_URLCONF = "app"); `python app.py` = runserver · E1-T1, E1-T4
  manage.py                             # generado por el Bootstrap (django startproject)
  config/
    __init__.py, asgi.py, wsgi.py       # generados por el Bootstrap; Render arranca config.wsgi
    settings.py                         # reemplazado en E1-T1 (literal)
  web/                                  # la única aplicación Django
    __init__.py, apps.py                # workspace/
    views.py                            # páginas públicas (Persona A) · E1-T1, E1-T4, E1-T5, E2-T1, E2-T2, E2-T3
    views_app.py                        # acceso y app (Persona B) · E1-T4, E2-T4, E2-T5, E2-T6
    context_processors.py               # `sitio` y `usuario` en todas las plantillas · E1-T1, E2-T4
    datos.py                            # contrato de datos · E1-T2
    auth_demo.py                        # login simulado · E2-T4
    simulacion_demo.py                  # motor de ejemplo · E2-T5
    data/mock/resultados.json           # E1-T2
    data/mock/perfiles.json             # E1-T2
    data/mock/simulaciones.json         # E1-T2
    templates/404.html, 500.html        # E1-T6
    templates/web/base.html             # E1-T4
    templates/web/inicio.html           # E1-T5
    templates/web/styleguide.html       # E2-T1
    templates/web/metodologia.html      # E2-T2
    templates/web/resultados.html       # E2-T3
    templates/web/acceso.html           # E2-T4
    templates/web/app/simulador.html    # E2-T5
    templates/web/app/simulaciones.html, simulacion_detalle.html   # E2-T6
    static/web/css/tokens.css, base.css, components.css            # E1-T3 (components se amplía en E2-T1)
    static/web/css/pages/inicio.css     # E1-T5
    static/web/css/pages/metodologia.css   # E2-T2
    static/web/css/pages/resultados.css    # E2-T3
    static/web/js/red.js                # E1-T5
    static/web/js/graficas.js           # E2-T3
    static/web/js/simulador.js          # E2-T5
  tests/                                # una prueba por paso, literal en los epics
    test_health.py · test_datos.py · test_estilos.py · test_rutas.py · test_inicio.py
    test_produccion.py · test_styleguide.py · test_metodologia.py · test_resultados.py
    test_acceso.py · test_simulador.py · test_simulaciones.py · test_accesibilidad.py
  scripts/py                            # workspace/ · ejecuta el Python de .venv (Git Bash y Unix)
  requirements.txt                      # workspace/ · web (lo que instala Render)
  requirements-dev.txt                  # workspace/ · + ruff, pytest, pytest-django
  requirements-ml.txt                   # workspace/ · librerías de los notebooks (no las instala Render)
  .python-version · ruff.toml · pytest.ini · .gitignore · .gitattributes · .env.example   # workspace/
  CLAUDE.md · AGENTS.md · .claude/      # workspace/ (§19)
  README.md                             # E1-T6 (literal)
  docs/                                 # del usuario: contexto y sistema de diseño de referencia
  blueprints/cauce/                     # este bundle (se sube al repo; excluido de ruff y pytest)
  .venv/ · staticfiles/                 # generados, ignorados por git
```

**Boundary rules**
- `app.py` es el único archivo con `urlpatterns`; no existen `config/urls.py` ni `urls.py` por app.
- Solo `web/datos.py` abre los JSON; solo `web/auth_demo.py` lee la clave de sesión del usuario.
- `web/datos.py` y `web/simulacion_demo.py` no importan Django (reutilizables desde notebooks).
- Solo `config/settings.py` lee variables de entorno.

Convención de importación: los módulos propios se importan por nombre de paquete desde la raíz
(`from web import datos`, `from web.auth_demo import …`); ver la matriz de §19.6.

---

## 4. Data Model

No hay tablas en la etapa 1. Las "entidades" son documentos JSON validados por `web/datos.py`
(contenido literal de los tres archivos en `epics/01-etapa-0-montaje.md`, tarea `E1-T2`).

**Resultados** (`resultados.json`) — métricas de la comparación de políticas.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `fuente` | str | `"datos_de_ejemplo"` hoy | Pasa a `"resultados_reales"` en la etapa 3 |
| `resumen` | list[{id, valor, etiqueta}] | exactamente 4 | Cifras de la portada; `valor` ya formateado (texto) |
| `politicas` | list[{id, nombre}] | ids `uniforme`, `reglas`, `rl` en ese orden | Nombres de leyenda |
| `metricas` | list[{id, nombre, unidad, mejor, valores}] | `mejor` ∈ {mayor, menor}; `valores` con las 3 políticas | 4 métricas del diseño experimental |
| `recompensa_por_episodio` | {episodios: list[int], series: {política: list[float]}} | cada serie mide lo mismo que `episodios` | Curva de aprendizaje |
| `sensibilidad_presupuesto` | {presupuesto_pct: list[int], series} | ídem | Robustez frente al presupuesto |
| `estabilidad` | {desviacion_recompensa: {política: float}, semillas: int} | 3 políticas | Variabilidad entre semillas |

**Perfiles** (`perfiles.json`) — K-means.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `k` | int | = número de perfiles | |
| `ejes` | {x: str, y: str} | | Rótulos de la dispersión |
| `perfiles` | list[{id, nombre, descripcion, n_eventos, centroide}] | ids únicos | |
| `puntos` | list[{x, y, perfil}] | `perfil` ∈ ids de `perfiles` | Muestra para la dispersión |

**Simulación guardada** (`simulaciones.json` → `simulaciones[]`).

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `id` | str (slug) | único | Aparece en la URL `/app/simulaciones/<id>/` |
| `nombre`, `fecha` | str | | |
| `parametros` | {presupuesto, recursos, emergencias, semilla} | enteros | Mismos nombres que la API |
| `resultado` | {métrica: {política: número}} | 3 políticas por métrica | |

**Usuario de la sesión** — `{"correo": str en minúsculas, "nombre": str}` bajo la clave
`cauce_usuario_demo` de la sesión (cookie firmada). No se persiste en ningún otro lugar.

### Relationships
`punto —(N:1)→ perfil` por `perfil`; no hay borrados (los datos son de solo lectura).

### Indexes
NOT APPLICABLE — no hay base de datos en la etapa 1.

### Schema
El esquema es el validador de `web/datos.py` (`validar_resultados`, `validar_perfiles`,
`validar_simulaciones`), literal en `epics/01-etapa-0-montaje.md`, tarea `E1-T2`.

### Migrations
NOT APPLICABLE en la etapa 1 (ninguna app con modelos instalada). En la etapa 2: migraciones de
Django, aplicadas como paso de release (`python manage.py migrate` antes de arrancar), nunca
destructivas en el mismo despliegue que el cambio de código.

### Seed data
Los tres JSON de ejemplo son la semilla: el sitio funciona en el primer arranque sin preparar nada.

---

## 5. API Design

### Conventions
- Base path: `/app/api/` (solo una ruta en v1).
- Respuesta de éxito: la salida de `simular()` tal cual. Error: `{"error": {"codigo": "<snake_case>", "mensaje": "<texto>"}}`.
- Códigos: `parametro_invalido` → 400 · `no_autenticado` → 401 · CSRF ausente → 403 (página de Django) · método distinto de POST → 405.
- Validación: `web.simulacion_demo.validar_parametros` (rangos en `LIMITES`).
- Paginación, idempotencia y límite de tasa: NOT APPLICABLE en v1 (cálculo determinista y barato; sin escrituras).

### Routes

| Method | Path | Description | Auth | Rate limit |
|---|---|---|---|---|
| GET | `/` | Portada | pública | — |
| GET | `/metodologia/` | Metodología | pública | — |
| GET | `/resultados/` | Panel de resultados | pública | — |
| GET | `/styleguide/` | Guía de estilo (404 si `DEBUG` es False) | pública en desarrollo | — |
| GET | `/health/` | Chequeo de salud `{"status": "ok", "app": "cauce"}` | pública | — |
| GET, POST | `/login/`, `/registro/` | Login / registro simulados | pública | — |
| POST | `/salir/` | Cierra la sesión | — | — |
| GET | `/app/simulador/` | Simulador | sesión | — |
| POST | `/app/api/simular/` | Ejecuta el motor de ejemplo | sesión + CSRF | — |
| GET | `/app/simulaciones/`, `/app/simulaciones/<id>/` | Lista y detalle | sesión | — |

### Critical endpoints — full detail

**`POST /app/api/simular/`** — cuerpo JSON `{"presupuesto": int 50–150, "recursos": int 5–50,
"emergencias": int 3–12, "semilla": int 0–9999}`. 200 → `{"fuente", "parametros", "politicas":
{"uniforme"|"reglas"|"rl": {"necesidades_atendidas_pct", "emergencias_sin_recursos",
"costo_total_mcop"}}, "asignacion": [{"municipio", "evento", "gravedad", "uniforme", "reglas",
"rl"}]}` ordenada por gravedad descendente, con una fila por emergencia y como máximo `recursos`
unidades por política. Errores: cuerpo no JSON, no objeto, parámetro ausente/no entero/fuera de
rango → 400 `parametro_invalido`; sin sesión → 401 `no_autenticado`; sin token CSRF → 403; GET →
405. Sin efectos secundarios. Código literal: `epics/02-etapa-1-interfaz.md`, tarea `E2-T5`.

**`POST /login/`** — formulario `correo`, `clave` (ignorada), `nombre` (solo registro). Correo
válido → sesión con `{correo, nombre}` y 302 a `next` si es interno, o a `/app/simulador/`.
Correo inválido → 200 con el error junto al campo. Literal en `E2-T4`.

---

## 6. Frontend Architecture

### Routes
| Route | Page | Data source | Auth |
|---|---|---|---|
| `/` | Portada | `datos.resultados()["resumen"]` | pública |
| `/metodologia/` | Metodología | `datos.perfiles()` + `FORMULACION` en `views.py` | pública |
| `/resultados/` | Resultados | `datos.resultados()`, `datos.perfiles()` → `json_script` | pública |
| `/login/`, `/registro/` | Acceso | — | pública |
| `/app/simulador/` | Simulador | `LIMITES` + API `fetch` | sesión |
| `/app/simulaciones/` y detalle | Mis simulaciones | `datos.simulaciones()` / `datos.simulacion(id)` | sesión |
| `/styleguide/` | Guía de estilo | constantes de `views.py` | solo `DEBUG` |

### Rendering strategy
Todo se renderiza en el servidor con plantillas de Django en cada petición (sin caché: los datos
son archivos pequeños en memoria gracias a `functools.cache`). El JavaScript es mejora progresiva:
`red.js` (decorativo), `graficas.js` (dibuja sobre datos ya presentes en tablas) y `simulador.js`
(única interacción que depende de JS).

### Component hierarchy
```
base.html
├── a.saltar-contenido
├── header.cabecera → a.logo · nav.nav-principal (4 enlaces) · acciones (usuario | login + CTA) · details.menu-movil
├── p.insignia-demo (si CAUCE_DATOS_DEMO)
├── main#contenido → {% block contenido %}
│   ├── inicio.html: section.hero (canvas#red-hero) · cifras (4 .stat) · 3 article.tarjeta[data-paso] · tarjeta-hundida
│   ├── resultados.html: 4 tarjetas .stat · 4 .panel-grafica (canvas + details>table) · json_script ×2
│   └── app/simulador.html: .dividido → form#form-simulador.tarjeta · #resultado-simulacion[aria-live]
└── footer.pie
```

### State management
Sin estado global en el cliente. El único estado de servidor es la sesión (usuario simulado). El
simulador guarda su último resultado solo en el DOM. Nada en `localStorage`.

### Loading, empty, and error states
| Superficie | Cargando | Vacío | Error |
|---|---|---|---|
| Simulador | `.cargando` + `aria-busy="true"` | mensaje inicial "Ajusta los controles…" | `.alerta-error` con el mensaje de la API o de red; 401 → login |
| Mis simulaciones | — (renderizado en servidor) | `.estado-vacio` con enlace al simulador | 404 propio en detalle inexistente |
| Resultados | gráficas se dibujan al cargar | — | sin Chart.js: se abren las tablas `<details>` |
| Login | — | — | error junto al campo con `aria-invalid` |

---

## 7. Design System

Producido con **ui-ux-pro-max** a partir de `docs/design/` (DESIGN.md, tokens.json, variables.css,
theme.css). Valores literales en `web/static/web/css/tokens.css` (literal en `E1-T3`).

### Colors
| Token | Light | Dark | Usage |
|---|---|---|---|
| `--color-teal` (primario de datos) | NOT APPLICABLE — sin modo claro | `#00827c` | Series de "reglas", degradado; nunca texto |
| `--color-sobre-aurora` (texto sobre primario) | — | `#012624` | Texto del botón primario sobre `--gradiente-aurora` |
| `--color-fondo` (background) | — | `#012624` | Página |
| `--color-alga` (surface) | — | `#003734` | Tarjetas, botón secundario |
| `--color-abismo` | — | `#011d1c` | Pie, paneles hundidos, fondo de gráficas, campos |
| `--color-borde` / `--color-borde-control` (border) | — | `rgba(255,255,255,0.12)` / `#869a99` | Separadores / bordes de campos |
| `--color-texto` (fg) | — | `#bbc7c6` | Cuerpo |
| `--color-titulo` / `--color-texto-enfasis` | — | `#ffffff` / `#edfffe` | Títulos / etiquetas y énfasis |
| `--color-cifra` | — | `#fde9ff` | Cifras grandes (`.stat`) y serie RL |
| `--color-error` (destructive) | — | `#ffb4a9` | Errores |
| `--color-exito` (success) / `--color-aviso` | — | `#7ee2b8` / `#ffd479` | Confirmaciones / aviso de datos de ejemplo |
| `--color-foco` | — | `#cbfffc` | Anillo de foco de 2px |
| `--gradiente-aurora` | — | `#cbfffc → #edfffe → #fffdfa → #fad1ff` | Solo el botón primario |

**Contraste (medido):** texto `#bbc7c6` sobre `#012624` = **9.28:1** y sobre `#003734` = 7.58:1;
`#012624` sobre el degradado aurora ≥ **11.99:1**; borde de campo `#869a99` sobre `#003734` =
**4.45:1** (≥ 3:1 de componente). `#707777` (3.52:1) y `#00827c` (3.44:1) **no se usan como texto**.

Correcciones aplicadas a `docs/design/`: Matter (de pago) → Inter; botón primario de radio 6px (se
descarta el 9999px contradictorio); relleno de botón 32px → 12×24px con alto mínimo 44px;
`--card-padding: 36-48px` (CSS inválido) → `clamp(24px, 3vw, 48px)`; títulos fijos de 96/295px →
tamaños fluidos con `clamp()`; etiquetas de 10px → 12px; tracking 0.24em → 0.12em; se agregan
error/aviso/éxito/foco; se excluye el texto de 295px y la esfera de partículas de la marca original.

### Typography
| Role | Family | Size / line-height | Weight | Tracking |
|---|---|---|---|---|
| Display | Inter | `clamp(2.5rem, 1.5rem + 5vw, 6rem)` / 1 | 500 | -0.04em |
| Heading | Inter | h1 `clamp(2.1rem, 1.4rem + 3.5vw, 3.8rem)`, h2 `clamp(1.75rem, 1.2rem + 2vw, 2.25rem)`, h3 1.5rem / 1 | 500 | -0.04em / -0.02em |
| Body | Inter | 1rem / 1.5 | 400 | 0 |
| Etiqueta | Inter | 0.75rem mayúsculas | 500 | 0.12em |
| Mono | NOT APPLICABLE — cifras con `font-variant-numeric: tabular-nums` en Inter | — | — | — |

**Font loading:** Google Fonts CSS2 `family=Inter:wght@400;500&display=swap` con `preconnect`;
respaldo `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.

### Spacing, radius, elevation
- Espaciado: base 4px — 4, 8, 12, 16, 20, 24, 32, 36, 40, 48, 64, 80, 120 (`--esp-1` … `--esp-30`).
- Radio: 6px botones, campos e insignias; 16px tarjetas y paneles. Nada más.
- Sombras: ninguna (`box-shadow` prohibido salvo `none`); la profundidad es el color de la superficie (abismo < fondo < alga).
- Ancho máximo 1440px; márgenes 16/24/48px; cortes 768px y 1024px; texto a 65ch.

### Motion
150ms (hover, foco) y 250ms (aparición), curva `cubic-bezier(0.2, 0, 0, 1)`, solo `transform` y
`opacity`. Dos animaciones en todo el sitio: el grafo de la portada y la transición de los
botones. `prefers-reduced-motion: reduce` deja el grafo estático y apaga transiciones y Chart.js.

### Component style
"Terminal de aguas profundas": lienzo verde azulado casi negro, tarjetas que flotan un tono más
claro sin sombra, etiquetas pequeñas en mayúsculas con mucho espaciado, cifras enormes en lavanda y
un único botón con degradado aurora por sección. Un componente nuevo pertenece si usa solo
superficies del trío abismo/fondo/alga, radios 6/16 y pesos 400/500. Referencia analizada:
`docs/design/DESIGN.md` (estilo extraído de auros.global; solo el estilo, nunca la marca).

---

## 8. Authentication & Authorization

### Provider and rationale
Login **simulado** (`web/auth_demo.py`) sobre sesión de Django en cookie firmada. Pedido explícito
del usuario: "un login vacío sin seguridad", con la posibilidad de conectar una base de datos
después. La etapa 2 reemplaza el interior de las funciones por `django.contrib.auth`.

### Flows
- **Login**: `/login/` → correo válido → sesión `{correo, nombre=parte local del correo}` → 302 a `next` interno o `/app/simulador/`. Correo inválido → error junto al campo.
- **Registro**: `/registro/` igual, con `nombre`. No hay verificación de correo (no hay correos).
- **Sesión**: dura lo que la cookie de sesión de Django por defecto (2 semanas); `cycle_key()` al entrar.
- **Salir**: `POST /salir/` → `session.flush()` → `/`.
- **Restablecer clave / borrar cuenta**: NOT APPLICABLE — no hay claves ni cuentas persistidas.

### Route protection
| Surface | Rule | Enforced where |
|---|---|---|
| `/app/*` páginas | sesión → si no, 302 a `/login/?next=` | `web/auth_demo.py` `login_requerido`, aplicado en `web/views_app.py` |
| `/app/api/*` | sesión → si no, 401 JSON | mismo decorador (detecta el prefijo `/app/api/`) |
| `/styleguide/` | `DEBUG` → si no, 404 | `web/views.py` |

**Enforcement rule:** la autorización se comprueba en el servidor en cada petición; ocultar enlaces no es seguridad.

### Roles and permissions
| Role | Can | Cannot |
|---|---|---|
| Anónimo | Ver portada, metodología, resultados; entrar | Usar `/app/` |
| Usuario simulado | Todo lo anterior + simulador y mis simulaciones | Nada administrativo (no existe) |

### Sessions
Backend `signed_cookies` (sin base de datos), `HttpOnly`, `Secure` en Render, `SameSite=Lax`
(valor por defecto de Django). CSRF con el middleware de Django: formularios con `{% csrf_token %}` y
el `fetch` del simulador con el encabezado `X-CSRFToken`.

### Multi-tenancy / row-level isolation
NOT APPLICABLE — no hay datos por usuario en la etapa 1.

---

## 9. BUILD ORDER

Las reglas de cada paso: un paso por sesión; cada uno con **Do**, **Done when**, **Verify** y
**Checkpoint**; los criterios en forma EARS; `Verify` es shell literal desde la raíz y sale con 0
cuando el paso está bien; nunca se adelanta un paso; un paso no rompe el `Verify` de uno anterior
(cada `Verify` termina con la suite completa `sh scripts/py -m pytest`).

**En bundle, la fuente de ejecución son `tasks.json` y los epics**: el **Do** de cada paso de abajo
resume y apunta a la tarea del epic que trae el contenido literal y las especificaciones. Los
criterios y comandos son idénticos en los tres lugares.

### Step map

| # | Step | Depends on | Touches | Gate |
|---|---|---|---|---|
| 1 | Django + `/health/` (E1-T1) | — | `config/settings.py`, `app.py`, `web/views.py`, `web/context_processors.py`, `tests/test_health.py` | `sh scripts/py -m pytest tests/test_health.py` |
| 2 | Contrato de datos (E1-T2) | 1 | `web/data/mock/*.json`, `web/datos.py`, `tests/test_datos.py` | `… tests/test_datos.py` |
| 3 | Tokens y CSS base (E1-T3) | 1 | `tokens.css`, `base.css`, `components.css`, `tests/test_estilos.py` | `… tests/test_estilos.py` |
| 4 | Rutas y plantilla base (E1-T4) | 3 | `app.py`, `web/views.py`, `web/views_app.py`, `base.html`, `tests/test_rutas.py` | `… tests/test_rutas.py` |
| 5 | Portada (E1-T5) | 2, 4 | `web/views.py`, `inicio.html`, `inicio.css`, `red.js`, `tests/test_inicio.py` | `… tests/test_inicio.py` |
| 6 | Producción y README (E1-T6) | 5 | `README.md`, `404.html`, `500.html`, `tests/test_produccion.py` | `… tests/test_produccion.py` |
| 7 | Componentes y guía de estilo (E2-T1) | 6 | `web/views.py`, `styleguide.html`, `components.css`, `tests/test_styleguide.py` | `… tests/test_styleguide.py tests/test_estilos.py` |
| 8 | Metodología (E2-T2) | 7 | `web/views.py`, `metodologia.html`, `metodologia.css`, `tests/test_metodologia.py` | `… tests/test_metodologia.py` |
| 9 | Resultados (E2-T3) | 8 | `web/views.py`, `resultados.html`, `graficas.js`, `resultados.css`, `tests/test_resultados.py` | `… tests/test_resultados.py tests/test_estilos.py` |
| 10 | Login simulado (E2-T4) | 6 | `auth_demo.py`, `context_processors.py`, `views_app.py`, `acceso.html`, `tests/test_acceso.py` | `… tests/test_acceso.py` |
| 11 | Simulador (E2-T5) | 10 | `simulacion_demo.py`, `views_app.py`, `simulador.html`, `simulador.js`, `tests/test_simulador.py` | `… tests/test_simulador.py` |
| 12 | Mis simulaciones (E2-T6) | 11 | `views_app.py`, `simulaciones.html`, `simulacion_detalle.html`, `tests/test_simulaciones.py` | `… tests/test_simulaciones.py` |
| 13 | Accesibilidad (E2-T7) | 9, 12 | `tests/test_accesibilidad.py`, `web/templates/**/*.html` | `… tests/test_accesibilidad.py` |

**Reparto para dos personas.** Hoy (etapa 0) pueden ir juntos o dividir los pasos 2 (datos) y 3
(CSS), que no comparten archivos. En la etapa 1, **Persona A** hace 7 → 8 → 9 (solo toca
`web/views.py` y CSS/JS de páginas) y **Persona B** hace 10 → 11 → 12 (solo toca
`web/views_app.py`, `auth_demo.py`, `simulacion_demo.py`); el paso 13 se hace al final, juntos.
Cada persona trabaja en su rama (`etapa1-a`, `etapa1-b`) y fusiona a `main` al terminar cada paso.

**Plazos estimados** (2 personas): etapa 0 = pasos 1–6, **hoy 24 oct (3–4 h)** · etapa 1 = pasos
7–13, **25 oct – 3 nov** · etapa 2 (login real + Postgres) **4–8 nov** · etapa 3 (resultados reales
y agente Q-learning en el simulador) **9–20 nov**, con los notebooks avanzando en paralelo desde el
día 1 · margen y ensayo **21–23 nov**. Las etapas 2 y 3 se planifican después con un nuevo
`/architect` (fuera de este blueprint).

#### Paso 1 — Proyecto Django con chequeo de salud /health/ (`E1-T1`)

**Do**
Reemplaza `config/settings.py` (entorno, Render, WhiteNoise solo en producción, sesión en cookie firmada, `ROOT_URLCONF = "app"`) y crea `app.py` con `/health/`, `web/views.py`, `web/context_processors.py` y su prueba, que levanta `runserver` de verdad. Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T1`. Archivos:
- `config/settings.py`
- `app.py`
- `web/views.py`
- `web/context_processors.py`
- `tests/test_health.py`

**Done when**
- [ ] WHEN se ejecuta `sh scripts/py manage.py check` THE SYSTEM SHALL terminar con código 0 sin reportar problemas.
- [ ] WHEN llega un GET a /health/ THE SYSTEM SHALL responder 200 con el JSON {"status": "ok", "app": "cauce"}.
- [ ] WHEN se arranca `manage.py runserver` como proceso real THE SYSTEM SHALL servir /health/ por HTTP con estado 200 (prueba test_servidor_real_sirve_health).
- [ ] WHEN se ejecuta `sh scripts/py app.py check` THE SYSTEM SHALL terminar con código 0, y `settings.ROOT_URLCONF` SHALL ser "app" (las rutas viven en app.py).
- [ ] WHEN se pide una ruta que ninguna URL define THE SYSTEM SHALL responder 404.
- [ ] WHEN se ejecutan `sh scripts/py -m ruff check .` y `sh scripts/py -m ruff format --check .` desde la raíz, con el bundle presente en blueprints/ THE SYSTEM SHALL terminar con código 0.

**Verify**
```bash
sh scripts/py manage.py check   # expect: exit 0
sh scripts/py app.py check   # expect: exit 0
sh scripts/py -m pytest tests/test_health.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T1: Proyecto Django con chequeo de salud /health/"
git tag step-01-django-health
# si el paso siguiente sale mal: git reset --hard step-01-django-health
```

#### Paso 2 — Contrato de datos y JSON de ejemplo (`E1-T2`)

**Do**
Crea los tres JSON de ejemplo y `web/datos.py`, que los carga, valida y cachea. Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T2`. Archivos:
- `web/data/mock/resultados.json`
- `web/data/mock/perfiles.json`
- `web/data/mock/simulaciones.json`
- `web/datos.py`
- `tests/test_datos.py`

**Done when**
- [ ] WHEN se llama `web.datos.resultados()` THE SYSTEM SHALL devolver web/data/mock/resultados.json con `fuente` igual a "datos_de_ejemplo" y las métricas necesidades_atendidas_pct, tiempo_atencion_h, costo_total_mcop y emergencias_sin_recursos en ese orden.
- [ ] WHEN a una métrica le falta alguna de las políticas uniforme, reglas o rl THE SYSTEM SHALL lanzar `web.datos.DatosInvalidos` con un mensaje que contiene "políticas".
- [ ] WHEN una serie de recompensa_por_episodio o sensibilidad_presupuesto tiene distinta longitud que su eje THE SYSTEM SHALL lanzar `DatosInvalidos` con un mensaje que contiene "misma longitud".
- [ ] WHEN un punto de K-means apunta a un perfil que perfiles.json no define THE SYSTEM SHALL lanzar `DatosInvalidos` con un mensaje que contiene "perfil desconocido".
- [ ] WHEN se llama `web.datos.simulacion(id)` con un id inexistente THE SYSTEM SHALL devolver None, y con un id existente SHALL devolver el diccionario de esa simulación.

**Verify**
```bash
sh scripts/py -m pytest tests/test_datos.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T2: Contrato de datos y JSON de ejemplo"
git tag step-02-contrato-datos
# si el paso siguiente sale mal: git reset --hard step-02-contrato-datos
```

#### Paso 3 — Tokens del sistema de diseño y CSS base (`E1-T3`)

**Do**
Crea `tokens.css` (literal) y escribe `base.css` y `components.css` según la especificación; la prueba hace cumplir las reglas del sistema de diseño en todo el CSS. Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T3`. Archivos:
- `web/static/web/css/tokens.css`
- `web/static/web/css/base.css`
- `web/static/web/css/components.css`
- `tests/test_estilos.py`

**Done when**
- [ ] WHEN se ejecuta tests/test_estilos.py THE SYSTEM SHALL encontrar declarada en web/static/web/css/tokens.css cada variable de la constante TOKENS, con la familia tipográfica "Inter".
- [ ] WHEN se revisa cualquier archivo CSS distinto de tokens.css THE SYSTEM SHALL no contener colores literales hex, rgb(), rgba(), hsl() ni hsla() (los colores solo entran por var(--…)).
- [ ] WHEN se revisa cualquier archivo CSS THE SYSTEM SHALL no contener box-shadow distinto de `none`, ni border-radius mayor de 16px o en %, ni font-weight distinto de 400 o 500.
- [ ] WHEN se revisa base.css THE SYSTEM SHALL definir `:focus-visible`, un bloque `prefers-reduced-motion: reduce` y el enlace `.saltar-contenido`.
- [ ] WHEN se revisa components.css THE SYSTEM SHALL definir .boton-primario, .boton-secundario, .boton-icono, .etiqueta, .tarjeta, .tarjeta-hundida, .stat e .insignia-demo.

**Verify**
```bash
sh scripts/py -m pytest tests/test_estilos.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T3: Tokens del sistema de diseño y CSS base"
git tag step-03-tokens-css
# si el paso siguiente sale mal: git reset --hard step-03-tokens-css
```

#### Paso 4 — Tabla de rutas completa y plantilla base (`E1-T4`)

**Do**
Reemplaza `app.py` con la tabla completa de rutas, `web/views.py` y `web/views_app.py` con páginas provisionales, y escribe `base.html` (cabecera, navegación con `aria-current`, menú móvil, aviso de datos de ejemplo, pie). Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T4`. Archivos:
- `app.py`
- `web/views.py`
- `web/views_app.py`
- `web/templates/web/base.html`
- `tests/test_rutas.py`

**Done when**
- [ ] WHEN llega un GET a /, /metodologia/, /resultados/, /login/ o /registro/ THE SYSTEM SHALL responder 200 con `<html lang="es">`, meta viewport, un título que termina en "Cauce", enlace de salto a #contenido, `<main id="contenido"`, `<nav aria-label="Principal"`, pie de página y exactamente un <h1>.
- [ ] WHEN se muestra cualquier página pública THE SYSTEM SHALL enlazar las rutas inicio, metodologia, resultados y simulador, y marcar la actual con aria-current="page".
- [ ] WHEN llega un GET a /app/simulador/, /app/simulaciones/ o /app/simulaciones/sim-001/ THE SYSTEM SHALL responder 200 o un 302 cuyo Location empieza por /login/.
- [ ] WHEN /salir/ o /app/api/simular/ reciben un GET THE SYSTEM SHALL responder 405, y WHEN /salir/ recibe un POST THE SYSTEM SHALL redirigir con 302 a /.
- [ ] WHEN CAUCE_DATOS_DEMO es True THE SYSTEM SHALL mostrar el texto "Datos de ejemplo" en todas las páginas, y WHEN es False SHALL no mostrarlo.
- [ ] WHEN DEBUG es False y se pide /styleguide/ THE SYSTEM SHALL responder 404.

**Verify**
```bash
sh scripts/py -m pytest tests/test_rutas.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T4: Tabla de rutas completa y plantilla base"
git tag step-04-rutas-base
# si el paso siguiente sale mal: git reset --hard step-04-rutas-base
```

#### Paso 5 — Portada con cifras del contrato de datos (`E1-T5`)

**Do**
Reemplaza `web/views.py` (portada real) y escribe `inicio.html`, `inicio.css` y `red.js` (grafo decorativo que respeta movimiento reducido). Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T5`. Archivos:
- `web/views.py`
- `web/templates/web/inicio.html`
- `web/static/web/css/pages/inicio.css`
- `web/static/web/js/red.js`
- `tests/test_inicio.py`

**Done when**
- [ ] WHEN llega un GET a / THE SYSTEM SHALL responder 200 con el titular "¿Quién recibe ayuda primero?", un elemento class="boton-primario" y enlaces a /app/simulador/ y /metodologia/.
- [ ] WHEN llega un GET a / THE SYSTEM SHALL mostrar exactamente 4 elementos class="stat", cada uno con el `valor` y la `etiqueta` de una entrada de `resumen` en resultados.json.
- [ ] WHEN llega un GET a / THE SYSTEM SHALL mostrar un elemento por cada uno de data-paso="datos", data-paso="kmeans" y data-paso="agente".
- [ ] WHEN llega un GET a / THE SYSTEM SHALL incluir `<canvas id="red-hero" aria-hidden="true"`, cargar web/js/red.js con defer y web/css/pages/inicio.css, y red.js SHALL contener una comprobación de prefers-reduced-motion.

**Verify**
```bash
sh scripts/py -m pytest tests/test_inicio.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T5: Portada con cifras del contrato de datos"
git tag step-05-portada
# si el paso siguiente sale mal: git reset --hard step-05-portada
```

#### Paso 6 — Listo para Render: errores propios y README (`E1-T6`)

**Do**
Crea `README.md` (literal, con los valores de Render), `404.html` y `500.html`; la prueba valida `check --deploy` y `collectstatic` de producción. Contenido literal y especificaciones: `epics/01-etapa-0-montaje.md`, tarea `E1-T6`. Archivos:
- `README.md`
- `web/templates/404.html`
- `web/templates/500.html`
- `tests/test_produccion.py`

**Done when**
- [ ] WHEN se ejecuta `manage.py check --deploy` con RENDER=true, un DJANGO_SECRET_KEY de 60 caracteres y RENDER_EXTERNAL_HOSTNAME=cauce.onrender.com THE SYSTEM SHALL terminar con código 0.
- [ ] WHEN se ejecuta cualquier comando de manage.py con RENDER=true y sin DJANGO_SECRET_KEY THE SYSTEM SHALL terminar con código 1 y "DJANGO_SECRET_KEY" en stderr.
- [ ] WHEN se ejecuta `manage.py collectstatic --noinput` con RENDER=true y una clave secreta THE SYSTEM SHALL terminar con código 0 y escribir staticfiles/staticfiles.json.
- [ ] WHEN se pide una ruta inexistente THE SYSTEM SHALL responder 404 con el texto "Página no encontrada" y un enlace a /, y la plantilla 500.html SHALL renderizarse sin contexto de petición con "Algo salió mal" y `<html lang="es">`.
- [ ] WHEN se lee README.md THE SYSTEM SHALL contener el comando de build `pip install -r requirements.txt && python manage.py collectstatic --noinput`, el de inicio `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`, DJANGO_SECRET_KEY, PYTHON_VERSION y /health/.

**Verify**
```bash
sh scripts/py -m pytest tests/test_produccion.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E1-T6: Listo para Render: errores propios y README"
git tag step-06-produccion
# si el paso siguiente sale mal: git reset --hard step-06-produccion
```

#### Paso 7 — Componentes de la etapa 1 y guía de estilo (`E2-T1`)

**Do**
Reemplaza `web/views.py`, amplía `components.css` (campos, tablas, alertas, paneles) y escribe `styleguide.html`. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T1`. Archivos:
- `web/views.py`
- `web/templates/web/styleguide.html`
- `web/static/web/css/components.css`
- `tests/test_styleguide.py`

**Done when**
- [ ] WHEN DEBUG es True y llega un GET a /styleguide/ THE SYSTEM SHALL responder 200 con secciones de id botones, tarjetas, cifras, etiquetas, formularios, tablas y alertas, incluyendo un ejemplo class="boton-primario" y uno class="stat".
- [ ] WHEN DEBUG es False y llega un GET a /styleguide/ THE SYSTEM SHALL responder 404.
- [ ] WHEN se revisa components.css THE SYSTEM SHALL definir .campo, .campo-error, .deslizador, .tabla, .alerta, .alerta-error, .dividido, .panel-grafica y .estado-vacio, y seguir cumpliendo todas las reglas de tests/test_estilos.py.

**Verify**
```bash
sh scripts/py -m pytest tests/test_styleguide.py tests/test_estilos.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T1: Componentes de la etapa 1 y guía de estilo"
git tag step-07-styleguide
# si el paso siguiente sale mal: git reset --hard step-07-styleguide
```

#### Paso 8 — Página de metodología (`E2-T2`)

**Do**
Reemplaza `web/views.py` (con `FORMULACION`) y escribe `metodologia.html` y `metodologia.css`. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T2`. Archivos:
- `web/views.py`
- `web/templates/web/metodologia.html`
- `web/static/web/css/pages/metodologia.css`
- `tests/test_metodologia.py`

**Done when**
- [ ] WHEN llega un GET a /metodologia/ THE SYSTEM SHALL responder 200 con `<section id="datos"`, `<section id="kmeans"`, `<section id="formulacion"` y `<section id="limitaciones"`, y el texto "Emergencias UNGRD V2".
- [ ] WHEN llega un GET a /metodologia/ THE SYSTEM SHALL mostrar celdas `<th scope="row">` para Agente, Entorno, Estado, Acciones, Recompensa, Restricciones y Episodio.
- [ ] WHEN llega un GET a /metodologia/ THE SYSTEM SHALL mostrar el `nombre` de cada perfil de perfiles.json y la frase "no es un modelo predictivo".

**Verify**
```bash
sh scripts/py -m pytest tests/test_metodologia.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T2: Página de metodología"
git tag step-08-metodologia
# si el paso siguiente sale mal: git reset --hard step-08-metodologia
```

#### Paso 9 — Panel de resultados con Chart.js (`E2-T3`)

**Do**
Reemplaza `web/views.py` y escribe `resultados.html`, `graficas.js` (Chart.js con los tokens) y `resultados.css`. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T3`. Archivos:
- `web/views.py`
- `web/templates/web/resultados.html`
- `web/static/web/js/graficas.js`
- `web/static/web/css/pages/resultados.css`
- `tests/test_resultados.py`

**Done when**
- [ ] WHEN llega un GET a /resultados/ THE SYSTEM SHALL incrustar los datos con `<script id="datos-resultados" type="application/json">` y `<script id="datos-perfiles" type="application/json">`.
- [ ] WHEN llega un GET a /resultados/ THE SYSTEM SHALL mostrar los canvas grafica-metricas, grafica-recompensa, grafica-sensibilidad y grafica-perfiles, cada uno con role="img" y aria-label no vacío, y al menos 4 <details> con una <table> de los mismos datos.
- [ ] WHEN llega un GET a /resultados/ THE SYSTEM SHALL mostrar un class="stat" por cada métrica de resultados.json, con el `nombre` de cada métrica.
- [ ] WHEN llega un GET a /resultados/ THE SYSTEM SHALL cargar Chart.js 4.5.1 desde cdnjs con su hash de integridad sha512 y crossorigin="anonymous", y después web/js/graficas.js.
- [ ] WHEN se lee web/js/graficas.js THE SYSTEM SHALL usar --serie-uniforme, --serie-reglas, --serie-rl y --fondo-grafica, comprobar prefers-reduced-motion y usar borderDash.

**Verify**
```bash
sh scripts/py -m pytest tests/test_resultados.py tests/test_estilos.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T3: Panel de resultados con Chart.js"
git tag step-09-resultados
# si el paso siguiente sale mal: git reset --hard step-09-resultados
```

#### Paso 10 — Login simulado que protege la app (`E2-T4`)

**Do**
Crea `web/auth_demo.py`, reemplaza `context_processors.py` y `views_app.py`, y escribe `acceso.html` (login y registro). Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T4`. Archivos:
- `web/auth_demo.py`
- `web/context_processors.py`
- `web/views_app.py`
- `web/templates/web/acceso.html`
- `tests/test_acceso.py`

**Done when**
- [ ] WHEN llega un GET a /login/ THE SYSTEM SHALL mostrar un formulario POST con <label for="id_correo">, un input email name="correo" id="id_correo", un input de clave con autocomplete="current-password", sin atributo onpaste, y el texto "Modo demostración".
- [ ] WHEN /login/ recibe un POST con cualquier correo válido THE SYSTEM SHALL guardar {correo en minúsculas, nombre} en la sesión y redirigir con 302 a /app/simulador/.
- [ ] WHEN /login/ recibe un POST con un correo inválido THE SYSTEM SHALL responder 200 con "Escribe un correo válido" y aria-invalid="true" en el campo, sin crear usuario en la sesión.
- [ ] WHEN el POST de login trae ?next=/app/simulaciones/ THE SYSTEM SHALL redirigir ahí, y WHEN next apunta a otro dominio SHALL redirigir a /app/simulador/.
- [ ] WHEN un visitante anónimo pide /app/simulador/ THE SYSTEM SHALL redirigir con 302 a /login/?next=%2Fapp%2Fsimulador%2F, y WHEN hay sesión SHALL mostrar en la cabecera el nombre del usuario y un formulario que envía a /salir/.
- [ ] WHEN /salir/ recibe un POST THE SYSTEM SHALL vaciar la sesión y redirigir a /.

**Verify**
```bash
sh scripts/py -m pytest tests/test_acceso.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T4: Login simulado que protege la app"
git tag step-10-login-demo
# si el paso siguiente sale mal: git reset --hard step-10-login-demo
```

#### Paso 11 — Simulador con motor de ejemplo y API JSON (`E2-T5`)

**Do**
Crea `web/simulacion_demo.py`, reemplaza `views_app.py` (simulador y API) y escribe `simulador.html` y `simulador.js`. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T5`. Archivos:
- `web/simulacion_demo.py`
- `web/views_app.py`
- `web/templates/web/app/simulador.html`
- `web/static/web/js/simulador.js`
- `tests/test_simulador.py`

**Done when**
- [ ] WHEN se llama `simular()` dos veces con los mismos parámetros THE SYSTEM SHALL devolver resultados idénticos, y otra semilla SHALL cambiar el resultado.
- [ ] WHEN `simular()` se ejecuta con las semillas 0, 7, 42, 2026 y 9999 THE SYSTEM SHALL asignar como máximo `recursos` unidades por política, devolver una fila por emergencia y ordenar necesidades_atendidas_pct como rl > reglas > uniforme.
- [ ] WHEN un parámetro sale de presupuesto 50-150, recursos 5-50, emergencias 3-12 o semilla 0-9999, o no es entero THE SYSTEM SHALL lanzar ValueError, y la API SHALL responder 400 con error.codigo "parametro_invalido".
- [ ] WHEN llega un POST a /app/api/simular/ sin sesión THE SYSTEM SHALL responder 401 con error.codigo "no_autenticado"; con sesión y JSON válido SHALL responder 200 con exactamente `simular(**parametros)`; sin token CSRF con verificación activa SHALL responder 403.
- [ ] WHEN un usuario con sesión abre /app/simulador/ THE SYSTEM SHALL mostrar los campos con etiqueta presupuesto, recursos, emergencias y semilla (ids id_<nombre>), una región `id="resultado-simulacion" aria-live="polite"`, un token CSRF y web/js/simulador.js.

**Verify**
```bash
sh scripts/py -m pytest tests/test_simulador.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T5: Simulador con motor de ejemplo y API JSON"
git tag step-11-simulador
# si el paso siguiente sale mal: git reset --hard step-11-simulador
```

#### Paso 12 — Mis simulaciones: lista, detalle y estado vacío (`E2-T6`)

**Do**
Reemplaza `views_app.py` y escribe `simulaciones.html` y `simulacion_detalle.html` con su estado vacío. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T6`. Archivos:
- `web/views_app.py`
- `web/templates/web/app/simulaciones.html`
- `web/templates/web/app/simulacion_detalle.html`
- `tests/test_simulaciones.py`

**Done when**
- [ ] WHEN un usuario con sesión abre /app/simulaciones/ THE SYSTEM SHALL listar cada simulación de simulaciones.json por su `nombre` con un enlace a /app/simulaciones/<id>/.
- [ ] WHEN un usuario con sesión abre /app/simulaciones/<id>/ con un id existente THE SYSTEM SHALL responder 200 con el nombre, una <table> y cada valor de los parámetros; con un id inexistente SHALL responder 404.
- [ ] WHEN no hay simulaciones THE SYSTEM SHALL mostrar "Aún no hay simulaciones guardadas" y un enlace a /app/simulador/.
- [ ] WHEN un visitante anónimo abre /app/simulaciones/ THE SYSTEM SHALL redirigir con 302 a una URL que empieza por /login/.

**Verify**
```bash
sh scripts/py -m pytest tests/test_simulaciones.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T6: Mis simulaciones: lista, detalle y estado vacío"
git tag step-12-simulaciones
# si el paso siguiente sale mal: git reset --hard step-12-simulaciones
```

#### Paso 13 — Revisión automática de accesibilidad (`E2-T7`)

**Do**
Agrega la prueba de accesibilidad y corrige las plantillas que no la pasen. Contenido literal y especificaciones: `epics/02-etapa-1-interfaz.md`, tarea `E2-T7`. Archivos:
- `tests/test_accesibilidad.py`
- `web/templates/**/*.html`

**Done when**
- [ ] WHEN se analizan todas las páginas públicas, las de la app con sesión, un detalle de simulación, la página 404 y la guía de estilo (con DEBUG) THE SYSTEM SHALL encontrar exactamente un <h1> en cada una.
- [ ] WHEN se analizan esas páginas THE SYSTEM SHALL no encontrar atributos style en línea ni manejadores on* en línea en ningún elemento.
- [ ] WHEN se analizan esas páginas THE SYSTEM SHALL encontrar alt en cada <img>, role="img" con aria-label (o aria-hidden="true") en cada <canvas>, rel="noopener" en cada enlace target="_blank" y un <label for> para cada <input> visible.
- [ ] WHEN se analiza la meta viewport THE SYSTEM SHALL no contener user-scalable=no ni maximum-scale=1.

**Verify**
```bash
sh scripts/py -m pytest tests/test_accesibilidad.py   # expect: exit 0
sh scripts/py -m ruff check .   # expect: exit 0
sh scripts/py -m ruff format --check .   # expect: exit 0
sh scripts/py -m pytest   # expect: exit 0
```

**Checkpoint**
```bash
git add -A && git commit -m "E2-T7: Revisión automática de accesibilidad"
git tag step-13-accesibilidad
# si el paso siguiente sale mal: git reset --hard step-13-accesibilidad
```

### 9.1 Parity and cutover

NOT APPLICABLE — greenfield build, no system is being replaced.

---

## 10. Environment Setup

### Prerequisites
| Tool | Version | Check |
|---|---|---|
| Python | ≥ 3.12 (se fija 3.14 en `.python-version`) | `python --version` |
| Git | ≥ 2.28, con `user.name` y `user.email` | `git --version` y `git config user.email` |
| Terminal `sh` | Git Bash en Windows; cualquier shell POSIX en Linux/macOS | `sh -c 'echo ok'` |

### Accounts to create first
- **GitHub** (ya existe el repositorio del usuario): necesario para publicar, no para construir.
- **Render** (https://dashboard.render.com, plan Free): lo usa el equipo después del paso 6 para crear el Web Service. Ningún paso de construcción lo necesita.

### Environment variables
| Variable | Purpose | Where to get it | Required by step | Secret? |
|---|---|---|---|---|
| `DJANGO_SECRET_KEY` | Clave de firma de Django (sesiones, CSRF) | Render → Environment → "Generate" | Solo en Render (paso 6 lo prueba con un valor de prueba) | sí |
| `DJANGO_DEBUG` | `1` desarrollo / `0` producción | Valor fijo | Opcional en todos (por defecto 1 en local, 0 en Render) | no |
| `CAUCE_DATOS_DEMO` | Muestra el aviso "Datos de ejemplo" | Valor fijo `1` | Opcional desde el paso 4 (por defecto 1) | no |
| `RENDER` | Lo define Render (`true`); activa modo producción | Automática | Paso 6 (la prueba lo define en un subproceso) | no |
| `RENDER_EXTERNAL_HOSTNAME` | Dominio `*.onrender.com` que se agrega a `ALLOWED_HOSTS` y CSRF | Automática | Paso 6 (ídem) | no |
| `PORT` | Puerto que gunicorn escucha en Render (10000 por defecto) | Automática | Solo en Render | no |
| `PYTHON_VERSION` | Opcional: versión exacta de Python en Render | Panel de Render | Ninguno (se usa `.python-version`) | no |

Ningún archivo `.env` se carga automáticamente: Django lee el entorno del proceso. En local nada es
obligatorio. Las pruebas que necesitan variables (paso 6) las pasan explícitamente al subproceso,
así que ningún comando de este blueprint depende de un `.env`.

### Files that must be committed

| File | Why it is committed | Ignore-file exception line |
|---|---|---|
| `.env.example` | Documenta las variables | `!.env.example` después de `.env.*` |
| `.gitignore`, `.gitattributes` | Gobiernan el repo desde el primer commit | — no los cubre ningún patrón |
| `requirements.txt`, `requirements-dev.txt`, `requirements-ml.txt` | Render y el equipo instalan de ahí | — no los cubre ningún patrón |
| `.python-version`, `ruff.toml`, `pytest.ini`, `scripts/py` | Configuración de los gates | — no los cubre ningún patrón |
| `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, `.claude/rules/*`, `.claude/skills/*` | Configuración del agente | solo se ignora `.claude/settings.local.json` |
| `web/data/mock/*.json` | Datos que muestra la web | — no los cubre ningún patrón |
| `blueprints/cauce/**` | El plan, para el equipo | — no lo cubre ningún patrón |

### Bootstrap
```bash
set -e
# El orden importa: copia del workspace (trae .gitignore, .gitattributes y configs) → repositorio
# → primer commit → entorno virtual → dependencias → esqueleto de Django → formato del esqueleto.
cp -Rn blueprints/cauce/workspace/. ./ || true  # -n: nunca pisa un archivo existente (requirements*, archivos ya editados). En macOS y coreutils >= 9.2 `cp -n` sale con 1 cuando salta archivos; saltar es lo esperado.
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git ls-files --error-unmatch .gitignore >/dev/null 2>&1 || { git add -A && git commit -m "chore: workspace, configuración y plan de construcción"; }  # una sola vez: cuando .gitignore aún no está en el repo (repo nuevo o ya creado por el equipo)
test -d .venv || python -m venv .venv || python3 -m venv .venv
sh scripts/py -m pip install --disable-pip-version-check -q -r requirements-dev.txt
test -f manage.py || { sh scripts/py -m django startproject config . && rm config/urls.py; }  # las rutas viven en app.py
sh scripts/py -m ruff format -q manage.py config
```

Archivos que la copia nunca pisa una vez existen: `requirements*.txt`, `README.md`, `app.py`,
`config/settings.py` y todo lo que la construcción ya editó. El commit del Bootstrap se crea **después**
de que `.gitignore` está en su sitio (y solo si `.gitignore` aún no estaba en el repo, así funciona igual con un repo nuevo o con uno que el equipo ya creó y conectó a GitHub), así `.venv/` y `staticfiles/` nunca se rastrean, y **antes**
de generar el esqueleto de Django, así la clave aleatoria de `startproject` nunca entra al historial
(el paso 1 reemplaza `settings.py` antes de su commit).

---

## 11. Dependencies

Verificado en vivo el 2026-10-24 en el hilo principal (sin subagente), contra PyPI, npm/cdnjs y la
documentación de Render.

### Runtime
| Package | Version | Source (registry URL or track file) | Checked | Installed by | Purpose |
|---|---|---|---|---|---|
| Django | 6.1.2 | https://pypi.org/pypi/django/json | 2026-10-24 | §10 Bootstrap (`requirements-dev.txt` → `requirements.txt`) | Framework web; requiere Python ≥ 3.12 |
| gunicorn | 26.2.0 | https://pypi.org/pypi/gunicorn/json | 2026-10-24 | §10 Bootstrap | Servidor WSGI en Render (no corre en Windows) |
| whitenoise | 6.12.0 | https://pypi.org/pypi/whitenoise/json | 2026-10-24 | §10 Bootstrap | Sirve el CSS/JS recolectado en producción |
| CPython | 3.14 (`.python-version`; Render usa 3.14.8 por defecto) | https://render.com/docs/python-version | 2026-10-24 | `.python-version` (workspace) | Intérprete |
| Chart.js | 4.5.1 (UMD, cdnjs, sha512 `WoViKh…MDhwMA==`) | https://registry.npmjs.org/chart.js · https://api.cdnjs.com/libraries/Chart.js/4.5.1?fields=sri | 2026-10-24 | paso 9 (`<script>` en `resultados.html`) | Gráficas. 4.6.1 salió el 2026-10-22: demasiado reciente, no se usa |
| Inter | Google Fonts CSS2, pesos 400 y 500 | https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap (200 OK) | 2026-10-24 | paso 4 (`<link>` en `base.html`) | Tipografía (sustituye a Matter) |

### Development
| Package | Version | Source (registry URL or track file) | Checked | Installed by | Purpose |
|---|---|---|---|---|---|
| ruff | 0.17.0 | https://pypi.org/pypi/ruff/json | 2026-10-24 | §10 Bootstrap (`requirements-dev.txt`) | Lint y formato. 0.17.1/0.17.2 tienen < 2 semanas |
| pytest | 9.1.1 | https://pypi.org/pypi/pytest/json | 2026-10-24 | §10 Bootstrap | Pruebas |
| pytest-django | 4.14.0 | https://pypi.org/pypi/pytest-django/json | 2026-10-24 | §10 Bootstrap | Fixtures `client`, `rf`, `settings` |

### Análisis y modelado (no los instala Render ni ningún paso)
Fijados por el equipo (su `pip freeze`, sin Flask) y verificados como existentes y no retirados en
PyPI el 2026-10-24 (`https://pypi.org/pypi/<paquete>/<versión>/json`): contourpy 1.3.3, cycler
0.12.1, fonttools 4.63.0, joblib 1.5.3, kiwisolver 1.5.1, matplotlib 3.11.1, narwhals 2.25.0, numpy
2.5.2, packaging 26.3, pandas 3.0.5, pillow 12.3.0, pyparsing 3.3.2, python-dateutil 2.9.0.post0,
scikit-learn 1.9.0, scipy 1.18.1, six 1.17.0, threadpoolctl 3.6.0, tzdata 2026.3. Se instalan a
mano para los notebooks (`sh scripts/py -m pip install -r requirements-ml.txt`). `gymnasium` se
agregará y verificará al empezar la etapa 3.

### Deliberately not used
| Rejected | Instead | Why |
|---|---|---|
| Flask (+ Werkzeug, Jinja2, click, blinker, itsdangerous) | Django | Decidido con el usuario: Django trae auth/sesiones/ORM para la etapa 2 |
| uv / `uv.lock` | pip + requirements | Pedido del usuario; con `uv.lock` Render cambiaría de instalador |
| Tailwind CSS | CSS con tokens | Evita Node y un paso de build en Render |
| python-dotenv | entorno del proceso | Nada necesita `.env`; menos piezas |
| stable-baselines3 / PyTorch en la web | numpy (etapa 3) | No caben en 512 MB de RAM |
| Chart.js 4.6.1 | 4.5.1 | Publicada hace 2 días |

---

## 12. Deployment Strategy

### Hosting
Render, **Web Service, plan Free** (0.1 CPU, 512 MB RAM, se apaga tras 15 min sin tráfico y tarda
≈1 min en despertar; 750 h/mes por workspace; disco efímero). Lo configura el equipo, no el
constructor. Valores (también en el README):

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| Health Check Path | `/health/` |
| Environment | `DJANGO_SECRET_KEY` (Generate), `CAUCE_DATOS_DEMO=1` |

### Environments
| Environment | Branch | URL | Database | Third-party mode |
|---|---|---|---|---|
| Local | cualquiera | http://127.0.0.1:8000 | ninguna | — |
| Preview | NOT APPLICABLE — no se usan previews en el plan Free | — | — | — |
| Production | `main` | `https://<servicio>.onrender.com` | ninguna | — |

### CI/CD
Sin CI externo en v1: el gate (§20.1) se corre en local antes de cada commit, y Render despliega
automáticamente cada `git push` a `main` (auto-deploy por defecto).

### Release and rollback
Cada paso tiene su etiqueta `step-NN-…`. Un despliegue malo se revierte desde el panel de Render
("Rollback" a un deploy anterior, ≈1–2 min) o con `git revert` + push. Sin migraciones en la etapa 1.

### Domain, DNS, TLS
NOT APPLICABLE en v1 — se usa el dominio `*.onrender.com` con TLS automático de Render.

---

## 13. Testing Strategy

| Layer | Framework | What it covers | Where | Runs |
|---|---|---|---|---|
| Unit | pytest | Contrato de datos, motor de ejemplo, reglas de CSS | `tests/test_datos.py`, `test_simulador.py`, `test_estilos.py` | cada paso |
| Integration | pytest-django (cliente de pruebas) | Cada ruta, login, API, plantillas, accesibilidad estática | `tests/test_*.py` | cada paso |
| E2E | Proceso real | `runserver` levantado y `/health/` por HTTP; `manage.py check --deploy` y `collectstatic` de producción | `tests/test_health.py`, `test_produccion.py` | pasos 1 y 6, y siempre en la suite |

### Critical flows to cover E2E
1. Arranque real del servidor y `/health/` (Render depende de él) — `test_servidor_real_sirve_health`.
2. Configuración de producción válida y recolección de estáticos — `test_produccion.py`.
3. Anónimo → login → simulador → API 200 — `test_acceso.py` + `test_simulador.py`.

### Test data
Los JSON de `web/data/mock/` son los datos de prueba; nunca se modifican en las pruebas (los casos
inválidos usan copias con `copy.deepcopy`). No hay base de datos que preparar.

### What is deliberately not tested
El dibujo real de Chart.js y la animación de `red.js` (necesitarían un navegador): se prueba que
los datos, los canvas descritos y las tablas alternativas existen, y se deja una revisión manual
en el checklist de §20.1.

---

## 14. Security & Secrets

| Concern | Control | Implemented in |
|---|---|---|
| Secret storage | `DJANGO_SECRET_KEY` solo en el panel de Render; en local una clave de desarrollo fija | `config/settings.py` |
| Secret rotation | Regenerar en Render y redeplegar (invalida sesiones) | Panel de Render |
| Input validation | `validar_parametros` (API), `validate_email` (login), validadores de `datos.py` | `web/simulacion_demo.py`, `web/auth_demo.py`, `web/datos.py` |
| Output encoding / XSS | Autoescape de Django; datos a JS con `json_script`; `textContent` en `simulador.js` | plantillas, JS |
| SQL injection | NOT APPLICABLE — no hay SQL en la etapa 1 | — |
| AuthN / AuthZ | §8, en el servidor en cada petición | `web/auth_demo.py` |
| CSRF | Middleware de Django + `X-CSRFToken` en `fetch` | `config/settings.py`, `simulador.js` |
| Redirección abierta | `url_has_allowed_host_and_scheme` en `destino_seguro` | `web/auth_demo.py` |
| Rate limiting / abuse | NOT APPLICABLE en v1 — sin escrituras ni costos por petición | — |
| Webhook verification | NOT APPLICABLE — no hay webhooks | — |
| Dependency audit | Versiones fijadas; revisión al iniciar cada etapa | `requirements*.txt` |
| Security headers | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin` (por defecto de Django); cookies `Secure` en Render. HSTS y redirección SSL de Django no se activan en v1 (avisos W004/W008 aceptados) | `config/settings.py` |
| Integridad de terceros | Chart.js con `integrity` sha512 + `crossorigin` | `resultados.html` |
| PII handling | Solo el correo y nombre que el usuario escribe, en una cookie firmada en su propio navegador; nada en el servidor | `web/auth_demo.py` |
| Logging hygiene | Sin logs propios en v1; Django no registra cuerpos de petición | — |

**Hard rules:** ningún secreto en el repo, en logs ni en el HTML; la autorización se verifica antes
del trabajo. Datos regulados: no se manejan (los datos de la UNGRD son abiertos y agregados).

---

## 15. Accessibility

**Target: WCAG 2.2 Level AA.**

| Requirement | Rule |
|---|---|
| Semantic HTML | `header`/`nav`/`main`/`footer`, un `h1` por página, encabezados en orden |
| Keyboard | Todo operable con teclado; enlace "Saltar al contenido"; menú móvil con `<details>` nativo |
| Focus visible | Contorno de 2px `#cbfffc` (12:1 sobre alga) en `:focus-visible` |
| Contrast | Texto ≥ 4.5:1 (§7); bordes de campos ≥ 3:1 |
| Forms | `<label for>` en cada campo; error en texto junto al campo con `aria-invalid` y `aria-describedby` |
| Images | Canvas decorativo con `aria-hidden`; gráficas con `role="img"` + `aria-label` + tabla |
| Motion | `prefers-reduced-motion` respetado en CSS, `red.js` y Chart.js |
| Zoom / reflow | Sin `user-scalable=no`; sin scroll horizontal a 320px (tablas en `.tabla-desplazable`) |
| Live regions | Resultado del simulador en `aria-live="polite"` con `aria-busy` |

### WCAG 2.2 additions — the ones most often missed
| SC | Requirement |
|---|---|
| 2.4.11 Focus Not Obscured | La cabecera no es fija: nada tapa el foco |
| 2.5.7 Dragging Movements | Los deslizadores se mueven con flechas del teclado y tienen `<output>`; la semilla es un campo numérico |
| 2.5.8 Target Size | Botones y enlaces de navegación ≥ 44px de alto |
| 3.3.7 Redundant Entry | NOT APPLICABLE — no hay flujos de varios pasos |
| 3.3.8 Accessible Authentication | Se permite pegar y usar gestores de contraseñas; sin pruebas cognitivas |

### Verification
```bash
sh scripts/py -m pytest tests/test_accesibilidad.py   # expect: exit 0, 0 failed
```
Manual antes de presentar: recorrido solo con teclado, una pasada con lector de pantalla (NVDA en
Windows) por inicio → login → simulador, y zoom al 200% a 375px.

---

## 16. Observability & Cost

### Instrumentation
| Signal | Tool | What it captures | Who looks at it |
|---|---|---|---|
| Errors | Logs de Render (salida de gunicorn/Django) | Excepciones no controladas | El equipo |
| Logs | Logs de Render | Peticiones de gunicorn | El equipo |
| Metrics | Panel de Render (CPU/RAM) | Uso del plan Free | El equipo |
| Uptime | Health Check de Render en `/health/` | Proceso vivo | Render (reinicia si falla) |

### The metrics that matter for this project
| Metric | Target | Alert at |
|---|---|---|
| `/health/` | 200 | Cualquier fallo del Health Check |
| RAM del servicio | < 200 MB | > 400 MB (el límite es 512 MB) |
| Horas de instancia | < 750 h/mes | Aviso de Render de horas agotadas |

### Health check
`/health/` confirma que el proceso responde. No toca base de datos porque no hay; en la etapa 2
debe ampliarse para comprobar la conexión.

### Cost model
| Service | Free tier | Cost at expected v1 scale | Cost at 10× | Cliff to watch |
|---|---|---|---|---|
| Render Web Service | 750 h/mes, 512 MB | 0 USD | 0 USD | Se apaga tras 15 min sin tráfico; plan pago desde 7 USD/mes |
| Render Postgres (etapa 2) | 1 GB, **vence a los 30 días** | — | — | Elegir proveedor antes de la etapa 2 |
| cdnjs / Google Fonts | Gratis | 0 USD | 0 USD | — |

**Costo mensual estimado al lanzar: 0 USD.** El riesgo no es de dinero sino de disponibilidad (el
arranque en frío de ≈1 min).

---

## 17. Model Routing

NOT APPLICABLE — this project does not call an LLM at runtime.

---

## 18. Skills to Use During Build

| Skill | Build steps | Why | Install |
|---|---|---|---|
| `ui-ux-pro-max` (se activa sola, sin barra) | 3, 5, 7, 8, 9 | Patrones de componentes, gráficas y accesibilidad al maquetar | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` y luego `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` (en este equipo ya está instalada) |

Si una skill no está disponible, el constructor sigue con las especificaciones de los epics y lo
anota en una línea.

---

## 19. Agent Workspace

Bundle: los archivos son reales bajo `blueprints/cauce/workspace/` y el Bootstrap los copia a la
raíz con `cp -Rn` (nunca pisa lo existente; `|| true` porque en macOS sale con 1 al saltar). Nunca
se emite `.claude/commands/`.

### 19.1 `CLAUDE.md`
Archivo real: `workspace/CLAUDE.md` (135 líneas): comandos primero, arquitectura con el camino de
una petición, fronteras, fuentes únicas, reglas de código, tokens y no negociables.

### 19.2 `AGENTS.md`
Archivo real: `workspace/AGENTS.md`: descripción, comandos, no negociables y puntero a `CLAUDE.md`.

### 19.3 `.claude/settings.json`
Archivo real. Permite `sh scripts/py:*` (cubre todos los `Verify`), `python -m venv .venv`, `git
status|diff|log|add|commit|tag|rev-parse|ls-files|check-ignore`, `test` y `ls`. Niega leer `.env`,
`git push`, `git reset --hard` y `rm -rf`.

### 19.4 Project skills — `.claude/skills/<name>/SKILL.md`
| Skill | Triggers on | What it automates |
|---|---|---|
| `agregar-pagina` | "agrega una página", "nueva ruta" | Ruta en `app.py`, vista, plantilla, CSS y prueba |
| `conectar-resultados-reales` | "conectar los datos reales", "quitar datos de ejemplo" | Validar y reemplazar los JSON, apagar `CAUCE_DATOS_DEMO` |

### 19.5 `.claude/rules/*.md`
| File | `paths` globs | Covers |
|---|---|---|
| `.claude/rules/plantillas-y-css.md` | `web/templates/**`, `web/static/**` | Plantillas, tokens, accesibilidad, gráficas |
| `.claude/rules/python-django.md` | `config/**`, `web/**/*.py`, `manage.py`, `app.py` | Rutas, vistas, datos, sesión, errores de API |
| `.claude/rules/pruebas.md` | `tests/**`, `pytest.ini` | Cómo correr y escribir pruebas |

### 19.6 Verify-critical config and local infrastructure

| File | Path in the project | Which `Verify` commands need it | Resolution/env handling it carries | Bundle-path exclusion |
|---|---|---|---|---|
| `scripts/py` | `scripts/py` | todos (pasos 1–13) | Elige `.venv/Scripts/python.exe` o `.venv/bin/python`; LF forzado por `.gitattributes` | n/a — no recorre el árbol |
| `pytest.ini` | `pytest.ini` | todos los `pytest` | `DJANGO_SETTINGS_MODULE = config.settings`; pytest-django agrega la raíz (donde está `manage.py`) a `sys.path`, así resuelven `app`, `config` y `web`; ninguna variable de entorno requerida | `norecursedirs = blueprints docs staticfiles .venv .git` |
| `ruff.toml` | `ruff.toml` | `ruff check .` y `ruff format --check .` (todos) | `known-first-party = ["app", "config", "web"]` para que el orden de imports no dependa de la máquina; no lee variables | `extend-exclude = ["blueprints", "docs", "staticfiles", ".venv"]` |
| `requirements*.txt` | raíz | Bootstrap | — | n/a |
| `.python-version` | raíz | Render | — | n/a |
| `.gitignore`, `.gitattributes` | raíz | Bootstrap (primer commit) | — | n/a — `blueprints/` se sube a propósito |
| `web/__init__.py`, `web/apps.py` | `web/` | todos (la app `web` está en `INSTALLED_APPS`) | — | n/a |

Servicios locales: NOT APPLICABLE — ningún `Verify` necesita base de datos, caché ni red.
Todos los archivos de prueba que ejecutan los `Verify` los crea su propio paso (literal en los epics).

#### Resolution convention matrix

**La convención, una sola vez:** imports absolutos por paquete desde la raíz del proyecto
(`from web import datos`, `from web.auth_demo import login_requerido`, `ROOT_URLCONF = "app"`).

| Context | Command that exercises it | Convention as it appears there | Config + literal setting that makes it work |
|---|---|---|---|
| Application source | `sh scripts/py manage.py check` · `sh scripts/py app.py check` | `from web import views, views_app` en `app.py` | `manage.py`/`app.py` se ejecutan desde la raíz, que queda en `sys.path` |
| Test files | `sh scripts/py -m pytest` | `from web import datos` en `tests/*.py` | `pytest.ini` — pytest-django encuentra `manage.py` y agrega su carpeta a `sys.path` |
| Standalone scripts | `sh scripts/py -c "from web import datos; …"` (skill `conectar-resultados-reales`) | `from web import datos` | Se ejecuta desde la raíz: Python agrega el directorio actual con `-c` |
| Build / bundle | `python manage.py collectstatic --noinput` (Render) y `test_collectstatic_de_produccion_genera_el_manifiesto` | rutas `web/css/…` en `{% static %}` | `STATIC_ROOT = BASE_DIR / "staticfiles"` en `settings.py` |
| Linter | `sh scripts/py -m ruff check .` | orden de imports | `ruff.toml` — `known-first-party` |

#### Cross-artifact value reconciliation

| Shared value | Single source — the file that decides it | Literal value | Every other place it appears | Compared |
|---|---|---|---|---|
| Módulo de rutas | `config/settings.py` — `ROOT_URLCONF` | `app` (archivo `app.py`) | `app.py` (docstring), `tests/test_health.py` (`settings.ROOT_URLCONF == "app"`), `CLAUDE.md`, `.claude/rules/python-django.md`, §3 | yes |
| Punto de entrada WSGI | `config/wsgi.py` (generado) — `application` | `config.wsgi:application` | `config/settings.py` `WSGI_APPLICATION = "config.wsgi.application"`, README (Start Command), `test_produccion.py`, §12 | yes |
| Ruta de salud | `app.py` — `path("health/", …)` | `/health/` | `test_health.py`, README (Health Check Path), `test_produccion.py`, §5, §12, §16 | yes |
| Carpeta de estáticos recolectados | `config/settings.py` — `STATIC_ROOT` | `staticfiles/` (`staticfiles/staticfiles.json`) | `.gitignore`, `ruff.toml`, `pytest.ini`, `test_produccion.py` | yes |
| Nombre de la app | `web/apps.py` — `name` | `web` | `INSTALLED_APPS`, `ruff.toml` `known-first-party`, imports | yes |
| Ruta del bundle | este bundle | `blueprints/` (`blueprints/cauce/`) | `ruff.toml` `extend-exclude`, `pytest.ini` `norecursedirs`, Bootstrap (`blueprints/cauce/workspace/.`) | yes |
| Script de Python | `scripts/py` | `sh scripts/py` | todos los `Verify`, `.claude/settings.json` (`Bash(sh scripts/py:*)`), `CLAUDE.md`, README | yes |
| Chart.js | `resultados.html` (paso 9) | `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js` + sha512 | `tests/test_resultados.py` (`CHART_JS`, `SRI_CHART_JS`), §11 | yes |
| Rutas de la app | `app.py` — nombres de ruta | `login` → `/login/`, `simulador` → `/app/simulador/`, `api_simular` → `/app/api/simular/` | `web/auth_demo.py` (`reverse('login')`, prefijo `/app/api/`), `tests/test_acceso.py`, `test_simulador.py`, §5 | yes |
| Puerto en Render | Render — `PORT` | `$PORT` (10000) | README Start Command (`--bind 0.0.0.0:$PORT`), `test_produccion.py`, §12 | yes |

#### Byte-exact artifact reconciliation

NOT APPLICABLE — this blueprint authors no byte-exact expected output. Las pruebas afirman
propiedades (claves, órdenes, códigos HTTP, presencia de textos que el propio proyecto escribe),
nunca la salida textual de una librería.

---

## 20. Acceptance Gate, Risks & Decision Log

### 20.1 Global acceptance gate

```bash
sh scripts/py -m pip install --disable-pip-version-check -q -r requirements-dev.txt   # expect: exit 0
sh scripts/py manage.py check                    # expect: exit 0, "System check identified no issues"
sh scripts/py -m ruff check .                    # expect: exit 0, "All checks passed!"
sh scripts/py -m ruff format --check .           # expect: exit 0
sh scripts/py -m pytest                          # expect: exit 0, 0 failed, 0 skipped, 0 warnings
sh scripts/py -m pytest tests/test_health.py::test_servidor_real_sirve_health tests/test_produccion.py   # expect: exit 0 — arranca el servidor real y valida la configuración de Render
sh scripts/py -m pytest tests/test_accesibilidad.py   # expect: exit 0, 0 failed
```

Manual, una vez antes de presentar:

- [ ] `git tag -l 'step-*'` lista las 13 etiquetas, de `step-01-django-health` a `step-13-accesibilidad`.
- [ ] Cada archivo de la tabla "Files that must be committed" está rastreado: `git ls-files --error-unmatch <ruta>` sale con 0, **una ruta por invocación**; y no está ignorado: `git check-ignore -q <ruta>; test $? -eq 1` para cada una.
- [ ] `.gitignore` entró en el commit del Bootstrap: `git log --diff-filter=A --format=%s -- .gitignore` muestra "chore: workspace, configuración y plan de construcción".
- [ ] El Bootstrap de §10 se volvió a ejecutar sobre el árbol ya construido, **terminó con código 0** y luego `sh scripts/py -m pytest` siguió en verde.
- [ ] Todas las filas de *Cross-artifact value reconciliation* dicen `yes` y ruff/pytest se corrieron con el bundle presente.
- [ ] Nada de la tabla Non-Goals de §1 está construido.
- [ ] En Render: `DJANGO_SECRET_KEY` definido; el Health Check en verde; la URL pública responde `/`, `/resultados/` y el flujo login → simulador.
- [ ] Recorrido solo con teclado y una pasada con lector de pantalla por inicio → login → simulador (§15).
- [ ] Un rollback de prueba desde el panel de Render a un deploy anterior.

**Ninguna advertencia se ignora** (`pytest.ini` las convierte en errores).

### 20.2 Risk register

| Risk | Likelihood | Impact | Early signal | Mitigation |
|---|---|---|---|---|
| Arranque en frío de Render (≈1 min) durante la revisión del docente | A | M | La primera visita tarda | Abrir la URL 2 min antes (README); opcional: plan pago |
| El docente toma los datos de ejemplo por resultados reales | M | A | Preguntas sobre las cifras | Aviso "Datos de ejemplo" en todas las páginas (`CAUCE_DATOS_DEMO`), `fuente` en cada JSON y en la API |
| El agente real (etapa 3) no cabe en 512 MB | M | A | RAM > 400 MB en Render | Solo numpy + tabla Q exportada en la web; entrenar fuera; nunca PyTorch en el servidor |
| Los resultados reales no siguen el formato del contrato | M | M | `DatosInvalidos` al reemplazar los JSON | Validadores reutilizables desde notebooks; skill `conectar-resultados-reales` |
| Conflictos de merge entre las dos personas | M | M | Cambios simultáneos en el mismo archivo | Carriles A (`views.py`) y B (`views_app.py`); `app.py` cerrado desde el paso 4 |
| CDN de Chart.js bloqueado en la red de la universidad | B | M | Gráficas vacías | Tablas `<details>` siempre presentes; `graficas.js` las abre si `Chart` no existe |
| Postgres gratis de Render vence a los 30 días (etapa 2) | A | M | Aviso de Render | Decidir el proveedor de base de datos al iniciar la etapa 2 |

### 20.3 Decision log

| # | Decision | Rejected alternative | Why | Would reverse if |
|---|---|---|---|---|
| 1 | Python + Django | FastAPI; Flask | Auth, sesiones, CSRF y ORM listos para la etapa 2 sin escribir seguridad a mano | El equipo debe entregar en Flask por requisito del curso |
| 2 | Rutas en `app.py` (`ROOT_URLCONF = "app"`) | `config/urls.py` estándar | Pedido del usuario; `python app.py` también arranca el servidor | El equipo prefiere la convención de Django |
| 3 | pip + `requirements.txt` | uv + `uv.lock` | Pedido del usuario; Render lo instala sin configuración | Builds lentos o conflictos de dependencias |
| 4 | `requirements-ml.txt` separado | Un solo `requirements.txt` | Decidido con el usuario: builds rápidos y livianos en Render | La web importe numpy en la etapa 3 (entonces numpy pasa a `requirements.txt`) |
| 5 | Login simulado en cookie firmada | Django auth con SQLite | Pedido del usuario; el disco de Render Free es efímero | Etapa 2 |
| 6 | CSS propio con tokens | Tailwind v4 | Sin Node ni build; el sistema de diseño ya viene en variables CSS | El CSS supere ~1.500 líneas o se sume un tercer desarrollador |
| 7 | Chart.js 4.5.1 por CDN | Plotly; gráficas en matplotlib como imágenes | Interactivo, accesible con tablas y liviano; matplotlib no permite tooltips | El docente pida exportar gráficas idénticas a las del informe |
| 8 | Datos de ejemplo en JSON con contrato | Esperar los resultados reales | Permite montar la página hoy | Los notebooks entreguen antes de lo previsto |
| 9 | Inter en lugar de Matter | Comprar Matter; DM Sans | Matter es de pago; Inter es la primera alternativa del propio `DESIGN.md` | Haya presupuesto de licencia |
| 10 | Grafo de red propio en la portada | La esfera de partículas de Auros | No copiar la marca de una empresa real; el grafo representa municipios y recursos | — |

### 20.4 What to build next

1. **Etapa 2 — login real y base de datos** (4–8 nov): `django.contrib.auth` dentro de `web/auth_demo.py`, Postgres (elegir proveedor sin vencimiento a 30 días), guardar simulaciones.
2. **Etapa 3 — resultados reales** (9–20 nov): reemplazar los JSON con la skill `conectar-resultados-reales` y `simular()` por la política Q-learning exportada, conservando firma y formato.
3. **Mapa por municipio**, si los datos reales lo justifican.
4. **Modo claro** para proyectar, si el docente lo pide.

---

*Fin del blueprint. El orden de construcción es §9 (ejecutado desde `tasks.json` y los epics).
Se termina cuando §20.1 está en verde.*
