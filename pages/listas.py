import streamlit as st
import pandas as pd
from io import BytesIO
import os
import json

def mostrar():
    st.title("📚 Mis Listas")

    if "usuario_data" not in st.session_state or not st.session_state.usuario_data["listas"]:
        st.info("No tienes listas creadas todavía.")
        return

    listas = st.session_state.usuario_data["listas"]

    for lista, contactos in listas.items():
        with st.expander(f"📋 {lista} ({len(contactos)} contactos)"):
            st.write(contactos)

    if st.button("📥 Descargar todas las listas en Excel"):
        buffer = BytesIO()
        # Crear un DataFrame donde cada lista es una columna
        listas_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in listas.items()]))
        listas_df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=buffer,
            file_name="listas_contactos.xlsx",
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

