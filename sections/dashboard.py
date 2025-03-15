import streamlit as st
from auth.decorators import require_auth

@require_auth
def show():
    st.title("Dashboard")
    st.write("Bienvenido al Dashboard.")