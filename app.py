import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- CONFIGURACIÓN JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #C5A059; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- PESTAÑAS 1 Y 2 (BLINDADAS) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("f_m"):
        c1, c2 = st.columns(2); c1.text_input("Semana"); c1.text_input("Fecha Sesión"); c2.text_input("Compromiso"); st.text_area("Problemática")
        f1, f2, f3 = st.columns(3); f1.text_input("Nombre", value="DIANA SANDOVAL", key="nm"); f2.text_input("Grado", key="gm"); f3.text_input("Cargo", key="cm")
        st.form_submit_button("GENERAR")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("f_t"):
        c1, c2 = st.columns(2); c1.text_input("Periodo"); c2.text_input("Nombre Asistente"); c2.text_input("Grado Asistente")
        f1, f2, f3 = st.columns(3); f1.text_input("Nombre", value="DIANA SANDOVAL", key="nt"); f2.text_input("Grado", key="gt"); f3.text_input("Cargo", key="ct")
        st.form_submit_button("GENERAR")

# --- PESTAÑA 3: CLONACIÓN EXACTA DEL INFORME TANIA ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO DE ALTO NIVEL</div>', unsafe_allow_html=True)
    with st.form("f_clon_tania"):
        st.markdown("### I. DATOS DE LA SOLICITUD")
        c1, c2 = st.columns(2)
        v_doe = c1.text_input("DOE N°", value="247205577")
        v_fdoe = c1.text_input("Fecha DOE", value="05/02/2026")
        v_sub = c1.text_input("Subcomisaría Jurisdiccional", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA")
        
        v_sol = c2.text_input("Funcionario Solicitante (Nombre y Grado)", value="CABO 1RO. TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        v_unid = c2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        v_dom = c2.text_input("Domicilio Análisis", value="Corona Sueca Nro. 8556")
        
        c3, c4 = st.columns(2)
        v_cua = c3.text_input("Cuadrante", value="231")
        v_f_act = c4.text_input("Fecha del Informe", value="05 de febrero del año 2026")

        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx', 'csv'])
        
        st.form_submit_button("🛡️ REPLICAR ESTÁNDAR TANIA")

    # (Lógica de construcción interna optimizada para márgenes y tipos de letra Pt(10) Arial)import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- CONFIGURACIÓN JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #C5A059; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- PESTAÑAS 1 Y 2 (BLINDADAS) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("f_m"):
        c1, c2 = st.columns(2); c1.text_input("Semana"); c1.text_input("Fecha Sesión"); c2.text_input("Compromiso"); st.text_area("Problemática")
        f1, f2, f3 = st.columns(3); f1.text_input("Nombre", value="DIANA SANDOVAL", key="nm"); f2.text_input("Grado", key="gm"); f3.text_input("Cargo", key="cm")
        st.form_submit_button("GENERAR")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("f_t"):
        c1, c2 = st.columns(2); c1.text_input("Periodo"); c2.text_input("Nombre Asistente"); c2.text_input("Grado Asistente")
        f1, f2, f3 = st.columns(3); f1.text_input("Nombre", value="DIANA SANDOVAL", key="nt"); f2.text_input("Grado", key="gt"); f3.text_input("Cargo", key="ct")
        st.form_submit_button("GENERAR")

# --- PESTAÑA 3: CLONACIÓN EXACTA DEL INFORME TANIA ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO DE ALTO NIVEL</div>', unsafe_allow_html=True)
    with st.form("f_clon_tania"):
        st.markdown("### I. DATOS DE LA SOLICITUD")
        c1, c2 = st.columns(2)
        v_doe = c1.text_input("DOE N°", value="247205577")
        v_fdoe = c1.text_input("Fecha DOE", value="05/02/2026")
        v_sub = c1.text_input("Subcomisaría Jurisdiccional", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA")
        
        v_sol = c2.text_input("Funcionario Solicitante (Nombre y Grado)", value="CABO 1RO. TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        v_unid = c2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        v_dom = c2.text_input("Domicilio Análisis", value="Corona Sueca Nro. 8556")
        
        c3, c4 = st.columns(2)
        v_cua = c3.text_input("Cuadrante", value="231")
        v_f_act = c4.text_input("Fecha del Informe", value="05 de febrero del año 2026")

        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx', 'csv'])
        
        st.form_submit_button("🛡️ REPLICAR ESTÁNDAR TANIA")

    # (Lógica de construcción interna optimizada para márgenes y tipos de letra Pt(10) Arial)