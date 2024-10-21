#Pagina industrial
import streamlit as st
import datetime
import numpy as np
from funciones import lista_festivos, predecir_industrial, df_ind, cargar_css
from streamlit_extras.switch_page_button import switch_page
import os


#Directorio actual
base_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(base_dir)
# Cargar DataFrames
cargar_css(os.path.join(parent_dir, 'style', 'styles.css'))

st.title("Predicción para Sector Industrial")
fecha = st.date_input("Selecciona una fecha:", datetime.date(2024, 5, 1))
dia_semana = fecha.weekday()
findesemana = 1 if dia_semana >= 5 else 0
festivos = 1 if fecha in lista_festivos else 0
tmed = st.number_input("Temperatura media", min_value=0, value=21)
t_1 = df_ind['consumo'].iloc[-1]
COVID=0
#Agrupar datos
datos_usuario_ind = np.array([[findesemana, festivos, COVID, tmed, t_1]])
datos_anterior_ind = df_ind.iloc[-1][['findesemana', 'festivos', 'COVID', 'tmed', 't-1']].values
# Combinar los datos anteriores y los proporcionados en un solo array
datos_ind = np.vstack([datos_anterior_ind, datos_usuario_ind])

if st.button("Predecir Consumo"):
    pred = predecir_industrial(datos_ind)
    st.success(f"Consumo previsto: {pred[0, 0]:.2f} MWh")

if st.button('Predecir otro sector'):
    switch_page('pagina_principal')
