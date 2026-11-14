import streamlit as st

from logica import clasificar_local


st.title("Análisis de sentimiento · pipeline local")
st.write(
    "El modelo se descarga y se ejecuta en esta computadora. "
    "Está preparado para texto en inglés."
)
texto = st.text_input("Frase", placeholder="I love this product")

if st.button("Analizar"):
    try:
        etiqueta, puntaje = clasificar_local(texto)
    except ValueError as error:
        st.error(str(error))
    else:
        st.metric("Etiqueta", etiqueta)
        st.metric("Puntaje del modelo", f"{puntaje:.1%}")
