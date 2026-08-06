### 1. Problema que se busca resolver


Actualmente, el seguimiento de las incidencias operativas y de infraestructura en la red de 29 oficinas bancarias se realiza de forma manual y reactiva mediante la revisión de reportes semanales del proveedor de mantenimiento. El problema radica en la incapacidad de anticipar qué tickets se van a enquistar, lo que genera retrasos que impactan en la operatividad de los gestores y las sucursales.
El proyecto busca predecir, en el momento exacto de la apertura de una incidencia, si dicho ticket tiene un alto riesgo de incumplir un SLA (Acuerdo de Nivel de Servicio) interno predefinido (ej. resolución > 21 días). El usuario final será el equipo de soporte central, que utilizará esta predicción para priorizar la supervisión de tickets críticos y transicionar hacia un modelo de gestión proactiva. El resultado se considerará útil si permite detectar con antelación una proporción significativa de los tickets que acaban sufriendo bloqueos prolongados.

### 2. Análisis de datos planteado y utilidad esperada


Antes del modelado, se realizará un Análisis Exploratorio de Datos (EDA) exhaustivo para comprender la naturaleza de las incidencias y validar hipótesis operativas:
    - Análisis descriptivo y temporal: Se evaluará el volumen de tickets por oficina y mes para detectar estacionalidad (ej. picos de           incidencias de climatización en verano o fallos de cajeros a final de mes).
    - Análisis comparativo de SLA: Se estudiará la tasa de incumplimiento del SLA cruzada con el origen de la incidencia y la sucursal para     comprobar si oficinas específicas sufren retrasos estructurales.
    - Análisis de texto simple (NLP): Se extraerán las palabras clave más frecuentes en la descripción inicial de los tickets que terminan       incumpliendo el SLA, para identificar patrones de averías críticas.
    - Utilidad: Este análisis alimentará el dashboard del MVP con indicadores operativos clave y ayudará a seleccionar las características       (features) más informativas para el modelo predictivo, descartando variables con ruido.

### 3. Tipo de modelos que se van a plantear


El proyecto se abordará como una tarea de Clasificación Binaria supervisada, donde el objetivo es predecir una etiqueta discreta: 1 (Riesgo de incumplir SLA) o 0 (Resolución en tiempo).

| Alternativa | Tipo | Por qué se plantea | Limitación principal |
| :--- | :--- | :--- | :--- |
| **Baseline** | Regla heurística simple | Proporciona una referencia mínima. Clasificará los tickets basándose puramente en la tasa de retraso histórica de cada oficina. | Su precisión será baja y no capta la complejidad de la descripción del problema. |
| **Candidato 1** | Regresión Logística | Modelo altamente interpretable. Permite entender qué palabras clave de la descripción o qué oficinas tienen mayor "peso" estadístico en el retraso. | Puede fallar al capturar relaciones no lineales entre variables complejas. |
| **Candidato 2** | Random Forest / XGBoost | Algoritmos de ensamble robustos frente a valores atípicos, capaces de manejar combinaciones complejas de variables categóricas (oficinas) y vectorización de textos. | Menor interpretabilidad directa (caja negra) y mayor riesgo de *overfitting* en datasets medianos. |

### 4. Datos de entrada del análisis y los modelos


Se utilizará la capa gold, extrayendo la etiqueta objetivo mediante la consolidación de reportes semanales históricos (snapshots) para calcular la vida del ticket de forma objetiva, evitando el uso de comentarios de cierre que generarían data leakage.

| Entrada | Descripción | Granularidad / tipo | Uso en el análisis o modelo |
| :--- | :--- | :--- | :--- |
| `tickets_gold` | Dataset final consolidado. | Una fila por ticket único | Fuente principal de variables. |
| `oficina` | Sucursal bancaria afectada. | Categórica | *Feature* predictiva espacial. |
| `origen_incidencia` | Quién reportó el problema. | Categórica | *Feature* de contexto. |
| `mes_apertura` | Mes extraído de la fecha de creación. | Numérica / Categórica | *Feature* para capturar estacionalidad. |
| `tfidf_descripcion` | Matriz vectorizada del texto de apertura. | Numérica continua | *Feature* clave generada vía NLP. |
| *Descartadas* | Estado final, comentarios de seguimiento y fecha de cierre. | Varias | **Excluidas estrictamente** por riesgo de *fuga de información*. No están disponibles al abrir el ticket. |

