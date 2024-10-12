##Streamlit para la web de interaccion con el usuario 
import streamlit as st
from tensorflow.keras.models import load_model


modelInd = load_model('../models/modelo_industrial.h5')
modelRes = load_model('../models/modelo_residencial.h5')
modelSer = load_model('../models/modelo_servicios.h5')

# Funciones de predicción por sector
def predecir_industrial(datos_usuario_ind):
    # Predecir los valores de prueba
    predInd_scaled = modelInd.predict(datos_usuario_ind)
    # Desescalar las predicciones y los valores reales para comparar
    predInd = scaler_y.inverse_transform(predInd_scaled)
    return predInd

def predecir_residencial(datos_usuario_res):
    # Predecir los valores de prueba
    predRes_scaled = modelRes.predict(datos_usuario_res)
    # Desescalar las predicciones y los valores reales para comparar
    predRes = scaler_y.inverse_transform(predRes_scaled)
    return predRes

def predecir_servicios(datos_usuario_ser):
    # Predecir los valores de prueba
    predSer_scaled = modelInd.predict(datos_usuario_ser)
    # Desescalar las predicciones y los valores reales para comparar
    predSer = scaler_y.inverse_transform(predSer_scaled)
    return predSer

# Página principal
def pagina_principal():
    st.title("AMH Solutions")
    st.write("Bienbenido al portal de predicciones de consumos en Barcelona")
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

    st.write("Introduce los datos necesarios (los que no se completen usarán valores predefinidos):")

    # Aquí puedes agregar más campos según los datos que necesites para este sector
    fecha = st.number_input("fecha", min_value=0, value=100)
    dato2 = st.number_input("Dato 2", min_value=0, value=50)
    
    datos_usuario = {
        "fecha": fecha,
        "dato2": dato2
    }

    if st.button("Predecir Consumo"):
        prediccion = predecir_industrial(datos_usuario)
        st.success(f"El dia {fecha} se prevee un  consumo de {prediccion}")

    if st.button("Volver"):
        st.session_state["page"] = "home"

# Página de predicción de sector residencial
def pagina_residencial():
    st.title("Predicción para Sector Residencial")

    st.write("Introduce los datos necesarios (los que no se completen usarán valores predefinidos):")

    # Aquí puedes agregar más campos según los datos que necesites para este sector
    fecha = st.number_input("fecha", min_value=0, value=100)
    dato2 = st.number_input("Dato 2", min_value=0, value=50)
    
    datos_usuario = {
        "fecha": fecha,
        "dato2": dato2
    }

    if st.button("Predecir Consumo"):
        prediccion = predecir_residencial(datos_usuario)
        st.success(f"El dia {fecha} se prevee un consumo de {prediccion}")

    if st.button("Volver"):
        st.session_state["page"] = "home"

# Página de predicción de sector 3
def pagina_servicios():
    st.title("Predicción para Sector Servicios")

    st.write("Introduce los datos necesarios (los que no se completen usarán valores predefinidos):")

    # Aquí puedes agregar más campos según los datos que necesites para este sector
    fecha = st.number_input("fecha", min_value=0, value=100)
    dato2 = st.number_input("Dato 2", min_value=0, value=50)
    
    datos_usuario = {
        "fecha": fecha,
        "dato2": dato2
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
