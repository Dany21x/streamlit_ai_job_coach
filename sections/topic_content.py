import requests
import streamlit as st
from auth.decorators import require_auth
import sections

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
        item_id = item.get("itemID", "")
        if st.button(item_name, key=f"topic_{item_id}"):
            st.session_state["current_section"] = 'chat'
            st.session_state["selected_item_id"] = topic_id
            st.session_state["item_name"] = item_name
            print(f'current_section changed 3: {st.session_state['current_section']}, {item_name}')
            st.rerun()

# Si el usuario ha seleccionado una sección, mostrarla
if st.session_state.get("current_section"):
    print(f'current_section changed 4: {st.session_state["current_section"]}')

    section_to_load = getattr(sections, st.session_state["current_section"], None)
    #st.session_state["current_section"] = None
    if section_to_load:
        section_to_load.show()