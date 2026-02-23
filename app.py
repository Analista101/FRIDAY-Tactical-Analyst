import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- PROTOCOLO VISUAL F.R.I.D.A.Y. ---
st.set_page_config(page_title="PROJECT F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MODULO STOP TRIMESTRAL (RESTAURADO) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("stop_t"):
        c1, c2 = st.columns(2)
        c1.text_input("Periodo")
        c2.text_input("Nombre Asistente") 
        c2.text_input("Grado Asistente")
        st.markdown('**PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="gt")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct")
        st.form_submit_button("GENERAR")

# --- MODULO INFORME GEO (OPTIMIZADO POR IA) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("geo_f"):
        st.markdown('### I. ANTECEDENTES Y SOLICITANTE')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio ({{ domicilio }})")
        v_ini = g2.text_input("Inicio Periodo")
        v_sol = g3.text_input("Nombre Solicitante")
        
        st.markdown('### II. PIE DE FIRMA')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo", value="OFICINA DE OPERACIONES")

        f_mapa = st.file_uploader("Subir Mapa", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx'])
        btn = st.form_submit_button("🛡️ ANALIZAR CON F.R.I.D.A.Y.")

    if btn and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel)
            # F.R.I.D.A.Y. agrupa automáticamente para evitar tablas infinitas
            df_grouped = df.groupby('DELITO')['CUENTA'].sum().reset_index().sort_values('CUENTA', ascending=False)
            
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'periodo_inicio': v_ini, 'solicitante': v_sol,
                'tabla_delitos': df_grouped.to_dict(orient='records'),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Análisis F.R.I.D.A.Y. listo.")
            st.download_button("📂 DESCARGAR", data=output.getvalue(), file_name="Informe_Final.docx")
        except Exception as e: st.error(f"Error: {e}")