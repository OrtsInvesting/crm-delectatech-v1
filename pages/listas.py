import streamlit as st
import pandas as pd
import os
import json
from io import BytesIO

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    st.title("📚 Mis Listas")

    listas = st.session_state.usuario_data["listas"]
    bd = st.session_state.usuario_data["bd"]

    if not listas:
        st.info("No tienes listas creadas todavía.")
        return

    excel_data = []

    for nombre_lista, nombres_contactos in listas.items():
        contactos_filtrados = bd[bd["Nombre completo"].isin(nombres_contactos)]
        st.subheader(f"📋 Lista: {nombre_lista} ({len(contactos_filtrados)} contacto/s)")

        for idx, row in contactos_filtrados.iterrows():
            with st.expander(f"{row['Nombre completo']} — {row['Cargo']} ({row['Empresa']})"):
                st.markdown(row["LinkedIn"], unsafe_allow_html=True)
                st.markdown(f"- ✉️ **Email:** {row.get('Email', 'No disponible')}")
                st.markdown(f"- 🚦 **Estado:** {row.get('Estado', 'No definido')}")
                st.markdown(f"- ⭐ **Favorito:** {'Sí' if row.get('Favorito') else 'No'}")
                st.markdown(f"- 📝 **Nota:** {row.get('Nota', 'Sin nota')}")

                # Preparar fila para Excel
                excel_data.append({
                    "Lista": nombre_lista,
                    "Nombre completo": row["Nombre completo"],
                    "Email": row.get("Email", ""),
                    "Cargo": row.get("Cargo", ""),
                    "Empresa": row.get("Empresa", ""),
                    "Estado": row.get("Estado", ""),
                    "Favorito": "Sí" if row.get("Favorito") else "No",
                    "Nota": row.get("Nota", "")
                })

    if excel_data:
        st.markdown("### 📥 Exportar todas las listas")
        buffer = BytesIO()
        df_export = pd.DataFrame(excel_data)
        df_export.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.download_button(
            label="Descargar archivo Excel",
            data=buffer,
            file_name="listas_completas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def guardar_usuario_data():
    user_file = f"data/usuarios/{st.session_state.usuario}.json"
    os.makedirs(os.path.dirname(user_file), exist_ok=True)
    data = {
        "bd": st.session_state.usuario_data["bd"].to_dict(orient="records"),
        "listas": st.session_state.usuario_data["listas"],
        "uploads": st.session_state.usuario_data["uploads"]
    }
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
