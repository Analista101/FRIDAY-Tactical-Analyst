import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# 1. PROTOCOLO DE VISUALIZACIÓN STARK (CONTRASTE MÁXIMO)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, .stTextInput>div>div>input {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; border-radius: 5px !important;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO 1: MENSUAL (RESTAURADO) ---
with tab1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_m"):
        c1, c2 = st.columns(2)
        with c1:
            sem_m = st.text_input("Semana de estudio")
            fec_m = st.text_input("Fecha de sesión")
        with c2:
            comp_m = st.text_input("Compromiso Carabineros")
        prob_m = st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            n_m = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm")
            g_m = st.text_input("Grado", value="C.P.R. Analista Social", key="gm")
        with f2:
            c_m = st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO 2: TRIMESTRAL (RESTAURADO) ---
with tab2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_t"):
        col1, col2 = st.columns(2)
        with col1:
            per_t = st.text_input("Periodo ({{ periodo }})")
            fec_t = st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with col2:
            asi_t = st.text_input("Asistente ({{ asistente }})")
            gra_t = st.text_input("Grado ({{ grado }})")
            
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2 = st.columns(2)
        with ft1:
            n_t = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
            g_t = st.text_input("Grado", value="C.P.R. Analista Social", key="gt")
        with ft2:
            c_t = st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO 3: INFORME GEO (CORREGIDO) ---
with tab3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
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

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        st.markdown('<div class="section-header">III. SUMINISTROS</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            v_ini = st.text_input("Inicio ({{ periodo_inicio }})")
            v_fin = st.text_input("Fin ({{ periodo_fin }})")
        with p2:
            f_mapa = st.file_uploader("Mapa ({{ mapa }})", type=['png', 'jpg'])
            f_det = st.file_uploader("Excel Detalle", type=['xlsx'])
            f_cal = st.file_uploader("Excel Calor", type=['xlsx'])

        st.markdown('<div class="section-header">🤖 IV. CONCLUSIÓN IA</div>', unsafe_allow_html=True)
        v_concl = st.text_area("Conclusión ({{ conclusion_ia }})")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        fg1, fg2 = st.columns(2)
        with fg1:
            n_g = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="ng")
            g_g = st.text_input("Grado", value="C.P.R. Analista Social", key="gg")
        with fg2:
            c_g = st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cg")

        st.form_submit_button("🛡️ PROCESAR INFORME GEO")