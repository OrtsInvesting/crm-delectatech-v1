import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    if "usuario" not in st.session_state:
        st.warning("Debes iniciar sesión para ver o subir contactos.")
        return

    st.title("📤 Subir nuevos contactos")

    archivo = st.file_uploader("Selecciona un archivo CSV con tus contactos")

    if archivo is not None:
        nombre_archivo = archivo.name
        nombres_archivos_existentes = [u["nombre_archivo"] for u in st.session_state.usuario_data["uploads"]]

        if nombre_archivo in nombres_archivos_existentes:
            st.error("Este archivo ya ha sido subido anteriormente.")
        else:
            try:
                nuevos_datos = pd.read_csv(archivo)
                st.session_state.usuario_data["bd"] = pd.concat([st.session_state.usuario_data["bd"], nuevos_datos], ignore_index=True)

                st.session_state.usuario_data["uploads"].append({
                    "nombre_archivo": nombre_archivo,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                guardar_usuario_data()
                st.success(f"Archivo '{nombre_archivo}' subido correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    st.title("📂 Histórico de uploads")

    uploads = st.session_state.usuario_data["uploads"]
    if uploads:
        for u in uploads:
            st.write(f"📎 {u['nombre_archivo']} — Subido el {u['fecha']}")
    else:
        st.info("Todavía no has subido ningún archivo.")

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
