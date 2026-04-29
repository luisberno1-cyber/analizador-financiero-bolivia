import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sistema Financiero Bolivia", layout="wide")

# Simulación de datos que el Centinela procesará de la ASFI
def obtener_datos():
    data = {
        'Entidad': ['Banco Unión', 'Banco Mercantil', 'BancoSol', 'BNB', 'Banco Ganadero'],
        'Activos (MM)': [15200, 14800, 9500, 13200, 8900],
        'Cartera Mora %': [2.1, 1.8, 3.5, 2.0, 2.4]
    }
    return pd.DataFrame(data)

st.title("📊 Monitor del Sistema Financiero de Bolivia")
st.sidebar.header("Nivel de Acceso")
nivel = st.sidebar.selectbox("Seleccione su suscripción", ["Free", "Premium", "Ultra Premium"])

df = obtener_datos()

# Dashboard Principal
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Análisis por Entidad")
    entidad = st.selectbox("Seleccione Banco/Cooperativa:", df['Entidad'])
    datos_entidad = df[df['Entidad'] == entidad].iloc[0]
    st.metric("Activo Total", f"{datos_entidad['Activos (MM)']} MM")
    
    if nivel != "Free":
        st.metric("Índice de Mora", f"{datos_entidad['Cartera Mora %']}%")
    else:
        st.info("🔒 Mora: Disponible en Premium")

with col2:
    st.subheader("Participación de Mercado")
    fig = px.pie(df, values='Activos (MM)', names='Entidad', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ El Centinela está activo buscando nuevos archivos en ASFI...")
