import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import branca
from streamlit_folium import folium_static

data = gpd.read_file("Nuevo_Leon.json")
data.rename(columns = {"NAME_2": "Municipio"}, inplace = True)
data.query(" `Municipio` in ['Santa Catarina',\
                          'San Nicolás de los Garza',\
                          'San Pedro Garza García',\
                          'Juárez',\
                          'Apodaca']", inplace = True)

errores = {
    'Santa Catarina': 4.88,
    'San Nicolás de los Garza': 7.27,
    'San Pedro Garza García': 4.88,
    'Juárez': 6.22,
    'Apodaca': 7.27
}

grado = {
    'Santa Catarina': 2,
    'San Nicolás de los Garza': 2,
    'San Pedro Garza García': 2,
    'Juárez': 2,
    'Apodaca': 2
}

data['Error Modelo MAE (µg/m3)'] = data['Municipio'].map(errores)
data['Grado del modelo'] = data['Municipio'].map(grado)# Crear la paleta de colores lineal con branca
colormap = branca.colormap.LinearColormap(
    vmin=data["Error Modelo MAE (µg/m3)"].min(),
    vmax=data["Error Modelo MAE (µg/m3)"].max(),
    colors=["green", "yellow", "red"],
    caption="Error Modelo MAE (µg/m3)"
)


m = folium.Map([25.7,-100.3], zoom_start=10) # dragging=False, scrollWheelZoom=False, doubleClickZoom=False, zoomControl=False

popup = folium.GeoJsonPopup(
    fields=["Error Modelo MAE (µg/m3)", "Grado del modelo"],
    localize=True,
    labels=True)
        
tooltip = folium.GeoJsonTooltip(
    fields=["Municipio"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800)

g = folium.GeoJson(
    data,
    tooltip=tooltip,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["Error Modelo MAE (µg/m3)"]),
        "color": "black",
        "fillOpacity": 0.3,
    },
    highlight_function=lambda x: {
        "fillColor": "dark_grey",
    },
    popup=popup,
    popup_keep_highlighted=True,
).add_to(m)

colormap.add_to(m)

st.markdown("# Resultados")

st.subheader("Precisión en las predicciones")
folium_static(m, width=800, height=800)