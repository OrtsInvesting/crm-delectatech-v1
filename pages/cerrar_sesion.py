import streamlit as st

def mostrar():
    st.title("🔚 Cerrar sesión")

    st.success("👋 Has cerrado sesión correctamente.")
    
    # Limpiar todo el session_state
    st.session_state.clear()

    # Rerun para volver a login
    st.experimental_rerun()

