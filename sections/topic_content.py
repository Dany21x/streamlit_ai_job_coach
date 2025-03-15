import requests
import streamlit as st
from auth.decorators import require_auth

@require_auth
def show():
    st.title("Contenido del Tema")

    topic_id = st.session_state.get("selected_topic_id")
    items = st.session_state.get("selected_topic_items", [])

    if not topic_id or not items:
        st.warning("No hay ítems para mostrar.")
        return

    st.markdown("### ¿Cuál tema deseas estudiar?:")
    for item in items:
        item_name = item.get("itemName", "Sin nombre")
        st.markdown(f"- {item_name}")