import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io
import os

# --- 1. CONFIGURACIÓN VISUAL JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    label { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Rutas permanentes GitHub
LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: ACTA STOP MENSUAL ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_m"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", key="m_s")
        c1.text_input("Fecha de sesión", key="m_f")
        c2.text_input("Compromiso Carabineros", key="m_c")
        st.text_area("Problemática Delictual 26ª Comisaría", key="m_p")
        
        st.markdown('**🖋️ PIE DE FIRMA INSTITUCIONAL**')
        f1, f2, f3 = st.columns(3)
        v_nom_m = f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="m_n")
        v_gra_m = f2.text_input("Grado", value="C.P.R. Analista Social", key="m_g")
        v_car_m = f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="m_ca")
        
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_t"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo (Ej: Nov-Dic-Ene)", key="t_pe")
        ct1.text_input("Fecha Sesión", key="t_fe")
        ct2.text_input("Nombre Asistente", key="t_as_n")
        ct2.text_input("Grado Asistente", key="t_as_g")
        
        st.markdown('**🖋️ PIE DE FIRMA INSTITUCIONAL**')
        ft1, ft2, ft3 = st.columns(3)
        v_nom_t = ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="t_n")
        v_gra_t = ft2.text_input("Grado", value="C.P.R. Analista Social", key="t_gr")
        v_car_t = ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="t_car")
        
        st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO (DISEÑO FINAL ARIAL MT) ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo_v5"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="g1")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="g2")
        v_fecha_inf = col1.text_input("Fecha del Informe", value="05 de febrero del año 2026", key="g3")
        
        v_sol = col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="g4")
        v_gsol = col2.text_input("Grado", value="CABO 1RO.", key="g5")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="g6")
        
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556", key="g7")
        v_sub = col3.text_input("Jurisdicción", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="g8")
        v_cua = col3.text_input("Cuadrante", value="231", key="g9")
        
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde", value="05 de noviembre del año 2025", key="g10")
        v_p_fin = cp1.text_input("Hasta", value="05 de febrero del año 2026", key="g11")
        f_mapa = cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="g12")
        f_excel = cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="g13")
        
        btn_run = st.form_submit_button("🚀 EJECUTAR CLONACIÓN DEFINITIVA")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            doc = Document()
            
            # Fuente Arial
            style = doc.styles['Normal']
            style.font.name = 'Arial'
            style.font.size = Pt(11)

            # 1. Portada con Logo Automático
            m = doc.add_paragraph()
            m.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            m.runs[0].font.size = Pt(9)
            
            if os.path.exists(LOGO_PATH):
                p_logo = doc.add_paragraph(); p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.8))
            
            for _ in range(5): doc.add_paragraph()
            p_tit = doc.add_paragraph(); p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_tit = p_tit.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            run_tit.bold = True; run_tit.font.size = Pt(14); run_tit.font.color.rgb = RGBColor(0, 74, 47)
            
            for _ in range(6): doc.add_paragraph()
            doc.add_paragraph(f"PUDAHUEL, {v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()

            # 2. Cuerpo con Sangría 7.5cm (2.95")
            def set_cell_bg(cell, color):
                shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color)
                cell._tc.get_or_add_tcPr().append(shd)

            def p_clon(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95)

            p_clon("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, Comuna De Pudahuel, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")
            p_clon("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:", f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")
            
            p_clon("III.- FUENTE DE LA INFORMACIÓN:", "A partir de los datos obtenidos en el traspaso de datos Aupol del Panel de Comando y Control, y del Sistema de Análisis de Información Territorial (SAIT 2.0).")

            # 3. Cuadros (DMCS y Matriz)
            doc.add_paragraph("\nIV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.5))
            
            # Tabla 2 (Delitos)
            doc.add_paragraph("\nDetalle Delitos DMCS:")
            counts = df['DELITO'].value_counts().reset_index()
            tab2 = doc.add_table(rows=1, cols=2); tab2.style = 'Table Grid'
            for i, txt in enumerate(["DELITO", "CANT."]):
                c = tab2.rows[0].cells[i]; c.text = txt
                set_cell_bg(c, "004A2F")
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
            for _, row in counts.iterrows():
                rc = tab2.add_row().cells; rc[0].text = str(row[0]); rc[1].text = str(row[1])

            # Tabla 3 (Horarios)
            doc.add_paragraph("\nTramo Horario y Días Críticos:")
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            tab3 = doc.add_table(rows=1, cols=len(matriz.columns)+1); tab3.style = 'Table Grid'
            hdr = tab3.rows[0].cells; hdr[0].text = "TRAMO HORA/DIA"
            for i, col in enumerate(matriz.columns): hdr[i+1].text = str(col)
            for cell in hdr:
                set_cell_bg(cell, "004A2F")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
            for idx, row in matriz.iterrows():
                rc = tab3.add_row().cells; rc[0].text = str(idx)
                for j, val in enumerate(row): rc[j+1].text = str(val)

            # 4. Firma Final
            p_clon("V.- CONCLUSIÓN:", "El entorno se considera de RIESGO BAJO para el funcionario.")
            for _ in range(2): doc.add_paragraph()
            if os.path.exists(FIRMA_PATH):
                f_p = doc.add_paragraph(); f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                f_p.add_run().add_picture(FIRMA_PATH, width=Inches(1.5))
            doc.add_paragraph("DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME DEFINITIVO", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")