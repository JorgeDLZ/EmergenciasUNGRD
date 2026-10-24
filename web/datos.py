"""Contrato de datos de Cauce.

Las páginas solo leen datos a través de este módulo. Hoy los JSON de `web/data/mock/` son
datos de EJEMPLO; cuando los notebooks del proyecto exporten resultados reales con el mismo
formato, basta con reemplazar esos archivos (y poner CAUCE_DATOS_DEMO=0). Ninguna plantilla
ni vista cambia.
"""

import json
from functools import cache
from pathlib import Path

DIRECTORIO_DATOS = Path(__file__).resolve().parent / "data" / "mock"
POLITICAS = ("uniforme", "reglas", "rl")


class DatosInvalidos(ValueError):
    """Un archivo de datos no cumple el contrato."""


def _leer(nombre: str) -> dict:
    with open(DIRECTORIO_DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def _exigir(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise DatosInvalidos(mensaje)


def _exigir_politicas(valores: dict, donde: str) -> None:
    _exigir(
        isinstance(valores, dict) and set(valores) == set(POLITICAS),
        f"{donde}: debe tener exactamente las políticas {POLITICAS}",
    )


def validar_resultados(datos: dict) -> None:
    for clave in (
        "fuente",
        "resumen",
        "politicas",
        "metricas",
        "recompensa_por_episodio",
        "sensibilidad_presupuesto",
        "estabilidad",
    ):
        _exigir(clave in datos, f"resultados.json: falta la clave '{clave}'")
    _exigir(len(datos["resumen"]) == 4, "resultados.json: 'resumen' debe tener 4 cifras")
    for cifra in datos["resumen"]:
        _exigir({"id", "valor", "etiqueta"} <= set(cifra), "resultados.json: cifra incompleta")
    _exigir(
        [p["id"] for p in datos["politicas"]] == list(POLITICAS),
        "resultados.json: 'politicas' debe listar uniforme, reglas, rl en ese orden",
    )
    for metrica in datos["metricas"]:
        _exigir(
            {"id", "nombre", "unidad", "mejor", "valores"} <= set(metrica),
            "resultados.json: métrica incompleta",
        )
        _exigir(metrica["mejor"] in ("mayor", "menor"), "resultados.json: 'mejor' inválido")
        _exigir_politicas(metrica["valores"], f"métrica {metrica['id']}")
    for clave, eje in (
        ("recompensa_por_episodio", "episodios"),
        ("sensibilidad_presupuesto", "presupuesto_pct"),
    ):
        bloque = datos[clave]
        _exigir_politicas(bloque["series"], clave)
        for politica in POLITICAS:
            _exigir(
                len(bloque["series"][politica]) == len(bloque[eje]),
                f"{clave}: la serie '{politica}' no tiene la misma longitud que '{eje}'",
            )
    _exigir_politicas(datos["estabilidad"]["desviacion_recompensa"], "estabilidad")


def validar_perfiles(datos: dict) -> None:
    for clave in ("fuente", "k", "ejes", "perfiles", "puntos"):
        _exigir(clave in datos, f"perfiles.json: falta la clave '{clave}'")
    _exigir(len(datos["perfiles"]) == datos["k"], "perfiles.json: 'k' no coincide con los perfiles")
    ids = {perfil["id"] for perfil in datos["perfiles"]}
    for punto in datos["puntos"]:
        _exigir(punto["perfil"] in ids, f"perfiles.json: punto con perfil desconocido {punto}")


def validar_simulaciones(datos: dict) -> None:
    _exigir("simulaciones" in datos, "simulaciones.json: falta la clave 'simulaciones'")
    vistos: set[str] = set()
    for sim in datos["simulaciones"]:
        for clave in ("id", "nombre", "fecha", "parametros", "resultado"):
            _exigir(clave in sim, f"simulaciones.json: a una simulación le falta '{clave}'")
        _exigir(sim["id"] not in vistos, f"simulaciones.json: id repetido {sim['id']}")
        vistos.add(sim["id"])
        for metrica in sim["resultado"].values():
            _exigir_politicas(metrica, f"simulación {sim['id']}")


@cache
def resultados() -> dict:
    datos = _leer("resultados.json")
    validar_resultados(datos)
    return datos


@cache
def perfiles() -> dict:
    datos = _leer("perfiles.json")
    validar_perfiles(datos)
    return datos


@cache
def simulaciones() -> list[dict]:
    datos = _leer("simulaciones.json")
    validar_simulaciones(datos)
    return datos["simulaciones"]


def simulacion(sim_id: str) -> dict | None:
    return next((sim for sim in simulaciones() if sim["id"] == sim_id), None)
