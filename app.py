import streamlit as st

# ✅ Importar las páginas desde la carpeta "pages"
from pages import inicio, contactos, listas, subidas, dashboard, ajustes, cerrar_sesion

st.set_page_config(page_title="CRM Leads Delectatech", layout="wide")

# ✅ Iniciar sesión del usuario
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ✅ Login por email
if not st.session_state.usuario:
    st.title("🔒 CRM Leads Delectatech - Login")
    email = st.text_input("Introduce tu correo electrónico")
    if st.button("Entrar"):
        if email.strip():
            st.session_state.usuario = email.strip().lower()
            st.success(f"✅ Bienvenido, {st.session_state.usuario}")
            st.rerun()
        else:
            st.warning("⚠️ Debes introducir un correo válido.")
else:
    # ✅ Menú de navegación manual
    with st.sidebar:
        st.header("🧭 Navegación")
        pagina = st.selectbox(
            "Selecciona una sección:",
            [
                "🏠 Inicio",
                "🧑‍💼 Contactos",
                "📚 Mis listas",
                "📂 Subidas",
                "📊 Dashboard",
                "⚙️ Ajustes",
                "🔚 Cerrar sesión",
            ]
        )

    # ✅ Cargar la página correspondiente
    if pagina == "🏠 Inicio":
        inicio.mostrar()
    elif pagina == "🧑‍💼 Contactos":
        contactos.mostrar()
    elif pagina == "📚 Mis listas":
        listas.mostrar()
    elif pagina == "📂 Subidas":
        subidas.mostrar()
    elif pagina == "📊 Dashboard":
        dashboard.mostrar()
    elif pagina == "⚙️ Ajustes":
        ajustes.mostrar()
    elif pagina == "🔚 Cerrar sesión":
        cerrar_sesion.mostrar()
