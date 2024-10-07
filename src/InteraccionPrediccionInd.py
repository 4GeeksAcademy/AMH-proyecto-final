#Fichero de comunicacion con el usuario
#Librerias
import pandas as pd
from datetime import datetime
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

#Cargar el modelo necesario
modelInd = load_model('../models/modelo_industrial.h5')
df_ind=pd.read_csv("../data/DF_modelos/df_industrial_total.csv")

# Lista de festivos a modificar
lista_festivos = pd.to_datetime(['2024-01-01', '2024-12-25'])

# Función para generar características necesarias en el modelo
def generar_caracteristicas_fecha(fecha_str):
    fecha = pd.to_datetime(fecha_str)
    dia_semana = fecha.weekday()
    
    # Determinar si es fin de semana
    findesemana = 1 if dia_semana >= 5 else 0
    
    # Determinar si es festivo
    festivos = 1 if fecha in lista_festivos else 0
    
    # Determinar si es lectivo
    lectivos = 1 if dia_semana < 5 and not festivos else 0
    
    # Otros valores generados por nosotros
    COVID = 0  
    tmed = 15  
    prec = 0.1  
    velmedia = 2.0  
    
    # Diccionario a devolver
    return {
        'findesemana': findesemana,
        'festivos': festivos,
        'lectivos': lectivos,
        'COVID': COVID,
        'tmed': tmed,
        'prec': prec,
        'velmedia': velmedia,
        'poblacion': 5628011,  # Valor fijo
        'PIB': 14279,  # Valor de ejemplo
        'Empleo': 604200  # Valor de ejemplo
    }


#Comunicacion con el usuario

ultima_fecha = df_ind.index.max()
print(f"La última fecha registrada en el dataset es: {ultima_fecha.date()}")

# Solicitar al usuario una fecha posterior a la última fecha registrada
fecha_a_predecir = input(f"Ingrese una fecha posterior a {ultima_fecha.date()} (YYYY-MM-DD): ")

# Fecha ingresada sea posterior a la ultima fecha del df
fecha_a_predecir_dt = pd.to_datetime(fecha_a_predecir)
if fecha_a_predecir_dt <= ultima_fecha:
    print(f"Error: La fecha ingresada debe ser posterior a {ultima_fecha.date()}")
else:
    # Generar características con la funcion creada
    caracteristicas = generar_caracteristicas_fecha(fecha_a_predecir)
    
    df_pred = pd.DataFrame([caracteristicas])
    
    # Normalizar
    df_pred_normalizado = scaler.transform(df_pred)
    
    # Realizar la predicción del modelo con los datos proporcionados
    prediccion_consumo = modelInd.predict(df_pred_normalizado)
    
    # Mostrar la predicción
    print(f"Predicción de consumo para el {fecha_a_predecir}: {prediccion_consumo[0][0]}")
