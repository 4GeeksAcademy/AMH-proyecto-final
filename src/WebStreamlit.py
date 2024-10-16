##Streamlit para la web de interaccion con el usuario 
#el comando para realizar la peticion de url de la we:
#python -m streamlit run WebStreamlit.py

import streamlit as st
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pickle
import datetime
import pandas as pd
import random
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ruta de la imagen local
img_path = "../data/imagen/fondo3.jpg"

# Convertimos la imagen a Base64
img_base64 = get_base64_of_bin_file(img_path)

# CSS para aplicar la imagen de fondo
page_bg_img = f'''
<style>
/* Fondo de la aplicación */
.stApp {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Color de texto en toda la app */
h1, h2, h3, h4, h5, p, label, div, .stMarkdown {{
    color: white !important;
}}

/* Botones personalizados oscuros */
div.stButton > button {{
    background-color: #333333 !important;  /* Gris oscuro */
    color: white !important;               /* Texto blanco */
    border: 1px solid #444444;             /* Borde más claro */
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}}

div.stButton > button:hover {{
    background-color: #555555 !important;  /* Gris más claro al pasar el cursor */
    border-color: #666666;
}}

/* Mensajes de éxito más resaltados */
.stAlert[data-baseweb="notification"] {{
    background-color: #198754 !important;  /* Verde intenso */
    color: white !important;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
    font-size: 18px;
}}
</style>
'''

# Incluir CSS en la aplicación
st.markdown(page_bg_img, unsafe_allow_html=True)

#Importo df
df_ind = pd.read_csv('../data/DF_modelos/df_industrial_modelo.csv')
df_res = pd.read_csv('../data/DF_modelos/df_residencial_modelo.csv')
df_serv = pd.read_csv('../data/DF_modelos/df_servicios_modelo.csv')

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
    #Predecir los valores de prueba
    datos_usuario_scaled_ind= scaler_X_ind.transform(datos_usuario_ind)
    #Crear la secuencia para el modelo
    datos_ususario_seq_ind = datos_usuario_scaled_ind.reshape((1, 2, 5))
    #Realizar prediccion
    predInd_scaled = modelInd.predict(datos_ususario_seq_ind)
    #Desescalar las predicciones y los valores reales para comparar
    predInd = scaler_y_ind.inverse_transform(predInd_scaled)
    return predInd

def predecir_residencial(datos_usuario_res):
    #Predecir los valores de prueba
    datos_usuario_scaled_res= scaler_X_res.transform(datos_usuario_res)
    #Crear la secuencia para el modelo
    datos_ususario_seq_res = datos_usuario_scaled_res.reshape((1, 1, 4))
    #Realizar la prediccion
    predRes_scaled = modelRes.predict(datos_ususario_seq_res)
    #Desescalar las predicciones y los valores reales para comparar
    predRes = scaler_y_res.inverse_transform(predRes_scaled)
    return predRes

def predecir_servicios(datos_usuario_ser):
    # Escalar los datos del usuario
    datos_usuario_scaled_ser = scaler_X_serv.transform(datos_usuario_ser)
    # Ajustar la forma del input a (1, 2, 6) para la predicción
    datos_usuario_seq_ser = datos_usuario_scaled_ser.reshape((1, 2, 6))
    # Realizar la predicción
    predSer_scaled = modelSer.predict(datos_usuario_seq_ser)
    # Desescalar la predicción
    predSer = scaler_y_serv.inverse_transform(predSer_scaled)
    return predSer


