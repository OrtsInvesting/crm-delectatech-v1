import streamlit as st

# Importamos todas las páginas
from pages import inicio, contactos, listas, subidas, dashboard, ajustes, cerrar_sesion

st.set_page_config(page_title="CRM Leads Delectatech", layout="wide")

# Inicializamos el estado del usuario si no existe
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# Login simple (email)
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
    # Menú de navegación
    pagina = st.sidebar.selectbox(
        "🧭 Navegación",
        ["🏠 Inicio", "🧑‍💼 Contactos", "📚 Mis listas", "📂 Subidas", "📊 Dashboard", "⚙️ Ajustes", "🔚 Cerrar sesión"]
    )

    # Ruteo a la página correspondiente
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
