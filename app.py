import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- CONFIGURACIÓN DE INTERFAZ STARK ---
st.markdown("""
    <style>
    .section-header {
        background-color: #004A2F; color: white; padding: 10px;
        border-radius: 5px; font-weight: bold; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUCTURA DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📄 ACTA MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    st.info("Sistemas de Acta Mensual en espera.")

with tab2:
    st.info("Sistemas de Acta Trimestral en espera.")

with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    
    # IMPORTANTE: Todo el contenido debe estar dentro de este bloque 'with'
    with st.form("form_geo_stark"):
        st.subheader("I. Antecedentes del Informe")
        c1, c2 = st.columns(2)
        with c1:
            domicilio = st.text_input("Domicilio ({{ domicilio }})")
            jurisdiccion = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            doe = st.text_input("N° DOE ({{ doe }})")
        with c2:
            f_doe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            cuadrante = st.text_input("Cuadrante ({{ cuadrante }})")
            f_actual = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        st.subheader("II. Datos del Solicitante")
        s1, s2, s3 = st.columns(3)
        with s1: solicitante = st.text_input("Nombre ({{ solicitante }})")
        with s2: grado_s = st.text_input("Grado ({{ grado_solic }})")
        with s3: unidad_s = st.text_input("Unidad ({{ unidad_solic }})")

        st.subheader("III. Periodo de Análisis")
        p1, p2 = st.columns(2)
        with p1: p_inicio = st.text_input("Inicio ({{ periodo_inicio }})")
        with p2: p_fin = st.text_input("Fin ({{ periodo_fin }})")

        st.subheader("IV. Carga de Inteligencia")
        st.write("Adjunte los archivos necesarios para las Figuras N°1, 2 y 3")
        up1, up2, up3 = st.columns(3)
        with up1: 
            f_mapa = st.file_uploader("Mapa ({{ mapa }})", type=['png', 'jpg'])
        with up2: 
            f_excel_det = st.file_uploader("Excel Detalle (Tabla 1)", type=['xlsx'])
        with up3: 
            f_excel_cal = st.file_uploader("Excel Calor (Tabla 2)", type=['xlsx'])

        st.subheader("V. Análisis de Riesgo IA")
        usa_ia = st.checkbox("Activar Análisis Táctico de F.R.I.D.A.Y.", value=True)
        conclusion = st.text_area("Conclusión ({{ conclusion_ia }})", placeholder="La IA redactará aquí si el sector es de riesgo...")

        # BOTÓN DE ACCIÓN
        submit = st.form_submit_button("🛡️ GENERAR INFORME GEO")

    if submit:
        st.success("Analizando datos... procesando total_dmcs, dia_max y hora_max.")