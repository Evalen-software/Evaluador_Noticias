import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import joblib
from io import BytesIO
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns  # Importación de seaborn para gráficos

# BACK END

# Función para extraer información del artículo de El Plural
def get_article_info_elplural(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        header_div = soup.find('div', class_='article-header')
        title_tag = header_div.find('h1') if header_div else None
        title = title_tag.get_text(strip=True) if title_tag else "Título no encontrado"
    except AttributeError:
        title = "Título no encontrado"
    
    try:
        author_span = soup.find('span', class_='author')
        author_tag = author_span.find('a') if author_span else None
        author = author_tag.get_text(strip=True) if author_tag else "Autor no encontrado"
    except AttributeError:
        author = "Autor no encontrado"
    
    try:
        content_div = soup.find('div', class_='article-body')
        article_text = ""
        for p in content_div.find_all('p'):
            for a in p.find_all('a'):
                a.decompose()
            paragraph_text = p.get_text(strip=True)
            article_text += paragraph_text + " "
        article_text = article_text.strip()
    except AttributeError:
        article_text = "Contenido no encontrado"
    
    return {
        'url': url,
        'title': title,
        'author': author,
        'text': article_text
    }

# Función para extraer información del artículo de El Diario
def get_article_info_eldiario(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        title = soup.find('h1', class_='title').get_text(strip=True)
    except AttributeError:
        title = "Título no encontrado"
    
    try:
        author = soup.find('a', href=lambda x: x and 'autores' in x).get_text(strip=True)
    except AttributeError:
        author = "Autor no encontrado"
    
    try:
        article_paragraphs = soup.find_all('p', class_='article-text')
        article_text = " ".join([p.get_text(strip=True) for p in article_paragraphs])
    except AttributeError:
        article_text = "Texto no encontrado"
    
    return {
        'url': url,
        'title': title,
        'author': author,
        'text': article_text
    }

# Función principal para seleccionar el medio y realizar el scraping
def get_article_info(url):
    if "elplural.com" in url:
        return get_article_info_elplural(url)
    elif "eldiario.es" in url:
        return get_article_info_eldiario(url)
    else:
        return {
            'url': url,
            'title': "Medio no soportado",
            'author': "Medio no soportado",
            'text': "Medio no soportado"
        }

# CARGAR EL MODELO Y EL VECTORIZADOR
def load_model_and_vectorizer():
    # URL de los archivos en GitHub
    model_url = "https://raw.githubusercontent.com/Evalen-software/modelo/main/model.pkl"
    vectorizer_url = "https://raw.githubusercontent.com/Evalen-software/modelo/main/vectorize.pkl"
    
    # Descargar y cargar el modelo
    model_response = requests.get(model_url)
    model = joblib.load(BytesIO(model_response.content))
    
    # Descargar y cargar el vectorizador
    vectorizer_response = requests.get(vectorizer_url)
    vectorizer = joblib.load(BytesIO(vectorizer_response.content))
    
    return model, vectorizer

# FRONT END
def main():
    st.title("Análisis de Noticias")
    
    # Solicitar la URL del artículo
    url = st.text_input("Introduce la URL del artículo:")
    
    if st.button("Analizar"):
        if url:
            # Obtener información del artículo
            article_info = get_article_info(url)
            st.subheader("Información del Artículo")
            st.write(f"**Título:** {article_info['title']}")
            st.write(f"**Autor:** {article_info['author']}")
            st.write(f"**URL:** {article_info['url']}")
            st.write(f"**Contenido:** {article_info['text']}")
            
            # Cargar modelo y vectorizador
            model, vectorizer = load_model_and_vectorizer()
            
            # Vectorizar el texto del artículo
            X = vectorizer.transform([article_info['text']])
            
            # Realizar la predicción
            prediction = model.predict(X)
            result = "Verdadera" if prediction[0] == 0 else "Bulo"
            
            # Mostrar el resultado
            st.subheader("Resultado del Análisis")
            st.write(result)
            
            # Gráficos de palabras más frecuentes
            st.subheader("Gráficos de Palabras Más Frecuentes")
            wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(article_info['text'])
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
            
            # Conteo de palabras
            words = article_info['text'].lower().split()
            word_counts = pd.Series(words).value_counts().head(20)
            plt.figure(figsize=(10, 5))
            sns.barplot(x=word_counts.values, y=word_counts.index, palette='viridis')
            plt.title('Top 20 Palabras Más Frecuentes')
            st.pyplot(plt)
        else:
            st.error("Por favor, introduce una URL válida.")

if __name__ == "__main__":
    main()
