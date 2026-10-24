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
