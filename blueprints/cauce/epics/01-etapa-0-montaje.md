# Epic 01: Etapa 0 — Montaje (la página publicada hoy)

> Al terminar este epic existe un sitio Django navegable con portada, plantilla base accesible,
> tokens de diseño, datos de ejemplo validados y todo lo necesario para que el equipo lo publique
> en Render (plan Free) desde GitHub.

| | |
|---|---|
| **Epic id** | `01-etapa-0-montaje` |
| **Tasks** | `E1-T1` … `E1-T6` (pasos 1 a 6 del plan) |
| **Depends on** | nada — se empieza aquí |
| **Unlocks** | `02-etapa-1-interfaz` |
| **Parallel with** | nada (la etapa 1 empieza cuando este epic termina). Dentro del epic, `E1-T2` y `E1-T3` no comparten archivos y pueden ir en paralelo |

No necesitas ningún otro archivo para completar este epic. Todo lo de abajo se repite aquí a propósito.

---

## Stack

Django 6.1 · Python 3.14 (mínimo 3.12) · plantillas de Django · CSS propio con tokens (sin
compilación) · sin base de datos en uso · sesión en cookie firmada · Render (Free) con gunicorn y
WhiteNoise. Gestor de paquetes: `pip` con `requirements.txt` (web, lo que instala Render),
`requirements-dev.txt` (ruff, pytest) y `requirements-ml.txt` (notebooks; la web no lo usa). Las
versiones exactas están en esos archivos: léelos, nunca supongas una. Python fijado en
`.python-version`.

**Las rutas de la página viven en `app.py`, en la raíz** (`ROOT_URLCONF = "app"`). No existe
`config/urls.py`: el Bootstrap lo borra justo después de generar el proyecto. `python app.py`
arranca el servidor de desarrollo y `python app.py <comando>` equivale a `python manage.py <comando>`.

| Tarea | Comando |
|---|---|
| Servidor local | `sh scripts/py app.py` → http://127.0.0.1:8000/ |
| Chequeo de Django | `sh scripts/py manage.py check` |
| Lint | `sh scripts/py -m ruff check .` |
| Formato | `sh scripts/py -m ruff format --check .` (corregir: `sh scripts/py -m ruff format .`) |
| Pruebas, un archivo | `sh scripts/py -m pytest tests/test_health.py` |
| Pruebas, todas | `sh scripts/py -m pytest` |

`sh scripts/py` ejecuta el Python de `.venv` en Windows (Git Bash) y en Linux/macOS. Todos los
comandos se ejecutan **desde la raíz del proyecto** (la carpeta que contiene `docs/` y
`blueprints/`). En PowerShell no funciona `sh`: usa Git Bash, o activa `.venv\Scripts\Activate.ps1`
y cambia `sh scripts/py` por `python`.

**Gate:** `sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check . && sh scripts/py -m pytest`
pasa antes de marcar cualquier tarea de este epic como hecha.

No hay servicios locales que levantar: ninguna prueba de este epic necesita base de datos ni red.

## Antes de `E1-T1`: Bootstrap (una sola vez; se puede repetir sin riesgo)

Requisitos en la máquina: Git ≥ 2.28 con `user.name` y `user.email` configurados
(`git config user.email` imprime un correo), Python ≥ 3.12 en el PATH como `python`
(o `python3`), y una terminal `sh` (Git Bash en Windows). Desde la raíz del proyecto:

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

Qué deja: el repositorio (si ya existía, con sus commits intactos) más un commit del workspace
con `.gitignore` ya presente, así `.venv/` nunca se sube, `.venv/` con Django, gunicorn, whitenoise, ruff, pytest y pytest-django, y el esqueleto
generado por Django (`manage.py`, `config/__init__.py`, `config/asgi.py`, `config/settings.py`,
`config/wsgi.py`). `E1-T1` reemplaza `config/settings.py` por completo. El esqueleto generado no
se sube hasta el commit de `E1-T1`, así su clave secreta aleatoria nunca entra al historial.

## Directory subtree

```
app.py                          # NUEVO en E1-T1 · la tabla única de rutas; crece en E1-T4
manage.py                       # generado por el Bootstrap · no se edita
config/
  settings.py                   # E1-T1 lo reemplaza entero (contenido literal abajo)
  wsgi.py, asgi.py, __init__.py # generados · no se editan (Render arranca config.wsgi)
web/
  __init__.py, apps.py          # vienen del workspace · no se editan
  views.py                      # E1-T1 (health) → E1-T4 (todas las páginas provisionales) → E1-T5 (portada)
  views_app.py                  # NUEVO en E1-T4 · acceso y app, provisionales (etapa 1 los completa)
  context_processors.py         # NUEVO en E1-T1 · variable `sitio` en todas las plantillas
  datos.py                      # NUEVO en E1-T2 · contrato de datos
  data/mock/*.json              # NUEVO en E1-T2 · datos de ejemplo
  templates/
    404.html, 500.html          # NUEVO en E1-T6
    web/base.html               # NUEVO en E1-T4
    web/inicio.html             # NUEVO en E1-T5
  static/web/
    css/tokens.css              # NUEVO en E1-T3 (literal)
    css/base.css                # NUEVO en E1-T3
    css/components.css          # NUEVO en E1-T3 (la etapa 1 lo amplía)
    css/pages/inicio.css        # NUEVO en E1-T5
    js/red.js                   # NUEVO en E1-T5
tests/
  test_health.py · test_datos.py · test_estilos.py · test_rutas.py · test_inicio.py · test_produccion.py
README.md                       # NUEVO en E1-T6 (literal)
```

Todo lo que está fuera de este árbol queda fuera del alcance del epic. Si una tarea parece
requerir editar otro archivo, detente e informa: significa que el límite del epic está mal.

## Data model touched here

No hay tablas: la etapa 1 no usa base de datos. Los "datos" son tres archivos JSON con un
contrato que valida `web/datos.py`:

| Archivo | Claves que lee la web | Reglas |
|---|---|---|
| `resultados.json` | `fuente`, `resumen` (4 cifras `id`/`valor`/`etiqueta`), `politicas`, `metricas`, `recompensa_por_episodio`, `sensibilidad_presupuesto`, `estabilidad` | Cada métrica y serie trae exactamente `uniforme`, `reglas`, `rl`; cada serie mide lo mismo que su eje |
| `perfiles.json` | `fuente`, `k`, `ejes`, `perfiles` (id, nombre, descripcion, n_eventos, centroide), `puntos` (x, y, perfil) | `k` = número de perfiles; cada punto apunta a un perfil existente |
| `simulaciones.json` | `simulaciones` (id, nombre, fecha, parametros, resultado) | ids únicos; cada métrica del resultado trae las tres políticas |

## Contracts

**Consumed** — nada: este epic es el primero.

**Produced** — la etapa 1 depende exactamente de estas firmas. Cambiarlas la rompe:

| Export | Signature | Used by |
|---|---|---|
| `app.py` → nombres de ruta | `inicio`, `metodologia`, `resultados`, `styleguide`, `health`, `login`, `registro`, `salir`, `simulador`, `api_simular`, `simulaciones`, `simulacion_detalle` | `02-etapa-1-interfaz` (plantillas con `{% url %}` y pruebas) |
| `web/datos.py` → `resultados()`, `perfiles()` | `() -> dict`, validados y en caché | `02-etapa-1-interfaz` |
| `web/datos.py` → `simulaciones()`, `simulacion(sim_id)` | `() -> list[dict]`, `(str) -> dict \| None` | `02-etapa-1-interfaz` |
| `web/datos.py` → `POLITICAS`, `DatosInvalidos` | `("uniforme", "reglas", "rl")`, subclase de `ValueError` | `02-etapa-1-interfaz` |
| `web/templates/web/base.html` | bloques `titulo`, `estilos`, `contenido`, `scripts`; variables `titulo`, `sitio`, `usuario` | todas las páginas |
| `web/static/web/css/tokens.css` | las variables listadas en `tests/test_estilos.py` | todo el CSS |

## Conventions that bite in this area

- **Las rutas están en `app.py`, no en `config/urls.py`.** Si ves `config/urls.py`, el Bootstrap no
  terminó: bórralo. `ROOT_URLCONF = "app"` ya está en el `settings.py` literal de `E1-T1`.
- **Los archivos marcados "contenido literal completo" se copian tal cual**, reemplazando la
  versión anterior entera. Las pruebas se copian sin editarlas; si una falla, se corrige el código.
- **`pytest.ini` convierte toda advertencia en error.** Una advertencia es una falla: corrige la causa.
- **WhiteNoise solo se activa en Render** (`RENDER=true`). En local, `runserver` con `DEBUG` sirve
  el CSS. Por eso las pruebas no necesitan `collectstatic`, salvo la de producción que lo ejecuta.
- **Ningún color literal fuera de `tokens.css`**, ni sombras, ni radios > 16px, ni pesos distintos
  de 400/500 en ningún CSS: `tests/test_estilos.py` revisa todos los archivos `.css`, también los que
  se creen después.
- **`gunicorn` no corre en Windows.** Se instala, pero solo se usa en Render.

Reglas completas del proyecto: `CLAUDE.md`. Reglas por área: `.claude/rules/*.md`. Ambas están en
la raíz del proyecto desde el Bootstrap.

---

## Tasks

En el mismo orden que `tasks.json`. Ese orden es el de construcción: de arriba abajo, sin reordenar.

### `E1-T1` — Proyecto Django con chequeo de salud /health/

**Depends on:** nada · **Priority:** p0 — metadato para recortes de alcance, no un orden

Reemplaza la configuración generada por una que lee todo de variables de entorno: en local
funciona sin configurar nada; en Render (`RENDER=true`) exige `DJANGO_SECRET_KEY`, apaga `DEBUG` y
acepta el dominio `*.onrender.com`. Las rutas viven en `app.py`, que además arranca el servidor de
desarrollo. La prueba levanta `runserver` de verdad y pide `/health/` por HTTP, y comprueba que
`python app.py check` funciona: así el punto de entrada se ejercita desde el primer paso.

**Files**
- `config/settings.py` — reemplazo completo
- `app.py` — nuevo
- `web/views.py` — nuevo
- `web/context_processors.py` — nuevo
- `tests/test_health.py` — nuevo

**`config/settings.py`** (contenido literal completo):

