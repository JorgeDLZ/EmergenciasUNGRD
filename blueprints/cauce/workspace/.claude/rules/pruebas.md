---
description: Convenciones de pruebas de Cauce
paths:
  - "tests/**"
  - "pytest.ini"
---

# Pruebas

- Cada tarea del plan trae su archivo de pruebas literal en el epic. Se copia tal cual; no se edita para que pase.
- Ejecutar: `sh scripts/py -m pytest` (todo) o `sh scripts/py -m pytest tests/<archivo>.py`.
- `pytest.ini` convierte toda advertencia en error (`filterwarnings = error`): se corrige la causa, no se silencia.
- Usar las fixtures de pytest-django: `client`, `rf`, `settings`. Para simular sesión, hacer `client.post(reverse("login"), {...})`.
- Nada de red externa en las pruebas. Los procesos que una prueba arranca (`runserver`, `manage.py`) se terminan en un `finally`.
- Afirmar propiedades (claves presentes, orden, códigos HTTP), no textos generados por librerías.
