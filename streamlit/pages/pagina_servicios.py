import streamlit as st
import datetime
import numpy as np
from funciones import lista_festivos, predecir_servicios, df_serv, cargar_css
from streamlit_extras.switch_page_button import switch_page

# Aplicamos el CSS personalizado y el fondo
cargar_css('style/styles.css')

st.title("Predicción para Sector Servicios")
fecha = st.date_input("Selecciona una fecha:", datetime.date(2024, 5, 1))
dia_semana = fecha.weekday()
findesemana = 1 if dia_semana >= 5 else 0
festivos = 1 if fecha in lista_festivos else 0
tmed = st.number_input("Temperatura media", min_value=0, value=21)
t_1 = df_serv['consumo'].iloc[-1]
pernoctaciones=743000
poblacion=5884873
#Agrupar los datos
datos_usuario_ser = np.array([findesemana, festivos, pernoctaciones, tmed, poblacion, t_1])
datos_anteriro_ser = df_serv.iloc[-1][['findesemana', 'festivos', 'pernoctaciones', 'tmed', 'poblacion', 't-1']].values
# Combinar los datos anteriores y los proporcionados en un solo array
datos_ser = np.vstack([datos_anteriro_ser, datos_usuario_ser])

if st.button("Predecir Consumo"):
    pred = predecir_servicios(datos_ser)
    st.success(f"Consumo previsto: {pred[0, 0]:.2f} MWh")

if st.button('Predecir otro Sector'):
    switch_page('pagina_principal')