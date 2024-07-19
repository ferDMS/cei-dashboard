import streamlit as st

API_PA = st.Page("API_PA/Peticion.py", title="Petición de datos")

AireLNL = st.Page("Downloads/AireNL.py", title="AireLNL")

PurpleAir = st.Page("Downloads/PurpleAir.py", title="Purple Air")

Emparejados = st.Page("Downloads/Emparejamiento.py", title="Emparejados")

Modelo = st.Page("Mejor_Modelo/Analisis.py", title="Análisis")

pg = st.navigation(
        {
            "Purple Air API": [API_PA],
            "Descarga de documentos": [AireLNL, PurpleAir, Emparejados],
            "Resultados Finales": [Modelo],
        }
    )

pg.run()