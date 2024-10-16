import streamlit as st
import time

# Título de la app
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