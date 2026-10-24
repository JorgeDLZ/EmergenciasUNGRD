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
