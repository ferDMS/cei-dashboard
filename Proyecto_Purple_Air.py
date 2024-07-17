import streamlit as st

AireLNL = st.Page("Downloads/AireNL.py", title="AireLNL", icon=":material/dashboard:")

PurpleAir = st.Page("downloads/PurpleAir.py", title="Purple Air", icon=":material/dashboard:")

Emparejados = st.Page("downloads/Emparejamiento.py", title="Emparejados", icon=":material/dashboard:")

pg = st.navigation(
        {
            "Descarga de documentos": [AireLNL, PurpleAir, Emparejados],
        }
    )

pg.run()