### 5. Datos de salida y forma de consumo


La salida principal se integrará en un panel visualizador (dashboard) orientado a la toma de decisiones del equipo de soporte operativo.

| Campo de salida | Descripción | Tipo | Uso posterior |
| :--- | :--- | :--- | :--- |
| `ticket_cbre` | Identificador único de la incidencia. | String | Trazabilidad y unión con el seguimiento diario. |
| `probabilidad_retraso` | Puntuación (*score*) del modelo. | Float (0.0 a 1.0) | Permite crear un *ranking* de tickets más urgentes a supervisar. |
| `alerta_sla` | Etiqueta final (1: Riesgo, 0: Normal) basada en un umbral de probabilidad. | Integer / Boolean | Activación de alertas visuales en el dashboard para intervención manual prioritaria. |

### 6. Estrategia para diseñar y seleccionar el modelo


El proceso de selección garantizará un equilibrio entre capacidad predictiva y viabilidad operativa:
    1) Preparación y Preprocesamiento: Se imputarán valores nulos mínimos, se aplicará codificación One-Hot a las variables categóricas y     vectorización TF-IDF a la limpieza del texto de descripción.
    2) Entrenamiento: Se entrenará el Baseline y los modelos candidatos optimizando hiperparámetros.
    3) Criterio de comparación: Dado el contexto del problema, el coste de un Falso Negativo (ignorar un ticket que acabará bloqueado) es     mayor que el de un Falso Positivo (revisar un ticket que luego se resuelve rápido). Por ello, la métrica clave para la selección será     el Recall (Exhaustividad) y el F1-Score, priorizándolas sobre la Accuracy pura.
    4) Regla de decisión: Se elegirá el modelo que supere ampliamente el Recall del Baseline manteniendo una interpretabilidad lógica         para el equipo operativo. Si Random Forest mejora menos de un 3% a la Regresión Logística, se optará por esta última por su mayor         simplicidad y bajo coste computacional.

### 7. Estrategia de validación y evaluación


Para evitar que el modelo acceda a patrones del futuro, la separación de los datos simulará el despliegue real en producción.

| Elemento | Decisión prevista | Justificación |
| :--- | :--- | :--- |
| **Separación de datos** | *Split Temporal* (Out-of-time validation). | Entrenar con los tickets antiguos y validar/testear con los tickets más recientes. Evita totalmente el cruce temporal. |
| **Métrica principal** | *Recall* de la clase 1 (Retraso) y *F1-Score*. | En mantenimiento operativo, es crucial maximizar la detección de cuellos de botella (minimizar falsos negativos). |
| **Baseline** | Regla simple heurística. | Medir la mejora real aportada por la IA frente a la asunción estática. |
| **Criterio de aceptación** | *Recall* > 70% en la clase crítica. | Asegura que el equipo capturará al menos 7 de cada 10 tickets problemáticos con antelación. |

### 8. Riesgos y alternativas


    - Riesgo 1 (Construcción del Target): La variable objetivo de retraso de SLA se debe inferir de la permanencia del ticket en cortes       de reportes semanales. Si el histórico de cortes presenta huecos temporales masivos, se puede corromper el etiquetado.
    - Riesgo 2 (Data Leakage): Máxima precaución en no incluir ninguna derivada del campo de "Comentarios de Facilities", ya que se           rellenan a posteriori. Se aplicará un filtro duro de columnas previas al pipeline.
    - Riesgo 3 (Clases desbalanceadas): Es muy probable que la inmensa mayoría de tickets se resuelvan en tiempo y solo una fracción           incumpla el SLA. Se preverá el uso de técnicas de balanceo sintético de datos (SMOTE) o pesos por clase durante el entrenamiento.
    - Alternativa: Si la vectorización NLP del texto resulta excesivamente ruidosa o reduce el rendimiento en el split de validación, se       prescindirá de la columna de texto y se construirá el modelo predictivo únicamente con las variables estructuradas (oficina, fecha,       origen), conformando un sistema de alerta temprana simplificado y sólido.
