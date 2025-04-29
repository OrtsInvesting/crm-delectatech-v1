import streamlit as st
import pandas as pd

def mostrar():
    st.title("📊 Dashboard de Actividad")

    if "usuario_data" not in st.session_state or st.session_state.usuario_data["bd"].empty:
        st.info("No tienes contactos todavía para mostrar métricas.")
        return

    bd = st.session_state.usuario_data["bd"]

    st.metric("Leads totales", len(bd))

    if not bd.empty and "Comentario" in bd.columns:
        porcentaje_comentados = (bd["Comentario"] != "").mean() * 100
        st.metric("Leads con comentario (%)", f"{porcentaje_comentados:.1f}%")
    
    if not bd.empty and "Favorito" in bd.columns:
        favoritos = bd[bd["Favorito"] == True]
        st.metric("Leads favoritos", len(favoritos))

    if not bd.empty and "Estado" in bd.columns:
        st.subheader("🚦 Distribución por Estado")
        estado_counts = bd["Estado"].value_counts()
        st.bar_chart(estado_counts)

    if not bd.empty and "Empresa" in bd.columns:
        st.subheader("🏢 Top 5 Empresas con más leads")
        empresas_top = bd["Empresa"].value_counts().head(5)
        st.table(empresas_top)

