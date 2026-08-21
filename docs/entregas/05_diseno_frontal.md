# Entrega 5: Diseño del frontal y experiencia de usuario

### 1. Resumen de la solución y del usuario
El proyecto resuelve la gestión reactiva de averías en la red de oficinas, anticipando qué incidencias corren el riesgo de enquistarse. 
* **Usuario principal:** Equipo de Branches Support encargado de supervisar el mantenimiento operativo.
* **Necesidad:** Priorizar qué tickets requieren seguimiento proactivo antes de que superen el SLA de 21 días.
* **Tipo de producto:** Un *dashboard* clasificador y predictor de riesgos.
* **Acción principal:** Identificar visualmente los tickets críticos para reclamar su resolución temprana al proveedor.

### 2. Imagen mockup del frontal
![Mockup del frontal](../assets/05_mockup_frontal.png)

### 3. Justificación del diseño
**3.1. Utilidad y valor de la solución**
El frontal transforma un histórico de Excel plano en una herramienta de triaje ágil. Ahorra tiempo al filtrar directamente el "ruido" (incidencias de resolución rápida) y concentra la atención del gestor solo en el porcentaje de tickets que el modelo señala como problemáticos, reduciendo el riesgo de bloqueo operativo en las sucursales. Se han ocultado intencionadamente métricas matemáticas complejas del modelo para centrarse en el impacto de negocio.

**3.2. Flujo de usuario**
1. **Entrada:** El usuario accede a la vista de "Tickets Pendientes".
2. **Procesamiento:** El sistema ya ha ejecutado el modelo de Machine Learning en *background* y presenta la lista ordenada de mayor a menor riesgo de incumplimiento de SLA.
3. **Selección:** El usuario hace clic en un ticket marcado en rojo (Alto Riesgo).
4. **Resultado:** Visualiza la probabilidad exacta de retraso calculada y las palabras clave de la descripción que han disparado la alerta.
5. **Acción:** Mediante un botón, puede marcar el ticket como "Revisado" o "Escalado".

**3.3. Experiencia de usuario**
* **Jerarquía visual:** Uso del sistema de semáforo (Rojo/Naranja/Verde) en la columna lateral para guiar la mirada inmediatamente hacia los problemas.
* **Simplicidad:** Interfaz limpia que emula las herramientas estándar de *ticketing*, minimizando la curva de aprendizaje.
* **Confianza:** El modelo muestra un porcentaje de probabilidad (ej. 85%), dejando claro que es una estimación estadística y manteniendo al usuario en control de la decisión final.

### 4. Presentación de resultados y explicabilidad
El resultado principal es una **clase (Riesgo / En tiempo)** acompañada de su **probabilidad**. Para evitar el efecto "caja negra", se incluye un apartado de explicabilidad donde se muestran los factores clave detectados por el modelo (por ejemplo, el peso TF-IDF de términos como "presupuesto" o "sin stock" y el historial de la oficina afectada). 

*Uso de IA Generativa:* No se utilizará IA Generativa en esta fase del MVP. La justificación es mantener un entorno controlado y determinista basado estrictamente en la Regresión Logística aprobada en fases anteriores, priorizando la fiabilidad técnica sobre la generación de texto.

### 5. Alcance del MVP
Para el final del curso, se implementará una versión funcional del *dashboard* utilizando la librería **Streamlit** en Python. 
* **Dentro del alcance:** La ingesta de datos, el cálculo predictivo en vivo, la tabla lateral ordenable por riesgo y la visualización de la probabilidad y características del ticket seleccionado.
* **Fuera del alcance:** La integración real con el correo electrónico, sistemas de login complejos o la conexión en tiempo real con la API del proveedor de mantenimiento externo; que en el diseño visual sí pueden aparecer sugeridos.