```python
"""Configuración de Django para Cauce.

Todo se lee de variables de entorno. En Render (RENDER=true) se exige DJANGO_SECRET_KEY y
DEBUG queda apagado; en un computador local funciona sin configurar nada.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Render define RENDER=true en todos sus servicios.
EN_RENDER = os.environ.get("RENDER") == "true"

DEBUG = os.environ.get("DJANGO_DEBUG", "0" if EN_RENDER else "1") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if EN_RENDER:
        raise ImproperlyConfigured("Falta la variable de entorno DJANGO_SECRET_KEY")
    SECRET_KEY = "solo-desarrollo-local-nunca-en-produccion"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS: list[str] = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if EN_RENDER:
    # WhiteNoise sirve el CSS/JS ya recolectado (collectstatic) en producción. En local lo
    # sirve `runserver` con DEBUG activo.
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "app"  # rutas en app.py (raíz del proyecto)
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "web.context_processors.sitio",
            ],
        },
    },
]

# Etapa 1: sin base de datos en uso. SQLite queda declarado para que la etapa 2 solo tenga
# que cambiar este bloque (Postgres) y activar django.contrib.auth.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Sesión en una cookie firmada: el login simulado no necesita base de datos.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = EN_RENDER
CSRF_COOKIE_SECURE = EN_RENDER
if EN_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if EN_RENDER
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        )
    },
}

# Muestra el aviso "Datos de ejemplo" en todas las páginas mientras no haya resultados reales.
CAUCE_DATOS_DEMO = os.environ.get("CAUCE_DATOS_DEMO", "1") == "1"
```

**`app.py`** (contenido literal completo):

```python
"""Rutas de la página Cauce: la ÚNICA tabla de URLs del proyecto (ROOT_URLCONF = "app").

En el paso 4 esta tabla crece con todas las páginas. Atajo: `python app.py` arranca el servidor
de desarrollo (equivale a `manage.py runserver`); `python app.py <comando>` ejecuta cualquier
comando de manage.py, p. ej. `python app.py check`.
"""

from django.urls import path

from web import views

urlpatterns = [
    path("health/", views.health, name="health"),
]


if __name__ == "__main__":
    import os
    import sys

    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line([sys.argv[0], *(sys.argv[1:] or ["runserver"])])
```

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.http import HttpRequest, JsonResponse


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**`web/context_processors.py`** (contenido literal completo):

```python
"""Variables disponibles en todas las plantillas."""

from django.conf import settings
from django.http import HttpRequest


def sitio(request: HttpRequest) -> dict:
    return {
        "sitio": {
            "nombre": "Cauce",
            "subtitulo": "Asignación inteligente de recursos ante emergencias",
            "datos_demo": settings.CAUCE_DATOS_DEMO,
        }
    }
```

**`tests/test_health.py`** (contenido literal completo):

```python
"""Paso 1: el proyecto arranca, app.py tiene las rutas y /health/ responde de verdad."""

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def test_health_responde_ok(client):
    respuesta = client.get("/health/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok", "app": "cauce"}


def test_ruta_inexistente_es_404(client):
    assert client.get("/no-existe/").status_code == 404


def test_contexto_del_sitio(rf):
    from web.context_processors import sitio

    datos = sitio(rf.get("/"))["sitio"]
    assert datos["nombre"] == "Cauce"
    assert isinstance(datos["datos_demo"], bool)


def _puerto_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_servidor_real_sirve_health():
    """Levanta `manage.py runserver` de verdad y pide /health/ por HTTP."""
    puerto = _puerto_libre()
    entorno = {**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings"}
    entorno.pop("RENDER", None)
    proceso = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", f"127.0.0.1:{puerto}", "--noreload"],
        cwd=RAIZ,
        env=entorno,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        cuerpo = None
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/health/", timeout=2) as r:
                    assert r.status == 200
                    cuerpo = json.loads(r.read())
                    break
            except OSError:
                time.sleep(0.5)
        assert cuerpo == {"status": "ok", "app": "cauce"}
    finally:
        proceso.terminate()
        proceso.wait(timeout=10)


def test_app_py_es_la_tabla_de_rutas_y_ejecuta_comandos():
    """`python app.py check` funciona igual que `manage.py check`."""
    from django.conf import settings

    assert settings.ROOT_URLCONF == "app"
    resultado = subprocess.run(
        [sys.executable, "app.py", "check"],
        cwd=RAIZ,
        env={k: v for k, v in os.environ.items() if k != "RENDER"},
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert resultado.returncode == 0, resultado.stderr
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se ejecuta `sh scripts/py manage.py check` THE SYSTEM SHALL terminar con código 0 sin reportar problemas.
2. WHEN llega un GET a /health/ THE SYSTEM SHALL responder 200 con el JSON {"status": "ok", "app": "cauce"}.
3. WHEN se arranca `manage.py runserver` como proceso real THE SYSTEM SHALL servir /health/ por HTTP con estado 200 (prueba test_servidor_real_sirve_health).
4. WHEN se ejecuta `sh scripts/py app.py check` THE SYSTEM SHALL terminar con código 0, y `settings.ROOT_URLCONF` SHALL ser "app" (las rutas viven en app.py).
5. WHEN se pide una ruta que ninguna URL define THE SYSTEM SHALL responder 404.
6. WHEN se ejecutan `sh scripts/py -m ruff check .` y `sh scripts/py -m ruff format --check .` desde la raíz, con el bundle presente en blueprints/ THE SYSTEM SHALL terminar con código 0.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py manage.py check
sh scripts/py app.py check
sh scripts/py -m pytest tests/test_health.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T1: Proyecto Django con chequeo de salud /health/"
git tag step-01-django-health
```

Si la siguiente tarea sale mal: `git reset --hard step-01-django-health` y repetirla.

### `E1-T2` — Contrato de datos y JSON de ejemplo

**Depends on:** `E1-T1` · **Priority:** p0

Las páginas nunca abren un JSON: llaman a `web.datos`. Hoy los tres archivos son **datos de
ejemplo** coherentes con el proyecto (políticas uniforme, reglas y RL; cuatro perfiles de K-means).
Cuando los notebooks exporten resultados reales con la misma forma, se reemplazan los archivos y
nada más cambia. `datos.py` no importa Django, para que los notebooks lo reutilicen y validen sus
exportaciones.

**Files**
- `web/data/mock/resultados.json` — nuevo
- `web/data/mock/perfiles.json` — nuevo
- `web/data/mock/simulaciones.json` — nuevo
- `web/datos.py` — nuevo
- `tests/test_datos.py` — nuevo

**`web/data/mock/resultados.json`** (contenido literal completo):

```json
{
  "fuente": "datos_de_ejemplo",
  "actualizado": "2026-10-24",
  "resumen": [
    {"id": "registros", "valor": "41.823", "etiqueta": "Registros UNGRD analizados"},
    {"id": "periodo", "valor": "2010–2025", "etiqueta": "Periodo cubierto"},
    {"id": "municipios", "valor": "1.103", "etiqueta": "Municipios con eventos"},
    {"id": "mejora_rl", "valor": "+12,4 pp", "etiqueta": "Necesidades atendidas: RL frente a reglas"}
  ],
  "politicas": [
    {"id": "uniforme", "nombre": "Política uniforme"},
    {"id": "reglas", "nombre": "Basada en reglas"},
    {"id": "rl", "nombre": "Agente RL (Q-learning)"}
  ],
  "metricas": [
    {
      "id": "necesidades_atendidas_pct",
      "nombre": "Necesidades atendidas",
      "unidad": "%",
      "mejor": "mayor",
      "valores": {"uniforme": 58.6, "reglas": 69.1, "rl": 81.5}
    },
    {
      "id": "tiempo_atencion_h",
      "nombre": "Tiempo simulado hasta la atención",
      "unidad": "h",
      "mejor": "menor",
      "valores": {"uniforme": 31.2, "reglas": 22.8, "rl": 17.4}
    },
    {
      "id": "costo_total_mcop",
      "nombre": "Costo total de asignación",
      "unidad": "M COP",
      "mejor": "menor",
      "valores": {"uniforme": 940.0, "reglas": 905.5, "rl": 872.3}
    },
    {
      "id": "emergencias_sin_recursos",
      "nombre": "Emergencias sin recursos",
      "unidad": "eventos",
      "mejor": "menor",
      "valores": {"uniforme": 6.0, "reglas": 3.0, "rl": 1.0}
    }
  ],
  "recompensa_por_episodio": {
    "episodios": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
    "series": {
      "uniforme": [-121.1, -121.4, -118.0, -121.2, -118.2, -119.1, -120.8, -118.1, -120.9, -118.5, -120.6],
      "reglas": [-82.5, -79.8, -76.9, -80.9, -80.1, -77.5, -75.5, -77.7, -78.7, -75.2, -80.8],
      "rl": [-156.4, -123.2, -98.6, -81.4, -67.7, -54.8, -55.9, -48.4, -45.4, -46.5, -43.7]
    }
  },
  "sensibilidad_presupuesto": {
    "presupuesto_pct": [50, 75, 100, 125, 150],
    "series": {
      "uniforme": [34.2, 47.9, 58.6, 66.0, 71.8],
      "reglas": [43.5, 58.0, 69.1, 76.4, 81.0],
      "rl": [52.7, 68.9, 81.5, 87.2, 90.6]
    }
  },
  "estabilidad": {
    "desviacion_recompensa": {"uniforme": 2.1, "reglas": 2.4, "rl": 6.8},
    "semillas": 10
  }
}
```

**`web/data/mock/perfiles.json`** (contenido literal completo):

