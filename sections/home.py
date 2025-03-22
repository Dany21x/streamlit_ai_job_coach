import streamlit as st
from auth.decorators import require_auth

@require_auth
def show():
    st.title("Bienvenido")
    
    # Preguntar estado de ánimo si no se ha registrado
    if "estado_animo" not in st.session_state:
        st.session_state["estado_animo"] = ""
    
    if not st.session_state["estado_animo"]:
        st.subheader("Antes de comenzar, ¿cómo te sientes hoy?")
        estados_animo = {
            "😊 Feliz": "¡Genial! Aprovecha esta energía para aprender algo nuevo.",
            "😐 Neutral": "Está bien sentirse neutral. ¿Qué tal explorar un nuevo curso?",
            "😔 Triste": "Si necesitas un descanso, tómatelo. Aprender puede ser un buen escape.",
            "😴 Cansado": "Quizás un café ayude ☕. Cuando estés listo, sigue aprendiendo.",
            "🤔 Curioso": "¡Perfecto! Hoy es un gran día para descubrir algo nuevo.",
            "😤 Estresado": "Respira profundo. Puedes aprender a tu propio ritmo, sin presiones."
        }
        
        seleccion = st.selectbox("Selecciona tu estado de ánimo:", list(estados_animo.keys()), key="animo_seleccionado")
        
        if st.button("Guardar Estado de Ánimo"):
            st.session_state["estado_animo"] = seleccion
            st.session_state["mensaje_animo"] = estados_animo[seleccion]
            st.rerun()
    else:
        st.success(f"Hoy te sientes: {st.session_state['estado_animo']}")
        st.write(st.session_state.get("mensaje_animo", "¡Que tengas un gran día de aprendizaje!"))
        
    st.markdown("---")
