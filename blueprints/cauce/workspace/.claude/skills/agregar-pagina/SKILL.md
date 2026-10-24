---
name: agregar-pagina
description: Agregar una página nueva al sitio Cauce (ruta, vista, plantilla, CSS y prueba). Úsala cuando pidan "agrega una página", "nueva sección", "otra vista" o "nueva ruta" en este proyecto Django.
---

# Agregar una página

## Cuándo usarla
Cuando el sitio necesita una URL nueva visible (pública o bajo `/app/`).

## Pasos
1. En `app.py` agrega `path("<ruta>/", views.<nombre>, name="<nombre>")` (pública) o en `views_app` si va bajo `/app/`.
2. Escribe la vista: lee datos solo con `web.datos`; si va bajo `/app/`, decórala con `@login_requerido`.
3. Crea `web/templates/web/<nombre>.html` que extienda `web/base.html`, con un único `<h1>` y `{% block estilos %}` si necesita CSS propio.
4. Si necesita estilos, crea `web/static/web/css/pages/<nombre>.css` usando solo `var(--…)`.
5. Si va en la navegación, agrega el enlace en `base.html` (ambos menús, escritorio y `.menu-movil`) con `aria-current` cuando sea la actual.
6. Crea `tests/test_<nombre>.py`: 200 en GET, un `<h1>`, y 302 a `/login/` sin sesión si va bajo `/app/`.

## Verify
```bash
sh scripts/py -m pytest tests/test_<nombre>.py tests/test_accesibilidad.py tests/test_estilos.py   # expect: exit 0, 0 failed
sh scripts/py -m ruff check . && sh scripts/py -m ruff format --check .                           # expect: exit 0
```

## No hagas
- Rutas escritas a mano en las plantillas (`href="/algo/"`): usa `{% url %}`.
- Colores o tamaños literales en el CSS de la página.
