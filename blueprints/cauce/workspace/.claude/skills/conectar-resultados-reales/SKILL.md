---
name: conectar-resultados-reales
description: Reemplazar los datos de ejemplo de Cauce por los resultados reales que exportan los notebooks (K-means, políticas, simulaciones). Úsala cuando digan "ya tenemos resultados", "conectar los datos reales", "quitar datos de ejemplo" o "actualizar las gráficas".
---

# Conectar resultados reales

## Cuándo usarla
Cuando los notebooks del equipo ya producen métricas, perfiles de K-means o simulaciones reales.

## Pasos
1. Desde el notebook, exporta tres JSON con exactamente la forma de `web/data/mock/resultados.json`, `perfiles.json` y `simulaciones.json` (mismas claves, políticas `uniforme`, `reglas`, `rl`). Cambia `"fuente"` a `"resultados_reales"`.
2. Valídalos antes de copiarlos, sin Django:
   `sh scripts/py -c "import json; from web import datos; datos.validar_resultados(json.load(open('resultados.json', encoding='utf-8')))"` (igual con `validar_perfiles` y `validar_simulaciones`).
3. Reemplaza los archivos de `web/data/mock/`.
4. Si `test_resultados_cumplen_contrato` o `test_datos.py` fallan por `fuente`, actualiza esa sola afirmación al nuevo valor en un commit propio que lo explique.
5. En Render, cambia `CAUCE_DATOS_DEMO` a `0` para quitar el aviso "Datos de ejemplo".

## Verify
```bash
sh scripts/py -m pytest tests/test_datos.py tests/test_inicio.py tests/test_resultados.py   # expect: exit 0, 0 failed
```

## No hagas
- Cambiar nombres de claves en el JSON sin cambiar el contrato en `web/datos.py` y sus pruebas.
- Leer los JSON desde una plantilla o una vista directamente.
