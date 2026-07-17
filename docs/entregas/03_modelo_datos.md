# Entrega 3: Almacenamiento de datos

1. Resumen de la idea y datos del proyecto
    - Problema: El equipo de Branches Support realiza un seguimiento manual de las incidencias operativas y de mantenimiento de 29 sucursales tramitadas por CBRE, lo que retrasa la detección de averías recurrentes o cuellos de botella prolongados.
    - Solución: Desarrollar un modelo predictivo y de clasificación que analice el histórico de averías para alertar sobre incidencias con alta probabilidad de retraso, optimizando el mantenimiento de forma proactiva.
    - Fuentes de datos: El archivo maestro interno de seguimiento ("Tareas mmto prl seguridad ssgg 2026.xlsx" en la pestaña "Facilities").
    - Tipo de información: Datos transaccionales de tickets, fechas de apertura, sucursal afectada, descripciones de texto libre y estado actual de la avería.
      
2. Tecnología o formato de almacenamiento elegido
Para el almacenamiento de los datos transformados se utilizará el formato CSV procesado en memoria mediante Pandas (Python).
El volumen actual del archivo maestro cuenta con alrededor de 1.500 registros históricos. Este tamaño es perfecto para el procesamiento en memoria RAM con Pandas, sin requerir la infraestructura de una base de datos relacional compleja. El formato CSV garantiza la ligereza y compatibilidad universal para las fases de Análisis Exploratorio de Datos (EDA) y entrenamiento del modelo predictivo durante el curso.

3. Estructura de capas de datos
Se implementará una arquitectura basada en capas (Medallion Architecture) gestionada a través de carpetas locales en el entorno de desarrollo (ignoradas en GitHub mediante .gitignore para proteger la privacidad bancaria):
    - data/raw/: Contendrá el fichero original sin alteraciones ("Tareas mmto prl seguridad ssgg 2026.xlsx").
    - data/processed/: Scripts intermedios de Python transformarán el Excel en un archivo CSV limpiando los nombres de las columnas, casteando formatos de fecha y estandarizando las categorías de los estados.
    - data/gold/: Almacenará el dataset final preparado (tickets_gold.csv), con el texto de las descripciones procesado (NLP) y las variables objetivo generadas y listas para consumir.

  4. Definición de la capa gold
El resultado final del pipeline será un único dataset consolidado.
    - Nombre del fichero: tickets_gold.csv
    - Descripción funcional: Dataset maestro histórico de incidencias limpias, preparadas para entrenar el modelo de predicción de tiempos de resolución y análisis de patrones.
    - Granularidad: Una fila por cada incidencia/ticket reportado.
    - Número aproximado esperado de registros: ~1.500 - 2.000 filas.
    - Campos principales y tipos:
       - ticket_cbre (string): Identificador del ticket (Clave Primaria).
       - fecha_ticket (datetime): Fecha de apertura.
       - oficina (string): Sucursal de origen.
       - origen_incidencia (category): Origen del reporte (Ej. Personal Oficina).
       - descripcion_limpia (string): Texto de la avería sin stopwords ni puntuación.
       - estado (category): Variable de cierre (Abierto/Cerrado).
       - dias_abierto (int): Variable objetivo generada. Días transcurridos.
    - Uso posterior: EDA, Dashboard interactivo y entrenamiento de modelos predictivos de NLP y regresión.

5. Relaciones entre datos
El proyecto utilizará un único dataset plano.
Toda la información relevante de la avería (ubicación, fecha, descripción, estado) se encuentra desnormalizada en el Excel de origen. Unir tablas externas (como un mapeo de la capacidad física de las oficinas) aportaría una complejidad innecesaria para el MVP, por lo que una tabla plana (sábana de datos) es la estructura más eficiente para la ingesta directa del modelo de Machine Learning.

6. Diccionario de datos inicial
Campo Original en Raw	        Campo Gold	              Descripción	                      Tipo de dato	    Obligatorio
Ticket CBRE	                  ticket_cbre	    ID alfanumérico generado por CBRE	              string	           Sí
Fecha ticket                 	fecha_ticket	    Fecha de creación del reporte	                datetime	         Sí
OFICINA	                        oficina        	Nombre de la sucursal afectada	              string	           Sí
Incidencia (ILUMINACION...	  descripcion	      Texto descriptivo de la avería	              string             Sí
Estado                        	estado	      Estado de resolución de la incidencia	          string             Sí

7. Problemas de calidad esperados
Basado en una auditoría inicial del fichero real, se prevén los siguientes problemas concretos:
    - Nombres de columnas complejos: Las cabeceras del Excel contienen saltos de línea (ej. Incidencia \n\n(ILUMINACION...) que dificultarán la sintaxis en Python.
    - Valores nulos: Hay aproximadamente 136 tickets sin el ID asignado de Ticket CBRE y registros sin fechas válidas, lo que rompe la clave primaria.
    - Textos desestructurados: El campo de la incidencia contiene texto libre introducido manualmente, con variaciones tipográficas y falta de contexto que afectarán el rendimiento del algoritmo de procesamiento de lenguaje natural (NLP).
    - Falta de fecha de cierre: La ausencia de una fecha estandarizada de resolución en la tabla complica el cálculo exacto del tiempo del ciclo de vida del ticket (lead time).

8. Decisiones de limpieza y transformación previstas
    - Tratamiento de nulos: Se eliminarán los registros que no cuenten con Ticket CBRE o Fecha ticket, al considerarse transacciones fantasma o incompletas.
    - Renombrado de variables: Se aplicará un script estandarizado para limpiar los saltos de línea de las cabeceras (\n) y convertirlas a formato snake_case.
    - Construcción de variables (Feature Engineering): Al no haber fecha de cierre documentada de forma estándar, se utilizarán expresiones regulares sobre la columna Comentario PRL / Facilities / Seguridad para intentar extraer la fecha real de reparación indicada en el texto (ej. extrayendo las fechas de formatos como "(CG 27/05) Reparado").
    - Procesamiento de texto: A la columna de incidencia se le aplicará un pipeline de NLP: conversión a minúsculas, eliminación de caracteres especiales, stop-words y derivación léxica (lemmatization).

9. Riesgos del modelo de datos
    - Parte más clara: El formato de lectura, almacenamiento (CSV) y la granularidad transaccional de los tickets.
    - Mayor incertidumbre: La capacidad de extraer numéricamente el tiempo de resolución. Depender de expresiones regulares sobre los comentarios escritos manualmente conlleva un alto riesgo de perder registros que no sigan un patrón estricto de escritura.
    - Alternativa / Simplificación: Si resulta imposible deducir los días exactos de resolución, la variable predictiva objetivo (target) se simplificará. En lugar de predecir tiempos, el modelo se centrará en categorizar automáticamente los tickets de texto libre en "familias de riesgo" o "prioridades operativas".
