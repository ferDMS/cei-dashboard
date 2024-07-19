import streamlit as st
import pandas as pd

st.markdown("# Introduccion")

st.markdown(
    """El cómite ecológico integral es un grupo cuyo propósito es trabajar a favor de la calidad del aire del entorno. Actualmente, uno de los proyectos que se están realizando 
    con relación a este propósito es la predicción de la calidad del aire en la Zona metropolitana de Monterrey mediante el uso de sensores (Purple Air's) que, por el momento, se
    ubican en: Santa Catarina, San Pedro, San Nicolás, Apodaca, Juárez, Cadereyta y en la Prepa Tec Eugenio Garza Lagüera.""")

st.write(
    """Se dispone de una página que permite conocer la calidad del aire con cercanía a estas ubicaciones, la cual usa fórmulas pre-esteblecidas (Factores de conversión) que se aplican
    a los datos recabados por los sensores para hacer las predicciones correspondientes. A continuación, se puede observar el apartado donde se da a detalle estos factores de 
    conversión junto con otros parámetros:
    """)

st.image('Images/Purple_Air_Map.png', caption='Contenido de la página de Purple Air')