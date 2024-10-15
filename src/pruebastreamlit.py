import streamlit as st
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pickle
import datetime
import pandas as pd

#Cargar el df
df = pd.read_csv('../data/DF_modelos/df_industrial_total.csv')

# Cargar el modelo
model = load_model('../models/modelo_industrial_def.h5')

#Cargar escala
with open('../data/scalers/scaler_X_ind.pkl', 'rb') as f:
    scaler_X = pickle.load(f)
with open('../data/scalers/scaler_y_ind.pkl', 'rb') as f:
    scaler_y = pickle.load(f)


# Función para realizar la predicción
# Función para realizar la predicción
def realizar_prediccion(input_data):
    # Crear un array de las características
    #input_data = np.array([[findesemana, festivos, COVID, tmed, t1], 
    #                        [findesemana, festivos, COVID, tmed, t1]])  # Duplicamos la entrada para tener 2 pasos de tiempo

    # Normalizar las características
    input_data_scaled = scaler_X.transform(input_data)

    # Crear la secuencia para el modelo
    input_data_scaled = input_data_scaled.reshape((1, 2, 5))  # (samples, time steps, features)

    # Realizar la predicción
    prediccion_scaled = model.predict(input_data_scaled)

    # Inversar la normalización para obtener el valor original
    prediccion = scaler_y.inverse_transform(prediccion_scaled)

    return prediccion[0][0]


# Interfaz de usuario
st.title("Predicción de Consumo")

# Campos de entrada para el usuario
findesemana = st.number_input("¿Es fin de semana? (1 = Sí, 0 = No)", value=0)
festivos = st.number_input("¿Es festivo? (1 = Sí, 0 = No)", value=0)
COVID = st.number_input("¿Es periodo de COVID? (1 = Sí, 0 = No)", value=0)
tmed = st.number_input("Temperatura media (tmed)", value=6.0)
t_1 = st.number_input("Consumo en el periodo anterior (t-1)", value=1000000)
datos_usuario =  np.array([[findesemana, festivos, COVID, tmed, t_1], 
                        [findesemana, festivos, COVID, tmed, t_1]])

# Botón para realizar la predicción
if st.button("Realizar Predicción"):
    resultado = realizar_prediccion(datos_usuario)
    st.success(f"La predicción de consumo es: {resultado:.2f}")

# Mensaje de ayuda si no se introducen datos
st.info("Si no introduces datos, el programa usará valores predeterminados.")
