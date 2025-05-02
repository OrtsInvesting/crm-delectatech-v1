import streamlit as st
import os
import json
import pandas as pd

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    st.title("⚙️ Ajustes")

    st.warning("⚠️ Esto borrará todos los datos de tu sesión (contactos, listas, archivos).")

    if st.button("🔄 Resetear usuario y empezar de 0"):
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}
        guardar_usuario_data()
        st.success("Usuario reseteado correctamente.")
        st.rerun()

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
