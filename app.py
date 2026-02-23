import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL F.R.I.D.A.Y. (NORMA ESTRICTA) ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")

st.markdown("""
    <style>
    /* Fondo General Blanco */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Pestañas con Colores (Fondo Verde, Letra Blanca) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #004A2F !important; 
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"] { 
        color: #FFFFFF !important; 
        font-weight: bold !important;
    }
    
    /* Encabezados Verdes / Letra Blanca */
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }

    /* Cuadros: Fondo Blanco / Letra Negra / Borde Verde */
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; border-radius: 5px !important;
    }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE IA PARA EL INFORME GEO ---
def generar_conclusion_ia(total_dmcs, dia_max, hora_max):
    # Lógica de Inteligencia Artificial de F.R.I.D.A.Y.
    if total_dmcs > 25:
        return f"ALTO RIESGO. Se detecta una saturación delictual de {total_dmcs} casos. El periodo crítico se concentra los {dia_max} ({hora_max}), sugiriendo un entorno hostil para el solicitante."
    return f"RIESGO MODERADO. Se registran {total_dmcs} delitos. El análisis temporal indica mayor actividad los días {dia_max} a las {hora_max}."

# --- 3. DESPLIEGUE DE INTERFAZ ---
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_m"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Semana de estudio")
            st.text_input("Fecha de sesión")
        with c2:
            st.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm")
            st.text_input("Grado", value="C.P.R. Analista Social", key="gm")
        with f2:
            st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

with tab2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_t"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Periodo ({{ periodo }})")
            st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with col2:
            st.text_input("Asistente ({{ asistente }})")
            st.text_input("Grado ({{ grado }})")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2 = st.columns(2)
        with ft1:
            st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
            st.text_input("Grado", value="C.P.R. Analista Social", key="gt")
        with ft2:
            st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

with tab3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL (IA F.R.I.D.A.Y.)</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SUMINISTROS</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
            f_mapa = st.file_uploader("Mapa SAIT ({{ mapa }})", type=['png', 'jpg'])
        with g2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único (Detalle y Rangos)", type=['xlsx'])

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        p_ini = st.text_input("Inicio Periodo ({{ periodo_inicio }})")
        p_fin = st.text_input("Fin Periodo ({{ periodo_fin }})")

        submit_geo = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS F.R.I.D.A.Y.")

    if submit_geo:
        # Lógica de procesamiento de archivos y descarga...
        st.success("Analizando datos... F.R.I.D.A.Y. está redactando la conclusión.")