# Cauce

Sitio web (Django) del proyecto de aprendizaje por refuerzo que asigna recursos ante emergencias en
Colombia con datos de la UNGRD. Lo usan el docente que evalúa y, después, el portafolio del equipo.

## Comandos

Todos se ejecutan desde la raíz del proyecto. `sh scripts/py` usa el Python de `.venv` en Windows
(Git Bash) y en Linux/macOS; en PowerShell, activa `.venv\Scripts\Activate.ps1` y usa `python`.

| Tarea | Comando |
|---|---|
| Crear entorno | `python -m venv .venv` |
| Instalar | `sh scripts/py -m pip install -r requirements-dev.txt` |
| Servidor local | `sh scripts/py app.py` (= `manage.py runserver`) → http://127.0.0.1:8000/ |
| Chequeo de Django | `sh scripts/py manage.py check` |
| Pruebas (todas) | `sh scripts/py -m pytest` |
| Pruebas (un archivo) | `sh scripts/py -m pytest tests/test_rutas.py` |
| Lint | `sh scripts/py -m ruff check .` |
| Formato | `sh scripts/py -m ruff format .` · comprobar: `sh scripts/py -m ruff format --check .` |
| Librerías de ML (notebooks) | `sh scripts/py -m pip install -r requirements-ml.txt` |

**Gate:** `sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check . && sh scripts/py -m pytest`
debe pasar antes de marcar cualquier tarea como hecha.

Python fijado en `.python-version` (3.14; mínimo 3.12). Versiones de dependencias en
`requirements*.txt`: léelas, nunca supongas una. `gunicorn` solo corre en Render (no en Windows).

## Plan de construcción

`blueprints/cauce/tasks.json` dice qué tarea sigue; `blueprints/cauce/epics/*.md` dice cómo hacerla.
Cada tarea termina con un commit `E{n}-T{n}: …` y su etiqueta `step-NN-…`.

## Stack

Django 6.1 (rutas en `app.py`) · plantillas de Django · CSS propio con tokens (sin Tailwind ni compilación) · Chart.js
desde cdnjs · sin base de datos en uso (SQLite declarado) · sesión en cookie firmada · Render (Free).

## Arquitectura

**Camino de una petición.** navegador → `app.py` (única tabla de rutas, `ROOT_URLCONF = "app"`) → `web/views.py`
(páginas públicas) o `web/views_app.py` (login y app) → `web/datos.py` (lee `web/data/mock/*.json`)
→ plantilla en `web/templates/web/` que extiende `base.html` → CSS en `web/static/web/css/`.
El simulador: `simulador.js` hace `POST /app/api/simular/` con JSON → `views_app.api_simular` →
`web/simulacion_demo.simular()` → JSON → el JS pinta la tabla y las cifras.

**Fronteras.**

| Capa | Puede importar | Nunca |
|---|---|---|
| `web/views.py`, `web/views_app.py` | `web.datos`, `web.auth_demo`, `web.simulacion_demo` | Abrir los JSON directamente |
| `web/datos.py` | solo la biblioteca estándar | Importar Django o vistas |
| `web/simulacion_demo.py` | `web.datos.POLITICAS` | Importar Django |
| `web/auth_demo.py` | Django | Ser saltado: la sesión solo se lee con `get_current_user()` |
| Plantillas | variables del contexto y `sitio` / `usuario` | Lógica de negocio, estilos en línea, JS en línea |

**Fuentes únicas de verdad.**

| Tema | Archivo |
|---|---|
| Rutas | `app.py` en la raíz (nombres: inicio, metodologia, resultados, styleguide, health, login, registro, salir, simulador, api_simular, simulaciones, simulacion_detalle) |
| Configuración y variables de entorno | `config/settings.py` |
| Datos que muestran las páginas | `web/datos.py` + `web/data/mock/*.json` |
| Usuario actual | `web/auth_demo.get_current_user()` · proteger vistas: `@login_requerido` |
| Tokens de diseño | `web/static/web/css/tokens.css` |

## Reglas de código

1. Vistas delgadas: leen datos con `web.datos`, llaman un servicio y renderizan. Máx. 30 líneas.
2. Una página = una plantilla que hace `{% extends "web/base.html" %}` con un solo `<h1>`.
3. Todo enlace interno usa `{% url 'nombre' %}`; nunca rutas escritas a mano en plantillas.
4. CSS: colores, tamaños, espacios y radios solo con `var(--…)` de `tokens.css`. El CSS de una
   página va en `web/static/web/css/pages/<pagina>.css`.
