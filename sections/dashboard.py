import streamlit as st
from auth.decorators import require_auth
import os

powerbi_url = os.getenv("POWER_BI_URL")

@require_auth
def show():
    st.title("Dashboard")
    st.write("¡Mira el progreso de tu equipo!")
    # URL pública del informe de Power BI
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiY2U5M2E5NzMtY2Y3Zi00YzY2LTg1MWQtYjY4NjY5ZDY2ZjY2IiwidCI6IjY2NjY2NjY2LTY2NjYtNGY2Ni1hNjY2LTY2NjY2NjY2NjY2NiJ9"

    # Mostrar el informe en Streamlit
    st.components.v1.iframe(powerbi_url, width=800, height=600)