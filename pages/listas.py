import streamlit as st
import pandas as pd
from io import BytesIO
import os
import json

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    st.title("📚 Mis Listas")

    if not st.session_state.usuario_data["listas"]:
        st.info("No tienes listas creadas todavía.")
        return

    listas = st.session_state.usuario_data["listas"]

    for lista, contactos in listas.items():
        with st.expander(f"📋 {lista} ({len(contactos)} contactos)"):
            if contactos:
                df_contactos = st.session_state.usuario_data["bd"].query("`Nombre completo` in @contactos")
                st.dataframe(df_contactos[[
                    "Nombre completo", "Cargo", "Empresa", "Email", "Estado", "Comentario", "Favorito"
                ]])
            else:
                st.write("(Lista vacía)")

    if st.button("📥 Descargar todas las listas en Excel"):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for nombre, contactos in listas.items():
                df_lista = st.session_state.usuario_data["bd"].query("`Nombre completo` in @contactos")
                df_lista.to_excel(writer, sheet_name=nombre[:31], index=False)
        buffer.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=buffer,
            file_name="listas_contactos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def guardar_usuario_data():
    if "usuario" not in st.session_state:
        return  # No hay sesión iniciada, no se guarda

    user_file = f"data/usuarios/{st.session_state.usuario}.json"
    os.makedirs(os.path.dirname(user_file), exist_ok=True)
    data = {
        "bd": st.session_state.usuario_data["bd"].to_dict(orient="records"),
        "listas": st.session_state.usuario_data["listas"],
        "uploads": st.session_state.usuario_data["uploads"]
    }
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
