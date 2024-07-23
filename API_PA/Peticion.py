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

sensorsDict = {"Tec Garza Laguera": 50871, "San Pedro": 39355, "Cadereyta": 39497, "Apodaca": 95337,
                "Juarez": 93927, "San Nicolas": 93745, "Santa Catarina": 39285}

# El de San Nico es simaUanl3

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
                            sensorsDict.keys())

columns = st.multiselect(
    "Columnas de intéres:",
    ["pm2.5_atm_a", "pm2.5_atm_b", "humidity_a", "temperature_a", "pressure_a"],
    ["pm2.5_atm_a", "pm2.5_atm_b", "humidity_a", "temperature_a", "pressure_a"])

api_key = st.text_input("API Key (Previamente creada en https://www.google.com/url?q=https%3A%2F%2Fdevelop.purpleair.com%2F):", key = 5)

period = st.number_input("Periodo, en minutos, de cada cuánto se quieren datos:", key = 6, value = 60, 
                         help = "60 minutos (1 hora) es con lo que se está trabajando hasta el momento")

sensor = st.number_input("Índice del sensor a obtener datos: ", key = 7, value = sensorsDict[municipality] if municipality in sensorsDict else 0)

agree = st.checkbox("Opción para observar los ID's de los sensores ya analizados")

if agree:
    Tabla = pd.DataFrame({"Nombre del sensor": sensorsDict.keys(), "ID": sensorsDict.values()})
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

    # Inicializar dataframe vacio solo una vez

    if 'df_full' not in st.session_state:
        st.session_state["df_full"] = pd.DataFrame(columns=columns)
    else:
        st.write("Actualizando dataframe..")

    # Para reiniciar el dataframe aunque ya haya sido inicilizado, correr esta línea
    # Dejar comentada después de usarse, por si acaso
    # df_full = pd.DataFrame(columns=columns)

    Funciones.getKeyInfo(api_key)

    
    df_aux = Funciones.getData(municipality, sensor, period, fields, columns, headers, offset, start_timestamp_date_format, end_timestamp_date_format)
    
    st.session_state["df_full"] = pd.concat([st.session_state["df_full"], df_aux], ignore_index=True)

    st.session_state["df_full"].sort_values("time_stamp", ascending=True, inplace=True)
    st.session_state["df_full"].reset_index(drop=True, inplace=True)
    
    st.dataframe(st.session_state["df_full"])

    st.write(f'{st.session_state["df_full"].shape[0]} registros agregados')

    st.download_button('Descargar CSV', st.session_state["df_full"].to_csv(index=False), file_name = f"{municipality}_API_{period}MINS.csv", mime="text/csv")