```json
{
  "fuente": "datos_de_ejemplo",
  "actualizado": "2026-10-24",
  "k": 4,
  "ejes": {"x": "Personas afectadas (log10)", "y": "Viviendas averiadas o destruidas (log10)"},
  "perfiles": [
    {
      "id": 0,
      "nombre": "Impacto bajo y localizado",
      "descripcion": "Pocas familias afectadas y daños menores en viviendas.",
      "n_eventos": 13304,
      "centroide": {"x": 2.0, "y": 1.2}
    },
    {
      "id": 1,
      "nombre": "Daño en viviendas",
      "descripcion": "Muchas viviendas averiadas con afectación moderada de personas.",
      "n_eventos": 12061,
      "centroide": {"x": 3.0, "y": 3.4}
    },
    {
      "id": 2,
      "nombre": "Afectación masiva",
      "descripcion": "Gran número de personas y familias afectadas; típico de inundaciones extensas.",
      "n_eventos": 5461,
      "centroide": {"x": 4.4, "y": 3.0}
    },
    {
      "id": 3,
      "nombre": "Emergencia crítica",
      "descripcion": "Alta afectación de personas y viviendas a la vez; requiere prioridad.",
      "n_eventos": 13020,
      "centroide": {"x": 4.6, "y": 4.4}
    }
  ],
  "puntos": [
    {"x": 2.16, "y": 1.27, "perfil": 0},
    {"x": 2.21, "y": 1.93, "perfil": 0},
    {"x": 1.61, "y": 1.39, "perfil": 0},
    {"x": 1.53, "y": 0.92, "perfil": 0},
    {"x": 1.73, "y": 2.05, "perfil": 0},
    {"x": 1.88, "y": 0.84, "perfil": 0},
    {"x": 1.46, "y": 0.92, "perfil": 0},
    {"x": 2.57, "y": 0.63, "perfil": 0},
    {"x": 1.67, "y": 2.56, "perfil": 0},
    {"x": 2.38, "y": 1.55, "perfil": 0},
    {"x": 2.36, "y": 4.37, "perfil": 1},
    {"x": 1.87, "y": 4.0, "perfil": 1},
    {"x": 3.56, "y": 3.7, "perfil": 1},
    {"x": 3.22, "y": 2.5, "perfil": 1},
    {"x": 2.75, "y": 3.79, "perfil": 1},
    {"x": 2.11, "y": 3.42, "perfil": 1},
    {"x": 3.2, "y": 3.49, "perfil": 1},
    {"x": 2.9, "y": 4.17, "perfil": 1},
    {"x": 3.74, "y": 3.72, "perfil": 1},
    {"x": 2.76, "y": 4.01, "perfil": 1},
    {"x": 4.58, "y": 2.63, "perfil": 2},
    {"x": 3.84, "y": 3.49, "perfil": 2},
    {"x": 4.95, "y": 3.08, "perfil": 2},
    {"x": 4.52, "y": 3.22, "perfil": 2},
    {"x": 5.2, "y": 3.31, "perfil": 2},
    {"x": 4.66, "y": 3.27, "perfil": 2},
    {"x": 3.62, "y": 3.64, "perfil": 2},
    {"x": 4.88, "y": 3.26, "perfil": 2},
    {"x": 3.41, "y": 2.68, "perfil": 2},
    {"x": 4.82, "y": 2.09, "perfil": 2},
    {"x": 4.28, "y": 3.27, "perfil": 3},
    {"x": 4.44, "y": 4.04, "perfil": 3},
    {"x": 4.62, "y": 4.57, "perfil": 3},
    {"x": 4.94, "y": 4.88, "perfil": 3},
    {"x": 5.35, "y": 4.46, "perfil": 3},
    {"x": 4.73, "y": 4.7, "perfil": 3},
    {"x": 4.9, "y": 4.79, "perfil": 3},
    {"x": 4.33, "y": 4.18, "perfil": 3},
    {"x": 5.16, "y": 4.96, "perfil": 3},
    {"x": 5.16, "y": 4.22, "perfil": 3}
  ]
}
```

**`web/data/mock/simulaciones.json`** (contenido literal completo):

```json
{
  "fuente": "datos_de_ejemplo",
  "simulaciones": [
    {
      "id": "sim-001",
      "nombre": "Presupuesto base",
      "fecha": "2026-10-20",
      "parametros": {"presupuesto": 100, "recursos": 20, "emergencias": 8, "semilla": 42},
      "resultado": {
        "necesidades_atendidas_pct": {"uniforme": 58.6, "reglas": 69.1, "rl": 81.5},
        "emergencias_sin_recursos": {"uniforme": 6, "reglas": 3, "rl": 1}
      }
    },
    {
      "id": "sim-002",
      "nombre": "Presupuesto recortado al 50 %",
      "fecha": "2026-10-21",
      "parametros": {"presupuesto": 50, "recursos": 12, "emergencias": 8, "semilla": 7},
      "resultado": {
        "necesidades_atendidas_pct": {"uniforme": 34.2, "reglas": 43.5, "rl": 52.7},
        "emergencias_sin_recursos": {"uniforme": 9, "reglas": 6, "rl": 4}
      }
    },
    {
      "id": "sim-003",
      "nombre": "Temporada de lluvias (12 emergencias)",
      "fecha": "2026-10-22",
      "parametros": {"presupuesto": 125, "recursos": 30, "emergencias": 12, "semilla": 2026},
      "resultado": {
        "necesidades_atendidas_pct": {"uniforme": 61.0, "reglas": 72.3, "rl": 84.9},
        "emergencias_sin_recursos": {"uniforme": 7, "reglas": 4, "rl": 2}
      }
    }
  ]
}
```

**`web/datos.py`** (contenido literal completo):

```python
"""Contrato de datos de Cauce.

Las páginas solo leen datos a través de este módulo. Hoy los JSON de `web/data/mock/` son
datos de EJEMPLO; cuando los notebooks del proyecto exporten resultados reales con el mismo
formato, basta con reemplazar esos archivos (y poner CAUCE_DATOS_DEMO=0). Ninguna plantilla
ni vista cambia.
"""

import json
from functools import cache
from pathlib import Path

DIRECTORIO_DATOS = Path(__file__).resolve().parent / "data" / "mock"
POLITICAS = ("uniforme", "reglas", "rl")


class DatosInvalidos(ValueError):
    """Un archivo de datos no cumple el contrato."""


def _leer(nombre: str) -> dict:
    with open(DIRECTORIO_DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def _exigir(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise DatosInvalidos(mensaje)


def _exigir_politicas(valores: dict, donde: str) -> None:
    _exigir(
        isinstance(valores, dict) and set(valores) == set(POLITICAS),
        f"{donde}: debe tener exactamente las políticas {POLITICAS}",
    )


def validar_resultados(datos: dict) -> None:
    for clave in (
        "fuente",
        "resumen",
        "politicas",
        "metricas",
        "recompensa_por_episodio",
        "sensibilidad_presupuesto",
        "estabilidad",
    ):
        _exigir(clave in datos, f"resultados.json: falta la clave '{clave}'")
    _exigir(len(datos["resumen"]) == 4, "resultados.json: 'resumen' debe tener 4 cifras")
    for cifra in datos["resumen"]:
        _exigir({"id", "valor", "etiqueta"} <= set(cifra), "resultados.json: cifra incompleta")
    _exigir(
        [p["id"] for p in datos["politicas"]] == list(POLITICAS),
        "resultados.json: 'politicas' debe listar uniforme, reglas, rl en ese orden",
    )
    for metrica in datos["metricas"]:
        _exigir(
            {"id", "nombre", "unidad", "mejor", "valores"} <= set(metrica),
            "resultados.json: métrica incompleta",
        )
        _exigir(metrica["mejor"] in ("mayor", "menor"), "resultados.json: 'mejor' inválido")
        _exigir_politicas(metrica["valores"], f"métrica {metrica['id']}")
    for clave, eje in (
        ("recompensa_por_episodio", "episodios"),
        ("sensibilidad_presupuesto", "presupuesto_pct"),
    ):
        bloque = datos[clave]
        _exigir_politicas(bloque["series"], clave)
        for politica in POLITICAS:
            _exigir(
                len(bloque["series"][politica]) == len(bloque[eje]),
                f"{clave}: la serie '{politica}' no tiene la misma longitud que '{eje}'",
            )
    _exigir_politicas(datos["estabilidad"]["desviacion_recompensa"], "estabilidad")


def validar_perfiles(datos: dict) -> None:
    for clave in ("fuente", "k", "ejes", "perfiles", "puntos"):
        _exigir(clave in datos, f"perfiles.json: falta la clave '{clave}'")
    _exigir(len(datos["perfiles"]) == datos["k"], "perfiles.json: 'k' no coincide con los perfiles")
    ids = {perfil["id"] for perfil in datos["perfiles"]}
    for punto in datos["puntos"]:
        _exigir(punto["perfil"] in ids, f"perfiles.json: punto con perfil desconocido {punto}")


def validar_simulaciones(datos: dict) -> None:
    _exigir("simulaciones" in datos, "simulaciones.json: falta la clave 'simulaciones'")
    vistos: set[str] = set()
    for sim in datos["simulaciones"]:
        for clave in ("id", "nombre", "fecha", "parametros", "resultado"):
            _exigir(clave in sim, f"simulaciones.json: a una simulación le falta '{clave}'")
        _exigir(sim["id"] not in vistos, f"simulaciones.json: id repetido {sim['id']}")
        vistos.add(sim["id"])
        for metrica in sim["resultado"].values():
            _exigir_politicas(metrica, f"simulación {sim['id']}")


@cache
def resultados() -> dict:
    datos = _leer("resultados.json")
    validar_resultados(datos)
    return datos


@cache
def perfiles() -> dict:
    datos = _leer("perfiles.json")
    validar_perfiles(datos)
    return datos


@cache
def simulaciones() -> list[dict]:
    datos = _leer("simulaciones.json")
    validar_simulaciones(datos)
    return datos["simulaciones"]


def simulacion(sim_id: str) -> dict | None:
    return next((sim for sim in simulaciones() if sim["id"] == sim_id), None)
```

**`tests/test_datos.py`** (contenido literal completo):

