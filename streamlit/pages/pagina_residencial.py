import streamlit as st
import datetime
import numpy as np
from funciones import predecir_residencial, df_res, cargar_css
from streamlit_extras.switch_page_button import switch_page

# Aplicamos el CSS personalizado y el fondo
cargar_css('style/styles.css')

st.title("Predicción para Sector Residencial")
fecha = st.date_input("Selecciona una fecha:", datetime.date(2024, 5, 1))
dia_semana = fecha.weekday()
findesemana = 1 if dia_semana >= 5 else 0
tmed = st.number_input("Temperatura media", min_value=0, value=21)
t_1 = df_res['consumo'].iloc[-1]
PIB=77268
datos_usuario_res = np.array([[findesemana, tmed, PIB, t_1]])

if st.button("Predecir Consumo"):
    pred = predecir_residencial(datos_usuario_res)
    st.success(f"Consumo previsto: {pred[0, 0]:.2f} MWh")

if st.button('Predecir otro sector'):
    switch_page('pagina_principal')