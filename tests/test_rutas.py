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
