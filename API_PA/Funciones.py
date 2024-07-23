import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import timedelta, datetime
import pytz
import sys
import json

def timestamp_to_date(timestamp):
    timestamp_date = timestamp.split("T")[0]

    timestamp_hour = timestamp.split("T")[1]
    timestamp_hour = timestamp_hour[:-1]
    timestamp_hour = timestamp_hour.split("%3A")
    timestamp_hour = ":".join(timestamp_hour)

    date = timestamp_date + " " + timestamp_hour
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date


def date_to_timestamp(timestamp):
    date = timestamp.strftime("%Y-%m-%d") + "T" + timestamp.strftime("%H") + "%3A" + timestamp.strftime("%M") + "%3A" + timestamp.strftime("%S") + "Z"
    return date


def httpRequest(url, headers):
    """
    Llamada directa de datos por medio de la API
    """

    response = requests.get(url, headers=headers)
    return response


def processResponse(response):
    """
    Formatear la columna "time_stamp" a un formato de fechas legible que se pueda ordenar
    al finalizar la llamada de datos
    """

    data_text = response.text
    data_file = StringIO(data_text)
    df_response = pd.read_csv(data_file)
    # print(type(df_response))
    # print(df_response)
    # print("\n")

    new_dates = []

    """
    En ocasiones el programa manda un error en la primera linea del siguiente bucle pero el mensaje de error simplemente
    dice 'time_stamp' sin decir mas informacion, eso se debe a que el servidor no devolvio ningun formato valido. Para
    ver la verdadera razon del error hay que descomentar los 3 prints previos para imprimir la respuesta con el mensaje
    que indica lo que desencadeno el error. Dichas lineas estan comentadas para no imprimir basura en las celdas cada
    vez que se hacen llamadas pero se pueden comentadas o descomentadas, no afectan en nada al procedimiento
    """
    for i in range(len(df_response)):
        date = df_response["time_stamp"].iloc[i]
        date = date[:-1]
        date = date.split("T")
        date = " ".join(date)
        new_dates.append(date)
    df_response["time_stamp"] = new_dates
    df_response["time_stamp"] = pd.to_datetime(df_response["time_stamp"], errors='coerce')
    df_response.dropna(subset=["time_stamp"], inplace=True)

    return df_response

