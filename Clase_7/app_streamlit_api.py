import streamlit as st

from logica import clasificar_api


st.title("Análisis de sentimiento · Inference API")
st.write(
    "La interfaz corre en esta computadora y Hugging Face procesa la frase. "
    "Está preparado para texto en inglés."
)
texto = st.text_input("Frase", placeholder="I love this product")

if st.button("Analizar"):
    try:
        etiqueta, puntaje = clasificar_api(texto)
    except ValueError as error:
        st.error(str(error))
    else:
        st.metric("Etiqueta", etiqueta)
        st.metric("Puntaje del modelo", f"{puntaje:.1%}")
