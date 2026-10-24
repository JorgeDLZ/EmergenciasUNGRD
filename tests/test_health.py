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
