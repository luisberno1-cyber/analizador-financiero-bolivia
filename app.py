import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# Configuración de página
st.set_page_config(page_title="SaaS Financiero Bolivia", layout="wide")

# Conexión Segura a la Base de Datos (usando tus Secrets)
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- FUNCIÓN DEL CENTINELA PARA COOPERATIVAS ---
def cargar_entidades():
    # El sistema busca en la base de datos lo que el Centinela ha procesado
    try:
        response = supabase.table("entidades").select("*").execute()
        if len(response.data) > 0:
            return pd.DataFrame(response.data)
    except:
        # Si la tabla está vacía aún, mostramos un mensaje amigable
        return pd.DataFrame({'nombre': ['Esperando al Centinela...'], 'tipo': ['N/A'], 'activos': [0]})

st.title("📊 Monitor Inteligente de Cooperativas y Bancos")

# Sidebar de niveles (Tu modelo de negocio)
nivel = st.sidebar.selectbox("Nivel de Acceso", ["Free", "Premium", "Ultra Premium"])

df = cargar_entidades()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Análisis de Entidad")
    entidad_sel = st.selectbox("Seleccione una Cooperativa o Banco:", df['nombre'])
    
    # Aquí el sistema mostrará los datos reales guardados por el Centinela
    st.info(f"Entidad seleccionada: {entidad_sel}")
    st.metric("Disponibilidades", "Calculando...", help="Datos en proceso de carga por el Centinela")

with col2:
    st.subheader("Distribución del Sector")
    # Este gráfico se actualizará solo conforme entren más cooperativas
    fig = px.bar(df, x='nombre', y='activos', color='tipo', title="Activos por Entidad")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("🚀 El Centinela está escaneando la ASFI ahora mismo. Los datos aparecerán automáticamente aquí.")
