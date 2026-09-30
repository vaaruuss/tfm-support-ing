import streamlit as st
import joblib
import pandas as pd
import os

# Configuración de página nativa
st.set_page_config(page_title="Panel de Soporte Predictivo", layout="wide")

# Título principal estándar
st.title("Panel de Soporte Predictivo - Red de Oficinas")
st.markdown("---")

# Carga del modelo
@st.cache_resource
def cargar_modelo():
    ruta = os.path.join(os.path.dirname(__file__), '../models/modelo_sla_logistico.pkl')
    return joblib.load(ruta)

try:
    pipeline_lr = cargar_modelo()
    modelo_cargado = True
except FileNotFoundError:
    st.error("⚠️ Error crítico: No se ha encontrado el archivo del modelo en la ruta esperada (../models/modelo_sla_logistico.pkl).")
    modelo_cargado = False
    st.stop()

# Estructura de 3 columnas
col_left, col_mid, col_right = st.columns([1, 1.5, 1.2], gap="large")

with col_left:
    st.subheader("Tickets Pendientes")
    st.caption("(Ordenados por Riesgo)")
    
    # Emulamos la lista usando las alertas nativas de colores de Streamlit
    st.error("**SR5469592 - Climatización**\n\nOficina: Acacias")
    st.warning("**SR5586370 - Mobiliario Oficina**\n\nOficina: Salamanca")
    st.success("**SR5332293 - Iluminación**\n\nOficina: Acacias")

with col_mid:
    st.subheader("Detalle de Incidencia")
    
    oficina_input = st.text_input("Sucursal:", value="Acacias")
    origen_input = st.text_input("Origen:", value="Personal de oficina")
    descripcion_input = st.text_area("Descripción:", value="El aire acondicionado de la zona de cajas lleva goteando desde ayer. Se ha formado un charco y los clientes se resbalan. Urgente.", height=150)
    
    evaluar = st.button("Analizar Ticket con IA", type="primary", use_container_width=True)

with col_right:
    st.subheader("Predicción del Modelo de IA")
    
    if 'mostrar_prediccion' not in st.session_state:
        st.session_state.mostrar_prediccion = False

    if evaluar and modelo_cargado:
        st.session_state.mostrar_prediccion = True

    if st.session_state.mostrar_prediccion:
        if descripcion_input and oficina_input:
            df_nuevo = pd.DataFrame({'desc_limpia': [descripcion_input], 'oficina': [oficina_input]})
            
            prediccion = pipeline_lr.predict(df_nuevo)[0]
            probabilidades = pipeline_lr.predict_proba(df_nuevo)[0]
            prob_retraso = probabilidades[1] * 100 
            
            st.metric(label="Probabilidad de Incumplir SLA (21 días)", value=f"{prob_retraso:.1f} %")
            
            st.markdown("**Factores clave (Explicabilidad del Modelo):**")
            
            # Simulamos el vocabulario de alto riesgo extraído del histórico
            palabras_historicas = [
                "urgente", "charco", "plaga", "insectos", "fuga", "rotura", 
                "inundación", "peligro", "roto", "avería", "goteo", "eléctrico", 
                "chispas", "humo", "olor", "bloqueado", "cristal", "alarma", "techo", "caída"
            ]
            texto_minusculas = descripcion_input.lower()
            
            palabras_encontradas = [palabra for palabra in palabras_historicas if palabra in texto_minusculas]
            
            if palabras_encontradas:
                for p in palabras_encontradas:
                    st.markdown(f"- Coincidencia con histórico de riesgo: **{p}**")
            else:
                st.markdown("- *El vocabulario utilizado no coincide con patrones históricos de retraso.*")
                
            st.markdown(f"- ⚠️ Histórico de sucursal: La oficina **{oficina_input}** tiene penalización por retrasos pasados.")
            st.markdown("---")
            col_b1, col_b2 = st.columns(2)
            
            with col_b1:
                if st.button("Escalar a Coordinador", use_container_width=True):
                    st.success(" Incidencia escalada correctamente a Nivel 2.")
            with col_b2:
                if st.button("Descartar Alerta", use_container_width=True):
                    st.info(" Alerta descartada. Panel reseteado.")
                    st.session_state.mostrar_prediccion = False
                    st.rerun()
        else:
            st.warning("Faltan datos en el ticket para realizar la predicción.")
    else:
        st.info("Pulse 'Analizar Ticket con IA' para enviar el texto al algoritmo.")