5. JS sin dependencias salvo Chart.js; se carga con `defer` desde `{% block scripts %}`. Nada de
   `onclick=` ni `<script>` en línea con lógica (solo `json_script`).
6. Textos visibles en español de Colombia. Mensajes de error que digan cómo corregir.
7. Las pruebas viven en `tests/test_<tema>.py`. Una tarea no inventa ni edita las pruebas de otra.
8. Sin dependencias nuevas sin justificarlas en el commit. Las de ML van en `requirements-ml.txt`.

## Sistema de diseño

Tema oscuro "aguas profundas". Valores completos en `tokens.css`; resumen:

| Rol | Token | Valor |
|---|---|---|
| Fondo de página | `--color-fondo` | `#012624` |
| Panel hundido / fondo de gráficas | `--color-abismo` | `#011d1c` |
| Tarjeta / botón secundario | `--color-alga` | `#003734` |
| Título | `--color-titulo` | `#ffffff` |
| Texto | `--color-texto` | `#bbc7c6` |
| Texto enfatizado y etiquetas | `--color-texto-enfasis` | `#edfffe` |
| Cifras grandes | `--color-cifra` | `#fde9ff` |
| Botón primario | `--gradiente-aurora` con texto `--color-sobre-aurora` | degradado aqua → rosa |
| Borde de campos | `--color-borde-control` | `#869a99` |
| Error / aviso / éxito | `--color-error` / `--color-aviso` / `--color-exito` | `#ffb4a9` / `#ffd479` / `#7ee2b8` |
| Foco | `--color-foco` | `#cbfffc`, contorno de 2px |

- **Tipografía:** Inter (Google Fonts), solo pesos 400 y 500. Títulos 500 con tracking -0.04em;
  etiquetas 12px en mayúsculas con tracking 0.12em; cuerpo 16px / 1.5.
- **Espaciado:** base 4px (`--esp-1` … `--esp-30`). Radios: 6px (botones, campos) y 16px (tarjetas).
- **Elevación:** plana. Sin sombras: la profundidad se expresa con el color de la superficie.
- **Movimiento:** 150–250ms, `--curva-salida`; solo transform y opacity; todo se apaga con
  `prefers-reduced-motion: reduce`.
- **Maquetación:** ancho máx. 1440px, márgenes 16/24/48px (móvil/tableta/escritorio), cortes en
  768px y 1024px, diseño desde móvil, sin scroll horizontal a 320px.
- **Gráficas:** uniforme `--serie-uniforme` discontinua, reglas `--serie-reglas`, RL `--serie-rl`
  gruesa; siempre con tabla alternativa.

## Entorno

| Variable | Obligatoria | La usa | Origen |
|---|---|---|---|
| `DJANGO_SECRET_KEY` | sí en Render | `config/settings.py` | Panel de Render → Environment |
| `DJANGO_DEBUG` | no | `config/settings.py` | 1 en local, 0 en Render por defecto |
| `CAUCE_DATOS_DEMO` | no | `config/settings.py` → aviso "Datos de ejemplo" | 1 por defecto |
| `RENDER`, `RENDER_EXTERNAL_HOSTNAME` | las pone Render | `config/settings.py` | automáticas |

`.env.example` se sube y se mantiene al día. Ningún `.env` con valores reales se sube.

## Reglas por área

| Archivo | Aplica a |
|---|---|
| `.claude/rules/plantillas-y-css.md` | `web/templates/**`, `web/static/**` |
| `.claude/rules/python-django.md` | `config/**`, `web/**/*.py` |
| `.claude/rules/pruebas.md` | `tests/**` |

## No negociable

1. Nunca subir secretos, `.env`, `.venv/` ni `staticfiles/`.
2. Nunca marcar una tarea como hecha con el gate en rojo, ni editar un comando `verify` para que pase.
3. La sesión solo se lee con `get_current_user()`; toda página bajo `/app/` lleva `@login_requerido`.
4. Las páginas solo leen datos con `web.datos`; cambiar los JSON exige que sus validadores pasen.
5. Ningún color, sombra, radio o peso fuera de `tokens.css` (lo vigila `tests/test_estilos.py`).
6. No construir nada de la tabla "Fuera de alcance" de `blueprints/cauce/blueprint.md` §1.
