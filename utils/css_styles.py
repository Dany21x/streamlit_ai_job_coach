# Estilo global para toda la aplicación basado en colores del logo de MentorIA+
# Con mejoras de contraste y estilo moderno tecnológico
global_style = """
<style>
    /* Variables de color - Paleta moderna y tecnológica */
    :root {
        --primary: #6200EA;          /* Morado más vibrante */
        --primary-light: #9D46FF;    /* Morado más claro */
        --primary-dark: #3700B3;     /* Morado más oscuro */
        --secondary: #DEDEDE;        /* Gris oscuro para textos */
        --accent: #00E5FF;           /* Acento cian */
        --accent-secondary: #00B8D4; /* Acento cian secundario */
        --background: #F8F9FA;       /* Fondo ligeramente grisáceo */
        --card-bg: #FFFFFF;          /* Fondo de tarjetas */
        --text: #DEDEDE;             /* Texto principal - casi negro para mejor contraste */
        --text-secondary: #DEDEDE;   /* Texto secundario - gris oscuro */
        --success: #00C853;          /* Verde éxito */
        --info: #0091EA;             /* Azul información */
        --warning: #FFD600;          /* Amarillo advertencia */
        --error: #D50000;            /* Rojo error */
        --white: #FFFFFF;
        --white-light: #D1B3FF;
    }

    /* Estilos globales */
    .main .block-container {
        background-color: var(--background);
        padding-top: 2rem;
        padding-bottom: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Estilo de encabezados - Mejora de contraste */
    h1 {
        color: var(--white) !important;
        font-weight: 700 !important;
        margin-bottom: 1rem;
    }

    h2, h3 {
        color: var(--white-light) !important;
        font-weight: 600 !important;
    }

    /* Estilo para texto regular con mejor contraste */
    p, div, span, label {
        color: var(--text);
        font-weight: 400;
    }

    /* Estilo para la barra lateral con degradado */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p {
        color: white !important;
        font-weight: 500;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }

    /* Estilo para botones con degradado */
    [data-testid="stButton"] > button {
        background: linear-gradient(to right, var(--primary), var(--primary-light));
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        transition: all 0.3s ease;
        font-weight: 500;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stButton"] > button:hover {
        background: linear-gradient(to right, var(--primary-light), var(--primary));
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }

    /* Estilo para selectbox y otros inputs */
    [data-testid="stSelectbox"], [data-testid="stTextInput"] > div {
        border-radius: 8px;
    }

    /* Estilo para inputs de texto */
    [data-testid="stTextInput"] > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 0.2rem rgba(98, 0, 234, 0.25);
    }

    /* Estilo para selectbox cuando está activo */
    [data-testid="stSelectbox"] > div[data-baseweb="select"] > div:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 0.2rem rgba(98, 0, 234, 0.25) !important;
    }

    /* Estilo para area de texto */
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 0.2rem rgba(98, 0, 234, 0.25);
    }

    /* Tarjetas de curso con estilo moderno y tecnológico */
    .course-card {
        background: linear-gradient(145deg, var(--card-bg) 0%, #F5F5F5 100%);
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border-left: 5px solid var(--primary);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .course-card::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 25%;
        height: 5px;
        background: linear-gradient(to right, transparent, var(--accent));
    }

    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .course-title {
        color: var(--primary-dark);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .course-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Estilizar divisores */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, var(--primary-light), transparent);
        opacity: 0.5;
        margin: 1.5rem 0;
    }

    /* Estilos para las burbujas de chat - Mejorado para contraste */
    [data-testid="stChatMessage"] {
        background-color: var(--card-bg);
        border-radius: 14px;
        padding: 12px 16px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* Personalización de las burbujas de chat */
    [data-testid="stChatMessage"][data-testid="user-message"] {
        background: linear-gradient(to right, #EFEFEF, #F5F5F5);
        border-bottom-right-radius: 4px;
        color: var(--text);
    }

    [data-testid="stChatMessage"][data-testid="assistant-message"] {
        background: linear-gradient(to right, #E8EAFD, #E0E4FF);
        border-bottom-left-radius: 4px;
        color: var(--text);
    }

    /* Estilo para el chat input */
    [data-testid="stChatInput"] {
        border-radius: 20px;
        border: 1px solid #E0E0E0;
        padding: 10px 16px;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 0.2rem rgba(98, 0, 234, 0.25);
    }

    /* Estilo para alertas y notificaciones */
    [data-testid="stAlert"] {
        border-radius: 10px;
        border-left-width: 8px;
    }

    /* Estilos de audio */
    [data-testid="stAudio"] {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Estilo para file uploader */
    [data-testid="stFileUploader"] {
        border-radius: 10px;
        border: 2px dashed var(--primary-light);
        padding: 22px;
        background-color: rgba(98, 0, 234, 0.03);
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        background-color: rgba(98, 0, 234, 0.05);
        border-color: var(--primary);
    }

    /* Estilo para el toggle */
    [data-testid="baseButton-secondary"] {
        background: linear-gradient(to right, var(--accent), var(--accent-secondary)) !important;
    }
</style>
"""