```python
"""Paso 2: los JSON de ejemplo cumplen el contrato de web/datos.py."""

import copy

import pytest

from web import datos


def test_resultados_cumplen_contrato():
    resultados = datos.resultados()
    assert resultados["fuente"] == "datos_de_ejemplo"
    assert [m["id"] for m in resultados["metricas"]] == [
        "necesidades_atendidas_pct",
        "tiempo_atencion_h",
        "costo_total_mcop",
        "emergencias_sin_recursos",
    ]


def test_perfiles_cumplen_contrato():
    perfiles = datos.perfiles()
    assert perfiles["k"] == len(perfiles["perfiles"])
    assert len(perfiles["puntos"]) >= 20


def test_simulaciones_y_busqueda_por_id():
    sims = datos.simulaciones()
    assert len(sims) >= 1
    primera = sims[0]
    assert datos.simulacion(primera["id"]) == primera
    assert datos.simulacion("no-existe") is None


def test_resultado_con_politica_faltante_es_invalido():
    roto = copy.deepcopy(datos.resultados())
    del roto["metricas"][0]["valores"]["rl"]
    with pytest.raises(datos.DatosInvalidos, match="políticas"):
        datos.validar_resultados(roto)


def test_serie_con_longitud_distinta_es_invalida():
    roto = copy.deepcopy(datos.resultados())
    roto["recompensa_por_episodio"]["series"]["rl"].pop()
    with pytest.raises(datos.DatosInvalidos, match="misma longitud"):
        datos.validar_resultados(roto)


def test_punto_con_perfil_desconocido_es_invalido():
    roto = copy.deepcopy(datos.perfiles())
    roto["puntos"][0]["perfil"] = 99
    with pytest.raises(datos.DatosInvalidos, match="perfil desconocido"):
        datos.validar_perfiles(roto)
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se llama `web.datos.resultados()` THE SYSTEM SHALL devolver web/data/mock/resultados.json con `fuente` igual a "datos_de_ejemplo" y las métricas necesidades_atendidas_pct, tiempo_atencion_h, costo_total_mcop y emergencias_sin_recursos en ese orden.
2. WHEN a una métrica le falta alguna de las políticas uniforme, reglas o rl THE SYSTEM SHALL lanzar `web.datos.DatosInvalidos` con un mensaje que contiene "políticas".
3. WHEN una serie de recompensa_por_episodio o sensibilidad_presupuesto tiene distinta longitud que su eje THE SYSTEM SHALL lanzar `DatosInvalidos` con un mensaje que contiene "misma longitud".
4. WHEN un punto de K-means apunta a un perfil que perfiles.json no define THE SYSTEM SHALL lanzar `DatosInvalidos` con un mensaje que contiene "perfil desconocido".
5. WHEN se llama `web.datos.simulacion(id)` con un id inexistente THE SYSTEM SHALL devolver None, y con un id existente SHALL devolver el diccionario de esa simulación.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_datos.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T2: Contrato de datos y JSON de ejemplo"
git tag step-02-contrato-datos
```

Si la siguiente tarea sale mal: `git reset --hard step-02-contrato-datos` y repetirla.

### `E1-T3` — Tokens del sistema de diseño y CSS base

**Depends on:** `E1-T1` · **Priority:** p0

`tokens.css` es literal: es el sistema de diseño de `docs/design/` (estilo "aguas profundas")
con las correcciones aprobadas (Inter en lugar de Matter, contraste medido, sin sombras, solo dos
radios). `base.css` y `components.css` los escribes tú con las especificaciones de abajo, **usando
solo `var(--…)`**. La prueba revisa todos los `.css`, incluidos los que se creen después.

**Files**
- `web/static/web/css/tokens.css` — nuevo (literal)
- `web/static/web/css/base.css` — nuevo
- `web/static/web/css/components.css` — nuevo
- `tests/test_estilos.py` — nuevo (literal)

**`web/static/web/css/tokens.css`** (contenido literal completo):

```css
/*
 * Cauce — tokens del sistema de diseño.
 * Basado en docs/design/ (estilo "aguas profundas"), con las correcciones del blueprint §7.
 * ÚNICO archivo con colores literales: el resto del CSS usa var(--…).
 */
:root {
  /* Superficies, de la más hundida a la más elevada. Sin sombras: la profundidad es color. */
  --color-abismo: #011d1c; /* pie, paneles hundidos, fondo de gráficas */
  --color-fondo: #012624; /* lienzo de la página */
  --color-alga: #003734; /* tarjetas, botón secundario */
  --color-pizarra: #707777; /* SOLO bordes y estados desactivados; nunca texto (3.5:1) */

  /* Texto */
  --color-titulo: #ffffff; /* títulos, navegación activa */
  --color-texto: #bbc7c6; /* cuerpo (9.3:1 sobre el fondo) */
  --color-texto-enfasis: #edfffe; /* etiquetas y cuerpo destacado */
  --color-cita: #f2f2f2;
  --color-cifra: #fde9ff; /* cifras grandes; nunca texto corrido */

  /* Acentos */
  --color-teal: #00827c; /* solo gráficas y degradados (3.4:1, no apto para texto) */
  --color-aqua: #cbfffc;
  --color-boton-icono: rgba(3, 81, 75, 0.5);
  --gradiente-aurora: linear-gradient(
    90deg,
    #cbfffc 0%,
    #edfffe 26.25%,
    #fffdfa 47.57%,
    #fad1ff 88.96%
  ); /* SOLO el botón primario */
  --gradiente-bioluminiscente: linear-gradient(90deg, #00827c 0%, #cbfffc 100%); /* barras y deslizadores */
  --color-sobre-aurora: #012624; /* texto sobre el degradado aurora (≥12:1) */

  /* Bordes */
  --color-borde: rgba(255, 255, 255, 0.12); /* separadores decorativos */
  --color-borde-control: #869a99; /* bordes de campos: 4.4:1 sobre alga, 5.4:1 sobre fondo */

  /* Estados (extensión del sistema original, solo para estados) */
  --color-error: #ffb4a9;
  --color-aviso: #ffd479;
  --color-exito: #7ee2b8;
  --color-foco: #cbfffc;

  /* Gráficas: el color nunca va solo, siempre con estilo de línea o marcador */
  --serie-uniforme: #bbc7c6; /* línea discontinua / barras rayadas */
  --serie-reglas: #00827c; /* línea continua */
  --serie-rl: #fde9ff; /* línea continua gruesa: la protagonista */
  --perfil-0: #fde9ff; /* círculo */
  --perfil-1: #cbfffc; /* triángulo */
  --perfil-2: #00827c; /* cuadrado */
  --perfil-3: #bbc7c6; /* rombo */
  --fondo-grafica: #011d1c;
  --rejilla-grafica: rgba(255, 255, 255, 0.08);

  /* Tipografía: Inter (Google Fonts) sustituye a Matter. Solo pesos 400 y 500. */
  --fuente: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --peso-regular: 400;
  --peso-medio: 500;
  --texto-etiqueta: 0.75rem; /* 12px, mayúsculas */
  --texto-pequeno: 0.875rem; /* 14px */
  --texto-base: 1rem; /* 16px */
  --texto-destacado: 1.25rem; /* 20px */
  --texto-subtitulo: 1.5rem; /* 24px */
  --texto-titulo: clamp(1.75rem, 1.2rem + 2vw, 2.25rem); /* 28 → 36px */
  --texto-titulo-lg: clamp(2.1rem, 1.4rem + 3.5vw, 3.8rem); /* 34 → 61px */
  --texto-display: clamp(2.5rem, 1.5rem + 5vw, 6rem); /* 40 → 96px */
  --tracking-etiqueta: 0.12em;
  --tracking-titulo: -0.04em;
  --tracking-subtitulo: -0.02em;
  --interlineado-titulo: 1;
  --interlineado-cuerpo: 1.5;

  /* Espaciado: base 4px */
  --esp-1: 4px;
  --esp-2: 8px;
  --esp-3: 12px;
  --esp-4: 16px;
  --esp-5: 20px;
  --esp-6: 24px;
  --esp-8: 32px;
  --esp-9: 36px;
  --esp-10: 40px;
  --esp-12: 48px;
  --esp-16: 64px;
  --esp-20: 80px;
  --esp-30: 120px;

  /* Maquetación */
  --ancho-max: 1440px;
  --ancho-lectura: 65ch;
  --margen-lateral: 16px; /* base.css lo sube a 24px (≥768px) y 48px (≥1024px) */
  --relleno-tarjeta: clamp(24px, 3vw, 48px);
  --separacion-seccion: clamp(64px, 10vw, 120px);
  --alto-cabecera: 72px;

  /* Forma: solo dos radios */
  --radio-pequeno: 6px; /* botones, campos, insignias */
  --radio-tarjeta: 16px; /* tarjetas y paneles */

  /* Movimiento */
  --duracion-rapida: 150ms;
  --duracion-media: 250ms;
  --curva-salida: cubic-bezier(0.2, 0, 0, 1);
}
```

**`web/static/web/css/base.css`** — escríbelo con exactamente esto:

| Selector / regla | Especificación |
|---|---|
| `*, *::before, *::after` | `box-sizing: border-box` |
| `html` | `-webkit-text-size-adjust: 100%`; `scroll-behavior: smooth` solo dentro de `@media (prefers-reduced-motion: no-preference)` |
| `body` | `margin: 0`; `background: var(--color-fondo)`; `color: var(--color-texto)`; `font-family: var(--fuente)`; `font-size: var(--texto-base)`; `line-height: var(--interlineado-cuerpo)`; `font-weight: var(--peso-regular)`; `min-height: 100vh`; `display: flex; flex-direction: column` |
| `main` | `flex: 1` |
| `h1, h2, h3` | `color: var(--color-titulo)`; `font-weight: var(--peso-medio)`; `line-height: var(--interlineado-titulo)`; `margin: 0 0 var(--esp-4)` |
| `h1` | `font-size: var(--texto-titulo-lg)`; `letter-spacing: var(--tracking-titulo)` |
| `h2` | `font-size: var(--texto-titulo)`; `letter-spacing: var(--tracking-subtitulo)` |
| `h3` | `font-size: var(--texto-subtitulo)`; `letter-spacing: var(--tracking-subtitulo)` |
| `p` | `margin: 0 0 var(--esp-4)`; `max-width: var(--ancho-lectura)` |
| `a` | `color: var(--color-texto-enfasis)`; `text-underline-offset: 3px`; en `:hover` `color: var(--color-titulo)` |
| `img, svg, canvas` | `max-width: 100%`; `display: block` |
| `:focus-visible` | `outline: 2px solid var(--color-foco)`; `outline-offset: 2px`; `border-radius: var(--radio-pequeno)` |
| `.contenedor` | `width: 100%`; `max-width: var(--ancho-max)`; `margin-inline: auto`; `padding-inline: var(--margen-lateral)` |
| `.seccion` | `padding-block: var(--separacion-seccion)` |
| `.saltar-contenido` | fuera de pantalla (`position: absolute; left: var(--esp-4); top: calc(-1 * var(--esp-16))`) y visible al recibir foco (`:focus` → `top: var(--esp-4)`), con `background: var(--color-alga)`, `color: var(--color-titulo)`, `padding: var(--esp-3) var(--esp-4)`, `z-index: 10` |
| `.visualmente-oculto` | patrón estándar de texto solo para lectores de pantalla (`position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap`) |
| `:root` | sube `--margen-lateral` a `var(--esp-6)` en `@media (min-width: 768px)` y a `var(--esp-12)` en `@media (min-width: 1024px)` |
| `@media (prefers-reduced-motion: reduce)` | `*, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }` |

