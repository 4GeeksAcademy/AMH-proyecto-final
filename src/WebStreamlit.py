##Streamlit para la web de interaccion con el usuario 
#el comando para realizar la peticion de url de la we:
#streamlit run WebStreamlit.py
#libreria pickle
import streamlit as st
from tensorflow.keras.models import load_model
import pickle
import datetime
import pandas as pd
import numpy as np

#Importo df
df_ind = pd.read_csv('../data/DF_modelos/df_industrial_total.csv')
df_res = pd.read_csv('../data/DF_modelos/df_residencial_total.csv')
df_serv = pd.read_csv('../data/DF_modelos/df_servicios_total.csv')

#Importamos modelo
modelInd = load_model('../models/modelo_industrial_def.h5')
modelRes = load_model('../models/modelo_residencial_def.h5')
modelSer = load_model('../models/modelo_servicios_def.h5')

#Importamos escalas
with open('../data/scalers/scaler_X_ind.pkl', 'rb') as f:
    scaler_X_ind = pickle.load(f)
with open('../data/scalers/scaler_y_ind.pkl', 'rb') as f:
    scaler_y_ind = pickle.load(f)
with open('../data/scalers/scaler_X_res.pkl', 'rb') as f:
    scaler_X_res = pickle.load(f)
with open('../data/scalers/scaler_y_res.pkl', 'rb') as f:
    scaler_y_res = pickle.load(f)
with open('../data/scalers/scaler_X_serv.pkl', 'rb') as f:
    scaler_X_serv = pickle.load(f)
with open('../data/scalers/scaler_y_serv.pkl', 'rb') as f:
    scaler_y_serv = pickle.load(f)

#Lista de festivos
lista_festivos = pd.to_datetime(['2024-05-01', '2024-05-20', '2024-06-24', '2024-08-15', '2024-09-11', '2024-09-24', '2024-10-12', '2024-11-01', '2024-12-06', '2024-12-25', '2024-12-26'])

# Funciones de predicción por sector
def predecir_industrial(datos_usuario_ind):
    # Predecir los valores de prueba
    datos_usuario_df_ind = pd.DataFrame([datos_usuario_ind])
    datos_usuario_scaled_ind= scaler_X_ind.transform(datos_usuario_df_ind)
    predInd_scaled = modelInd.predict(datos_usuario_scaled_ind)
    # Desescalar las predicciones y los valores reales para comparar
    predInd = scaler_y_ind.inverse_transform(predInd_scaled)
    return predInd

def predecir_residencial(datos_usuario_res):
    # Predecir los valores de prueba
    datos_usuario_df_res = pd.DataFrame([datos_usuario_res])
    datos_usuario_scaled_res= scaler_X_res.transform(datos_usuario_df_res)
    predRes_scaled = modelRes.predict(datos_usuario_scaled_res)
    # Desescalar las predicciones y los valores reales para comparar
    predRes = scaler_y_res.inverse_transform(predRes_scaled)
    return predRes

def predecir_servicios(datos_usuario_ser):
    # Predecir los valores de prueba
    datos_usuario_df_ser = pd.DataFrame([datos_usuario_ser])
    datos_usuario_scaled_ser= scaler_X_serv.transform(datos_usuario_df_ser)
    predSer_scaled = modelSer.predict(datos_usuario_scaled_ser)
    # Desescalar las predicciones y los valores reales para comparar
    predSer = scaler_y_serv.inverse_transform(predSer_scaled)
    return predSer

# Página principal
def pagina_principal():
    st.title("AMH Solutions")
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Selecciona el sector", ["Inicio", "Industrial", "Residencial", "Servicios"])

    if page == "Industrial":
        st.session_state["page"] = "industrial"
    elif page == "Residencial":
        st.session_state["page"] = "residencial"
    elif page == "Servicios":
        st.session_state["page"] = "servicios"
    else:
        st.session_state["page"] = "home"



# Página de predicción de sector industrial
def pagina_industrial():
    st.title("Predicción para Sector Industrial")

    st.write("Introduce los datos conocidos:")

    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date(2024, 5, 1),   # Valor predeterminado
        min_value=datetime.date(2024, 5, 1),  # Fecha mínima
        max_value=datetime.date(2024, 5, 2)  # Fecha máxima
    )

    dia_semana = fecha.weekday()
    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0
    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=35)
    
    if temperatura < 0 or temperatura > 35:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    temperatura_final = temperatura_def if temperatura == 35 else temperatura

    t_1=df_ind['consumo'].iloc[-1]

    datos_usuario = {
        "tmed": temperatura_final,
        "COVID": 0,
        "findesemana": findesemana,
        "festivos": festivos,
        "t-1": t_1
    }

    if st.button("Predecir Consumo"):
        prediction = predecir_industrial(datos_usuario)
        st.success(f"El día {fecha} se prevé un consumo de {prediction[0][0]:.2f}")

    if st.sidebar.button("Volver al inicio"):
        st.session_state["page"] = "home"


# Página de predicción de sector residencial
def pagina_residencial():
    st.title("Predicción para Sector Residencial")

    st.write("Introduce los datos conocidos:")

    #Solicitamos la fecha a predecir
    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date(2024, 5, 1),   # Valor predeterminado
        min_value=datetime.date(2024, 5, 1),  # Fecha mínima
        max_value=datetime.date(2024, 5, 2)  # Fecha máxima
    )

    dia_semana = fecha.weekday()

    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0

    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=35)
    
    if temperatura < 0 or temperatura > 35:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    temperatura_final = temperatura_def if temperatura == 35 else temperatura

    PIB = 77268

    t_1=df_res['consumo'].iloc[-1]

    datos_usuario = {
        "tmed": temperatura_final,
        "PIB": PIB,
        "findesemana": findesemana,
        't-1': t_1
    }

    if st.button("Predecir Consumo"):
        prediction = predecir_residencial(datos_usuario)
        st.success(f"El día {fecha} se prevé un consumo de {prediction[0][0]:.2f}")

    if st.sidebar.button("Volver al inicio"):
        st.session_state["page"] = "home"

# Página de predicción de sector 3
def pagina_servicios():
    st.title("Predicción para Sector Servicios")

    st.write("Introduce los datos conocidos:")

    #Solicitamos la fecha a predecir
    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date(2024, 5, 1),   # Valor predeterminado
        min_value=datetime.date(2024, 5, 1),  # Fecha mínima
        max_value=datetime.date(2024, 5, 2)  # Fecha máxima
    )

    dia_semana = fecha.weekday()

    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0

    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=35)
    
    if temperatura < 0 or temperatura > 35:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    temperatura_final = temperatura_def if temperatura == 35 else temperatura
    

    t_1=df_res['consumo'].iloc[-1]

    poblacion=5884873

    pernoctaciones=743000

    datos_usuario = {
        "tmed": temperatura_final,
        "pernoctaciones": pernoctaciones,
        "findesemana": findesemana,
        't-1': t_1,
        'festivos': festivos,
        'poblacion': poblacion            
    }

    if st.button("Predecir Consumo"):
        prediction = predecir_servicios(datos_usuario)
        st.success(f"El día {fecha} se prevé un consumo de {prediction[0][0]:.2f}")

    if st.sidebar.button("Volver al inicio"):
        st.session_state["page"] = "home"

# Navegación de páginas
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    if st.session_state["page"] == "home":
        pagina_principal()
    elif st.session_state["page"] == "residencial":
        pagina_residencial()
    elif st.session_state["page"] == "servicios":
        pagina_servicios()
    elif st.session_state["page"] == "industrial":
        pagina_industrial()

if __name__ == "__main__":
    main()

