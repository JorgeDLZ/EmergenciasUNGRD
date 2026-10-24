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