**`web/static/web/css/components.css`** — en este paso, estos componentes:

| Clase | Especificación |
|---|---|
| `.boton-primario` | `display: inline-flex; align-items: center; gap: var(--esp-2)`; `min-height: 44px`; `padding: var(--esp-3) var(--esp-6)`; `background: var(--gradiente-aurora)`; `color: var(--color-sobre-aurora)`; `border: 0`; `border-radius: var(--radio-pequeno)`; `font-size: var(--texto-pequeno)`; `font-weight: var(--peso-medio)`; `text-transform: uppercase`; `letter-spacing: var(--tracking-etiqueta)`; `text-decoration: none`; `cursor: pointer`; transición de `opacity` en `var(--duracion-rapida)`; en `:hover` `opacity: 0.9` |
| `.boton-secundario` | igual tamaño y tipografía que el primario, con `background: var(--color-alga)`, `color: var(--color-titulo)`, `border: 1px solid var(--color-borde)`; en `:hover` `border-color: var(--color-borde-control)` |
| `.boton-icono` | `width: 32px; height: 32px`; `display: inline-grid; place-items: center`; `background: var(--color-boton-icono)`; `color: var(--color-titulo)`; `border-radius: var(--radio-pequeno)`; contiene una flecha ↗ en SVG con `aria-hidden="true"` |
| `.etiqueta` | `font-size: var(--texto-etiqueta)`; `text-transform: uppercase`; `letter-spacing: var(--tracking-etiqueta)`; `color: var(--color-texto-enfasis)`; `font-weight: var(--peso-medio)`; `margin: 0 0 var(--esp-3)` |
| `.tarjeta` | `background: var(--color-alga)`; `border-radius: var(--radio-tarjeta)`; `padding: var(--relleno-tarjeta)`; sin borde ni sombra |
| `.tarjeta-hundida` | `background: var(--color-abismo)`; `border-radius: var(--radio-tarjeta)`; `padding: var(--esp-30) var(--relleno-tarjeta)` en escritorio y `var(--esp-16) var(--relleno-tarjeta)` en móvil |
| `.stat` | `font-size: var(--texto-display)`; `line-height: var(--interlineado-titulo)`; `letter-spacing: var(--tracking-titulo)`; `font-weight: var(--peso-medio)`; `color: var(--color-cifra)`; `font-variant-numeric: tabular-nums`; `margin: 0` |
| `.stat-etiqueta` | `font-size: var(--texto-pequeno)`; `text-transform: uppercase`; `letter-spacing: var(--tracking-etiqueta)`; `color: var(--color-texto-enfasis)`; `margin-top: var(--esp-2)` |
| `.insignia-demo` | `display: inline-flex; gap: var(--esp-2)`; `padding: var(--esp-1) var(--esp-3)`; `border: 1px solid var(--color-aviso)`; `color: var(--color-aviso)`; `border-radius: var(--radio-pequeno)`; `font-size: var(--texto-etiqueta)`; `text-transform: uppercase`; `letter-spacing: var(--tracking-etiqueta)` |
| `.cabecera` | `min-height: var(--alto-cabecera)`; `display: flex; align-items: center; justify-content: space-between; gap: var(--esp-6)`; `border-bottom: 1px solid var(--color-borde)` |
| `.nav-principal a` | `font-size: var(--texto-etiqueta)`; `text-transform: uppercase`; `letter-spacing: var(--tracking-etiqueta)`; `color: var(--color-texto)`; `text-decoration: none`; `padding: var(--esp-3) var(--esp-2)` (área táctil ≥ 44px); `[aria-current="page"]` y `:hover` → `color: var(--color-titulo)` |
| `.menu-movil` | visible por debajo de 1024px y oculto desde `@media (min-width: 1024px)`; `.nav-principal` y las acciones de la cabecera hacen lo contrario. El `<summary>` mide al menos 44×44px; el panel abierto ocupa el ancho completo con `background: var(--color-abismo)` y enlaces apilados con `padding: var(--esp-4)` |
| `.pie` | `background: var(--color-abismo)`; `padding-block: var(--esp-16)`; `margin-top: var(--separacion-seccion)`; texto en `var(--texto-pequeno)` |

**`tests/test_estilos.py`** (contenido literal completo):

```python
"""Paso 3: los tokens del sistema de diseño existen y el CSS respeta sus reglas."""

import re
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "web" / "static" / "web" / "css"

TOKENS = [
    "--color-abismo", "--color-fondo", "--color-alga", "--color-pizarra",
    "--color-titulo", "--color-texto", "--color-texto-enfasis", "--color-cita", "--color-cifra",
    "--color-teal", "--color-aqua", "--color-boton-icono",
    "--gradiente-aurora", "--gradiente-bioluminiscente", "--color-sobre-aurora",
    "--color-borde", "--color-borde-control",
    "--color-error", "--color-aviso", "--color-exito", "--color-foco",
    "--serie-uniforme", "--serie-reglas", "--serie-rl",
    "--perfil-0", "--perfil-1", "--perfil-2", "--perfil-3",
    "--fondo-grafica", "--rejilla-grafica",
    "--fuente", "--peso-regular", "--peso-medio",
    "--texto-etiqueta", "--texto-pequeno", "--texto-base", "--texto-destacado",
    "--texto-subtitulo", "--texto-titulo", "--texto-titulo-lg", "--texto-display",
    "--tracking-etiqueta", "--tracking-titulo", "--tracking-subtitulo",
    "--interlineado-titulo", "--interlineado-cuerpo",
    "--esp-1", "--esp-2", "--esp-3", "--esp-4", "--esp-5", "--esp-6", "--esp-8", "--esp-9",
    "--esp-10", "--esp-12", "--esp-16", "--esp-20", "--esp-30",
    "--ancho-max", "--ancho-lectura", "--margen-lateral", "--relleno-tarjeta",
    "--separacion-seccion", "--alto-cabecera",
    "--radio-pequeno", "--radio-tarjeta",
    "--duracion-rapida", "--duracion-media", "--curva-salida",
]  # fmt: skip

COMPONENTES_BASE = [
    ".boton-primario", ".boton-secundario", ".boton-icono", ".etiqueta",
    ".tarjeta", ".tarjeta-hundida", ".stat", ".insignia-demo",
]  # fmt: skip


def _hojas() -> list[Path]:
    return sorted(CSS.rglob("*.css"))


def _sin_comentarios(texto: str) -> str:
    return re.sub(r"/\*.*?\*/", "", texto, flags=re.S)


def test_tokens_define_todas_las_variables():
    tokens = (CSS / "tokens.css").read_text(encoding="utf-8")
    faltantes = [t for t in TOKENS if f"{t}:" not in tokens]
    assert faltantes == []


def test_fuente_es_inter():
    assert '"Inter"' in (CSS / "tokens.css").read_text(encoding="utf-8")


def test_colores_literales_solo_en_tokens():
    for hoja in _hojas():
        if hoja.name == "tokens.css":
            continue
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b", texto), f"color hex en {hoja.name}"
        assert not re.search(r"\b(rgb|rgba|hsl|hsla)\(", texto), f"color literal en {hoja.name}"


def test_sin_sombras():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        assert not re.search(r"box-shadow\s*:\s*(?!none)", texto), f"sombra en {hoja.name}"


def test_radios_maximo_16px():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        for valor in re.findall(r"border-radius\s*:\s*([^;}]+)", texto):
            assert "%" not in valor, f"radio en % en {hoja.name}"
            for numero in re.findall(r"(\d+(?:\.\d+)?)px", valor):
                assert float(numero) <= 16, f"radio {numero}px en {hoja.name}"


def test_solo_pesos_400_y_500():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        for peso in re.findall(r"font-weight\s*:\s*(\d+)", texto):
            assert peso in ("400", "500"), f"peso {peso} en {hoja.name}"


def test_base_tiene_foco_visible_y_movimiento_reducido():
    base = (CSS / "base.css").read_text(encoding="utf-8")
    assert ":focus-visible" in base
    assert "prefers-reduced-motion: reduce" in base
    assert ".saltar-contenido" in base


def test_componentes_base_existen():
    componentes = (CSS / "components.css").read_text(encoding="utf-8")
    faltantes = [c for c in COMPONENTES_BASE if c not in componentes]
    assert faltantes == []
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se ejecuta tests/test_estilos.py THE SYSTEM SHALL encontrar declarada en web/static/web/css/tokens.css cada variable de la constante TOKENS, con la familia tipográfica "Inter".
2. WHEN se revisa cualquier archivo CSS distinto de tokens.css THE SYSTEM SHALL no contener colores literales hex, rgb(), rgba(), hsl() ni hsla() (los colores solo entran por var(--…)).
3. WHEN se revisa cualquier archivo CSS THE SYSTEM SHALL no contener box-shadow distinto de `none`, ni border-radius mayor de 16px o en %, ni font-weight distinto de 400 o 500.
4. WHEN se revisa base.css THE SYSTEM SHALL definir `:focus-visible`, un bloque `prefers-reduced-motion: reduce` y el enlace `.saltar-contenido`.
5. WHEN se revisa components.css THE SYSTEM SHALL definir .boton-primario, .boton-secundario, .boton-icono, .etiqueta, .tarjeta, .tarjeta-hundida, .stat e .insignia-demo.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_estilos.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T3: Tokens del sistema de diseño y CSS base"
git tag step-03-tokens-css
```

Si la siguiente tarea sale mal: `git reset --hard step-03-tokens-css` y repetirla.

### `E1-T4` — Tabla de rutas completa y plantilla base

**Depends on:** `E1-T3` · **Priority:** p0

Todas las URLs del sitio existen desde ya; las que aún no tienen contenido muestran una página
"Próximamente" con la misma plantilla base. Así la navegación nunca apunta a una ruta inexistente,
y la Persona A (`views.py`) y la Persona B (`views_app.py`) trabajan en archivos distintos en la
etapa 1. `app.py`, `views.py` y `views_app.py` son literales; `base.html` lo escribes tú con la
especificación de abajo.

