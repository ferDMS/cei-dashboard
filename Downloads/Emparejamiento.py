import streamlit as st
import pandas as pd

SanNicolas = pd.read_csv("Emparejados/SanNicolas2023_full.csv", parse_dates=["time_stamp"])
SantaCatarina = pd.read_csv("Emparejados/SantaCatarina2023_full.csv", parse_dates=["time_stamp"])
SanPedro = pd.read_csv("Emparejados/sanpedro_emparejado.csv", parse_dates=["date"])
Juarez = pd.read_csv("Emparejados/juarez_emparejado.csv", parse_dates=["date"])
Cadereyta = pd.read_csv("Emparejados/cadereyta_emparejado.csv", parse_dates=["date"])
Apodaca = pd.read_csv("Emparejados/apodaca_emparejado.csv", parse_dates=["date"])

SanPedro.rename(columns = {"date": "time_stamp"}, inplace=True) 
Juarez.rename(columns = {"date": "time_stamp"}, inplace=True) 
Cadereyta.rename(columns = {"date": "time_stamp"}, inplace=True) 
Apodaca.rename(columns = {"date": "time_stamp"}, inplace=True) 

Municipalities = [SanNicolas, SantaCatarina, SanPedro, Juarez, Cadereyta, Apodaca]
Names = ["San Nicolas", "Santa Catarina", "Juarez", "San Pedro", "Cadereyta", "Apodaca"]

Mun_Dict = dict(zip(Names, Municipalities))

st.markdown("# Descarga de datos")

option = st.selectbox(
    '¿De cuál lugar deseas descargar datos?',
    Names)

st.dataframe(Mun_Dict[option])

sorted_dates = Mun_Dict[option]["time_stamp"].sort_values()

f'Fechas comprendidas: {sorted_dates.iloc[0].date()} a {sorted_dates.iloc[-1].date()}'

st.download_button(f'Descargar CSV', Mun_Dict[option].to_csv(), file_name = f"{option}.csv", mime="text/csv")
