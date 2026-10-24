"""Paso 3: los tokens del sistema de diseño existen y el CSS respeta sus reglas."""

import re
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "web" / "static" / "web" / "css"

TOKENS = [
    "--color-abismo", "--color-fondo", "--color-alga", "--color-pizarra",
    "--color-titulo", "--color-texto", "--color-texto-enfasis", "--color-cita", "--color-cifra",
    "--color-teal", "--color-aqua", "--color-boton-icono",
    "--gradiente-aurora", "--gradiente-bioluminiscente", "--color-sobre-aurora",
    "--color-borde", "--color-borde-control",
    "--color-error", "--color-aviso", "--color-exito", "--color-foco",
    "--serie-uniforme", "--serie-reglas", "--serie-rl",
    "--perfil-0", "--perfil-1", "--perfil-2", "--perfil-3",
    "--fondo-grafica", "--rejilla-grafica",
    "--fuente", "--peso-regular", "--peso-medio",
    "--texto-etiqueta", "--texto-pequeno", "--texto-base", "--texto-destacado",
    "--texto-subtitulo", "--texto-titulo", "--texto-titulo-lg", "--texto-display",
    "--tracking-etiqueta", "--tracking-titulo", "--tracking-subtitulo",
    "--interlineado-titulo", "--interlineado-cuerpo",
    "--esp-1", "--esp-2", "--esp-3", "--esp-4", "--esp-5", "--esp-6", "--esp-8", "--esp-9",
    "--esp-10", "--esp-12", "--esp-16", "--esp-20", "--esp-30",
    "--ancho-max", "--ancho-lectura", "--margen-lateral", "--relleno-tarjeta",
    "--separacion-seccion", "--alto-cabecera",
    "--radio-pequeno", "--radio-tarjeta",
    "--duracion-rapida", "--duracion-media", "--curva-salida",
]  # fmt: skip

COMPONENTES_BASE = [
    ".boton-primario", ".boton-secundario", ".boton-icono", ".etiqueta",
    ".tarjeta", ".tarjeta-hundida", ".stat", ".insignia-demo",
]  # fmt: skip


def _hojas() -> list[Path]:
    return sorted(CSS.rglob("*.css"))


def _sin_comentarios(texto: str) -> str:
    return re.sub(r"/\*.*?\*/", "", texto, flags=re.S)


def test_tokens_define_todas_las_variables():
    tokens = (CSS / "tokens.css").read_text(encoding="utf-8")
    faltantes = [t for t in TOKENS if f"{t}:" not in tokens]
    assert faltantes == []


def test_fuente_es_inter():
    assert '"Inter"' in (CSS / "tokens.css").read_text(encoding="utf-8")


def test_colores_literales_solo_en_tokens():
    for hoja in _hojas():
        if hoja.name == "tokens.css":
            continue
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b", texto), f"color hex en {hoja.name}"
        assert not re.search(r"\b(rgb|rgba|hsl|hsla)\(", texto), f"color literal en {hoja.name}"


def test_sin_sombras():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        assert not re.search(r"box-shadow\s*:\s*(?!none)", texto), f"sombra en {hoja.name}"


def test_radios_maximo_16px():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        for valor in re.findall(r"border-radius\s*:\s*([^;}]+)", texto):
            assert "%" not in valor, f"radio en % en {hoja.name}"
            for numero in re.findall(r"(\d+(?:\.\d+)?)px", valor):
                assert float(numero) <= 16, f"radio {numero}px en {hoja.name}"


def test_solo_pesos_400_y_500():
    for hoja in _hojas():
        texto = _sin_comentarios(hoja.read_text(encoding="utf-8"))
        for peso in re.findall(r"font-weight\s*:\s*(\d+)", texto):
            assert peso in ("400", "500"), f"peso {peso} en {hoja.name}"


def test_base_tiene_foco_visible_y_movimiento_reducido():
    base = (CSS / "base.css").read_text(encoding="utf-8")
    assert ":focus-visible" in base
    assert "prefers-reduced-motion: reduce" in base
    assert ".saltar-contenido" in base


def test_componentes_base_existen():
    componentes = (CSS / "components.css").read_text(encoding="utf-8")
    faltantes = [c for c in COMPONENTES_BASE if c not in componentes]
    assert faltantes == []
