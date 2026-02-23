import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL BLINDADO (VERDE OPACO / LETRA NEGRA) ---
st.set_page_config(page_title="PROJECT JARVIS", layout="wide")
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
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 2px solid #004A2F !important; 
    }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVEGACIÓN DE SISTEMAS ---
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO: ACTA STOP MENSUAL (RESTAURACIÓN TOTAL) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_mensual_completo"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Semana de estudio")
            st.text_input("Fecha de sesión")
        with c2:
            st.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('<div class="section-header">🖋️ PIE DE FIRMA</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3) # Restaurado a tres columnas
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_m_f")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="g_m_f")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_m_f")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO: STOP TRIMESTRAL (RESTAURACIÓN TOTAL) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trimestral_completo"):
        ct1, ct2 = st.columns(2)
        with ct1:
            st.text_input("Periodo ({{ periodo }})")
            st.text_input("Fecha Sesión ({{ fecha_sesion }})")
        with ct2:
            st.text_input("Nombre Asistente", key="asist_nom") # RE-INCIDIDO
            st.text_input("Grado Asistente", key="asist_gra")   # RE-INCIDIDO
            
        st.markdown('<div class="section-header">🖋️ PIE DE FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2, ft3 = st.columns(3) # Restaurado a tres columnas
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_t_f")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="g_t_f")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_t_f")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO: INFORME GEO (IDENTIDADES SEPARADAS) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        st.markdown('### I. ANTECEDENTES DEL SOLICITANTE')
        g1, g2 = st.columns(2)
        v_dom = g1.text_input("Domicilio Solicitante ({{ domicilio }})")
        v_doe = g1.text_input("N° DOE ({{ doe }})")
        v_fdoe = g2.text_input("Fecha DOE ({{ fecha_doe }})")
        v_cua = g2.text_input("Cuadrante ({{ cuadrante }})")
        
        st.markdown('### II. PERIODO Y SOLICITANTE')
        p1, p2, p3 = st.columns(3)
        v_ini = p1.text_input("Inicio Periodo")
        v_fin = p1.text_input("Fin Periodo")
        v_sol = p2.text_input("Nombre Solicitante")
        v_gs = p2.text_input("Grado Solicitante")
        v_us = p3.text_input("Unidad Solicitante")
        v_fact = p3.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
        
        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx'])

        st.markdown('### III. FIRMA RESPONSABLE (DIANA SANDOVAL)')
        rf1, rf2 = st.columns(2)
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel, engine='openpyxl')
            total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicicion': v_dom, 'doe': v_doe, 'fecha_doe': v_fdoe, 'cuadrante': v_cua,
                'periodo_inicio': v_ini, 'periodo_fin': v_fin, 'solicitante': v_sol,
                'grado_solic': v_gs, 'unidad_solic': v_us, 'fecha_actual': v_fact,
                'total_dmcs': total, 'dia_max': "VIERNES", 'hora_max': "20:00 - 23:59",
                'conclusion_ia': f"Escenario de riesgo con {total} eventos detectados.",
                'tabla_delitos': df.to_dict(orient='records'),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5))
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name="Informe_GEO.docx")
        except Exception as e: st.error(f"Fallo: {e}")