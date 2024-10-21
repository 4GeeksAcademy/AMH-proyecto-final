# Electricity Consumption Forecast in Barcelona

This project aims to predict electricity consumption in the province of Barcelona using historical data and machine learning techniques. We use climate, demographic, macroeconomic, economic shocks, tourism indicators, and holiday data to train models that predict daily electricity consumption.

## Structure

The project is organized into several folders and key files for managing the data, models, and web application code. Below are the main sections of the project:

- `data` - This folder stores the data used in the project, organized into various subfolders:
  - `DF_modelos` - Stores the final processed DataFrames.
  - `Final_Data` - Contains the CSV files with the data used in the DataFrames for different sectors (residential, industrial, services).
  - `imagen` - Contains images used in the web application, such as wallpapers.
  - `interim` - Contains the raw, unprocessed data.
  - `processed` - Contains processed data.
  - `scalers` - Stores scaler files used to normalize data for user requests.
- `models` - This folder contains the trained predictive models saved as `.h5` files.
- `src` - This folder contains the project's source code, with various scripts for managing data flow and user interaction:
  - `Procesado de datos` - Scripts related to data cleaning and preprocessing.
  - `Procesado de modelos` - Contains scripts that perform training and evaluation of predictive models.
  - `Procesos prueba` - Folder for testing scripts of models and WebStreamlit.
  - `StreamlitAntes.py` - Previous version of the Streamlit web application code.
  - `WebStreamlit.py` - Updated version of the web application implemented in Streamlit, allowing users to interact with the models and predict electricity consumption.
- `requirements.txt` - File containing the necessary dependencies and libraries to run the project.
    
## Dependency Installation

**Prerequisites**

Make sure you have Python 3.11+ installed. You will also need pip to install the required Python packages.

**Installation**

Clone the project repository to your local machine.

Navigate to the project directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Project

To run the electricity consumption prediction model, execute the following command:
```bash
python src/main.py
```

## Data

The data used in this project includes climate variables, population data, and energy consumption data from 2019 to 2024.

- Electricity consumption (MWh): https://datos.gob.es/es/catalogo/l01080193-consumo-de-electricidad-mwh-por-codigo-postal-sector-economico-y-tramo-horario
- Climate variables (Average Temperature, Precipitation, and Wind Speed): https://opendata.aemet.es/centrodedescargas/inicio
- Sociodemographic variables (Population, Income, Employment, GDP, and Overnight Stays): https://www.ine.es/
- Temporal variables and social subsidies: Independent searches on the internet.

## Models

The models used are as follows:
-	XGBoost (Extreme Gradient Boosting): Identifies potential variables that may explain electricity consumption by sector.
-	LSTM (Long Short-Term Memory): Makes predictions of electricity demand by sector.

## Contributions

If you wish to contribute to this project, please fork and submit a pull request.

## Contact

For questions or comments, contact: 
- Héctor Postigo Gómez (hpostigogomez@gmail.com)
- Alba Estévez Bauluz (albaebauluz@hotmail.com)