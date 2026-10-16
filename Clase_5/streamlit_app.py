import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from logica import crear_saludo


st.title("Creador de saludos")
st.write("Escribí un nombre y elegí el estilo del saludo.")

nombre = st.text_input("Nombre", placeholder="Por ejemplo: Alex")
estilo = st.selectbox("Estilo del saludo", ["Informal", "Formal"])

if st.button("Crear saludo"):
    st.write(crear_saludo(nombre, estilo))
