---
description: Convenciones de Python y Django en Cauce
paths:
  - "config/**"
  - "web/**/*.py"
  - "manage.py"
  - "app.py"
---

# Python y Django

- Rutas: solo en `app.py` (raíz; `ROOT_URLCONF = "app"`). No existe `config/urls.py` ni `urls.py` por aplicación. No se renombran los nombres de ruta existentes: las plantillas y las pruebas dependen de ellos.
- Vistas públicas en `web/views.py`; acceso y app en `web/views_app.py`. Máx. 30 líneas por vista.
- Datos: solo `web.datos.resultados()`, `perfiles()`, `simulaciones()`, `simulacion(id)`. Nunca `open()` sobre los JSON desde una vista.
- Usuario: solo `web.auth_demo.get_current_user(request)`. Toda vista bajo `/app/` lleva `@login_requerido`; en vistas solo-POST, `@require_POST` va **encima** de `@login_requerido`.
- Configuración: toda variable de entorno se lee en `config/settings.py`; ningún otro módulo usa `os.environ`.
- `web/datos.py` y `web/simulacion_demo.py` no importan Django: así los notebooks pueden reutilizarlos.
- Errores de API: `{"error": {"codigo": "<snake_case>", "mensaje": "<texto para personas>"}}` con 400, 401 o 405.
- Tipado en funciones públicas. Líneas ≤ 100. `ruff check` y `ruff format --check` limpios.
- No agregar `django.contrib.auth`, `admin` ni modelos en la etapa 1: eso es la etapa 2.
