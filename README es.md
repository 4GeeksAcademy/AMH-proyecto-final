# Predicción del consumo de electricidad en Barcelona

Este proyecto tiene como objetivo predecir el consumo de electricidad en la provincia de Barcelona utilizando datos históricos y técnicas de aprendizaje automático. Utilizamos datos climáticos, demográficos, macroeconómicos, shocks económicos, indicadores turísticos y días festivos para entrenar modelos que predigan el consumo de electricidad diario.


## Web de predicción

El enlace a la web en la nube es:
- https://amh-barcelona-electricidad.streamlit.app/pagina_principal


## Estructura

El proyecto está organizado en varias carpetas y archivos clave para gestionar los datos, los modelos y el código de la aplicación web. A continuación, se detallan las secciones principales del proyecto:

- `data` - Esta carpeta almacena los datos utilizados en el proyecto, organizados en varias subcarpetas:
  - `DF_modelos` - Almacena los DataFrame finales procesados.
  - `Final_Data` - Contiene los archivos CSV con los datos utilizados en los DataFrame de los diferentes sectores (residencial, industrial, servicios).
  - `imagen` - Contiene las imágenes utilizadas en la aplicación web, como fondos de pantalla.
  - `interim` - Contiene los datos originales sin procesar.
  - `processed` - Contiene datos procesados.
  - `scalers` - Guarda los archivos de scalers utilizados para normalizar los datos para las peticiones del usuario.
- `models` - Esta carpeta contiene los modelos predictivos entrenados guardados como archivos `.h5`.
- `src` - Esta carpeta contiene el código fuente del proyecto, con diferentes scripts para la gestión del flujo de datos y diversas pruebas de código:
  - `Procesado de datos` - Scripts relacionados con la limpieza y el preprocesamiento de los datos.
  - `Proceso de modelos` - Contiene scripts que realizan el entrenamiento y la evaluación de los modelos predictivos.
  - `Procesos prueba` - Carpeta para scripts de prueba de los modelos y de WebStreamlit. 
  - `StreamlitAntes.py` - Versión anterior del código de la aplicación web en Streamlit.
  - `WebStreamlit.py` - Versión actualizada de la aplicación web implementada en Streamlit, que permite a los usuarios interactuar con los modelos y predecir el consumo de electricidad. 
- `stremalit` - Esta carpeta contiene el código de la creación de la web para la interacción con el usuario:
  - `pages` - Scripts relacionados con la visualización e interación del usuario con cada una de las diferentes páginas de la web en stremlit share.
  - `style` - Contiene un único archivo .css que nos permite realizar la personalización del contenido de la Web.
  - `funciones.py` - Archivo que almacena todas las funciones necesarias para la interacción del usuario en las predicciones deseadas.
  - `mainStreamlit.py` - Archivo principal de manejo de la Web. 
- `requirements.txt` - Archivo que contiene las dependencias y bibliotecas necesarias para ejecutar el proyecto.
    
## Instlación de dependencias

**Requisitos**

Asegúrate de tener Python 3.11+ instalado en tu sistema. También necesitarás pip para instalar los paquetes de Python.

**Instalación**

Clona el repositorio del proyecto en tu máquina local.

Navega hasta el directorio del proyecto e instala los paquetes de Python necesarios:

```bash
pip install -r requirements.txt
```

## Ejecución del Proyecto

Para ejecutar el modelo de predicción de consumo, ejecuta el siguiente comando:
```bash
python -m streamlit run streamlit/mainStreamlit.py
```

## Datos

Los datos utilizados en este proyecto incluyen variables climáticas, de población y datos de consumo energético desde 2019 hasta 2024.

- Consumo de electricidad (MWh): https://datos.gob.es/es/catalogo/l01080193-consumo-de-electricidad-mwh-por-codigo-postal-sector-economico-y-tramo-horario
- Variables climáticas (Temperatura media, Precipitaciones y Velocidad del viento): https://opendata.aemet.es/centrodedescargas/inicio
- Variables sociodemográficas (Población, Renta, Empleo, PIB y Pernoctaciones): https://www.ine.es/
- Variables temporales y bono social: Búsquedas independientes en internet.


## Modelos

Los modelos utilizados son los siguientes:
-	XGBoost (Extreme Gradient Boosting): Identifica las variables potenciales que pueden explicar el consumo de electricidad por sectores.
-	LSTM (Long Short-Term Memory): Realiza predicciones de la demanda de electricidad por sectores.


## Contribuciones

Si deseas contribuir a este proyecto, por favor, crea un fork y envía un pull request.

## Contacto

Para preguntas o comentarios, contacta con: 
- Héctor Postigo Gómez (hpostigogomez@gmail.com) 
- Alba Estévez Bauluz (albaebauluz@hotmail.com)

