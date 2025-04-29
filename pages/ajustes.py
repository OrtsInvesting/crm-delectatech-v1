import streamlit as st
import os
import json
import pandas as pd

def mostrar():
    st.title("⚙️ Ajustes")

    st.warning("⚠️ Cuidado: al resetear, perderás todos tus contactos, listas y archivos subidos.")

    if st.button("🔄 Resetear CRM y empezar de 0"):
        # Reiniciar los datos del usuario
        st.session_state.usuario_data = {
            "bd": pd.DataFrame(),
            "listas": {},
            "uploads": []
        }
        guardar_usuario_data()
        st.success("✅ Usuario reseteado. Puedes empezar desde cero.")
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
