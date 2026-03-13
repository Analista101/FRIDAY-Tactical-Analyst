import pandas as pd
import re
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from docx.shared import Mm
import matplotlib.pyplot as plt
import textwrap
import streamlit as st
import json
import os
import requests
import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Proyecto FRIDAY - Stark Industries", layout="wide")

# Menú Lateral Estilo Stark
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b5/Stark_Industries_logo.png", width=200)
st.sidebar.title("SISTEMA FRIDAY")

opcion = st.sidebar.radio("MÓDULOS ACTIVOS:", 
    ["Georreferenciación", "Acta Mensual", "Acta Trimestral", "Carta de Situación"])

# Enrutador de funciones
if opcion == "Georreferenciación":
    render_pestana_georreferenciacion()
elif opcion == "Acta Mensual":
    render_pestana_mensual()
elif opcion == "Acta Trimestral":
    render_pestana_trimestral()
elif opcion == "Carta de Situación":
    render_pestana_situacion()