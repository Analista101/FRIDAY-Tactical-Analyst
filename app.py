import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# Intentar importar matplotlib; si falla, F.R.I.D.A.Y. enviará una alerta
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# --- ESTÉTICA F.R.I.D.A.Y. ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if not MATPLOTLIB_AVAILABLE:
    st.error("⚠️ F.R.I.D.A.Y. Error: Falta la librería 'matplotlib'. Por favor, agréguela al archivo requirements.txt")

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- MÓDULO STOP TRIMESTRAL (BLOQUEADO) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("t_f"):
        c1, c2 = st.columns(2)
        c1.text_input("Periodo")
        c2.text_input("Nombre Asistente") 
        c2.text_input("Grado Asistente")
        st.markdown('**🖋️ PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="gt")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct")
        st.form_submit_button("🛡️ GENERAR")

# --- MÓDULO INFORME GEO (TABLA-IMAGEN) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("geo_img"):
        st.markdown('### I. ANTECEDENTES Y SOLICITANTE')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio")
        v_doe = g2.text_input("N° DOE")
        v_sol = g3.text_input("Nombre Solicitante")
        
        st.markdown('### III. PIE DE FIRMA')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx', 'csv'])
        btn = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS SELLADO")

    if btn and f_excel and f_mapa and MATPLOTLIB_AVAILABLE:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # --- CREACIÓN DE LA TABLA COMO IMAGEN ---
            df_counts = df['DELITO'].value_counts().reset_index()
            df_counts.columns = ['DELITO', 'CANTIDAD']
            
            fig, ax = plt.subplots(figsize=(8, len(df_counts)*0.5 + 1))
            ax.axis('off')
            tabla_vis = ax.table(cellText=df_counts.values, colLabels=df_counts.columns, 
                                 loc='center', cellLoc='left', colColours=['#004A2F', '#004A2F'])
            tabla_vis.auto_set_font_size(False)
            tabla_vis.set_fontsize(10)
            for (row, col), cell in tabla_vis.get_celld().items():
                if row == 0: cell.get_text().set_color('white')

            img_tabla = io.BytesIO()
            plt.savefig(img_tabla, format='png', bbox_inches='tight', dpi=200)
            img_tabla.seek(0)
            plt.close()

            # --- CARGA DE PLANTILLA ---
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'doe': v_doe, 'solicitante': v_sol,
                'total_dmcs': len(df),
                'tabla': InlineImage(doc, img_tabla, width=Inches(5.5)),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Análisis F.R.I.D.A.Y. completado.")
            st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name="Informe_Final.docx")
        except Exception as e:
            st.error(f"Error técnico: {e}")