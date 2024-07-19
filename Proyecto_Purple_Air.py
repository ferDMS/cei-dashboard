import streamlit as st

API_PA = st.Page("API_PA/Peticion.py", title="Petición de datos")

AireLNL = st.Page("Downloads/AireNL.py", title="AireLNL")

PurpleAir = st.Page("Downloads/PurpleAir.py", title="Purple Air")

Emparejados = st.Page("Downloads/Emparejamiento.py", title="Emparejados")

Introduccion = st.Page("Documentacion/Introduccion.py", title="Introduccion")

Desarrollo = st.Page("Documentacion/Desarrollo.py", title="Desarrollo")

Resultados = st.Page("Documentacion/Resultados.py", title="Resultados")

pg = st.navigation(
        {
            "Purple Air API": [API_PA],
            "Descarga de documentos": [AireLNL, PurpleAir, Emparejados],
            "Documentación": [Introduccion, Desarrollo, Resultados],
        }
    )

pg.run()