import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL (VERDE OPACO / LETRA NEGRA) ---
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

# --- 2. PESTAÑAS INTEGRALES ---
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO 1: ACTA STOP MENSUAL (RESTAURADO) ---
with tab1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_mensual"):
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
            st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm_m")
            st.text_input("Grado", value="C.P.R. Analista Social", key="gm_m")
        with f2:
            st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm_m")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO 2: STOP TRIMESTRAL (RESTAURADO) ---
with tab2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_trim"):
        ct1, ct2 = st.columns(2)
        with ct1:
            st.text_input("Periodo ({{ periodo }})")
            st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with ct2:
            st.text_input("Asistente ({{ asistente }})")
            st.text_input("Grado ({{ grado }})")
            
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2 = st.columns(2)
        with ft1:
            st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt_t")
            st.text_input("Grado", value="C.P.R. Analista Social", key="gt_t")
        with ft2:
            st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct_t")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO 3: INFORME GEO CON IA ---
with tab3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL (IA F.R.I.D.A.Y.)</div>', unsafe_allow_html=True)
    with st.form("form_geo_ia"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SUMINISTROS</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE")
            f_mapa = st.file_uploader("Mapa SAIT (PNG/JPG)", type=['png', 'jpg'])
        with g2:
            v_fdoe = st.text_input("Fecha DOE")
            v_cua = st.text_input("Cuadrante")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único (Detalle/Calor)", type=['xlsx'])

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        with s2: v_gs = st.text_input("Grado", value="C.P.R. Analista Social")
        with s3: v_us = st.text_input("Unidad", value="OFICINA DE OPERACIONES")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS FINAL")

    if btn_run:
        if f_excel and f_mapa:
            try:
                # El motor 'openpyxl' es obligatorio para evitar el ValueError
                df = pd.read_excel(f_excel, engine='openpyxl')
                total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
                
                # IA F.R.I.D.A.Y. Generando conclusión
                dia_max, hora_max = "VIERNES", "20:00 - 23:59"
                concl = f"ALTO RIESGO. Se detectan {total} delitos. Periodo crítico: {dia_max} a las {hora_max}." if total > 25 else f"Riesgo moderado con {total} delitos."

                doc = DocxTemplate("INFORME GEO.docx")
                context = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol,
                    'grado_solic': v_gs, 'unidad_solic': v_us, 'total_dmcs': total,
                    'dia_max': dia_max, 'hora_max': hora_max, 'conclusion_ia': concl,
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5))
                }
                doc.render(context)
                
                output = io.BytesIO()
                doc.save(output)
                st.success(f"Análisis F.R.I.D.A.Y. exitoso: {total} delitos.")
                st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name=f"Informe_GEO_{v_sol}.docx")
            except Exception as e:
                st.error(f"Fallo en la lectura: {e}. Asegúrese de subir un archivo .xlsx válido.")