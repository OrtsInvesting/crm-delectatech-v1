import streamlit as st
import pandas as pd
import os
import json

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}

    st.title("🧑‍💼 Contactos")

    bd = st.session_state.usuario_data["bd"]

    lista_filtro = st.sidebar.selectbox("📋 Filtrar por lista", ["Todas"] + list(st.session_state.usuario_data["listas"].keys()))
    buscar_nombre = st.sidebar.text_input("🔎 Buscar por nombre")

    if lista_filtro != "Todas":
        contactos_lista = st.session_state.usuario_data["listas"].get(lista_filtro, [])
        bd = bd[bd["Nombre completo"].isin(contactos_lista)]

    if buscar_nombre:
        bd = bd[bd["Nombre completo"].str.contains(buscar_nombre, case=False, na=False)]

    if bd.empty:
        st.info("No hay contactos que coincidan con los filtros.")
        return

    for idx, row in bd.iterrows():
        with st.expander(f"{row['Nombre completo']} — {row['Cargo']} ({row['Empresa']})"):

            st.markdown(row["LinkedIn"], unsafe_allow_html=True)
            st.caption(row["Comentario"] if row["Comentario"] else "Sin comentario")

            # ⭐ Favorito
            favorito = st.checkbox("⭐ Favorito", value=row.get("Favorito", False), key=f"fav_{idx}")
            if favorito != row.get("Favorito", False):
                st.session_state.usuario_data["bd"].at[idx, "Favorito"] = favorito
                guardar_usuario_data()

            # 🚦 Estado
            estado = st.selectbox(
                "🚦 Estado del contacto",
                ["Nuevo", "Contactado", "No interesado", "En negociación", "Cerrado"],
                index=["Nuevo", "Contactado", "No interesado", "En negociación", "Cerrado"].index(row.get("Estado", "Nuevo")),
                key=f"estado_{idx}"
            )
            if estado != row.get("Estado", ""):
                st.session_state.usuario_data["bd"].at[idx, "Estado"] = estado
                guardar_usuario_data()

            # 📝 Nota
            nota = st.text_area("📝 Nota interna", value=row.get("Nota", ""), key=f"nota_{idx}")
            if nota != row.get("Nota", ""):
                st.session_state.usuario_data["bd"].at[idx, "Nota"] = nota
                guardar_usuario_data()

            # ➕ Añadir a lista
            listas_disponibles = list(st.session_state.usuario_data["listas"].keys()) + ["Crear nueva lista..."]
            lista_seleccionada = st.selectbox("📂 Seleccionar lista", listas_disponibles, key=f"lista_{idx}")

            if lista_seleccionada == "Crear nueva lista...":
                nueva_lista = st.text_input("Nombre de nueva lista", key=f"nueva_lista_{idx}")
                if nueva_lista:
                    st.session_state.usuario_data["listas"].setdefault(nueva_lista, [])
                    guardar_usuario_data()
                    st.success(f"Lista '{nueva_lista}' creada.")
                    st.rerun()

            if lista_seleccionada != "Crear nueva lista..." and st.button("➕ Añadir a lista", key=f"add_{idx}"):
                if row["Nombre completo"] not in st.session_state.usuario_data["listas"].get(lista_seleccionada, []):
                    st.session_state.usuario_data["listas"][lista_seleccionada].append(row["Nombre completo"])
                    guardar_usuario_data()
                    st.success(f"{row['Nombre completo']} añadido a {lista_seleccionada}")
                    st.rerun()
                else:
                    st.info("Este contacto ya está en esa lista.")

            # 🗑️ Borrar contacto
            if st.button(f"🗑️ Eliminar contacto {row['Nombre completo']}", key=f"del_{idx}"):
                nombre_contacto = row["Nombre completo"]
                st.session_state.usuario_data["bd"].drop(idx, inplace=True)

                for lista in st.session_state.usuario_data["listas"].keys():
                    if nombre_contacto in st.session_state.usuario_data["listas"][lista]:
                        st.session_state.usuario_data["listas"][lista].remove(nombre_contacto)

                guardar_usuario_data()
                st.rerun()

    guardar_usuario_data()

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