# Estilo de alto contraste mejorado para accesibilidad siguiendo WCAG
high_contrast_style = """
<style>
    /* Estilos para alto contraste - WCAG 2.1 AA compliance */
    body {
        background-color: #0D0D0D; /* Fondo casi negro */
    }

    .main .block-container {
        background-color: #0D0D0D;
        border: 2px solid #4D4D4D; /* Borde gris medio para definir elementos */
        box-shadow: 0 0 0 1px #FFFFFF;
    }

    h1 {
        color: #FFFFFF !important; /* Blanco puro para máximo contraste */
        font-weight: 700 !important;
        border-bottom: 2px solid #FFFF00; /* Amarillo para separaciones */
        padding-bottom: 5px;
    }

    h2, h3 {
        color: #FFFF00 !important; /* Amarillo para encabezados secundarios - ratio de contraste >7:1 */
        font-weight: 700 !important;
    }

    p, div, span, label {
        color: #FFFFFF !important; /* Blanco puro para texto - ratio de contraste >7:1 */
        font-weight: 500;
    }

    /* Barra lateral con color sólido */
    [data-testid="stSidebar"] {
        background: #0D0D0D; /* Negro sólido */
        border-right: 2px solid #FFFF00; /* Amarillo para definir bordes */
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* Botones en color plano con alto contraste */
    [data-testid="stButton"] > button {
        background: #FFFF00; /* Amarillo sólido - WCAG AAA con fondo negro */
        color: #000000 !important; /* Texto negro para contraste con fondo amarillo */
        border: 2px solid #FFFFFF; /* Borde blanco para definir */
        font-weight: 700; /* Negrita para mejorar legibilidad */
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
        box-shadow: none; /* Sin sombras que reduzcan contraste */
    }

    [data-testid="stButton"] > button:hover {
        background: #FFFFFF; /* Blanco al hacer hover */
        color: #000000 !important;
        border: 2px solid #FFFF00;
        transform: scale(1.05);
    }

    /* Tarjetas con contraste mejorado */
    .course-card {
        background-color: #1A1A1A; /* Gris muy oscuro */
        border: 2px solid #FFFF00; /* Amarillo para borde */
        border-left: 8px solid #FFFF00;
        box-shadow: 0 0 0 1px #FFFFFF; /* Sombra blanca para definir */
    }

    .course-card::after {
        content: none; /* Eliminamos el degradado */
    }

    .course-card:hover {
        background-color: #2A2A2A; /* Más claro al hacer hover */
        transform: translateY(-5px);
    }

    .course-title {
        color: #FFFF00 !important; /* Amarillo para títulos - alto contraste */
        font-size: 1.3rem;
        font-weight: 700;
    }

    .course-description {
        color: #FFFFFF !important; /* Blanco para descripciones */
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Burbujas de chat con alto contraste */
    [data-testid="stChatMessage"] {
        background-color: #1A1A1A;
        border: 2px solid #4D4D4D;
        box-shadow: none;
    }

    [data-testid="stChatMessage"][data-testid="user-message"] {
        background-color: #2A2A2A; /* Gris oscuro sólido */
        border-left: 8px solid #FFFF00; /* Amarillo para identificar */
    }

    [data-testid="stChatMessage"][data-testid="assistant-message"] {
        background-color: #1A1A1A; /* Más oscuro para asistente */
        border-left: 8px solid #FFFFFF; /* Blanco para identificar */
    }

    [data-testid="stChatInput"] {
        background-color: #2A2A2A;
        border: 2px solid #FFFFFF;
        color: white !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #FFFF00;
        box-shadow: 0 0 0 2px #FFFF00;
    }

    /* File uploader con alto contraste */
    [data-testid="stFileUploader"] {
        border: 2px dashed #FFFF00;
        background-color: #1A1A1A;
    }

    [data-testid="stFileUploader"]:hover {
        background-color: #2A2A2A;
        border: 2px dashed #FFFFFF;
    }

    /* Alertas y notificaciones */
    [data-testid="stAlert"] {
        background-color: #1A1A1A;
        border-left: 8px solid #FFFF00;
        color: #FFFFFF !important;
    }

    /* Divisores sólidos */
    hr {
        background: #FFFF00;
        height: 2px;
        opacity: 1;
    }

    /* Selectbox con alto contraste */
    [data-testid="stSelectbox"] > div[data-baseweb="select"] {
        background-color: #1A1A1A;
        border: 2px solid #FFFFFF;
    }

    [data-testid="stSelectbox"] > div[data-baseweb="select"] > div:focus {
        border-color: #FFFF00 !important;
        box-shadow: 0 0 0 2px #FFFF00 !important;
    }

    /* Inputs de texto con alto contraste */
    [data-testid="stTextInput"] > div {
        background-color: #1A1A1A;
        border: 2px solid #FFFFFF;
    }

    [data-testid="stTextInput"] > div:focus-within {
        border-color: #FFFF00;
        box-shadow: 0 0 0 2px #FFFF00;
    }

    /* Area de texto con alto contraste */
    [data-testid="stTextArea"] textarea {
        background-color: #1A1A1A;
        border: 2px solid #FFFFFF;
        color: #FFFFFF !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: #FFFF00;
        box-shadow: 0 0 0 2px #FFFF00;
    }

    /* Elementos de formulario */
    [data-testid="stForm"] {
        border: 2px solid #4D4D4D;
        background-color: #1A1A1A;
        padding: 10px;
    }

    /* Toggle con alto contraste */
    [data-testid="baseButton-secondary"] {
        background-color: #FFFF00 !important;
        color: #000000 !important;
    }
</style>
"""

