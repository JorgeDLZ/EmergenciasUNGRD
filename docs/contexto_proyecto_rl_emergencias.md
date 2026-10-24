# Aprendizaje por Refuerzo para la Asignación de Recursos de Respuesta ante Emergencias en Colombia

**Tipo de documento:** Contexto y alcance del proyecto
**Fuente de datos principal:** Emergencias UNGRD V2 (Datos Abiertos Colombia)

---

## 1. Resumen

Colombia enfrenta emergencias de distinta naturaleza (inundaciones, incendios forestales, movimientos en masa) cuyos impactos varían según el territorio. Los recursos de respuesta son limitados, por lo que la pregunta central es: **¿quién recibe ayuda primero y en qué cantidad?**

El proyecto **no busca predecir dónde ocurrirá un desastre**. Busca diseñar y evaluar un agente de aprendizaje por refuerzo (RL) que aprenda a distribuir recursos limitados entre municipios afectados, dentro de una simulación construida a partir de datos históricos reales de la UNGRD.

---

## 2. Planteamiento del problema

Las emergencias producen impactos humanos y materiales diferentes en cada territorio. La asignación de recursos debe considerar la gravedad de cada evento y las limitaciones operativas (presupuesto, inventario y capacidad de atención).

Los registros históricos de la UNGRD permiten caracterizar las emergencias y sus consecuencias. A partir de ellos se propone un entorno simulado donde un agente aprenda a distribuir recursos entre varios eventos simultáneos.

**Limitación estructural:** los registros históricos no muestran qué habría ocurrido con decisiones distintas. Por eso el agente aprende dentro de una simulación y **no** a partir de las consecuencias causales de decisiones reales.

---

## 3. Pregunta de investigación

¿En qué medida una política aprendida mediante aprendizaje por refuerzo puede mejorar la asignación simulada de recursos de atención frente a estrategias convencionales, bajo restricciones de presupuesto y disponibilidad?

---

## 4. Objetivos

### Objetivo general

Diseñar y evaluar un agente de aprendizaje por refuerzo que aprenda a asignar recursos de respuesta ante emergencias en un entorno simulado, utilizando datos históricos de Colombia para representar las características de los eventos.

### Objetivos específicos

1. Caracterizar los patrones históricos de emergencias por territorio, tipo de evento y afectación.
2. Aplicar K-means para identificar perfiles de emergencias con características similares.
3. Diseñar un entorno simulado con recursos limitados, acciones disponibles y una función de recompensa.
4. Entrenar un agente de RL y compararlo con políticas de referencia.
5. Evaluar su desempeño, robustez y sensibilidad a cambios en la disponibilidad de recursos.

---

## 5. Datos

**Dataset principal:** Emergencias UNGRD V2, publicado por la Unidad Nacional para la Gestión del Riesgo de Desastres en Datos Abiertos Colombia.

**Contenido descrito en su ficha:** tipo de evento, fecha, ubicación, personas afectadas y daños reportados.

**Verificación inicial obligatoria** (no se asume nada sin inspeccionar el archivo descargado):

- Número de registros de la versión actual.
- Período que cubre.
- Proporción de registros con datos completos.
- Disponibilidad real de cada variable.

---

## 6. Formulación del problema de RL

| Elemento | Propuesta inicial |
|---|---|
| **Agente** | Sistema que asigna recursos de respuesta |
| **Entorno** | Simulación de varios municipios y emergencias |
| **Estado** | Eventos pendientes, gravedad estimada, recursos disponibles y tiempo transcurrido |
| **Acciones** | Asignar una unidad de recurso a una emergencia, priorizarla o reservar recursos |
| **Recompensa** | Premia la atención de necesidades; penaliza demoras, necesidades no atendidas y costos |
| **Restricciones** | Presupuesto, inventario de recursos y capacidad de atención |
| **Episodio** | Un escenario simulado de emergencia con horizonte temporal definido |

