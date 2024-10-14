##Streamlit para la web de interaccion con el usuario 
#el comando para realizar la peticion de url de la we:
#streamlit run WebStreamlit.py
#libreria pickle
import streamlit as st
from tensorflow.keras.models import load_model
import pickle
import datetime
import pandas as pd
#Importo df
df_ind = pd.read_csv('../data/DF_modelos/df_industrial_total.csv')
df_res = pd.read_csv('../data/DF_modelos/df_residencial_total.csv')
df_serv = pd.read_csv('../data/DF_modelos/df_servicios_total.csv')

#Importamos modelo
modelInd = load_model('../models/modelo_industrial.h5')
modelRes = load_model('../models/modelo_residencial.h5')
modelSer = load_model('../models/modelo_servicios.h5')

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
    datos_usuario_scaled= scaler_X_ind.transform(datos_usuario_ind)
    predInd_scaled = modelInd.predict(datos_usuario_scaled)
    # Desescalar las predicciones y los valores reales para comparar
    predInd = scaler_y_ind.inverse_transform(predInd_scaled)
    return predInd

def predecir_residencial(datos_usuario_res):
    # Predecir los valores de prueba
    datos_usuario_scaled= scaler_X_res.transform(datos_usuario_res)
    predRes_scaled = modelRes.predict(datos_usuario_scaled)
    # Desescalar las predicciones y los valores reales para comparar
    predRes = scaler_y_res.inverse_transform(predRes_scaled)
    return predRes

def predecir_servicios(datos_usuario_ser):
    # Predecir los valores de prueba
    datos_usuario_scaled= scaler_X_serv.transform(datos_usuario_ser)
    predSer_scaled = modelInd.predict(datos_usuario_scaled)
    # Desescalar las predicciones y los valores reales para comparar
    predSer = scaler_y_serv.inverse_transform(predSer_scaled)
    return predSer

# Página principal
def pagina_principal():
    st.title("AMH Solutions")
    st.write("Bienvenido al portal de predicciones de consumos en Barcelona")
    st.write("Escoja el sector que quiere consultar")

    if st.button("Industrial"):
        st.session_state["page"] = "industrial"
    if st.button("Residencial"):
        st.session_state["page"] = "residencial"
    if st.button("Servicios"):
        st.session_state["page"] = "servicios"

# Página de predicción de sector industrial
def pagina_industrial():
    st.title("Predicción para Sector Industrial")

    st.write("Introduce los datos conocidos:")

    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date.today(),  # Valor predeterminado
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
    
    t_1=df_ind['consumo'].index[-1]

    if temperatura == 35:
        temperatura_final = temperatura_def
    else:
        temperatura_final = temperatura

    datos_usuario = {
        "fecha": fecha,
        "tmed": temperatura_final,
        "COVID": 0,
        "findesemana": findesemana,
        "festivos": festivos,
        "t-1": t_1
    }

    if st.button("Predecir Consumo"):
        prediction = predecir_industrial(datos_usuario)
        st.success(f"El dia {fecha} se prevee un  consumo de {prediction}")

    if st.button("Volver"):
        st.session_state["page"] = "home"

# Página de predicción de sector residencial
def pagina_residencial():
    st.title("Predicción para Sector Residencial")

    st.write("Introduce los datos conocidos:")

    #Solicitamos la fecha a predecir
    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date.today(),  # Valor predeterminado
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
    
    if temperatura == 35:
        temperatura_final = temperatura_def
    else:
        temperatura_final = temperatura

    PIB = 77268

    t_1=df_res['consumo'].index[-1]

    datos_usuario = {
        "fecha": fecha,
        "tmed": temperatura_final,
        "PIB": PIB,
        "findesemana": findesemana,
        't-1': t_1
    }

    if st.button("Predecir Consumo"):
        prediccion = predecir_residencial(datos_usuario)
        st.success(f"El dia {fecha} se prevee un consumo de {prediccion}")

    if st.button("Volver"):
        st.session_state["page"] = "home"

# Página de predicción de sector 3
def pagina_servicios():
    st.title("Predicción para Sector Servicios")

    st.write("Introduce los datos conocidos:")

    #Solicitamos la fecha a predecir
    fecha = st.date_input(
        "Selecciona una fecha:",
        value=datetime.date.today(),  # Valor predeterminado
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
    
    if temperatura == 35:
        temperatura_final = temperatura_def
    else:
        temperatura_final = temperatura
    

    t_1=df_res['consumo'].index[-1]

    poblacion=5884873

    pernoctaciones=743000

    datos_usuario = {
        "fecha": fecha,
        "tmed": temperatura_final,
        "pernoctaciones": pernoctaciones,
        "findesemana": findesemana,
        't-1': t_1,
        'festivos': festivos,
        'poblacion': poblacion            
    }

    if st.button("Predecir Consumo"):
        prediccion = predecir_servicios(datos_usuario)
        st.success(f"El dia {fecha} se prevee un  consumo de {prediccion}")

    if st.button("Volver"):
        st.session_state["page"] = "home"

# Navegación de páginas
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    
    if st.session_state["page"] == "home":
        pagina_principal()
    elif st.session_state["page"] == "industrial":
        pagina_industrial()
    elif st.session_state["page"] == "residencial":
        pagina_residencial()
    elif st.session_state["page"] == "servicios":
        pagina_servicios()

if __name__ == "__main__":
    main()
