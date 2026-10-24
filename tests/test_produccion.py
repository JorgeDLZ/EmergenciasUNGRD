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
