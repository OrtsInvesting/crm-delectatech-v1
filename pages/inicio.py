import streamlit as st
import pandas as pd

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}
        
    st.title("🏠 Inicio")

    if "usuario_data" not in st.session_state or st.session_state.usuario_data["bd"].empty:
        st.info("No tienes contactos todavía. ¡Sube un archivo CSV para empezar!")
        return

    bd = st.session_state.usuario_data["bd"]

    st.metric("Leads totales", len(bd))

    if not bd.empty and "Empresa" in bd.columns:
        st.metric("Empresas únicas", bd["Empresa"].nunique())
    else:
        st.metric("Empresas únicas", 0)

    if not bd.empty and "Comentario" in bd.columns:
        porcentaje = (bd["Comentario"] != "").mean() * 100
        st.metric("Leads con comentario (%)", f"{porcentaje:.1f}%")
    else:
        st.metric("Leads con comentario (%)", "0%")

