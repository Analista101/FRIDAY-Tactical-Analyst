import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE SISTEMAS CENTRALES
st.set_page_config(page_title="PROYECTO JARVIS - 26ª COM. PUDAHUEL", page_icon="🛡️", layout="wide")

# 2. INTERFAZ VISUAL STARK INDUSTRIES (Resalte Verde)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .section-header {
        background-color: #004A2F; color: #FFFFFF !important;
        padding: 8px 15px; border-radius: 4px; display: inline-block;
        margin-bottom: 15px; font-weight: bold; text-transform: uppercase;
        border-left: 5px solid #C5A059;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        color: #000000 !important; border: 2px solid #004A2F !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    div.stButton > button {
        background-color: #004A2F !important; color: white !important;
        border: 2px solid #C5A059 !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. NÚCLEO DE PROCESAMIENTO DE DOCUMENTOS
def procesar_firma(datos):
    rt = RichText()
    rt.add(datos['n_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
    rt.add('\n')
    rt.add(datos['g_oficial'], bold=False, font='Bookman Old Style', size=22)
    rt.add('\n')
    rt.add(datos['c_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
    return rt

# 4. DESPLIEGUE DE PESTAÑAS OPERATIVAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO 1: MENSUAL ---
with tab1:
    st.markdown('<div class="section-header">📝 ACTA MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_mensual"):
        c1, c2 = st.columns(2)
        with c1:
            sem_m = st.text_input("Semana de estudio")
            fec_m = st.text_input("Fecha de sesión")
        with c2:
            comp_m = st.text_input("Compromiso Carabineros")
        prob_m = st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        n_m = st.text_input("Nombre Oficial", value="DIANA SANDOVAL ASTUDILLO", key="nm")
        btn_m = st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO 2: TRIMESTRAL ---
with tab2:
    st.markdown('<div class="section-header">📈 ANÁLISIS STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trimestral"):
        col1, col2 = st.columns(2)
        with col1:
            val_per = st.text_input("Periodo ({{ periodo }})")
            val_fec = st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with col2:
            val_asi = st.text_input("Asistente ({{ asistente }})")
            val_gra = st.text_input("Grado ({{ grado }})")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        n_t = st.text_input("Nombre Oficial", value="DIANA SANDOVAL ASTUDILLO", key="nt")
        btn_t = st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO 3: INFORME GEO (RESTAURADO) ---
with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_stark"):
        # I. Antecedentes del Informe
        st.markdown('<div class="section-header">I. ANTECEDENTES DEL INFORME</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            domicilio = st.text_input("Domicilio ({{ domicilio }})")
            jurisdiccion = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            doe = st.text_input("N° DOE ({{ doe }})")
        with g2:
            f_doe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            cuadrante = st.text_input("Cuadrante ({{ cuadrante }})")
            f_actual = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        # II. Datos del Solicitante
        st.markdown('<div class="section-header">II. DATOS DEL SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: solicitante = st.text_input("Nombre ({{ solicitante }})")
        with s2: grado_s = st.text_input("Grado ({{ grado_solic }})")
        with s3: unidad_s = st.text_input("Unidad ({{ unidad_solic }})")

        # III. Periodo de Análisis
        st.markdown('<div class="section-header">III. PERIODO DE ANÁLISIS</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: p_inicio = st.text_input("Inicio ({{ periodo_inicio }})")
        with p2: p_fin = st.text_input("Fin ({{ periodo_fin }})")

        # IV. Carga de Inteligencia
        st.markdown('<div class="section-header">📊 IV. CARGA DE MAPA Y EXCEL</div>', unsafe_allow_html=True)
        up1, up2, up3 = st.columns(3)
        with up1: f_mapa = st.file_uploader("Mapa ({{ mapa }})", type=['png', 'jpg'])
        with up2: f_det = st.file_uploader("Excel Detalle (Tabla 1)", type=['xlsx'])
        with up3: f_cal = st.file_uploader("Excel Calor (Tabla 2)", type=['xlsx'])

        # V. Conclusión IA
        st.markdown('<div class="section-header">🤖 V. ANÁLISIS DE RIESGO IA</div>', unsafe_allow_html=True)
        activar_ia = st.checkbox("Activar Conclusión Inteligente de JARVIS", value=True)
        conclusion_ia = st.text_area("Resultado del Análisis", placeholder="JARVIS determinará el nivel de riesgo aquí...")

        btn_geo = st.form_submit_button("🛡️ PROCESAR INFORME GEO")