import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# 1. ESTILO STARK: Fondo gris claro, inputs blancos con borde verde
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6 !important; }
    .section-header {
        background-color: #004A2F; color: #FFFFFF !important;
        padding: 8px 15px; border-radius: 4px; display: inline-block;
        margin-bottom: 15px; font-weight: bold; text-transform: uppercase;
        border-left: 5px solid #C5A059;
    }
    input, textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #004A2F !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    
    # Iniciamos el formulario
    with st.form("main_form_geo"):
        st.subheader("I. ANTECEDENTES")
        col1, col2 = st.columns(2)
        with col1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción ({{ jurisdiccion }})", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
        with col2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        st.subheader("II. DATOS DEL SOLICITANTE")
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        st.subheader("III. PERIODO Y ARCHIVOS")
        p1, p2 = st.columns(2)
        with p1:
            v_ini = st.text_input("Inicio ({{ periodo_inicio }})")
            v_fin = st.text_input("Fin ({{ periodo_fin }})")
        with p2:
            f_mapa = st.file_uploader("Subir Mapa ({{ mapa }})", type=['png', 'jpg'])
            f_det = st.file_uploader("Excel Detalle (Tabla 1)", type=['xlsx'])
            f_cal = st.file_uploader("Excel Calor (Tabla 2)", type=['xlsx'])

        st.subheader("IV. CONCLUSIÓN IA")
        v_concl = st.text_area("Análisis ({{ conclusion_ia }})")

        # BOTÓN DE ENVÍO DENTRO DEL FORMULARIO
        submit_button = st.form_submit_button("🛡️ PROCESAR INFORME GEO")

    if submit_button:
        if f_det and f_cal:
            st.success("Sistemas sincronizados. Analizando datos delictuales...")
        else:
            st.warning("Señor, el análisis requiere ambos archivos Excel para proceder.")