import streamlit as st
import time

# Configuración de la página (logo en pestaña y título)
st.set_page_config(page_title="Buscador de Fake News", page_icon="logo.png", layout="wide")

# Definir el estilo para el menú lateral con botones personalizados
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .button {
        display: block;
        width: 100%;
        background-color: #e0e0e0;
        color: black;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        border: 2px solid #B61421;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        text-decoration: none;
    }
    .button:hover {
        background-color: #B61421;
        color: white;
    }
    .button-selected {
        background-color: #B61421 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializamos la variable de la página
if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'

# Crear un menú de navegación en la barra lateral con botones
st.sidebar.markdown(f'<a href="?page=Inicio" class="button {"button-selected" if st.session_state.page == "Inicio" else ""}">Inicio</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a href="?page=Resultados" class="button {"button-selected" if st.session_state.page == "Resultados" else ""}">Resultados</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a href="?page=Noticias Parecidas" class="button {"button-selected" if st.session_state.page == "Noticias Parecidas" else ""}">Noticias Parecidas</a>', unsafe_allow_html=True)

# Actualizar la página seleccionada usando st.query_params (sin paréntesis)
query_params = st.query_params
if query_params.get('page'):
    st.session_state.page = query_params.get('page')[0]

# Mostrar el contenido de la página seleccionada
st.image("infocomun.png", width=400)  # Imagen del título más grande

if st.session_state.page == 'Inicio':
    st.title('Buscador de Fake News')

    # Descripción de la app
    st.markdown('''Esta aplicación te ayuda a identificar si una noticia es potencialmente falsa. 
    Introduce la URL de la noticia y obtendrás un análisis de la probabilidad de que sea fake news.''')

    # Input para la URL de la noticia
    url = st.text_input('Introduce la URL de la noticia')

    # Botón para iniciar el análisis
    if st.button('Analizar'):
        if url:  # Verifica si se introdujo una URL
            st.write('Analizando la noticia...')

            # Simulación de una barra de progreso
            progress_bar = st.progress(0)
            for percent_complete in range(0, 31):
                time.sleep(0.05)  # Simula el tiempo de procesamiento
                progress_bar.progress(percent_complete)

            # Resultado
            st.success('Análisis completado: 30% de probabilidad de ser Fake News')
        else:
            st.warning('Por favor, introduce una URL válida')

elif st.session_state.page == 'Resultados':
    st.title("Resultados")
    st.write("Aquí se mostrarán los resultados del análisis...")

elif st.session_state.page == 'Noticias Parecidas':
    st.title("Noticias Parecidas")
    st.write("Aquí se mostrarán noticias similares a la introducida...")
