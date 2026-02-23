import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- ESTILO JARVIS (VERDE OPACO / LETRA NEGRA) ---
st.set_page_config(page_title="PROJECT JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PROTOCOLO STOP (BLOQUEADO Y COMPLETO) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("t_f"):
        c1, c2 = st.columns(2)
        c1.text_input("Periodo")
        c2.text_input("Nombre Asistente") # Restaurado
        c2.text_input("Grado Asistente")   # Restaurado
        st.markdown('**PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_t")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="g_t")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_t")
        st.form_submit_button("GENERAR")

# --- PROTOCOLO GEO (CON IA DE ORDENAMIENTO) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("geo_f"):
        st.markdown('### I. DATOS DEL SOLICITANTE Y PERIODOS')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio ({{ domicilio }})")
        v_ini = g2.text_input("Inicio Periodo")
        v_fin = g2.text_input("Fin Periodo")
        v_sol = g3.text_input("Nombre Solicitante")
        v_gsol = g3.text_input("Grado Solicitante")
        
        st.markdown('### II. PIE DE FIRMA (DIANA SANDOVAL)')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        f_mapa = st.file_uploader("Subir Mapa", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx'])
        btn = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS IA")

    if btn and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel)
            # IA DE ORDENAMIENTO: Agrupamos y limpiamos para que la tabla sea perfecta
            df_limpio = df.groupby('DELITO')['CUENTA'].sum().reset_index().sort_values(by='CUENTA', ascending=False)
            
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'periodo_inicio': v_ini, 'periodo_fin': v_fin,
                'solicitante': v_sol, 'grado_solic': v_gsol,
                'total_dmcs': int(df_limpio['CUENTA'].sum()),
                'tabla_delitos': df_limpio.to_dict(orient='records'),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'conclusion_ia': f"Análisis finalizado: Se detectan {int(df_limpio['CUENTA'].sum())} eventos con alta concentración en {v_dom}."
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Tabla ordenada por IA. Lista para descarga.")
            st.download_button("📂 DESCARGAR", data=output.getvalue(), file_name="Informe_Final.docx")
        except Exception as e: st.error(f"Error: {e}")