import streamlit as st
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
import os
import base64

#Directorio actual
base_dir = os.path.dirname(__file__)

# Cargar DataFrames
df_ind = pd.read_csv(os.path.join(base_dir, '..','data', 'DF_modelos', 'df_industrial_modelo.csv'))
df_res = pd.read_csv(os.path.join(base_dir, '..', 'data', 'DF_modelos', 'df_residencial_modelo.csv'))
df_serv = pd.read_csv(os.path.join(base_dir, '..','data', 'DF_modelos', 'df_servicios_modelo.csv'))

# Cargar modelos
modelInd = load_model(os.path.join(base_dir, '..', 'models', 'modelo_industrial_Def.h5'))
modelRes = load_model(os.path.join(base_dir, '..', 'models', 'modelo_residencial_Def.h5'))
modelSer = load_model(os.path.join(base_dir, '..', 'models', 'modelo_servicios_Def.h5'))

# Cargar escaladores
def cargar_escalador(ruta):
    with open(ruta, 'rb') as f:
        return pickle.load(f)

scaler_X_ind = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_X_ind.pkl'))
scaler_y_ind = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_y_ind.pkl'))
scaler_X_res = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_X_res.pkl'))
scaler_y_res = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_y_res.pkl'))
scaler_X_serv = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_X_serv.pkl'))
scaler_y_serv = cargar_escalador(os.path.join(base_dir, '..','data', 'scalers', 'scaler_y_serv.pkl'))


# Lista de festivos
lista_festivos = pd.to_datetime([
    '2024-05-01', '2024-05-20', '2024-06-24', '2024-08-15', 
    '2024-09-11', '2024-09-24', '2024-10-12', '2024-11-01', 
    '2024-12-06', '2024-12-25', '2024-12-26'
])

#Funcion imagen de fondo 
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')
    
def cargar_css(css_file):
    # Cargar CSS desde el archivo
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Obtener la ruta de la imagen de fondo
    base_dir = os.path.dirname(__file__)
    img_path = os.path.join(base_dir, '..', 'data', 'imagen', 'fondo4.jpg')
    # Convertir la imagen a base64 y aplicar el fondo
    try:
        img_base64 = get_base64_of_bin_file(img_path)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("El archivo de imagen no se encontró. Verifica la ruta.")


# Funciones de predicción
def predecir_industrial(datos):
    datos_scaled = scaler_X_ind.transform(datos)
    datos_seq = datos_scaled.reshape((1, 2, 5))
    pred_scaled = modelInd.predict(datos_seq)
    return scaler_y_ind.inverse_transform(pred_scaled)

def predecir_residencial(datos):
    datos_scaled = scaler_X_res.transform(datos)
    datos_seq = datos_scaled.reshape((1, 1, 4))
    pred_scaled = modelRes.predict(datos_seq)
    return scaler_y_res.inverse_transform(pred_scaled)

def predecir_servicios(datos):
    datos_scaled = scaler_X_serv.transform(datos)
    datos_seq = datos_scaled.reshape((1, 2, 6))
    pred_scaled = modelSer.predict(datos_seq)
    return scaler_y_serv.inverse_transform(pred_scaled)
