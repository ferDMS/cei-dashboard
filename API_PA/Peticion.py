import streamlit as st
import pandas as pd
from datetime import timedelta
import sys


import requests
import pandas as pd
from io import StringIO
from datetime import timedelta, datetime
import pytz
import sys
import json

import API_PA.Funciones as Funciones

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Fecha Inicial', key = 1)
    start_time = st.time_input('Tiempo Inicial', key = 2)


start_timestamp = str(start_date).replace(":", "-") + "T" + str(start_time) + "Z"

with col2:
    end_date = st.date_input('Fecha Final', key = 3)
    end_time = st.time_input('Tiempo Final', key = 4)

end_timestamp = str(end_date).replace(":", "-") + "T" + str(end_time) + "Z"

municipality = st.selectbox("Lugar de donde se extraeran datos (Definirá el nombre del archivo):",
                            ["Tec Garza Laguera", "San Pedro", "Cadereyta", "Apodaca", "Juarez", "San Nicolas", "Santa Catarina"])

columns = st.multiselect(
    "Columnas de intéres:",
    ["pm2.5_atm_a", "pm2.5_atm_b", "humidity_a", "temperature_a", "pressure_a"],
    ["pm2.5_atm_a", "pm2.5_atm_b", "humidity_a", "temperature_a", "pressure_a"])

api_key = st.text_input("API Key (Previamente creada en https://www.google.com/url?q=https%3A%2F%2Fdevelop.purpleair.com%2F):", key = 5)

period = st.number_input("Periodo, en minutos, de cada cuánto se quieren datos:", key = 6, value = None, format = "%.0f")

sensor = st.number_input("Índice del sensor a obtener datos: ", key = 7, value = None, format = "%.0f")

agree = st.checkbox("Opción para observar los ID's de los sensores ya analizados")

if agree:
    Tabla = pd.DataFrame({
        "Nombre del sensor": ["Tec Garza Laguera", "San Pedro", "Cadereyta", "Apodaca", "Juarez", "San Nicolas", "Santa Catarina"], 
        "ID": [50871, 39355, 39497, 95337, 93927, 93745, 39285]})
    st.dataframe(Tabla)

if st.button('Ejecutar Request'):
    # No cambiar nada de aquí para abajo de este bloque de código

    # Desfase de horas entre horario UTC y mexicano
    offset = 5

    # Codificar los dos puntos de la fecha
    start_timestamp = start_timestamp.replace(":", "%3A")

    # Obtener el start_timestamp en formato de fecha y aplicando desfase
    start_timestamp_date_format = Funciones.timestamp_to_date(start_timestamp)
    start_timestamp_date_format += timedelta(hours=offset)

    # Obtener el end_timestamp en formato de fecha y aplicando desfase
    end_timestamp_date_format = Funciones.timestamp_to_date(end_timestamp)
    end_timestamp_date_format += timedelta(hours=offset)

    # Verificar que la fecha final no sea menor o igual que la inicial
    if end_timestamp_date_format <= start_timestamp_date_format:
        st.write("ERROR: rango de fechas invalido")
        sys.exit()

    # Regresar las fechas ajustadas como timestamps
    start_timestamp = Funciones.date_to_timestamp(start_timestamp_date_format)
    end_timestamp = Funciones.date_to_timestamp(end_timestamp_date_format)


    # si son varias columnas para la solicitud de datos se debe agregar el separador '%2C%20' pero si solo es una columna se omite
    fields = ""
    if len(columns) > 1:
        fields += columns[0]
        for i in range(1, len(columns)):
            fields += "%2C%20"
            fields += columns[i]
    else:
        fields = columns[0]

    headers = {
        "X-API-Key": api_key
    }

    # Aqui se agrega o modifica el sensor de los municipios deseados
    sensorsDict = {"Tec Garza Laguera": 50871, "San Pedro": 39355, "Cadereyta": 39497, "Apodaca": 95337,
                "Juarez": 93927, "San Nicolas": 93745, "Santa Catarina": 39285}

    sensorsDict[municipality] = sensor

    try:
        sensor_id = sensorsDict[municipality]
    except:
        st.write("ERROR: municipio invalido")
        sys.exit()

    st.write(start_timestamp)
    st.write(start_timestamp_date_format)
    st.write(end_timestamp)
    st.write(end_timestamp_date_format)
    st.write(sensor_id)
    st.write(fields)
    st.write(period)