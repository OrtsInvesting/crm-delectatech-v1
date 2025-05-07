import streamlit as st
import pandas as pd
from io import BytesIO
import os
import json

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    if "usuario" not in st.session_state:
        st.warning("Debes iniciar sesión para ver tus listas.")
        return

    st.title("📚 Mis Listas")

    listas = st.session_state.usuario_data["listas"]

    if not listas:
        st.info("No tienes listas creadas todavía.")
        return

    for lista, contactos in listas.items():
        with st.expander(f"📋 {lista} ({len(contactos)} contactos)"):
            df = st.session_state.usuario_data["bd"]
            df_lista = df[df["Nombre completo"].isin(contactos)]
            st.dataframe(df_lista[["Nombre completo", "Cargo", "Empresa", "LinkedIn"]])

            if st.button(f"🗑️ Borrar lista '{lista}'", key=f"borrar_{lista}"):
                del st.session_state.usuario_data["listas"][lista]
                guardar_usuario_data()
                st.success(f"Lista '{lista}' eliminada.")
                st.rerun()

    if st.button("📥 Descargar todas las listas en Excel"):
        buffer = BytesIO()
        excel_writer = pd.ExcelWriter(buffer, engine='openpyxl')
        for lista, contactos in listas.items():
            df = st.session_state.usuario_data["bd"]
            df_lista = df[df["Nombre completo"].isin(contactos)]
            df_lista.to_excel(excel_writer, sheet_name=lista[:31], index=False)
        excel_writer.close()
        buffer.seek(0)

        st.download_button(
            label="Descargar Excel",
            data=buffer,
            file_name="listas_contactos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def guardar_usuario_data():
    if "usuario" not in st.session_state:
        return

    user_file = f"data/usuarios/{st.session_state.usuario}.json"
    os.makedirs(os.path.dirname(user_file), exist_ok=True)
    data = {
        "bd": st.session_state.usuario_data["bd"].to_dict(orient="records"),
        "listas": st.session_state.usuario_data["listas"],
        "uploads": st.session_state.usuario_data["uploads"]
    }
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
