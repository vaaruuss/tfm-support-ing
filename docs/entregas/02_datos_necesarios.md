# Entrega 2: Análisis de datos necesarios

1. Idea seleccionada
Problema que resuelve:
El equipo de Branches Support gestiona de forma centralizada las incidencias operativas, de infraestructura y mantenimiento (tramitadas a través del proveedor CBRE) para una red de 29 oficinas. Actualmente, el seguimiento es puramente reactivo y manual: se procesan reportes semanales en hojas de cálculo para identificar tickets paralizados ("en hold") o no resueltos. Esto genera una respuesta tardía frente a incidencias recurrentes, afectando la operatividad de los gestores en las sucursales y consumiendo horas de trabajo manual en tareas de cruce de bases de datos.

Solución planteada:
La solución consiste en desarrollar un modelo analítico y predictivo basado en el histórico de tickets de incidencias. Mediante técnicas de Machine Learning (como clasificación y NLP para los textos descriptivos), el sistema analizará la temporalidad, tipología de la avería, oficina de origen y tiempos de resolución pasados. El modelo predecirá qué tickets tienen un alto riesgo de bloqueo prolongado y detectará patrones operativos (por ejemplo, fallos recurrentes de climatología o cajeros en zonas específicas), permitiendo pasar a un mantenimiento proactivo.

MVP del proyecto final:
El Producto Mínimo Viable (MVP) será un dashboard interactivo que sustituirá el actual seguimiento estático. Este panel ingerirá el listado de tickets y mostrará: 1) Una visualización del estado de salud operativo de las 29 oficinas, 2) Un sistema de clasificación que alerte de tickets entrantes con alta probabilidad de retraso, y 3) Una predicción del volumen de incidencias esperado a corto plazo segmentado por categoría.

2. Datos necesarios
Para desarrollar este modelo analítico, se requieren los siguientes datos:
    - Variables imprescindibles: ID del Ticket CBRE, Oficina de origen, Fecha de apertura, Estado (Abierto/Cerrado), Origen de la     incidencia y Descripción del problema (texto libre).
    - Variables deseables: Fecha exacta de cierre (para medir lead time), comentarios de seguimiento (Facilities/Seguridad) e importe/coste de la reparación si estuviera disponible.
    - Granularidad: A nivel transaccional. Un registro (fila) por cada ticket de incidencia generado.
    - Profundidad histórica: Se necesitará el histórico de al menos los últimos 12 a 24 meses (idealmente 2024, 2025 y lo que va de 2026) para captar estacionalidad (ej. averías de aire acondicionado en verano).
    - Volumen: Se estima necesario un volumen de varios miles de registros (mínimo 2.000 - 3.000 tickets) para que el entrenamiento del modelo predictivo y de NLP tenga validez estadística.

3. Fuentes de datos previstas
    - Fuente: Los reportes semanales emitidos por el proveedor CBRE y el repositorio consolidado internamente en el Excel maestro ("Tareas mmto prl seguridad ssgg 2026.xlsx").
    - Accesibilidad: Es una fuente de datos interna y privada del entorno laboral, accesible directamente por el rol desempeñado en el equipo de Support Branches.
    - Formato: Exportaciones estructuradas en .xlsx y .csv.
    - Estabilidad: Muy estable, ya que es un reporte estandarizado que se envía semanalmente (cada viernes) como parte de un proceso operativo consolidado.
    - Riesgos detectados: El mayor riesgo radica en la calidad de la columna "Descripción", al ser texto libre introducido por personal de oficina, puede contener errores tipográficos, falta de contexto o estructura inconsistente que requerirá un fuerte preprocesamiento en Python.

4. Consideraciones de privacidad y protección de datos
Dado que se trata de incidencias operativas y de mantenimiento de instalaciones corporativas, el dataset base no contiene información financiera, ni datos de clientes bancarios.
    - Riesgo de datos personales: Es posible que en las descripciones de texto libre aparezcan nombres de empleados de las sucursales o de los técnicos de reparación.
    - Mitigación y Anonimización: Antes de extraer el dataset del entorno corporativo para el TFM, se aplicará un filtrado estricto. Se eliminarán columnas no esenciales y se utilizarán scripts de ofuscación para eliminar nombres propios del texto libre. Las sucursales se mantendrán por ubicación geográfica, no representando riesgo confidencial.
5. Viabilidad inicial del proyecto
    - Viabilidad general: El proyecto es altamente viable y realista para la duración del curso. Al depender de una fuente de datos interna con la que se interactúa semanalmente, la barrera de obtención de datos es mínima.
    - Calidad e histórico: La granularidad es perfecta (a nivel de ticket), y el histórico necesario existe en los archivos de la compañía, aunque dependerá de compilar los excels pasados.
    - Principal riesgo: La fase de limpieza de datos (Data Cleaning) y la aplicación de NLP sobre las descripciones de averías, ya que requerirá homogeneizar textos muy dispares.
    - Alternativa (Plan B): Si existiera un bloqueo inesperado por parte del departamento de Compliance para extraer la base de datos anonimizada, el modelo analítico, el código y el dashboard MVP se desarrollarían utilizando un dataset público de tickets de mantenimiento (tipo Facilities Helpdesk de plataformas como Kaggle), adaptando la estructura para demostrar la competencia técnica adquirida en el máster.