# Página principal
def pagina_principal():
    # Simula una recarga añadiendo un parámetro aleatorio a la URL.
    #st.experimental_set_query_params(rerun=str(random.randint(0, 10000)))
    st.title("AMH Solutions")
    st.text("Binvenido a la plataforma de preddicion de consumo de Barcelona")
    #st.sidebar.title("Navegación")
    #page = st.sidebar.radio("Selecciona el sector", ["Inicio", "Industrial", "Residencial", "Servicios"])

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
                st.session_state["page"] = "industrial"
            elif sector == "Residencial":
                st.session_state["page"] = "residencial"
            elif sector == "Servicios":
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
        max_value=datetime.date(2024, 5, 5)  # Fecha máxima
    )

    dia_semana = fecha.weekday()
    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0
    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=45)
    
    if temperatura < 0 or temperatura > 45:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    tmed = temperatura_def if temperatura == 45 else temperatura

    t_1=df_ind['consumo'].iloc[-1]

    COVID=0

    datos_anteriro_ind = df_ind.iloc[-1][['findesemana', 'festivos', 'COVID', 'tmed', 't-1']].values
    # Crear la lista de nuevos datos proporcionados por el usuario (debe tener la misma longitud)
    datos_usuario_ind = np.array([findesemana, festivos, COVID, tmed, t_1])
    # Combinar los datos anteriores y los proporcionados en un solo array
    datos_ind = np.vstack([datos_anteriro_ind, datos_usuario_ind])

    if st.button("Predecir Consumo"):
        prediction_ind = predecir_industrial(datos_ind)
        # Asegúrate de que prediction_ind es un número escalar
        valor_prediccion = prediction_ind[0, 0]

        # Mostrar el resultado correctamente
        st.success(f"El día {fecha} se prevé un consumo de {valor_prediccion:.2f}")
        #st.write(f"Forma de prediction_ind: {prediction_ind.shape}, Valor: {prediction_ind}")

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
        max_value=datetime.date(2024, 5, 5)  # Fecha máxima
    )

    dia_semana = fecha.weekday()

    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0

    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=45)
    
    if temperatura < 0 or temperatura > 45:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    tmed = temperatura_def if temperatura == 45 else temperatura

    PIB = 77268

    t_1=df_res['consumo'].iloc[-1]

    datos_usuario_res =  np.array([[findesemana, tmed, PIB, t_1]])

    if st.button("Predecir Consumo"):
        prediction_res = predecir_residencial(datos_usuario_res)
        valor_prediccion_res = prediction_res[0, 0]

        # Mostrar el resultado correctamente
        st.success(f"El día {fecha} se prevé un consumo de {valor_prediccion_res:.2f}")
        #st.write(f"Forma de prediction_ind: {prediction_res.shape}, Valor: {prediction_res}")

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
        max_value=datetime.date(2024, 5, 5)  # Fecha máxima
    )

    dia_semana = fecha.weekday()

    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0

    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0

    temperatura_def = 21
    temperatura = st.number_input("temperatura media", min_value=0, value=45)
    
    if temperatura < 0 or temperatura > 45:
        st.error("Por favor, introduce una temperatura válida entre 0 y 35.")

    tmed = temperatura_def if temperatura == 45 else temperatura
    

    t_1=df_res['consumo'].iloc[-1]

    poblacion=5884873

    pernoctaciones=743000



    datos_anteriro_ser = df_serv.iloc[-1][['findesemana', 'festivos', 'pernoctaciones', 'tmed', 'poblacion', 't-1']].values
    # Crear la lista de nuevos datos proporcionados por el usuario (debe tener la misma longitud)
    datos_usuario_ser = np.array([findesemana, festivos, pernoctaciones, tmed, poblacion, t_1])
    # Combinar los datos anteriores y los proporcionados en un solo array
    datos_ind = np.vstack([datos_anteriro_ser, datos_usuario_ser])

    if st.button("Predecir Consumo"):
        prediction_ser = predecir_servicios(datos_usuario_ser)
        valor_prediccion_ser = prediction_ser[0, 0]

        # Mostrar el resultado correctamente
        st.success(f"El día {fecha} se prevé un consumo de {valor_prediccion_ser:.2f}")
        #st.write(f"Forma de prediction_ind: {prediction_ser.shape}, Valor: {prediction_ser}")


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

