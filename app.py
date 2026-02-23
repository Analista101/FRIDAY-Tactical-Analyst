import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import io
from datetime import datetime

# Intentar importar seaborn para el mapa de calor de la Figura 3
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

# --- CONFIGURACIÓN VISUAL JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { 
        background-color: #004A2F !important; color: white; 
        padding: 10px; border-radius: 5px; font-weight: bold; 
        margin-bottom: 15px; border-left: 10px solid #C5A059; 
    }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- PESTAÑA 1: ACTA STOP MENSUAL ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_mensual_v2"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", key="m_sem")
        c1.text_input("Fecha de sesión", key="m_fec")
        c2.text_input("Compromiso Carabineros", key="m_comp")
        st.text_area("Problemática Delictual 26ª Comisaría", key="m_prob")
        st.markdown('**🖋️ PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="m_n1")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="m_g1")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="m_c1")
        st.form_submit_button("🛡️ GENERAR ACTA")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trimestral_v2"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo (Ej: Nov-Dic-Ene)", key="t_per")
        ct1.text_input("Fecha Sesión", key="t_fec")
        ct2.text_input("Nombre Asistente", key="t_as_n")
        ct2.text_input("Grado Asistente", key="t_as_g")
        st.markdown('**🖋️ PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="t_n1")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="t_g1")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="t_c1")
        st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO (CLON TANIA) ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: ESTÁNDAR TANIA GUTIÉRREZ</div>', unsafe_allow_html=True)
    if not SEABORN_AVAILABLE:
        st.warning("⚠️ Módulo de Gráficos de Calor (Seaborn) no detectado. El informe se generará sin la Figura N° 3.")
    
    with st.form("form_tania_clon_v2"):
        st.markdown("### I. DATOS DE LA SOLICITUD")
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="geo_doe")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="geo_fdoe")
        v_sol = col2.text_input("Grado y Nombre Funcionario", key="geo_sol")
        v_unid = col2.text_input("Unidad Dependiente", key="geo_uni")
        v_dom = col3.text_input("Domicilio", key="geo_dom")
        v_sub = col3.text_input("Jurisdicción (Subcomisaría)", key="geo_jur")
        
        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="geo_map")
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="geo_exc")
        st.form_submit_button("🚀 CLONAR INFORME PROFESIONAL")