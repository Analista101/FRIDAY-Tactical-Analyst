import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE SISTEMAS
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")

# 2. ESTILO TÁCTICO: CUADROS BLANCOS, BORDES VERDES
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6 !important; }
    /* Encabezados de sección verdes */
    .section-header {
        background-color: #004A2F; color: #FFFFFF !important;
        padding: 8px 15px; border-radius: 4px; display: inline-block;
        margin-bottom: 15px; font-weight: bold; text-transform: uppercase;
        border-left: 5px solid #C5A059;
    }
    /* CONFIGURACIÓN DE LOS INPUTS: Fondo blanco, borde verde, texto negro */
    .stTextInput>div>div>input, .stTextArea>div>textarea, .stDateInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #004A2F !important;
        border-radius: 5px !important;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    
    /* Botones */
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important; color: white !important;
        border: 2px solid #C5A059 !important; font-weight: bold !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ OPERATIVA
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO 1: MENSUAL ---
with tab1:
    st.markdown('<div class="section-header">📝 ACTA MENSUAL</div>', unsafe_allow_html=True)
    with st.form("m1"):
        c1, c2 = st.columns(2)
        with c1:
            sem_m = st.text_input("Semana de estudio")
            fec_m = st.text_input("Fecha de sesión")
        with c2:
            comp_m = st.text_input("Compromiso Carabineros")
        prob_m = st.text_area("Problemática Delictual 26ª Comisaría")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO 2: TRIMESTRAL ---
with tab2:
    st.markdown('<div class="section-header">📈 ANÁLISIS STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("m2"):
        c1, c2 = st.columns(2)
        with c1:
            v_per = st.text_input("Periodo ({{ periodo }})")
            v_fec = st.text_input("Fecha Sesión")
        with c2:
            v_asi = st.text_input("Asistente")
            v_gra = st.text_input("Grado")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO 3: INFORME GEO (VISIBILIDAD MEJORADA) ---
with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("m3"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SOLICITANTE</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})") [cite: 3, 10]
            v_jur = st.text_input("Jurisdicción ({{ jurisdiccion }})", value="26ª COM. PUDAHUEL") [cite: 3, 13]
            v_doe = st.text_input("N° DOE ({{ doe }})") [cite: 10]
        with g2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})") [cite: 10]
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})") [cite: 13]
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y')) [cite: 4, 8]

        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre Solicitante ({{ solicitante }})") [cite: 10]
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})") [cite: 10]
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})") [cite: 10]

        st.markdown('<div class="section-header">🗓️ II. PERIODO Y SUMINISTROS</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: 
            v_ini = st.text_input("Inicio ({{ periodo_inicio }})") [cite: 12]
            v_fin = st.text_input("Fin ({{ periodo_fin }})") [cite: 12]
        with p2:
            f_mapa = st.file_uploader("Subir Mapa ({{ mapa }})", type=['png', 'jpg']) [cite: 17]
            f_det = st.file_uploader("Excel Detalle Delictual", type=['xlsx']) [cite: 21]
            f_cal = st.file_uploader("Excel Zona de Calor", type=['xlsx']) [cite: 24]

        st.markdown('<div class="section-header">🤖 III. ANÁLISIS DE RIESGO IA</div>', unsafe_allow_html=True)
        v_concl = st.text_area("Conclusión ({{ conclusion_ia }})") [cite: 27]
        
        btn_geo = st.form_submit_button("🛡️ PROCESAR INFORME GEO")