import streamlit as st
import pandas as pd

SanNicolas = pd.read_csv("SanNicolas2023_full.csv")
SantaCatarina = pd.read_csv("SantaCatarina2023_full.csv")
SanPedro = pd.read_csv("sanpedro_emparejado.csv")
Juarez = pd.read_csv("juarez_emparejado.csv")
Cadereyta = pd.read_csv("cadereyta_emparejado.csv")
Apodaca = pd.read_csv("apodaca_emparejado.csv")

Municipalities = [SanNicolas, SantaCatarina, SanPedro, Juarez, Cadereyta, Apodaca]
Names = ["San Nicolas", "Santa Catarina", "Juarez", "San Pedro", "Cadereyta", "Apodaca"]

Mun_Dict = dict(zip(Names, Municipalities))

st.markdown("# Descarga de datos")

option = st.selectbox(
    '¿De cuál municipio deseas descargar datos?',
    Names)

st.download_button(f'Descargar CSV', Mun_Dict[option].to_csv(), file_name = f"{option}.csv", mime="text/csv")