Los tipos de recurso podrían ser kits humanitarios, unidades de rescate o equipos de atención. Sus cantidades, capacidades y costos deben obtenerse de fuentes adicionales o **definirse como supuestos explícitos** del experimento.

---

## 7. Rol de K-means

K-means es un componente **complementario** para descubrir perfiles de emergencias. Variables candidatas:

- Personas y familias afectadas.
- Personas fallecidas, heridas o desaparecidas.
- Viviendas destruidas y averiadas.
- Vías y puentes afectados.
- Tipo de evento (con codificación adecuada).

Se comparará si una política funciona mejor usando estos perfiles como parte del estado frente a una que usa directamente las variables agregadas.

**Precauciones:**

- No tratar códigos de municipio como cantidades numéricas.
- Normalizar las variables antes de agrupar.
- Excluir o tratar con cuidado variables conocidas solo después de atender la emergencia (evitar fuga de información futura).

---

## 8. Diseño experimental

Se comparan tres estrategias sobre los mismos escenarios:

1. **Política uniforme:** reparto según una regla fija.
2. **Política basada en reglas:** prioriza eventos con mayor necesidad estimada, respetando restricciones.
3. **Política de RL:** agente entrenado para maximizar la recompensa acumulada.

**Métricas:**

- Porcentaje de necesidades atendidas.
- Tiempo simulado hasta la atención.
- Costo total de asignación.
- Número de emergencias sin recursos.
- Recompensa acumulada por episodio.
- Variabilidad del desempeño entre escenarios (estabilidad).

**Controles de validez:**

- Separar períodos históricos para que el diseño del entorno no use información del futuro.
- Repetir experimentos con distintas semillas aleatorias y distintos presupuestos.

---

## 9. Herramientas (Python)

| Librería | Uso |
|---|---|
| pandas, numpy | Preparación y agregación de registros |
| scikit-learn | Preprocesamiento, K-means y evaluación de grupos |
| gymnasium | Construcción del entorno de simulación |
| stable-baselines3 | Entrenamiento de PPO o DQN |
| matplotlib | Visualización de resultados |

**Estrategia de implementación:** empezar con un entorno pequeño y discreto para comparar una política de reglas con Q-learning; ampliar a PPO o DQN solo si la complejidad lo justifica.

---

## 10. Alcances

**Incluye:**

- Análisis exploratorio y caracterización de los registros UNGRD V2.
- Agrupamiento de emergencias con K-means.
- Entorno simulado propio (gymnasium) con recursos limitados.
- Entrenamiento de un agente RL (inicialmente Q-learning; PPO/DQN opcional).
- Comparación con política uniforme y política basada en reglas.
- Evaluación de desempeño, robustez y sensibilidad a presupuesto y disponibilidad.

## 11. Limitaciones y fuera de alcance

- **Es una simulación, no la realidad:** los resultados no son recomendaciones operativas directas para la UNGRD ni evidencia causal sobre decisiones reales.
- **No es un modelo predictivo:** no se pronostica dónde u cuándo ocurrirá un desastre.
- **Supuestos explícitos:** cantidades, capacidades y costos de recursos provienen de fuentes adicionales o se declaran como supuestos.
- **Dependencia de la calidad del dato:** la completitud y consistencia del dataset condicionan el diseño; se verifica antes de modelar.
- **Sin información futura:** el diseño temporal debe evitar fuga de datos.
- **Escala inicial reducida:** entorno pequeño y discreto; la ampliación a algoritmos más complejos es condicional.
- **No se modela** logística real de transporte, coordinación interinstitucional ni dinámica detallada de cada tipo de evento (salvo lo que se defina como supuesto).

---

## 12. Próximos pasos

1. Descargar el dataset y ejecutar la verificación inicial (registros, período, completitud).
2. Definir y documentar los supuestos de recursos (tipos, cantidades, costos, capacidad).
3. Preparar variables y aplicar K-means.
4. Construir el entorno en gymnasium y las dos políticas de referencia.
5. Entrenar Q-learning, evaluar y decidir si se escala a PPO/DQN.
