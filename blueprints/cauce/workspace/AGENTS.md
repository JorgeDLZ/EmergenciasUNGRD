# Cauce — instrucciones para agentes

Sitio web (Django) del proyecto de aprendizaje por refuerzo que asigna recursos ante emergencias en
Colombia con datos de la UNGRD.

## Comandos

| Tarea | Comando |
|---|---|
| Crear entorno | `python -m venv .venv` |
| Instalar | `sh scripts/py -m pip install -r requirements-dev.txt` |
| Servidor local | `sh scripts/py app.py` |
| Pruebas | `sh scripts/py -m pytest` · un archivo: `sh scripts/py -m pytest tests/test_rutas.py` |
| Lint / formato | `sh scripts/py -m ruff check .` · `sh scripts/py -m ruff format --check .` |

## No negociable

1. Nunca subir secretos, `.env`, `.venv/` ni `staticfiles/`.
2. Nunca marcar una tarea como hecha con el gate en rojo, ni editar un comando `verify` para que pase.
3. La sesión solo se lee con `get_current_user()`; toda página bajo `/app/` lleva `@login_requerido`.
4. Las páginas solo leen datos con `web.datos`; cambiar los JSON exige que sus validadores pasen.
5. Ningún color, sombra, radio o peso fuera de `tokens.css` (lo vigila `tests/test_estilos.py`).
6. No construir nada de la tabla "Fuera de alcance" de `blueprints/cauce/blueprint.md` §1.

Arquitectura, fronteras y tokens de diseño completos: `CLAUDE.md` en este mismo directorio.
