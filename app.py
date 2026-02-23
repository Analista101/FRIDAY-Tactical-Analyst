import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# 1. ESTILOS TÁCTICOS: FONDO BLANCO, LETRA NEGRA, TÍTULOS VERDES
st.markdown("""
    <style>
    /* Fondo general de la aplicación en blanco para máximo contraste */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Encabezados: FONDO VERDE / LETRA BLANCA */
    .section-header {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 20px;
        border-left: 8px solid #C5A059;
    }

    /* Subtítulos y etiquetas: FONDO BLANCO / LETRA NEGRA */
    .stApp label, .stMarkdown p, h3 { 
        color: #000000 !important; 
        font-weight: bold !important;
        background-color: #FFFFFF !important;
    }

    /* Cuadros de entrada: FONDO BLANCO / BORDE VERDE / LETRA NEGRA */
    input, textarea, .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #004A2F !important;
        border-radius: 5px !important;
    }

    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTRUCTURA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    
    with st.form("main_form_geo"):
        # I. ANTECEDENTES [cite: 10]
        st.markdown('<div class="section-header">I. ANTECEDENTES</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción ({{ jurisdiccion }})", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
        with col2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        # II. DATOS SOLICITANTE [cite: 10]
        st.markdown('<div class="section-header">II. DATOS DEL SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        # III. PERIODO Y ARCHIVOS [cite: 12, 17]
        st.markdown('<div class="section-header">III. PERIODO Y SUMINISTROS</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            v_ini = st.text_input("Inicio ({{ periodo_inicio }})")
            v_fin = st.text_input("Fin ({{ periodo_fin }})")
        with p2:
            f_mapa = st.file_uploader("Subir Mapa ({{ mapa }})", type=['png', 'jpg'])
            f_det = st.file_uploader("Excel Detalle Delictual", type=['xlsx'])
            f_cal = st.file_uploader("Excel Zona de Calor", type=['xlsx'])

        # IV. CONCLUSIÓN IA 
        st.markdown('<div class="section-header">🤖 IV. CONCLUSIÓN E INTELIGENCIA DE RIESGO</div>', unsafe_allow_html=True)
        v_concl = st.text_area("Análisis ({{ conclusion_ia }})", height=150)

        # BOTÓN DE ENVÍO OBLIGATORIO
        submit_geo = st.form_submit_button("🛡️ PROCESAR INFORME GEO-TÁCTICO")

    if submit_geo:
        st.success("Analizando datos delictuales... JARVIS calculando nivel de riesgo.")