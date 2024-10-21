import streamlit as st
import numpy as np
from funciones import cargar_css
from streamlit_extras.switch_page_button import switch_page

# Aplicamos el CSS personalizado y el fondo
cargar_css('style/styles.css')

st.title("AMH Solutions")
st.text("Binvenido a la plataforma de preddicion de consumo de Barcelona")

# Centramos las opciones usando columnas
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("Selecciona el sector que desea predecir:")
    
    # Selector de radio para elegir sector
    sector = st.radio(
        "Elige un sector para continuar:",
        ('Industrial', 'Residencial', 'Servicios'),
        index=0
    )

    # Botón de aceptar
    if st.button("Aceptar"):

        if sector == "Industrial":
            switch_page('pagina_industrial')
        elif sector == "Residencial":
            switch_page('pagina_residencial')
        elif sector == "Servicios":
            switch_page('pagina_servicios')
        else:
            switch_page('pagina_principal')