**Files**
- `app.py` — reemplazo completo
- `web/views.py` — reemplazo completo
- `web/views_app.py` — nuevo
- `web/templates/web/base.html` — nuevo
- `tests/test_rutas.py` — nuevo (literal)

**`app.py`** (contenido literal completo):

```python
"""Rutas de la página Cauce: la ÚNICA tabla de URLs del proyecto (ROOT_URLCONF = "app").

Todas las rutas existen desde el paso 4 (con una página "Próximamente" donde aún no hay
contenido), así la navegación nunca apunta a una URL inexistente.

Atajo: `python app.py` arranca el servidor de desarrollo (equivale a `manage.py runserver`);
`python app.py <comando>` ejecuta cualquier comando de manage.py, p. ej. `python app.py check`.
"""

from django.urls import path

from web import views, views_app

urlpatterns = [
    # Públicas: web/views.py (Persona A)
    path("", views.inicio, name="inicio"),
    path("metodologia/", views.metodologia, name="metodologia"),
    path("resultados/", views.resultados, name="resultados"),
    path("styleguide/", views.styleguide, name="styleguide"),
    path("health/", views.health, name="health"),
    # Acceso y aplicación: web/views_app.py (Persona B)
    path("login/", views_app.login, name="login"),
    path("registro/", views_app.registro, name="registro"),
    path("salir/", views_app.salir, name="salir"),
    path("app/simulador/", views_app.simulador, name="simulador"),
    path("app/api/simular/", views_app.api_simular, name="api_simular"),
    path("app/simulaciones/", views_app.simulaciones, name="simulaciones"),
    path(
        "app/simulaciones/<slug:sim_id>/",
        views_app.simulacion_detalle,
        name="simulacion_detalle",
    ),
]


if __name__ == "__main__":
    import os
    import sys

    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line([sys.argv[0], *(sys.argv[1:] or ["runserver"])])
```

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    """Página provisional: base.html muestra "Próximamente" en su bloque de contenido."""
    return render(request, "web/base.html", {"titulo": titulo})


