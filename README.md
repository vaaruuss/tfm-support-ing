# tfm-support-ing
Trabajo de Fin de Máster - Modelo predictivo para soporte en sucursales
# Panel de Soporte Predictivo - SLA Facilities

**Autor:** Álvaro Alba Grau  
**Formación:** Máster en Data Science & AI (Evolve Academy)  

## Objetivo del Proyecto
Este proyecto de Trabajo de Fin de Máster (TFM) desarrolla una solución analítica para predecir el riesgo de incumplimiento de los Acuerdos de Nivel de Servicio (SLA > 21 días) en la resolución de incidencias de mantenimiento y *facilities* en una red de oficinas corporativas.

## Arquitectura del Modelo
El motor predictivo se basa en un pipeline híbrido de **Regresión Logística**:
- **Procesamiento de Lenguaje Natural (NLP):** Vectorización TF-IDF de las descripciones técnicas de los tickets.
- **Variables Categóricas:** One-Hot Encoding para las ubicaciones (oficinas) y orígenes de la incidencia.
- **Explicabilidad:** El modelo permite identificar qué palabras clave (ej. "charco", "urgente") disparan la probabilidad de retraso, facilitando la toma de decisiones.

## Despliegue y Reproducción
Para ejecutar el Dashboard interactivo en un entorno local, sigue estos pasos:

1. Clona el repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt