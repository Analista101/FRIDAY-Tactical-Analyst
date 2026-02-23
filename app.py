import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- ESTILO VISUAL JARVIS ---
st.set_page_config(page_title="PROJECT JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px;
    }
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; color: #000000 !important;
    }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- (Pestañas 1 y 2 se mantienen bloqueadas y completas por protocolo) ---

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        # Secciones I y II (Antecedentes, Periodo y Solicitante)
        # ... (Campos restaurados de la versión anterior) ...
        
        # SECCIÓN III: TRIPLE FIRMA (RESTAURADA)
        st.markdown('### III. PIE DE FIRMA RESPONSABLE')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx'])
        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel, engine='openpyxl')
            # Limpiamos los datos para evitar el error 'unexpected .'
            df.columns = [c.upper().strip() for c in df.columns]
            tabla_limpia = df.to_dict(orient='records')

            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                # ... (Variables de domicilio, periodos, solicitante) ...
                'total_dmcs': int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0,
                'tabla_delitos': tabla_limpia,
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Informe procesado. Verifique la estructura de la tabla en su Word.")
            st.download_button("📂 DESCARGAR", data=output.getvalue(), file_name="Informe_GEO.docx")
        except Exception as e:
            st.error(f"Error de sistema: {e}")