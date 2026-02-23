import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL: VERDE OPACO / LETRA NEGRA ---
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
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; 
    }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO: ACTA STOP MENSUAL (PIE DE FIRMA COMPLETO) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_m"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio")
        c1.text_input("Fecha de sesión")
        c2.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        st.markdown('<div class="section-header">🖋️ PIE DE FIRMA</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm1")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="gm1")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm1")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- MÓDULO: STOP TRIMESTRAL (ASISTENTE Y PIE DE FIRMA COMPLETO) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_t"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo ({{ periodo }})")
        ct1.text_input("Fecha Sesión")
        ct2.text_input("Nombre Asistente") # RESTAURADO
        ct2.text_input("Grado Asistente")   # RESTAURADO
        st.markdown('<div class="section-header">🖋️ PIE DE FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt1")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="gt1")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct1")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- MÓDULO: INFORME GEO (IDENTIDADES SEPARADAS Y ERROR FIX) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_fix"):
        st.markdown('### I. ANTECEDENTES Y SOLICITANTE')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio ({{ domicilio }})")
        v_jur = g1.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
        v_doe = g2.text_input("N° DOE")
        v_fdoe = g2.text_input("Fecha DOE")
        v_cua = g3.text_input("Cuadrante")
        v_fact = g3.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
        
        st.markdown('### II. PERIODO Y DATOS DEL SOLICITANTE')
        p1, p2, p3 = st.columns(3)
        v_ini = p1.text_input("Inicio Periodo")
        v_fin = p1.text_input("Fin Periodo")
        v_sol = p2.text_input("Nombre Solicitante")
        v_gsol = p2.text_input("Grado Solicitante")
        v_unid = p3.text_input("Unidad Solicitante")

        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel Delitos", type=['xlsx'])

        st.markdown('### III. PIE DE FIRMA RESPONSABLE')
        rf1, rf2, rf3 = st.columns(3) # AHORA CON TRES CUADROS
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS FINAL")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel, engine='openpyxl')
            total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
            
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol,
                'grado_solic': v_gsol, 'unidad_solic': v_unid, 'periodo_inicio': v_ini,
                'periodo_fin': v_fin, 'total_dmcs': total, 'dia_max': "VIERNES",
                'hora_max': "20:00 - 23:59", 'conclusion_ia': f"Escenario detectado con {total} delitos.",
                'tabla_delitos': df.to_dict(orient='records'),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5))
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Análisis exitoso.")
            st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name=f"Informe_GEO_{v_sol}.docx")
        except Exception as e:
            st.error(f"Fallo técnico: {e}. Revise que en el Word no haya puntos dentro de las llaves.")