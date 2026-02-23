import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# 1. PROTOCOLO DE VISUALIZACIÓN (NORMA: FONDO BLANCO / LETRA NEGRA / TÍTULO VERDE)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .section-header {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #004A2F !important;
        border-radius: 5px !important;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    div.stButton > button {
        background-color: #004A2F !important; color: white !important;
        border: 2px solid #C5A059 !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO 1: ACTA MENSUAL (RESTAURADO) ---
with tab1:
    st.markdown('<div class="section-header">📝 FORMULARIO ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_mensual_final"):
        m1, m2 = st.columns(2)
        with m1:
            semana = st.text_input("Semana de estudio")
            fecha_sesion = st.text_input("Fecha de sesión")
        with m2:
            compromiso = st.text_input("Compromiso Carabineros")
        problematica = st.text_area("Problemática Delictual detectada")
        
        st.markdown('<div class="section-header">🖋️ FIRMA RESPONSABLE</div>', unsafe_allow_html=True)
        f_nom = st.text_input("Nombre Oficial", value="DIANA SANDOVAL ASTUDILLO")
        f_gra = st.text_input("Grado Oficial", value="C.P.R. Analista Social")
        
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO 2: STOP TRIMESTRAL (RESTAURADO) ---
with tab2:
    st.markdown('<div class="section-header">📈 FORMULARIO STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trimestral_final"):
        t1, t2 = st.columns(2)
        with t1:
            periodo_t = st.text_input("Periodo ({{ periodo }})")
            fecha_t = st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with t2:
            asistente_t = st.text_input("Asistente ({{ asistente }})")
            grado_t = st.text_input("Grado ({{ grado }})")
        
        st.markdown('<div class="section-header">🖋️ FIRMA RESPONSABLE</div>', unsafe_allow_html=True)
        f_nom_t = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
        
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO 3: INFORME GEO (MANTENIDO) ---
with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        st.markdown('<div class="section-header">I. ANTECEDENTES</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
        with g2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        st.markdown('<div class="section-header">II. DATOS DEL SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        st.markdown('<div class="section-header">III. PERIODO Y SUMINISTROS</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            v_ini = st.text_input("Inicio ({{ periodo_inicio }})")
            v_fin = st.text_input("Fin ({{ periodo_fin }})")
        with p2:
            f_mapa = st.file_uploader("Subir Mapa ({{ mapa }})", type=['png', 'jpg'])
            f_det = st.file_uploader("Excel Detalle (Tabla 1)", type=['xlsx'])
            f_cal = st.file_uploader("Excel Calor (Tabla 2)", type=['xlsx'])

        st.markdown('<div class="section-header">🤖 IV. CONCLUSIÓN IA</div>', unsafe_allow_html=True)
        v_concl = st.text_area("Conclusión ({{ conclusion_ia }})")

        st.form_submit_button("🛡️ PROCESAR INFORME GEO")