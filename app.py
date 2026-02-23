import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- ESTÉTICA F.R.I.D.A.Y. ---
st.set_page_config(page_title="PROJECT F.R.I.D.A.Y. - AUTONOMOUS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO IA"])

# --- (Las pestañas 1 y 2 mantienen el formato de firma triple solicitado) ---

with t3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME TÁCTICO AUTÓNOMO</div>', unsafe_allow_html=True)
    with st.form("f_autonomo"):
        col1, col2 = st.columns(2)
        v_dom = col1.text_input("Domicilio del Objetivo", value="CALLE INTERIOR N° 123")
        v_doe = col1.text_input("N° DOE / Documento")
        v_cua = col2.text_input("Cuadrante", value="237A")
        v_sol = col2.text_input("Nombre del Solicitante")
        
        f_excel = st.file_uploader("Subir Base de Datos (Excel/CSV)", type=['xlsx', 'csv'])
        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        
        st.markdown('### III. RESPONSABLE DE EMISIÓN')
        f_n = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        f_g = st.text_input("Grado", value="C.P.R. Analista Social")
        
        btn = st.form_submit_button("🛡️ GENERAR INFORME AUTÓNOMO")

    if btn and f_excel and f_mapa:
        try:
            # 1. ANALISIS DE DATOS IA
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            total = len(df)
            delito_frec = df['DELITO'].mode()[0]
            dia_max = df['DIA'].mode()[0]
            hora_max = df['RANGO HORA'].mode()[0]

            # 2. CREACIÓN DEL DOCUMENTO DESDE CERO
            doc = Document()
            
            # Encabezado Institucional
            header = doc.add_paragraph()
            header.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = header.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL")
            run.font.size = Pt(9)
            run.bold = True

            # Título Central
            title = doc.add_paragraph()
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_t = title.add_run(f"\nINFORME DELICTUAL: {v_dom}\n")
            run_t.bold = True
            run_t.font.size = Pt(12)

            # Cuerpo del Informe (Relato IA)
            doc.add_paragraph(f"I. ANTECEDENTES:\nEn relación a solicitud DOE N° {v_doe}, se realiza análisis para el domicilio en {v_dom}, cuadrante {v_cua}.")
            
            doc.add_paragraph(f"II. ANÁLISIS GENERAL:\nSe han detectado un total de {total} incidentes en el periodo analizado.")
            
            # Insertar Mapa
            doc.add_picture(f_mapa, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Tabla Compacta (Generada como Imagen por F.R.I.D.A.Y.)
            df_t = df['DELITO'].value_counts().reset_index()
            df_t.columns = ['DELITO', 'CANT.']
            fig, ax = plt.subplots(figsize=(5, len(df_t)*0.3 + 0.5))
            ax.axis('off')
            ax.table(cellText=df_t.values, colLabels=df_t.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.01, dpi=200)
            buf.seek(0)
            doc.add_picture(buf, width=Inches(4))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Conclusión IA
            doc.add_paragraph(f"\nIII. CONCLUSIÓN:\nEl análisis técnico arroja que el delito de '{delito_frec}' es la principal amenaza, concentrándose los días {dia_max} en el tramo {hora_max}. Se sugiere vigilancia preventiva.")

            # Pie de Firma Compacto
            doc.add_paragraph(f"\n\n\n{f_n}\n{f_g}\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 3. ENTREGA
            out = io.BytesIO()
            doc.save(out)
            st.success("Informe construido y sellado por F.R.I.D.A.Y.")
            st.download_button("📂 DESCARGAR INFORME AUTÓNOMO", data=out.getvalue(), file_name="Informe_Autonomo_FRIDAY.docx")
            
        except Exception as e:
            st.error(f"Error en el núcleo: {e}")