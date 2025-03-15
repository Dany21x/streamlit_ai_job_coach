import streamlit as st
from functools import wraps

def require_auth(func):
    """Decorador para proteger páginas que requieren autenticación."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authenticated", False):
            st.warning("Debes iniciar sesión para acceder a esta página.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