def getData(municipality, sensor_id, period, fields, columns, headers, offset, start_timestamp_date_format, end_timestamp_date_format):
    """
    Recibe la fecha inicial y la fecha final, con esos datos calcula la longitud de los bloques de llamadas
    dependiendo de la frecuencia de datos
    """

    if period == 60:
        max_time_span = 336
    elif period == 10:
        max_time_span = 72

    # =============================== LLAMADAS AL SERVIDOR EN BLOQUES DINAMICOS ===============================

    df_full = pd.DataFrame(columns=columns) #  dataframe vacio

    total_days = end_timestamp_date_format - start_timestamp_date_format
    total_hours = total_days.total_seconds() / 3600
    total_days = total_days.days

    if total_hours % max_time_span == 0: # rango de fechas con dias cerrados
        temporal_start_timestamp = start_timestamp_date_format
        temporal_end_timestamp = start_timestamp_date_format + timedelta(hours=max_time_span)
        while temporal_end_timestamp <= end_timestamp_date_format:

            # Solicitud de datos en bloques exactos
            dinamic_start_timestamp = date_to_timestamp(temporal_start_timestamp)
            dinamic_end_timestamp = date_to_timestamp(temporal_end_timestamp)

            # print(temporal_start_timestamp)
            # print(temporal_end_timestamp)
            # print("\n")

            url = f"https://api.purpleair.com/v1/sensors/{sensor_id}/history/csv?start_timestamp={dinamic_start_timestamp}&end_timestamp={dinamic_end_timestamp}&average={period}&fields={fields}"
            response = httpRequest(url, headers)

            if response.status_code != 200:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                print(response.text)
                return

            df_aux = processResponse(response)

            # Agregando la informacion de la nueva solicitud a todos los demas datos
            df_full = pd.concat([df_full, df_aux], ignore_index=True)

            temporal_start_timestamp = temporal_end_timestamp
            temporal_end_timestamp += timedelta(hours=max_time_span)
    else: # rango de fechas con el primer o ultimo dia incompleto o un rango de fechas no exacto

        """
        Si la fecha de inicio no empieza a las 00:00:00 hrs se ajusta para
        que las siguientes llamadas se hagan en bloques dinamicos dependiendo
        la frecuencia solicitada de los datos empezando a las 00:00:00 hrs.
        Si la fecha final no termina a las 00:00:00 hrs sucede algo similar,
        donde se itera en bloques dinamicos hasta llegar al ultimo dia donde
        se hace una ultima llamada desde las 00:00:00 hrs hasta el end_timestamp
        """

        temporal_start_timestamp = start_timestamp_date_format
        temporal_start_timestamp_time = start_timestamp_date_format.strftime("%H:%M:%S")

        temporal_end_timestamp = end_timestamp_date_format
        temporal_end_timestamp_time = end_timestamp_date_format.strftime("%H:%M:%S")

        limit = temporal_end_timestamp

        if temporal_start_timestamp_time != "00:00:00":
            temporal_end_timestamp = start_timestamp_date_format.replace(hour=0, minute=0, second=0, microsecond=0)
            temporal_end_timestamp += timedelta(hours=24)
        else:
            temporal_end_timestamp = temporal_start_timestamp + timedelta(hours=max_time_span)

        if temporal_end_timestamp_time != "00:00:00":
            limit = end_timestamp_date_format.replace(hour=0, minute=0, second=0, microsecond=0)

        while temporal_end_timestamp <= limit:
            # print(temporal_start_timestamp)
            # print(temporal_end_timestamp)
            # print("\n")

            # Solicitud de datos en bloques cerrados
            dinamic_start_timestamp = date_to_timestamp(temporal_start_timestamp)
            dinamic_end_timestamp = date_to_timestamp(temporal_end_timestamp)
            url = f"https://api.purpleair.com/v1/sensors/{sensor_id}/history/csv?start_timestamp={dinamic_start_timestamp}&end_timestamp={dinamic_end_timestamp}&average={period}&fields={fields}"
            response = httpRequest(url, headers)

            if response.status_code != 200:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                print(response.text)
                return

            df_aux = processResponse(response)

            # Agregando la informacion de la nueva solicitud a todos los demas datos
            df_full = pd.concat([df_full, df_aux], ignore_index=True)

            temporal_start_timestamp = temporal_end_timestamp
            temporal_end_timestamp += timedelta(hours=max_time_span)

        if temporal_start_timestamp < end_timestamp_date_format:
            # print(temporal_start_timestamp)
            # print(end_timestamp_date_format)

            # Falta hacer una ultima llamada
            dinamic_start_timestamp = date_to_timestamp(temporal_start_timestamp)
            dinamic_end_timestamp = date_to_timestamp(end_timestamp_date_format)
            url = f"https://api.purpleair.com/v1/sensors/{sensor_id}/history/csv?start_timestamp={dinamic_start_timestamp}&end_timestamp={dinamic_end_timestamp}&average={period}&fields={fields}"
            response = httpRequest(url, headers)

            if response.status_code != 200:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                print(response.text)
                return

            df_aux = processResponse(response)

            # Agregando la informacion de la nueva solicitud a todos los demas datos
            df_full = pd.concat([df_full, df_aux], ignore_index=True)

    # Agregar al dataframe una columna del municipio en string
    df_full["Source"] = municipality

    # Regresar registros al horario mexicano
    df_full["time_stamp"] = df_full["time_stamp"] - timedelta(hours=offset)

    # Ordenar registros por fecha de forma ascendente
    df_full.sort_values("time_stamp", ascending=True, inplace=True)
    df_full.reset_index(drop=True, inplace=True)


    return df_full

def getKeyInfo(api_key):
    # Desplegar número de tokens restantes en la API key después de la ejecución
    key_info_url = f"https://api.purpleair.com/v1/organization"
    key_info_headers = {"X-API-Key": api_key}

    # Mandar llamada y recibir respuesta
    response = httpRequest(key_info_url, key_info_headers).json()

    # Obtener tokens usados hasta ahora y restantes
    remaining = int(response["remaining_points"])
    used = 1000000 - remaining

    # Desplegar información
    st.write(f"Puntos usados (De 1,000,000): {used}")
    st.write(f"Restantes: {remaining}")
