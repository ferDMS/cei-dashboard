import streamlit as st
import pandas as pd

GarzaLaguera = pd.read_csv("AireNL/Serena.csv", parse_dates=["Fecha"])
Cadereyta = pd.read_csv("AireNL/Cadereyta.csv", parse_dates=["date"])
Juarez = pd.read_csv("AireNL/Juarez.csv", parse_dates=["date"])
SanNicolas = pd.read_csv("AireNL/SanNicolas.csv", parse_dates=["date"])
SanPedro = pd.read_csv("AireNL/SanPedro.csv", parse_dates=["date"])
SantaCatarina = pd.read_csv("AireNL/SantaCatarina.csv", parse_dates=["date"])

GarzaLaguera.rename(columns = {"Fecha": "date"}, inplace=True) 

Names = ["Tec Garza Laguera", "Cadereyta", "Juarez", "San Nicolas", "San Pedro", "Santa Catarina"]

Municipalities = [GarzaLaguera, Cadereyta, Juarez, SanNicolas, SanPedro, SantaCatarina]

Mun_Dict = dict(zip(Names, Municipalities))

st.markdown("# Descarga de datos")

option = st.selectbox(
    '¿De cuál lugar deseas descargar datos?',
    Names)

st.dataframe(Mun_Dict[option])

sorted_dates = Mun_Dict[option]["date"].sort_values()

f'Fechas comprendidas: {sorted_dates.iloc[0].date()} a {sorted_dates.iloc[-1].date()}'

st.download_button(f'Descargar CSV', Mun_Dict[option].to_csv(), file_name = f"{option}.csv", mime="text/csv")