# El estilo de las tarjetas de curso actualizado
course_card = """
<style>
    .course-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F5F5F5 100%);
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border-left: 5px solid #6200EA;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .course-card::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 25%;
        height: 5px;
        background: linear-gradient(to right, transparent, #00E5FF);
    }

    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .course-title {
        color: #3700B3;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .course-description {
        color: #424242;
        font-size: 0.95rem;
        line-height: 1.5;
    }
</style>
"""


# Función para cargar todos los estilos
def load_all_styles():
    """
    Carga todos los estilos CSS para la aplicación.
    Esta función debe llamarse al inicio de la aplicación.
    """
    import streamlit as st
    st.markdown(global_style, unsafe_allow_html=True)


# Función para aplicar modo de alto contraste
def toggle_contrast_mode(is_high_contrast=False):
    """
    Cambia entre modo normal y alto contraste.

    Args:
        is_high_contrast (bool): True para activar el modo de alto contraste,
                                False para desactivarlo.
    """
    import streamlit as st
    if is_high_contrast:
        st.markdown(high_contrast_style, unsafe_allow_html=True)
    else:
        st.markdown(global_style, unsafe_allow_html=True)


# Función para aplicar solo el estilo de las tarjetas de curso
def apply_course_card_style():
    """
    Aplica solo el estilo de las tarjetas de curso.
    Útil si solo necesitas ese componente específico.
    """
    import streamlit as st
    st.markdown(course_card, unsafe_allow_html=True)


# Función para estilos locales que ya estás usando
def local_css():
    """
    Función de compatibilidad con el código existente.
    """
    import streamlit as st
    st.markdown(course_card, unsafe_allow_html=True)