import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        # SECCIÓN I: ANTECEDENTES
        st.markdown('### I. ANTECEDENTES Y SUMINISTROS')
        c1, c2 = st.columns(2)
        with c1:
            v_dom = st.text_input("Domicilio del Solicitante")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE")
            f_mapa = st.file_uploader("Mapa SAIT (PNG/JPG)", type=['png', 'jpg'])
        with c2:
            v_fdoe = st.text_input("Fecha DOE")
            v_cua = st.text_input("Cuadrante")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único", type=['xlsx'])

        # SECCIÓN II: PERIODOS (RECUPERADOS)
        st.markdown('### II. PERIODO DE ANÁLISIS')
        p1, p2 = st.columns(2)
        v_ini = p1.text_input("Inicio Periodo")
        v_fin = p2.text_input("Fin Periodo")

        # SECCIÓN III: DATOS DEL SOLICITANTE (EL QUE PIDE PERNOCTAR)
        st.markdown('### III. DATOS DEL SOLICITANTE')
        s1, s2, s3 = st.columns(3)
        v_sol = s1.text_input("Nombre Solicitante")
        v_gs = s2.text_input("Grado Solicitante")
        v_us = s3.text_input("Unidad Solicitante")

        # SECCIÓN IV: FIRMA RESPONSABLE (DIANA SANDOVAL)
        st.markdown('### IV. FIRMA DE RESPONSABILIDAD')
        f1, f2 = st.columns(2)
        v_firma_nom = f1.text_input("Nombre de quien firma", value="DIANA SANDOVAL ASTUDILLO")
        v_firma_gra = f2.text_input("Grado de quien firma", value="C.P.R. Analista Social")

        btn_run = st.form_submit_button("🛡️ GENERAR INFORME GEO")

    if btn_run:
        if f_excel and f_mapa:
            try:
                df = pd.read_excel(f_excel, engine='openpyxl')
                total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
                
                # IA F.R.I.D.A.Y. - Conclusión Elaborada
                conclusion_ia = f"Tras el análisis técnico, se concluye un ESCENARIO DE ALTO RIESGO en las cercanías de {v_dom}. Se registran {total} DMCS..."
                
                doc = DocxTemplate("INFORME GEO.docx")
                context = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 
                    'solicitante': v_sol, 'grado_solic': v_gs, 'unidad_solic': v_us, # Datos Solicitante
                    'periodo_inicio': v_ini, 'periodo_fin': v_fin,
                    'total_dmcs': total, 'dia_max': "VIERNES", 'hora_max': "20:00 - 23:59",
                    'conclusion_ia': conclusion_ia,
                    'tabla_delitos': df.to_dict(orient='records'),
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5.5))
                }
                # Si desea que la firma en el Word use las variables v_firma_nom y v_firma_gra,
                # asegúrese de poner {{ firma_nombre }} y {{ firma_grado }} en el pie del Word.
                context['firma_nombre'] = v_firma_nom
                context['firma_grado'] = v_firma_gra
                
                doc.render(context)
                output = io.BytesIO()
                doc.save(output)
                st.success("Análisis completo. Datos de solicitante y firma diferenciados.")
                st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name=f"Informe_GEO_{v_sol}.docx")
            except Exception as e:
                st.error(f"Error: {e}")