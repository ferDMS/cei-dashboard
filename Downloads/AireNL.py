import streamlit as st
import pandas as pd

GarzaLaguera = pd.read_csv("AireNL/Serena.csv", parse_dates=["Fecha"])

Names = ["Tec Garza Laguera"]
Municipalities = [GarzaLaguera]

Mun_Dict = dict(zip(Names, Municipalities))

st.markdown("# Descarga de datos")

option = st.selectbox(
    '¿De cuál lugar deseas descargar datos?',
    Names)

st.dataframe(Mun_Dict[option])

sorted_dates = Mun_Dict[option]["Fecha"].sort_values()

f'Fechas comprendidas: {sorted_dates.iloc[0].date()} a {sorted_dates.iloc[-1].date()}'

st.download_button(f'Descargar CSV', Mun_Dict[option].to_csv(), file_name = f"{option}.csv", mime="text/csv")
