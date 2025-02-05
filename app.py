import streamlit as st
import fitz  # PyMuPDF
import pandas as pd

# Configurar la página
st.set_page_config(layout="wide", page_title="Curso Interactivo")
st.markdown("""
    <style>
        .progress-bar-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
            background-color: #000000;
            z-index: 1000;
            display: flex;
            align-items: center;
        }

        .progress-bar {
            height: 100%;
            background-color: #676767;
            transition: width 0.3s ease-in-out;
            flex-grow: 1;
        }

        .progress-text {
            margin-left: 20px;
            font-size: 16px;
            color: #FFFFFF;
        }

        .content {
            padding-top: 20px;
            padding: 10px;
        }

        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px;
        }

        .progress-container {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            position: relative;
        }

        .progress-text {
            position: absolute;
            top: -20px;
            right: 0;
            font-weight: bold;
        }

        .question-text {
            font-size: 22px;
            font-weight: bold;
        }

        /* Estilos para los botones de navegación */
        .stButton>button {
            border: 2px solid #ccc !important; /* Borde predeterminado */
            background-color: black !important; /* Fondo negro */
            color: white !important;
            transition: all 0.3s ease-in-out;
        }

        .stButton>button:hover {
            border: 2px solid #587bff !important; /* Cambia el borde al pasar el mouse */
            color: #587bff !important; /* Cambia el texto al pasar el mouse */
            background-color: black !important; /* Mantiene el fondo negro */
        }

        /* Estilos para los botones de selección */
        div[data-baseweb="radio"] label {
            color: white !important;
        }

        div[data-baseweb="radio"] input:checked + div {
            background-color: #587bff !important;
            color: white !important;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de la sesión
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "page" not in st.session_state:
    st.session_state.page = 0
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = {}
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "can_proceed" not in st.session_state:
    st.session_state.can_proceed = True

# Cargar el PDF
pdf_path = "curso.pdf"
doc = fitz.open(pdf_path)
total_pages = len(doc)

# Diccionario con preguntas asignadas a páginas específicas
preguntas_por_pagina = {
    2: {"pregunta": "¿Cuál es la velocidad de la luz?", "opciones": ["300 km/s", "300,000 km/s", "150,000 km/s", "3,000 km/s"], "correcta": "300,000 km/s"},
    5: {"pregunta": "¿Quién formuló la teoría de la relatividad?", "opciones": ["Newton", "Galileo", "Einstein", "Bohr"], "correcta": "Einstein"},
    7: {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "opciones": ["Marte", "Tierra", "Júpiter", "Saturno"], "correcta": "Júpiter"},
}

# Mostrar contenido
if st.session_state.page >= total_pages:
    st.markdown("<p style='text-align:center; font-size:30px; font-weight:bold; color:white; background-color:#587bff; padding:20px; border-radius:10px;'>¡Gracias por tu tiempo!</p>", unsafe_allow_html=True)
    if st.button("← Anterior"):
        st.session_state.page -= 1
        st.rerun()
else:
    col1, col2 = st.columns([3, 0.6])
    with col1:
        st.image("logo.png", width=150)
    with col2:
        progress = (st.session_state.page + 1) / total_pages * 100
        st.markdown(f'<div class="progress-container"><span class="progress-text">{progress:.0f}%</span></div>', unsafe_allow_html=True)
        st.progress(progress / 100)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        img = doc[st.session_state.page].get_pixmap()
        st.image(img.tobytes(), use_container_width=True)
    with col2:
        if st.session_state.page in preguntas_por_pagina:
            pregunta_data = preguntas_por_pagina[st.session_state.page]
            question = pregunta_data["pregunta"]
            options = pregunta_data["opciones"]
            correct_answer = pregunta_data["correcta"]
            
            st.markdown(f'<p style="font-size:22px; font-weight:bold;">{question}</p>', unsafe_allow_html=True)
            
            user_answer = st.radio("Selecciona una opción:", options, key=f"q_{st.session_state.page}")
            
            if "answered_questions" not in st.session_state:
                st.session_state.answered_questions = {}
            
            if st.button("Enviar respuesta"):
                if user_answer:
                    if user_answer == correct_answer:
                        st.session_state.answered_questions[st.session_state.page] = True
                        st.session_state.can_proceed = True
                        st.success("¡Correcto! Puedes continuar.")
                    else:
                        st.session_state.can_proceed = False
                        st.error("Respuesta incorrecta. Intenta de nuevo.")
                else:
                    st.session_state.can_proceed = False
                    st.warning("Debes seleccionar una opción antes de continuar.")
    
    # Botones de navegación debajo de la imagen
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Anterior") and st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()
    with col2:
        if st.session_state.page == total_pages - 1:
            if st.button("Finalizar"):
                st.session_state.page += 1
                st.rerun()
        elif st.session_state.page not in preguntas_por_pagina or st.session_state.answered_questions.get(st.session_state.page, False):
            if st.button("Siguiente →"):
                st.session_state.page += 1
                st.rerun()

