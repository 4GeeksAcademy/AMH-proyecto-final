# Fichero de comunicación con el usuario
# Librerias
import pandas as pd
from datetime import datetime
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Cargar el modelo necesario
modelInd = load_model('../models/modelo_industrial.h5')
df_ind = pd.read_csv("../data/DF_modelos/df_industrial_total.csv")

# Convertir la columna 'fecha' a tipo datetime
df_ind['fecha'] = pd.to_datetime(df_ind['fecha'])

# Escalar las variables para tenerlas normalizadas en el fichero
# Normalizar las columnas numéricas
scaler = StandardScaler()
# Solo se escalan las variables numéricas que se usaron para el modelo
num_columns = ['tmed', 'prec', 'velmedia', 'poblacion', 'PIB']
df_ind[num_columns] = scaler.fit_transform(df_ind[num_columns])

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

    # Convertir la fecha a segundos desde la época
    fecha_seg = fecha.value // 10**9 

    # Otros valores generados por nosotros
    COVID = 0  
    tmed = 15  # Valor de ejemplo
    prec = 0.1  # Valor de ejemplo
    velmedia = 2.0  # Valor de ejemplo

    # Diccionario a devolver
    return {
        'fecha': fecha_seg,
        'findesemana': findesemana,
        'festivos': festivos,
        'lectivos': lectivos,
        'COVID': COVID,
        'tmed': tmed,
        'prec': prec,
        'velmedia': velmedia,
        'poblacion': 5884873,  # ultimo valor df
        'PIB': 16405,  # ultimo valor df
        'Empleo': 625100  # ultimo valor df
    }

# Comunicación con el usuario
ultima_fecha = df_ind['fecha'].max()  # Obtener la última fecha sin usar como índice
print(f"La última fecha registrada en el dataset es: {ultima_fecha.date()}")

# Solicitar al usuario una fecha posterior a la última fecha registrada
fecha_a_predecir = input(f"Ingrese una fecha posterior a {ultima_fecha.date()} (YYYY-MM-DD): ")

# Fecha ingresada debe ser posterior a la última fecha del DataFrame
fecha_a_predecir_dt = pd.to_datetime(fecha_a_predecir)
if fecha_a_predecir_dt <= ultima_fecha:
    print(f"Error: La fecha ingresada debe ser posterior a {ultima_fecha.date()}")
else:
    # Generar características con la función creada
    caracteristicas = generar_caracteristicas_fecha(fecha_a_predecir)

    df_pred = pd.DataFrame([caracteristicas])

    # Solo escalamos las columnas numéricas (como en el entrenamiento)
    df_pred_num = df_pred[['tmed', 'prec', 'velmedia', 'poblacion', 'PIB']]
    df_pred_num_normalizado = scaler.transform(df_pred_num)

    # Añadir las columnas no numéricas sin escalar
    df_pred_final = df_pred.copy()
    df_pred_final[['tmed', 'prec', 'velmedia', 'poblacion', 'PIB']] = df_pred_num_normalizado

    # Realizar la predicción del modelo con los datos proporcionados
    prediccion_consumo = modelInd.predict(df_pred_final)

    # Mostrar la predicción
    print(f"Predicción de consumo para el {fecha_a_predecir}: {prediccion_consumo[0][0]}")


