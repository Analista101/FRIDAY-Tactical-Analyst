import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- 1. PROTOCOLO VISUAL F.R.I.D.A.Y. (BLINDADO) ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 2: STOP TRIMESTRAL (RESTAURADA CON ASISTENTE) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("t_f"):
        c1, c2 = st.columns(2)
        c1.text_input("Periodo")
        c2.text_input("Nombre Asistente") 
        c2.text_input("Grado Asistente")
        st.markdown('**PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nt")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="gt")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ct")
        st.form_submit_button("🛡️ GENERAR")

# --- PESTAÑA 3: INFORME GEO (MÓDULO DE IMAGEN) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL</div>', unsafe_allow_html=True)
    with st.form("geo_img"):
        st.markdown('### I. ANTECEDENTES Y SOLICITANTE')
        g1, g2, g3 = st.columns(3)
        v_dom = g1.text_input("Domicilio")
        v_doe = g2.text_input("N° DOE")
        v_sol = g3.text_input("Nombre Solicitante")
        
        st.markdown('### II. PIE DE FIRMA')
        rf1, rf2, rf3 = st.columns(3)
        v_f_nom = rf1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        v_f_gra = rf2.text_input("Grado", value="C.P.R. Analista Social")
        v_f_car = rf3.text_input("Cargo", value="OFICINA DE OPERACIONES")

        f_mapa = st.file_uploader("Subir Mapa", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel", type=['xlsx', 'csv'])
        btn = st.form_submit_button("🛡️ GENERAR INFORME DEFINITIVO")

    if btn and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # --- FUNCIÓN IA PARA CREAR TABLA-IMAGEN ---
            def crear_tabla_img(dataframe, titulo_cols):
                fig, ax = plt.subplots(figsize=(7, len(dataframe)*0.6 + 0.7))
                ax.axis('off')
                tbl = ax.table(cellText=dataframe.values, colLabels=titulo_cols, 
                               loc='center', cellLoc='left', colColours=['#004A2F']*len(titulo_cols))
                tbl.auto_set_font_size(False)
                tbl.set_fontsize(9)
                for c in range(len(titulo_cols)):
                    tbl[0, c].get_text().set_color('white')
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
                buf.seek(0)
                plt.close()
                return buf

            # Procesar datos
            df_delitos = df['DELITO'].value_counts().reset_index()
            df_delitos.columns = ['DELITO', 'CANTIDAD']
            
            df_horarios = df['RANGO HORA'].value_counts().reset_index()
            df_horarios.columns = ['TRAMO HORARIO', 'CASOS']

            img_delitos = crear_tabla_img(df_delitos, ['DELITO', 'CANTIDAD'])
            img_horarios = crear_tabla_img(df_horarios, ['TRAMO HORARIO', 'CASOS'])

            # --- RENDERIZADO FINAL ---
            doc = DocxTemplate("INFORME GEO.docx")
            context = {
                'domicilio': v_dom, 'doe': v_doe, 'solicitante': v_sol,
                'total_dmcs': len(df),
                'tabla': InlineImage(doc, img_delitos, width=Inches(5.0)),
                'tabla_horarios': InlineImage(doc, img_horarios, width=Inches(4.5)),
                'mapa': InlineImage(doc, f_mapa, width=Inches(5.5)),
                'firma_nombre': v_f_nom, 'firma_grado': v_f_gra, 'firma_cargo': v_f_car,
                'dia_max': df['DIA'].mode()[0], 'hora_max': df['RANGO HORA'].mode()[0],
                'conclusion_ia': f"Análisis finalizado con {len(df)} eventos registrados."
            }
            doc.render(context)
            output = io.BytesIO()
            doc.save(output)
            st.success("Protocolo F.R.I.D.A.Y. ejecutado con éxito.")
            st.download_button("📂 DESCARGAR INFORME SELLADO", data=output.getvalue(), file_name="Informe_Final_JARVIS.docx")
        except Exception as e: st.error(f"Error en el núcleo: {e}")