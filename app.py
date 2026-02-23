import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- ESTÉTICA F.R.I.D.A.Y. (PROTOCOLOS ORIGINALES) ---
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
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: ACTA STOP MENSUAL ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_m"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio")
        c1.text_input("Fecha de sesión")
        c2.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        st.markdown('**🖋️ PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm1")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="gm1")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm1")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_t"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo ({{ periodo }})")
        ct1.text_input("Fecha Sesión")
        ct2.text_input("Nombre Asistente") # RECUPERADO
        ct2.text_input("Grado Asistente")   # RECUPERADO
        st.markdown('**🖋️ PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt1")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="gt1")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct1")
        st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        st.markdown('### I. ANTECEDENTES')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio ({{ domicilio }})")
        v_doe = g2.text_input("N° DOE")
        v_fdoe = g2.text_input("Fecha DOE")
        v_cua = g3.text_input("Cuadrante")
        v_fact = g3.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
        
        st.markdown('### II. DATOS DEL SOLICITANTE')
        p1, p2, p3 = st.columns(3)
        v_ini = p1.text_input("Inicio Periodo")
        v_fin = p1.text_input("Fin Periodo")
        v_sol = p2.text_input("Nombre Solicitante")
        v_gsol = p2.text_input("Grado Solicitante")
        v_unid = p3.text_input("Unidad Solicitante")

        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx', 'csv'])

        st.markdown('### III. PIE DE FIRMA')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS SELLADO")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # Gráfico Compacto F.R.I.D.A.Y.
            df_t = df['DELITO'].value_counts().reset_index()
            df_t.columns = ['DELITO', 'CANT.']
            fig, ax = plt.subplots(figsize=(6, len(df_t)*0.4 + 0.5))
            ax.axis('off')
            ax.table(cellText=df_t.values, colLabels=df_t.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05, dpi=200)
            buf.seek(0)

            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'doe': v_doe, 'fecha_doe': v_fdoe, 'cuadrante': v_cua,
                'periodo_inicio': v_ini, 'periodo_fin': v_fin, 'solicitante': v_sol,
                'grado_solic': v_gsol, 'unidad_solic': v_unid, 'fecha_actual': v_fact,
                'total_dmcs': len(df),
                'tabla': InlineImage(doc, buf, width=Inches(4.8)),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Análisis F.R.I.D.A.Y. finalizado correctamente.")
            st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name="Informe_Final.docx")
        except Exception as e: st.error(f"Fallo: {e}")