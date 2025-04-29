import streamlit as st

# Importar tus módulos personalizados (de la carpeta /pages/)
from pages import inicio, contactos, listas, subidas, dashboard, ajustes, cerrar_sesion

st.set_page_config(page_title="CRM Leads Delectatech", layout="wide")

# Inicializar estado de usuario
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# LOGIN
if not st.session_state.usuario:
    st.title("🔒 CRM Leads Delectatech - Login")
    email = st.text_input("Introduce tu correo electrónico")
    if st.button("Entrar"):
        if email.strip():
            st.session_state.usuario = email.strip().lower()
            st.success(f"✅ Bienvenido, {st.session_state.usuario}")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Debes introducir un correo válido.")
else:
    # Menú lateral de navegación
    with st.sidebar:
        st.header("🧭 Navegación")
        pagina = st.selectbox(
            "Ir a la sección:",
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

    # Ruteo entre secciones
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