def inicio(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Inicio")


def metodologia(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Metodología")


def resultados(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Resultados")


def styleguide(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        raise Http404("La guía de estilo solo existe en desarrollo")
    return _proximamente(request, "Guía de estilo")


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**`web/views_app.py`** (contenido literal completo):

```python
"""Vistas de acceso (login simulado) y de la aplicación (simulador, simulaciones)."""

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    return render(request, "web/base.html", {"titulo": titulo})


def login(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Iniciar sesión")


def registro(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Crear cuenta")


@require_POST
def salir(request: HttpRequest) -> HttpResponse:
    return redirect("inicio")


def simulador(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Simulador")


@require_POST
def api_simular(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {"error": {"codigo": "no_implementado", "mensaje": "El simulador llega en el paso 11"}},
        status=501,
    )


def simulaciones(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Mis simulaciones")


def simulacion_detalle(request: HttpRequest, sim_id: str) -> HttpResponse:
    return _proximamente(request, "Simulación")
```

**`web/templates/web/base.html`** — escríbelo así, en este orden:

1. `{% load static %}<!doctype html>` y `<html lang="es">`.
2. `<head>`: `<meta charset="utf-8">`; `<meta name="viewport" content="width=device-width, initial-scale=1">`;
   `<title>{% block titulo %}{{ titulo }}{% endblock %} · Cauce</title>`;
   `<meta name="description" content="{{ sitio.subtitulo }}: aprendizaje por refuerzo con datos de la UNGRD.">`;
   `<link rel="preconnect" href="https://fonts.googleapis.com">`;
   `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`;
   `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap">`;
   los tres CSS con `{% static %}` en este orden: `web/css/tokens.css`, `web/css/base.css`,
   `web/css/components.css`; luego `{% block estilos %}{% endblock %}`.
3. `<body>`: primero `<a class="saltar-contenido" href="#contenido">Saltar al contenido</a>`.
4. `<header class="cabecera contenedor">` con:
   - el logotipo de texto: `<a class="logo" href="{% url 'inicio' %}">Cauce</a>`;
   - `{% with actual=request.resolver_match.url_name %}` y dentro
     `<nav aria-label="Principal" class="nav-principal">` con cuatro enlaces en este orden: Inicio
     (`inicio`), Metodología (`metodologia`), Resultados (`resultados`), Simulador (`simulador`).
     Cada enlace se escribe exactamente como `<a href="{% url 'NOMBRE' %}"{% if actual == 'NOMBRE' %} aria-current="page"{% endif %}>Texto</a>`;
   - las acciones: `{% if usuario %}` el nombre (`{{ usuario.nombre }}`) y
     `<form method="post" action="{% url 'salir' %}">{% csrf_token %}<button type="submit" class="boton-secundario">Salir</button></form>`,
     `{% else %}` `<a href="{% url 'login' %}">Iniciar sesión</a>` y
     `<a class="boton-primario" href="{% url 'simulador' %}">Probar el simulador</a>` `{% endif %}`;
   - el menú móvil: `<details class="menu-movil"><summary>Menú</summary><nav aria-label="Principal (móvil)">…los mismos cuatro enlaces…</nav></details>`;
   - `{% endwith %}`.
5. `{% if sitio.datos_demo %}<div class="contenedor"><p class="insignia-demo" role="note">Datos de ejemplo — los resultados reales llegan en la etapa 3</p></div>{% endif %}`.
6. `<main id="contenido" tabindex="-1">{% block contenido %}` con el contenido provisional por
   defecto: `<section class="seccion contenedor"><p class="etiqueta">Próximamente</p><h1>{{ titulo }}</h1><p>Esta sección se construye en la etapa 1 del proyecto.</p></section>`
   y `{% endblock %}</main>`.
7. `<footer class="pie"><div class="contenedor">` con: `<p>{{ sitio.nombre }} · {{ sitio.subtitulo }}</p>`,
   `<p>Proyecto académico. Datos: Emergencias UNGRD V2 — Datos Abiertos Colombia. Los resultados son de una simulación, no recomendaciones operativas.</p>`
   y `</div></footer>`.
8. `{% block scripts %}{% endblock %}` justo antes de `</body>`.

Reglas: un único `<h1>` por página (el de cada plantilla hija o el provisional); ningún atributo
`style=` ni `on*=`; ningún `<script>` en línea.

**`tests/test_rutas.py`** (contenido literal completo):

```python
"""Paso 4: todas las rutas existen y comparten la plantilla base accesible."""

import pytest
from django.urls import reverse

PUBLICAS = ["inicio", "metodologia", "resultados", "login", "registro"]
DE_LA_APP = ["simulador", "simulaciones"]
NAVEGACION = ["inicio", "metodologia", "resultados", "simulador"]


@pytest.mark.parametrize("nombre", PUBLICAS)
def test_pagina_publica_usa_la_plantilla_base(client, nombre):
    respuesta = client.get(reverse(nombre))
    assert respuesta.status_code == 200
    html = respuesta.content.decode()
    assert '<html lang="es">' in html
    assert 'name="viewport"' in html
    assert "<title>" in html and "Cauce</title>" in html
    assert 'class="saltar-contenido" href="#contenido"' in html
    assert '<main id="contenido"' in html
    assert '<nav aria-label="Principal"' in html
    assert "<footer" in html
    assert html.count("<h1") == 1
    for destino in NAVEGACION:
        assert f'href="{reverse(destino)}"' in html


def test_enlace_actual_marcado_con_aria_current(client):
    html = client.get(reverse("metodologia")).content.decode()
    assert f'href="{reverse("metodologia")}" aria-current="page"' in html


def test_menu_movil_presente(client):
    html = client.get(reverse("inicio")).content.decode()
    assert 'class="menu-movil"' in html
    assert "<summary" in html


@pytest.mark.parametrize("nombre", DE_LA_APP)
def test_paginas_de_la_app_existen(client, nombre):
    respuesta = client.get(reverse(nombre))
    assert respuesta.status_code in (200, 302)
    if respuesta.status_code == 302:
        assert respuesta["Location"].startswith(reverse("login"))


def test_detalle_de_simulacion_existe(client):
    respuesta = client.get(reverse("simulacion_detalle", args=["sim-001"]))
    assert respuesta.status_code in (200, 302)


def test_salir_solo_acepta_post(client):
    assert client.get(reverse("salir")).status_code == 405
    respuesta = client.post(reverse("salir"))
    assert respuesta.status_code == 302
    assert respuesta["Location"] == reverse("inicio")


def test_api_simular_solo_acepta_post(client):
    assert client.get(reverse("api_simular")).status_code == 405


def test_aviso_de_datos_de_ejemplo_se_controla_por_configuracion(client, settings):
    settings.CAUCE_DATOS_DEMO = True
    assert "Datos de ejemplo" in client.get(reverse("inicio")).content.decode()
    settings.CAUCE_DATOS_DEMO = False
    assert "Datos de ejemplo" not in client.get(reverse("inicio")).content.decode()


def test_styleguide_no_existe_en_produccion(client, settings):
    settings.DEBUG = False
    assert client.get(reverse("styleguide")).status_code == 404
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN llega un GET a /, /metodologia/, /resultados/, /login/ o /registro/ THE SYSTEM SHALL responder 200 con `<html lang="es">`, meta viewport, un título que termina en "Cauce", enlace de salto a #contenido, `<main id="contenido"`, `<nav aria-label="Principal"`, pie de página y exactamente un <h1>.
2. WHEN se muestra cualquier página pública THE SYSTEM SHALL enlazar las rutas inicio, metodologia, resultados y simulador, y marcar la actual con aria-current="page".
3. WHEN llega un GET a /app/simulador/, /app/simulaciones/ o /app/simulaciones/sim-001/ THE SYSTEM SHALL responder 200 o un 302 cuyo Location empieza por /login/.
4. WHEN /salir/ o /app/api/simular/ reciben un GET THE SYSTEM SHALL responder 405, y WHEN /salir/ recibe un POST THE SYSTEM SHALL redirigir con 302 a /.
5. WHEN CAUCE_DATOS_DEMO es True THE SYSTEM SHALL mostrar el texto "Datos de ejemplo" en todas las páginas, y WHEN es False SHALL no mostrarlo.
6. WHEN DEBUG es False y se pide /styleguide/ THE SYSTEM SHALL responder 404.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_rutas.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T4: Tabla de rutas completa y plantilla base"
git tag step-04-rutas-base
```

Si la siguiente tarea sale mal: `git reset --hard step-04-rutas-base` y repetirla.

### `E1-T5` — Portada con cifras del contrato de datos

**Depends on:** `E1-T2`, `E1-T4` · **Priority:** p0

La portada cuenta el proyecto en una pantalla: el problema, cuatro cifras grandes en lavanda
(leídas de `resultados.json`), los tres componentes (datos → K-means → agente) y la invitación al
simulador. La animación es un grafo de red propio (municipios ↔ recursos) en `<canvas>`,
decorativo, que no se mueve si el usuario pidió reducir movimiento. `views.py` es literal; la
plantilla, el CSS y el JS los escribes tú.

**Files**
- `web/views.py` — reemplazo completo
- `web/templates/web/inicio.html` — nuevo
- `web/static/web/css/pages/inicio.css` — nuevo
- `web/static/web/js/red.js` — nuevo
- `tests/test_inicio.py` — nuevo (literal)

**`web/views.py`** (contenido literal completo):

```python
"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from web import datos


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
    return _proximamente(request, "Guía de estilo")


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
```

**`web/templates/web/inicio.html`** — `{% extends "web/base.html" %}{% load static %}`, con
`{% block estilos %}` cargando `web/css/pages/inicio.css` y `{% block scripts %}` cargando
`<script src="{% static 'web/js/red.js' %}" defer></script>`. Bloque `contenido`, en orden:

1. **Hero** — `<section class="hero">`, altura mínima `min(100vh, 820px)`, texto centrado en una
   columna de máx. 720px, con `<canvas id="red-hero" aria-hidden="true"></canvas>` de fondo
   (posición absoluta, detrás del texto). Contenido:
   - `<p class="etiqueta">UNGRD · Aprendizaje por refuerzo</p>`
   - `<h1>¿Quién recibe ayuda primero?</h1>` (usa `--texto-display`)
   - `<p>Cauce simula emergencias simultáneas en municipios de Colombia y compara cómo reparten recursos limitados tres estrategias: una regla uniforme, una basada en prioridades y un agente de aprendizaje por refuerzo.</p>`
   - `<a class="boton-primario" href="{% url 'simulador' %}">Probar el simulador</a>` y
     `<a class="boton-secundario" href="{% url 'metodologia' %}">Ver metodología</a>`.
2. **Cifras** — `<section class="seccion contenedor" aria-labelledby="titulo-cifras">` con
   `<h2 id="titulo-cifras" class="visualmente-oculto">El proyecto en cifras</h2>` y una rejilla
   (1 columna en móvil, 2 en ≥768px, 4 en ≥1024px). Por cada `cifra` de `resumen`:
   `<div><p class="stat">{{ cifra.valor }}</p><p class="stat-etiqueta">{{ cifra.etiqueta }}</p></div>`.
   Exactamente 4 elementos `class="stat"` en la página (la prueba los cuenta).
3. **Cómo funciona** — `<section class="seccion contenedor">` con `<p class="etiqueta">Cómo funciona</p>`,
   `<h2>De los registros históricos a una política de asignación</h2>` y tres
   `<article class="tarjeta" data-paso="…">` (rejilla de 1 → 3 columnas):
   - `data-paso="datos"`: `<h3>Datos de la UNGRD</h3>` · `<p>Emergencias UNGRD V2: tipo de evento, fecha, ubicación, personas afectadas y daños reportados.</p>`
   - `data-paso="kmeans"`: `<h3>Perfiles con K-means</h3>` · `<p>Agrupamos las emergencias en perfiles de impacto para describir mejor cada escenario.</p>`
   - `data-paso="agente"`: `<h3>Agente de RL</h3>` · `<p>Un agente aprende a repartir recursos limitados y se compara con dos estrategias de referencia.</p>`
   Cada tarjeta termina con un `.boton-icono` que enlaza a `{% url 'metodologia' %}` y tiene `aria-label="Ver metodología: <título>"`.
4. **Cierre** — `<section class="contenedor"><div class="tarjeta-hundida">` centrado con
   `<h2>Prueba distintos presupuestos y mira qué cambia</h2>`,
   `<p>El simulador muestra, para cada municipio, cuántos recursos asigna cada estrategia.</p>` y
   `<a class="boton-primario" href="{% url 'simulador' %}">Abrir el simulador</a>`.

**`web/static/web/css/pages/inicio.css`** — solo `var(--…)`: `.hero` (posición relativa,
`overflow: hidden`, `display: grid; place-items: center`, `text-align: center`); `#red-hero`
(`position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.55; pointer-events: none`);
el contenido del hero con `position: relative`; `.hero h1` con `font-size: var(--texto-display)`;
las rejillas de cifras y tarjetas con `gap: var(--esp-5)`; `.tarjeta-hundida` centrada.

**`web/static/web/js/red.js`** — sin dependencias. Al cargar: toma `#red-hero`; si no existe,
termina. Dibuja ~60 nodos (radio 1.5–3px) unidos por líneas finas cuando están a menos de 140px.
Colores leídos de los tokens con
`getComputedStyle(document.documentElement).getPropertyValue('--color-aqua')` (nodos),
`--color-cifra` (1 de cada 8 nodos, los "recursos") y `--rejilla-grafica` (líneas). Ajusta el
tamaño al contenedor y a `devicePixelRatio`, y se redibuja en `resize`. Si
`window.matchMedia('(prefers-reduced-motion: reduce)').matches` es verdadero, dibuja **un solo
cuadro estático**; si no, anima con `requestAnimationFrame` a deriva lenta (≤ 0.3px por cuadro) y
se pausa cuando `document.hidden` es verdadero.

**`tests/test_inicio.py`** (contenido literal completo):

```python
"""Paso 5: la portada cuenta el proyecto y lee sus cifras del contrato de datos."""

from pathlib import Path

from django.urls import reverse

from web import datos

JS = Path(__file__).resolve().parent.parent / "web" / "static" / "web" / "js"


def _html(client) -> str:
    respuesta = client.get(reverse("inicio"))
    assert respuesta.status_code == 200
    return respuesta.content.decode()


def test_portada_tiene_el_titular_y_las_llamadas_a_la_accion(client):
    html = _html(client)
    assert "¿Quién recibe ayuda primero?" in html
    assert 'class="boton-primario"' in html
    assert f'href="{reverse("simulador")}"' in html
    assert f'href="{reverse("metodologia")}"' in html


def test_portada_muestra_las_cuatro_cifras_del_resumen(client):
    html = _html(client)
    assert html.count('class="stat"') == 4
    for cifra in datos.resultados()["resumen"]:
        assert cifra["valor"] in html
        assert cifra["etiqueta"] in html


def test_portada_explica_los_tres_componentes(client):
    html = _html(client)
    for paso in ("datos", "kmeans", "agente"):
        assert f'data-paso="{paso}"' in html


def test_animacion_de_la_portada_es_decorativa_y_respeta_movimiento_reducido(client):
    html = _html(client)
    assert '<canvas id="red-hero" aria-hidden="true"' in html
    assert "web/js/red.js" in html and "defer" in html
    assert "web/css/pages/inicio.css" in html
    assert "prefers-reduced-motion" in (JS / "red.js").read_text(encoding="utf-8")
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN llega un GET a / THE SYSTEM SHALL responder 200 con el titular "¿Quién recibe ayuda primero?", un elemento class="boton-primario" y enlaces a /app/simulador/ y /metodologia/.
2. WHEN llega un GET a / THE SYSTEM SHALL mostrar exactamente 4 elementos class="stat", cada uno con el `valor` y la `etiqueta` de una entrada de `resumen` en resultados.json.
3. WHEN llega un GET a / THE SYSTEM SHALL mostrar un elemento por cada uno de data-paso="datos", data-paso="kmeans" y data-paso="agente".
4. WHEN llega un GET a / THE SYSTEM SHALL incluir `<canvas id="red-hero" aria-hidden="true"`, cargar web/js/red.js con defer y web/css/pages/inicio.css, y red.js SHALL contener una comprobación de prefers-reduced-motion.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_inicio.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T5: Portada con cifras del contrato de datos"
git tag step-05-portada
```

Si la siguiente tarea sale mal: `git reset --hard step-05-portada` y repetirla.

### `E1-T6` — Listo para Render: errores propios y README

**Depends on:** `E1-T5` · **Priority:** p0

Cierra la etapa 0: la configuración de producción pasa el chequeo de despliegue de Django, falla
de forma clara sin clave secreta, recolecta el CSS con el manifiesto de WhiteNoise, las páginas de
error son propias y el README trae exactamente lo que el equipo escribe en Render. Al terminar,
el equipo puede hacer `git push` y crear el servicio. `README.md` es literal.

**Files**
- `README.md` — nuevo (literal)
- `web/templates/404.html` — nuevo
- `web/templates/500.html` — nuevo
- `tests/test_produccion.py` — nuevo (literal)

**`README.md`** (contenido literal completo):

````markdown
# Cauce — Asignación inteligente de recursos ante emergencias

Sitio web del proyecto de aprendizaje por refuerzo que estudia **quién recibe ayuda primero y en
qué cantidad** cuando varios municipios de Colombia enfrentan emergencias a la vez. Usa los
registros históricos de la UNGRD (Emergencias UNGRD V2, Datos Abiertos Colombia) para construir
una simulación y comparar tres políticas: uniforme, basada en reglas y un agente de RL.

> **Etapa actual: interfaz.** Los resultados, perfiles y simulaciones que muestra el sitio son
> **datos de ejemplo** (`web/data/mock/`). El login es simulado: cualquier correo válido entra.

## Correr en local

Requisitos: Python 3.12 o superior (el proyecto fija 3.14 en `.python-version`) y Git.

```bash
python -m venv .venv
sh scripts/py -m pip install -r requirements-dev.txt
sh scripts/py app.py
```

Abre http://127.0.0.1:8000/. `python app.py` equivale a `python manage.py runserver`, y `python app.py check` (o cualquier otro comando) funciona igual que con `manage.py`. En PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1` y
usa `python` en lugar de `sh scripts/py`.

Para los notebooks de análisis y modelado (EDA, K-means, entorno, Q-learning) instala además
`sh scripts/py -m pip install -r requirements-ml.txt`. Render no instala ese archivo.

| Tarea | Comando |
|---|---|
| Pruebas | `sh scripts/py -m pytest` |
| Lint | `sh scripts/py -m ruff check .` |
| Formato | `sh scripts/py -m ruff format .` |

## Publicar en Render

Crea un **Web Service** conectado a este repositorio, con el plan **Free**, y usa estos valores:

| Campo | Valor |
|---|---|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| Health Check Path | `/health/` |

Variables de entorno del servicio:

| Variable | Valor |
|---|---|
| `DJANGO_SECRET_KEY` | Una cadena larga y aleatoria (Render puede generarla con "Generate"). Obligatoria |
| `CAUCE_DATOS_DEMO` | `1` mientras el sitio muestre datos de ejemplo; `0` cuando sean reales |
| `PYTHON_VERSION` | Opcional. Si no se define, Render usa la versión de `.python-version` |

Render define por su cuenta `RENDER=true` y `RENDER_EXTERNAL_HOSTNAME`; la configuración los usa
para apagar `DEBUG`, exigir la clave secreta y aceptar el dominio `*.onrender.com`.

**Antes de una presentación:** el plan gratis apaga el servicio tras 15 minutos sin visitas y tarda
cerca de un minuto en despertar. Abre la URL un par de minutos antes.

## Subir este repositorio a GitHub

```bash
git remote add origin <URL-de-tu-repositorio>
git push -u origin main --tags
```

Si el repositorio de GitHub ya tenía commits (por ejemplo un README creado desde la web), primero
integra su historia: `git pull origin main --allow-unrelated-histories`, resuelve conflictos y
vuelve a hacer `git push`.

## Cómo está organizado

- `app.py`: la tabla única de rutas de la página (y atajo para arrancar el servidor).
- `config/`: configuración de Django (`settings.py`, `wsgi.py`).
- `web/`: la aplicación. Vistas públicas (`views.py`), vistas de la app (`views_app.py`), login
  simulado (`auth_demo.py`), contrato de datos (`datos.py`) y motor de ejemplo
  (`simulacion_demo.py`).
- `web/templates/` y `web/static/`: plantillas, CSS (tokens del sistema de diseño) y JavaScript.
- `docs/`: contexto del proyecto y sistema de diseño de referencia.
- `blueprints/cauce/`: el plan de construcción paso a paso.
````

**`web/templates/404.html`** — `{% extends "web/base.html" %}` con `{% block titulo %}Página no encontrada{% endblock %}` y en `contenido`:
`<section class="seccion contenedor"><p class="etiqueta">Error 404</p><h1>Página no encontrada</h1><p>La dirección no existe o cambió de lugar.</p><a class="boton-primario" href="{% url 'inicio' %}">Volver al inicio</a></section>`.

**`web/templates/500.html`** — **no** extiende `base.html` (Django lo renderiza sin contexto ni
procesadores). Documento propio: `{% load static %}<!doctype html><html lang="es">`, `<head>` con
charset, el mismo viewport, `<title>Error · Cauce</title>` y los CSS `web/css/tokens.css` y
`web/css/base.css` vía `{% static %}`; `<body>` con
`<main id="contenido" class="seccion contenedor"><p class="etiqueta">Error 500</p><h1>Algo salió mal</h1><p>Estamos trabajando para solucionarlo. Intenta de nuevo en unos minutos.</p><a href="/">Volver al inicio</a></main>`.

**`tests/test_produccion.py`** (contenido literal completo):

```python
"""Paso 6: el proyecto queda listo para que el equipo lo publique en Render."""

import os
import subprocess
import sys
from pathlib import Path

from django.template.loader import render_to_string

RAIZ = Path(__file__).resolve().parent.parent
CLAVE_DE_PRUEBA = "prueba-" + "x" * 60


def _manage(*argumentos: str, entorno_extra: dict[str, str]) -> subprocess.CompletedProcess:
    entorno = {k: v for k, v in os.environ.items() if k not in ("RENDER", "DJANGO_SECRET_KEY")}
    entorno.update(entorno_extra)
    return subprocess.run(
        [sys.executable, "manage.py", *argumentos],
        cwd=RAIZ,
        env=entorno,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_configuracion_de_produccion_pasa_el_chequeo_de_despliegue():
    resultado = _manage(
        "check",
        "--deploy",
        entorno_extra={
            "RENDER": "true",
            "DJANGO_SECRET_KEY": CLAVE_DE_PRUEBA,
            "RENDER_EXTERNAL_HOSTNAME": "cauce.onrender.com",
        },
    )
    assert resultado.returncode == 0, resultado.stderr


def test_produccion_sin_clave_secreta_no_arranca():
    resultado = _manage("check", entorno_extra={"RENDER": "true"})
    assert resultado.returncode == 1
    assert "DJANGO_SECRET_KEY" in resultado.stderr


def test_collectstatic_de_produccion_genera_el_manifiesto():
    resultado = _manage(
        "collectstatic",
        "--noinput",
        entorno_extra={"RENDER": "true", "DJANGO_SECRET_KEY": CLAVE_DE_PRUEBA},
    )
    assert resultado.returncode == 0, resultado.stderr
    assert (RAIZ / "staticfiles" / "staticfiles.json").is_file()


def test_pagina_404_propia(client):
    respuesta = client.get("/pagina-que-no-existe/")
    assert respuesta.status_code == 404
    html = respuesta.content.decode()
    assert "Página no encontrada" in html
    assert 'href="/"' in html


def test_pagina_500_propia_no_depende_del_contexto():
    html = render_to_string("500.html")
    assert "Algo salió mal" in html
    assert '<html lang="es">' in html


def test_readme_documenta_el_despliegue_en_render():
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for texto in (
        "pip install -r requirements.txt && python manage.py collectstatic --noinput",
        "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
        "DJANGO_SECRET_KEY",
        "PYTHON_VERSION",
        "/health/",
    ):
        assert texto in readme, f"falta en README.md: {texto}"
```

**Acceptance**

Copiados textualmente del arreglo `acceptance` de esta tarea en `tasks.json`. Cada uno lo decide un comando de abajo, en esta máquina, durante la construcción.

1. WHEN se ejecuta `manage.py check --deploy` con RENDER=true, un DJANGO_SECRET_KEY de 60 caracteres y RENDER_EXTERNAL_HOSTNAME=cauce.onrender.com THE SYSTEM SHALL terminar con código 0.
2. WHEN se ejecuta cualquier comando de manage.py con RENDER=true y sin DJANGO_SECRET_KEY THE SYSTEM SHALL terminar con código 1 y "DJANGO_SECRET_KEY" en stderr.
3. WHEN se ejecuta `manage.py collectstatic --noinput` con RENDER=true y una clave secreta THE SYSTEM SHALL terminar con código 0 y escribir staticfiles/staticfiles.json.
4. WHEN se pide una ruta inexistente THE SYSTEM SHALL responder 404 con el texto "Página no encontrada" y un enlace a /, y la plantilla 500.html SHALL renderizarse sin contexto de petición con "Algo salió mal" y `<html lang="es">`.
5. WHEN se lee README.md THE SYSTEM SHALL contener el comando de build `pip install -r requirements.txt && python manage.py collectstatic --noinput`, el de inicio `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`, DJANGO_SECRET_KEY, PYTHON_VERSION y /health/.

**Verify** — cada comando, en orden, desde la raíz del proyecto. Cada uno termina con código 0 cuando la tarea está bien; la tarea está hecha cuando el último termina con 0. Esperado en todos: código 0, `0 failed` en pytest, `All checks passed!` en ruff.

```bash
sh scripts/py -m pytest tests/test_produccion.py
sh scripts/py -m ruff check .
sh scripts/py -m ruff format --check .
sh scripts/py -m pytest
```

**Checkpoint** — solo después de que el último comando de Verify termine con 0:

```bash
git add -A && git commit -m "E1-T6: Listo para Render: errores propios y README"
git tag step-06-produccion
```

Si la siguiente tarea sale mal: `git reset --hard step-06-produccion` y repetirla.

---

## Epic acceptance

El epic está hecho cuando las seis tareas están `done` **y**:

1. **WHEN** se ejecuta la suite completa desde la raíz, con el bundle en `blueprints/` **THE SYSTEM SHALL** terminar con código 0, 0 fallas y 0 advertencias, y ruff limpio.
2. **WHEN** se arranca `python app.py` y se pide `/` y `/health/` **THE SYSTEM SHALL** responder 200 en ambas (cubierto por `test_servidor_real_sirve_health` y `test_portada_tiene_el_titular_y_las_llamadas_a_la_accion`).

```bash
sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check . && sh scripts/py -m pytest
sh scripts/py manage.py check
```

## Pitfalls

- **Volver a crear `config/urls.py`** por costumbre — las rutas están en `app.py` y `ROOT_URLCONF` apunta ahí.
- **Correr comandos desde `blueprints/cauce/`** — todo se ejecuta desde la raíz del proyecto; desde el bundle no existe `manage.py`.
- **`collectstatic` de producción con un CSS que referencia un archivo inexistente** (`url(...)`): el manifiesto de WhiteNoise falla. No uses `url()` hacia archivos que no existen.
- **Un `<h1>` de más en `base.html`** — el título de cada página lo pone la plantilla hija; el de `base.html` está solo dentro del bloque por defecto.

## Before moving on

- [ ] Las seis tareas están `done` en `tasks.json`; ninguna quedó `in_progress`.
- [ ] Pasaron todos los comandos `verify` de cada tarea, no solo el primero.
- [ ] Ningún comando `verify` se editó ni se saltó.
- [ ] Cada tarea tiene su etiqueta: `git tag -l 'step-*'` lista `step-01-django-health` a `step-06-produccion`.
- [ ] El gate pasa limpio desde la raíz.
- [ ] Existen los contratos "Produced" con las firmas indicadas.
- [ ] Ningún archivo fuera del árbol del epic se modificó.
- [ ] `.env.example` sigue listando `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` y `CAUCE_DATOS_DEMO` (este epic no agrega variables).
- [ ] Un commit por tarea, con el prefijo de su id y seguido de su etiqueta.
- [ ] Para publicar hoy: `git remote add origin <URL>` y `git push -u origin main --tags`, y crear el Web Service en Render con los valores del README.
