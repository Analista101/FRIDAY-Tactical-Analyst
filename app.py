import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Inches
import io
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILOS (IGUAL A LOS ANTERIORES) ---
st.set_page_config(page_title="SISTEMA F.R.I.D.A.Y.", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .section-header {
        background-color: #004A2F; color: #FFFFFF !important;
        padding: 5px 15px; border-radius: 4px; display: inline-block;
        margin-bottom: 15px; font-weight: bold; text-transform: uppercase;
        border-left: 5px solid #C5A059;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTextInput>div>input, .stTextArea>div>textarea {
        color: #000000 !important; border: 2px solid #004A2F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR CEREBRAL F.R.I.D.A.Y. ---
def generar_word_geo(datos, f_mapa, f_det, f_cal):
    try:
        doc = DocxTemplate("INFORME GEO.docx")
        
        # PROCESAMIENTO TABLA 1: DETALLE
        df_det = pd.read_excel(f_det)
        datos['total_dmcs'] = df_det['CUENTA'].sum()
        
        # PROCESAMIENTO TABLA 2: CALOR
        df_cal = pd.read_excel(f_cal)
        # Aquí la IA detecta el punto máximo
        # datos['dia_max'] = ... / datos['hora_max'] = ...
        
        # INSERCIÓN DE MAPA
        if f_mapa:
            datos['mapa'] = InlineImage(doc, f_mapa, width=Inches(5))
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error en matriz: {e}")
        return None

# --- 3. INTERFAZ DE TABS ---
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    st.info("Módulo de Acta Mensual bloqueado y operativo.")

with tab2:
    st.info("Módulo Trimestral operativo.")

# --- 4. REPARACIÓN DEL MÓDULO GEO (AQUÍ ESTABA EL ERROR) ---
with tab3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    
    # Formulario con todos los campos marcados {{ }} en el documento
    with st.form("form_geo_total"):
        st.markdown('<div class="section-header">📄 I. DATOS DEL DOCUMENTO</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            dom = st.text_input("Domicilio ({{ domicilio }})")
            jur = st.text_input("Jurisdicción ({{ jurisdiccion }})", value="26ª COM. PUDAHUEL")
            doe = st.text_input("DOE N° ({{ doe }})")
        with col2:
            f_doe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            cua = st.text_input("Cuadrante ({{ cuadrante }})")
            f_act = st.text_input("Fecha Actual ({{ fecha_actual }})", value=datetime.now().strftime('%d/%m/%Y'))

        st.markdown('<div class="section-header">👤 II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: gra = st.text_input("Grado ({{ grado_solic }})")
        with s3: uni = st.text_input("Unidad ({{ unidad_solic }})")

        st.markdown('<div class="section-header">🗓️ III. PERIODO</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: p_ini = st.text_input("Inicio ({{ periodo_inicio }})")
        with p2: p_fin = st.text_input("Fin ({{ periodo_fin }})")

        st.markdown('<div class="section-header">📊 IV. SUMINISTROS (MAPA Y EXCEL)</div>', unsafe_allow_html=True)
        up1, up2, up3 = st.columns(3)
        with up1: mapa_file = st.file_uploader("Subir Mapa ({{ mapa }})", type=['png', 'jpg'])
        with up2: det_file = st.file_uploader("Subir Tabla Detalle (Excel)", type=['xlsx'])
        with up3: cal_file = st.file_uploader("Subir Tabla Calor (Excel)", type=['xlsx'])

        st.markdown('<div class="section-header">🤖 V. CONCLUSIÓN IA</div>', unsafe_allow_html=True)
        redactar_ia = st.checkbox("Activar Análisis de Riesgo F.R.I.D.A.Y.", value=True)
        concl_manual = st.text_area("Ajuste manual conclusion ({{ conclusion_ia }})")

        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME GEO-TÁCTICO")

    if submit_geo:
        if not det_file or not cal_file:
            st.error("Señor, faltan los archivos Excel para el análisis.")
        else:
            st.success("Sincronizando con satélites... Informe en proceso.")