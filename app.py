import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- ESTÉTICA F.R.I.D.A.Y. (VERDE OPACO / LETRA NEGRA) ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .section-header {
        background-color: #004A2F !important; color: white;
        padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 10px;
    }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- (Pestañas 1 y 2 permanecen blindadas con sus firmas y asistentes) ---

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL INTELIGENTE</div>', unsafe_allow_html=True)
    with st.form("f_geo_ia"):
        c1, c2, c3 = st.columns(3)
        v_dom = c1.text_input("Domicilio", placeholder="Ej: Av. Las Torres 123")
        v_doe = c2.text_input("N° DOE")
        v_fdoe = c2.text_input("Fecha DOE")
        v_cua = c3.text_input("Cuadrante")
        v_fact = c3.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))

        st.markdown('### II. DATOS DEL SOLICITANTE')
        p1, p2, p3 = st.columns(3)
        v_ini = p1.text_input("Inicio Periodo")
        v_fin = p1.text_input("Fin Periodo")
        v_sol = p2.text_input("Nombre Solicitante")
        v_gsol = p2.text_input("Grado Solicitante")
        v_unid = p3.text_input("Unidad Solicitante")

        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx', 'csv'])

        st.markdown('### III. PIE DE FIRMA (DIANA SANDOVAL)')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo", value="OFICINA DE OPERACIONES")

        btn = st.form_submit_button("🛡️ GENERAR INFORME CON IA")

    if btn and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # --- PROCESAMIENTO IA DE DATOS ---
            total = len(df)
            delito_frec = df['DELITO'].mode()[0]
            dia_critico = df['DIA'].mode()[0]
            tramo_critico = df['RANGO HORA'].mode()[0]
            
            # --- GENERACIÓN DE TABLA COMPACTA (SIN MÁRGENES) ---
            df_t = df['DELITO'].value_counts().reset_index()
            df_t.columns = ['DELITO', 'CANT.']
            
            fig, ax = plt.subplots(figsize=(6, len(df_t)*0.4 + 0.5))
            ax.axis('off')
            tabla_img = ax.table(cellText=df_t.values, colLabels=df_t.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            tabla_img.auto_set_font_size(False)
            tabla_img.set_fontsize(9)
            for c in range(2): tabla_img[0, c].get_text().set_color('white')

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05, dpi=200) # MÁRGENES MÍNIMOS
            buf.seek(0)

            # --- REDACCIÓN DE RELATO IA ---
            relato = (f"Al efectuar la georreferenciación en el sector de {v_dom}, se aprecia la ocurrencia de {total} delitos. "
                      f"El análisis técnico identifica que el fenómeno delictual predominante es '{delito_frec}', "
                      f"con una concentración crítica los días {dia_critico} durante el tramo {tramo_critico}. "
                      f"Esta tendencia sugiere una focalización de recursos preventivos en dicho horario.")

            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'doe': v_doe, 'fecha_doe': v_fdoe, 'cuadrante': v_cua,
                'periodo_inicio': v_ini, 'periodo_fin': v_fin, 'solicitante': v_sol,
                'grado_solic': v_gsol, 'unidad_solic': v_unid, 'fecha_actual': v_fact,
                'total_dmcs': total, 'dia_max': dia_critico, 'hora_max': tramo_critico,
                'tabla': InlineImage(doc, buf, width=Inches(4.8)), # Tabla compacta
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'conclusion_ia': relato, # Relato modificado por IA
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Informe procesado. Relato y tablas sincronizados por F.R.I.D.A.Y.")
            st.download_button("📂 DESCARGAR INFORME", data=output.getvalue(), file_name="Informe_IA_Final.docx")
        except Exception as e: st.error(f"Fallo en el sistema: {e}")