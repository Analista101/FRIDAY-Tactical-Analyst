import streamlit as st

# Importamos las funciones desde sus respectivos archivos
from pestana_geo import render_pestana_georreferenciacion
from pestana_cartasituacion import render_pestana_situacion

st.set_page_config(page_title="Proyecto JARVIS", layout="wide")

st.title("SISTEMA DE INTELIGENCIA FRIDAY")

# Selector de Pestañas
tabs = st.tabs(["GEORREFERENCIACIÓN", "CARTA DE SITUACIÓN", "CONFIGURACIÓN"])

with tabs[0]:
    # Llama a la lógica que está en pestana_geo.py
    render_pestana_georreferenciacion()

with tabs[1]:
    # Llama a la lógica que está en pestana_cartasituacion.py
    render_pestana_situacion()

with tabs[2]:
    st.write("Configuraciones del sistema Stark.")