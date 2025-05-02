import streamlit as st
import pandas as pd
import os
import json

def mostrar():
    if "usuario_data" not in st.session_state:
        st.session_state.usuario_data = {"bd": pd.DataFrame(), "listas": {}, "uploads": []}
        
    st.title("🧑‍💼 Contactos")

    if "usuario_data" not in st.session_state or st.session_state.usuario_data["bd"].empty:
        st.info("No tienes contactos todavía. ¡Sube un archivo CSV primero!")
        return

    bd = st.session_state.usuario_data["bd"]

    # Filtro por listas
    lista_filtro = st.sidebar.selectbox("📋 Filtrar por lista", ["Todas"] + list(st.session_state.usuario_data["listas"].keys()))

    # Buscador de contactos
    buscar_nombre = st.sidebar.text_input("🔎 Buscar por nombre")

    # Aplicar filtros
    if lista_filtro != "Todas":
        contactos_lista = st.session_state.usuario_data["listas"].get(lista_filtro, [])
        bd = bd[bd["Nombre completo"].isin(contactos_lista)]

    if buscar_nombre:
        bd = bd[bd["Nombre completo"].str.contains(buscar_nombre, case=False, na=False)]

    # Mostrar contactos
    if bd.empty:
        st.info("No hay contactos que coincidan con los filtros.")
    else:
        for idx, row in bd.iterrows():
            with st.expander(f"{row['Nombre completo']} — {row['Cargo']} ({row['Empresa']})"):
                st.markdown(row["LinkedIn"], unsafe_allow_html=True)
                st.caption(row["Comentario"] if row["Comentario"] else "Sin comentario")

                # Asignar favorito
                favorito = st.checkbox("⭐ Favorito", value=row.get("Favorito", False), key=f"fav_{idx}")
                st.session_state.usuario_data["bd"].at[idx, "Favorito"] = favorito

                # Asignar estado
                estado = st.selectbox(
                    "🚦 Estado del contacto",
                    ["Nuevo", "Contactado", "No interesado", "En negociación", "Cerrado"],
                    index=["Nuevo", "Contactado", "No interesado", "En negociación", "Cerrado"].index(row.get("Estado", "Nuevo")) if row.get("Estado") else 0,
                    key=f"estado_{idx}"
                )
                st.session_state.usuario_data["bd"].at[idx, "Estado"] = estado

                # Nota interna
                nota = st.text_area("🗒️ Nota interna", value=row.get("Nota", ""), key=f"nota_{idx}")
                st.session_state.usuario_data["bd"].at[idx, "Nota"] = nota

                # Añadir a lista
listas_disponibles = list(st.session_state.usuario_data["listas"].keys()) + ["Crear nueva lista..."]
lista_seleccionada = st.selectbox("➕ Seleccionar lista", listas_disponibles, key=f"lista_{idx}")

# Crear nueva lista si se selecciona esa opción
if lista_seleccionada == "Crear nueva lista...":
    nueva_lista = st.text_input("Nombre de nueva lista", key=f"nueva_lista_{idx}")
    if nueva_lista:
        st.session_state.usuario_data["listas"].setdefault(nueva_lista, [])
        guardar_usuario_data()
        st.success(f"Lista '{nueva_lista}' creada.")
        st.rerun()

# Botón para añadir contacto a lista
if lista_seleccionada != "Crear nueva lista..." and st.button("➕ Añadir a lista", key=f"add_{idx}"):
    if row["Nombre completo"] not in st.session_state.usuario_data["listas"].get(lista_seleccionada, []):
        st.session_state.usuario_data["listas"][lista_seleccionada].append(row["Nombre completo"])
        guardar_usuario_data()
        st.success(f"{row['Nombre completo']} añadido a la lista {lista_seleccionada}")
        st.rerun()
    else:
        st.info("Este contacto ya está en esa lista.")


                # Borrar contacto
                if st.button(f"🗑️ Eliminar contacto {row['Nombre completo']}", key=f"del_{idx}"):
                    nombre_contacto = row["Nombre completo"]
                    st.session_state.usuario_data["bd"].drop(idx, inplace=True)

                    # También quitar de todas las listas
                    for lista in st.session_state.usuario_data["listas"].keys():
                        if nombre_contacto in st.session_state.usuario_data["listas"][lista]:
                            st.session_state.usuario_data["listas"][lista].remove(nombre_contacto)

                    guardar_usuario_data()
                    st.rerun()

        guardar_usuario_data()

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

