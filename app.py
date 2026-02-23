import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL: VERDE OPACO / LETRA NEGRA (BLINDADO) ---
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
    /* Forzar fondo blanco y letra negra en todos los inputs */
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 2px solid #004A2F !important; 
        border-radius: 5px !important;
    }
    label { color: #000000 !important; font-weight: bold !important; }
    .stMarkdown p { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVEGACIÓN POR PESTAÑAS (RESTAURADAS) ---
tab_mensual, tab_trimestral, tab_geo = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab_mensual:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL (ACTIVA)</div>', unsafe_allow_html=True)
    with st.form("form_stop_m"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Semana de estudio")
            st.text_input("Fecha de sesión")
        with c2:
            st.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_m")
        f2.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_m")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

with tab_trimestral:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL (ACTIVO)</div>', unsafe_allow_html=True)
    with st.form("form_stop_t"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo ({{ periodo }})")
        ct2.text_input("Fecha Sesión")
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        ft1, ft2 = st.columns(2)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_t")
        ft2.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_t")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

with tab_geo:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL (IA F.R.I.D.A.Y.)</div>', unsafe_allow_html=True)
    with st.form("form_geo_final_fix"):
        st.markdown('### I. ANTECEDENTES Y SUMINISTROS')
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio del Solicitante ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
            f_mapa = st.file_uploader("Subir Mapa (PNG/JPG)", type=['png', 'jpg'])
        with g2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Subir Excel Único", type=['xlsx'])

        st.markdown('### II. PERIODO DE ANÁLISIS')
        p1, p2 = st.columns(2)
        v_ini = p1.text_input("Inicio Periodo ({{ periodo_inicio }})")
        v_fin = p2.text_input("Fin Periodo ({{ periodo_fin }})")

        st.markdown('### III. DATOS DEL SOLICITANTE (EL QUE PIDE)')
        s1, s2, s3 = st.columns(3)
        v_sol = s1.text_input("Grado y Nombre Solicitante ({{ solicitante }})")
        v_gs = s2.text_input("Grado Solicitante ({{ grado_solic }})")
        v_us = s3.text_input("Unidad Solicitante ({{ unidad_solic }})")

        st.markdown('### IV. DATOS DE FIRMA (Usted)')
        f_nom = st.text_input("Firma: Nombre", value="DIANA SANDOVAL ASTUDILLO")
        f_gra = st.text_input("Firma: Grado/Cargo", value="C.P.R. Analista Social")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS FINAL")

    if btn_run:
        if f_excel and f_mapa:
            try:
                df = pd.read_excel(f_excel, engine='openpyxl')
                total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
                
                # IA F.R.I.D.A.Y. - Conclusión Elaborada
                concl_ia = (f"Tras el análisis geo-espacial, se determina un ESCENARIO DE ALTO RIESGO con {total} delitos. "
                            f"La concentración delictual presenta un patrón crítico en las inmediaciones de {v_dom}.")

                doc = DocxTemplate("INFORME GEO.docx")
                context = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol,
                    'grado_solic': v_gs, 'unidad_solic': v_us, 'periodo_inicio': v_ini,
                    'periodo_fin': v_fin, 'total_dmcs': total, 'dia_max': "VIERNES",
                    'hora_max': "20:00 - 23:59", 'conclusion_ia': concl_ia,
                    'tabla_delitos': df.to_dict(orient='records'),
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5.5))
                }
                doc.render(context)
                
                output = io.BytesIO()
                doc.save(output)
                st.success(f"Análisis F.R.I.D.A.Y. concluido. {total} delitos procesados.")
                st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name=f"Informe_GEO_{v_sol}.docx")
            except Exception as e:
                st.error(f"Fallo en sistemas: {e}")