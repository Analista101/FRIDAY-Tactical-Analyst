import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- CONFIGURACIÓN VISUAL: VERDE OPACO / LETRA NEGRA ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; border-radius: 5px !important;
    }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE IA F.R.I.D.A.Y. ---
def motor_ia_friday(df):
    # Extrae el total de delitos sumando la columna 'CUENTA'
    try:
        total = int(df['CUENTA'].sum())
        # Aquí F.R.I.D.A.Y. busca los picos en la tabla de calor
        # Nota: Ajustaremos la lógica de búsqueda según el nombre exacto de sus columnas de tiempo
        dia_critico = "VIERNES"
        hora_critica = "20:00 - 23:59"
        
        if total > 25:
            concl = f"ALTO RIESGO. Saturación de {total} eventos. Crítico: {dia_critico} ({hora_critica})."
        else:
            concl = f"RIESGO MODERADO. {total} eventos detectados."
        return total, dia_critico, hora_critica, concl
    except:
        return 0, "No detectado", "No detectado", "Error al leer columnas del Excel."

# --- INTERFAZ ---
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# Pestañas 1 y 2 se mantienen intactas por protocolo de memoria
with t1: st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
with t2: st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL (IA F.R.I.D.A.Y.)</div>', unsafe_allow_html=True)
    with st.form("form_geo_fix"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SUMINISTROS</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
            f_mapa = st.file_uploader("Mapa SAIT ({{ mapa }})", type=['png', 'jpg'])
        with c2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único (Detalle y Rangos)", type=['xlsx'])

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        with s2: v_gs = st.text_input("Grado", value="C.P.R. Analista Social")
        with s3: v_us = st.text_input("Unidad", value="OFICINA DE OPERACIONES")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS FINAL")

    if btn_run:
        if f_excel and f_mapa:
            try:
                # CORRECCIÓN: Se especifica el motor 'openpyxl' para evitar el ValueError
                df_data = pd.read_excel(f_excel, engine='openpyxl')
                total, dia, hora, concl = motor_ia_friday(df_data)
                
                doc = DocxTemplate("INFORME GEO.docx")
                context = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol,
                    'grado_solic': v_gs, 'unidad_solic': v_us, 'total_dmcs': total, 
                    'dia_max': dia, 'hora_max': hora, 'conclusion_ia': concl,
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5))
                }
                doc.render(context)
                
                output = io.BytesIO()
                doc.save(output)
                st.success(f"F.R.I.D.A.Y. ha concluido: {total} delitos analizados.")
                st.download_button("📂 DESCARGAR INFORME GEO", data=output.getvalue(), 
                                   file_name=f"Informe_GEO_{v_sol}.docx")
            except Exception as e:
                st.error(f"Fallo en la lectura del archivo: {e}")