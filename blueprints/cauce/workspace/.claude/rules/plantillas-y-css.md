---
description: Convenciones de plantillas, CSS y JavaScript de Cauce
paths:
  - "web/templates/**"
  - "web/static/**"
---

# Plantillas, CSS y JS

- Toda página hace `{% extends "web/base.html" %}`, llena `{% block contenido %}` y tiene un solo `<h1>`.
- CSS propio de una página: `{% block estilos %}` con `web/css/pages/<pagina>.css`. JS: `{% block scripts %}` con `defer`.
- Enlaces internos solo con `{% url 'nombre' %}`. Enlaces externos con `target="_blank"` llevan `rel="noopener"`.
- Prohibido `style="…"`, `onclick=`/`on*=` y `<script>` con lógica en línea. Datos para JS: `{{ valor|json_script:"id" }}`.
- Cada `<input>` visible tiene `<label for="id_…">`. Los errores van junto al campo (`.campo-error`) y el campo lleva `aria-invalid="true"` y `aria-describedby`.
- Colores, espacios, tamaños, radios y duraciones solo con `var(--…)` de `tokens.css`. `tests/test_estilos.py` falla con un hex, `rgb(`, sombra, radio > 16px o peso distinto de 400/500.
- Botón primario = `.boton-primario` (degradado aurora). Solo uno por sección. El resto: `.boton-secundario`.
- Cifras grandes = `.stat` en `--color-cifra`; nunca texto corrido en ese color.
- `--color-pizarra` y `--color-teal` nunca como color de texto (contraste < 4.5:1).
- Gráficas: `<canvas role="img" aria-label="…">` + `<details>` con `<table>` de los mismos datos. Uniforme = discontinua, reglas = continua, RL = continua gruesa.
- Animaciones: solo `transform` y `opacity`, ≤ 250ms, y apagadas con `prefers-reduced-motion: reduce`.
- Diseño desde móvil. Cortes: `@media (min-width: 768px)` y `@media (min-width: 1024px)`. Sin scroll horizontal a 320px.
