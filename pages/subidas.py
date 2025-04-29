import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

def mostrar():
    st.title("📂 Subida de contactos")

    file = st.file_uploader("📄 Sube un archivo CSV o Excel", type=["csv", "xlsx"])

    if file:
        nombres_archivos_existentes = [u["nombre_archivo"] for u in st.session_state.usuario_data["uploads"]]

        # ✅ Verificar si ya existe el archivo
        if file.name in nombres_archivos_existentes:
            st.error(f"❌ Ya has subido un archivo llamado '{file.name}'. Cambia el nombre y vuelve a intentarlo.")
        else:
            # ✅ Procesar archivo
            try:
                if file.name.endswith(".xlsx"):
                    new_df = pd.read_excel(file)
                else:
                    new_df = pd.read_csv(file)
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")
                return

            # ✅ Procesamiento básico
            new_df["Related to"] = new_df["Related to"].ffill()
            new_df["Nombre completo"] = new_df["Name"].fillna('') + " " + new_df["Last Name"].fillna('')
            new_df["Empresa"] = new_df["Related to"].fillna("Desconocida")
            new_df["Comentario"] = new_df["Description"].fillna("")
            new_df["Cargo_normalizado"] = new_df["Cargo"].str.lower().fillna("")
            new_df["LinkedIn"] = new_df.apply(
                lambda r: f'<a href="https://www.linkedin.com/sales/search/people/?keywords={r["Nombre completo"]} {r["Empresa"]}" target="_blank">🔗 Sales Nav</a>',
                axis=1
            )

            # ✅ Añadir campos adicionales
            new_df["archivo_origen"] = file.name
            new_df["Favorito"] = False
            new_df["Estado"] = "Nuevo"
            new_df["Nota"] = ""

            # ✅ Agregar a la base de datos del usuario
            st.session_state.usuario_data["bd"] = pd.concat([st.session_state.usuario_data["bd"], new_df], ignore_index=True)

            # ✅ Registrar el archivo subido
            st.session_state.usuario_data["uploads"].append({
                "nombre_archivo": file.name,
                "fecha_subida": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "contactos_subidos": len(new_df)
            })

            guardar_usuario_data()
            st.success(f"✅ Archivo '{file.name}' subido y procesado correctamente.")
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

