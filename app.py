import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (DISEÑO INSTITUCIONAL)"])

# --- (Pestañas 1 y 2 Blindadas) ---

with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: ESTÁNDAR PORTADA Y SANGRÍA 7.5</div>', unsafe_allow_html=True)
    with st.form("form_geo_final_design"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="f1")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="f2")
        v_fecha_inf = col1.text_input("Fecha Informe", value="05 de febrero del año 2026", key="f3")
        
        v_sol = col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="f4")
        v_gsol = col2.text_input("Grado", value="CABO 1RO.", key="f5")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="f6")
        
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556", key="f7")
        v_sub = col3.text_input("Jurisdicción/Subcomisaría", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="f8")
        v_cua = col3.text_input("Cuadrante", value="231", key="f9")
        
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde", value="05 de noviembre del año 2025", key="f10")
        v_p_fin = cp1.text_input("Hasta", value="05 de febrero del año 2026", key="f11")
        f_mapa = cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="f12")
        f_excel = cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="f13")
        
        btn_build = st.form_submit_button("🚀 GENERAR CLON INSTITUCIONAL")

    if btn_build and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            doc = Document()
            
            # --- CONFIGURACIÓN DE PÁGINA Y FUENTE ---
            for section in doc.sections:
                section.top_margin = Inches(1); section.bottom_margin = Inches(1)
                section.left_margin = Inches(1); section.right_margin = Inches(1)
            
            style = doc.styles['Normal']
            style.font.name = 'Arial'; style.font.size = Pt(11)

            # --- 1. PORTADA (Basada en imagen_e3d01b) ---
            h = doc.add_paragraph()
            h.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            h.runs[0].font.size = Pt(9)
            
            for _ in range(12): doc.add_paragraph() # Espacio para el escudo
            
            p_tit = doc.add_paragraph()
            p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_tit = p_tit.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            run_tit.bold = True; run_tit.font.color.rgb = RGBColor(0, 74, 47)
            
            for _ in range(6): doc.add_paragraph()
            doc.add_paragraph(f"{v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()

            # --- 2. CUERPO (Sangría 7.5 y Justificado - Basado en imagen_e3d05b) ---
            def add_inst_para(title, content):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(content)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95) # Aproximación a sangría de 7.5cm en Word

            add_inst_para("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, Comuna De Pudahuel, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")
            
            add_inst_para("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:", f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")

            # --- 3. TABLAS CON ENCABEZADO VERDE ---
            def set_cell_bg(cell, color):
                shd = OxmlElement('w:shd')
                shd.set(qn('w:fill'), color)
                cell._tc.get_or_add_tcPr().append(shd)

            doc.add_paragraph("\nIV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.5)) # Marco negro se asume por el borde de la imagen subida
            
            # Tabla Delitos (Cabecera Verde)
            counts = df['DELITO'].value_counts().reset_index()
            tab2 = doc.add_table(rows=1, cols=2); tab2.style = 'Table Grid'
            for i, txt in enumerate(["DELITO", "CANT."]):
                tab2.rows[0].cells[i].text = txt
                set_cell_bg(tab2.rows[0].cells[i], "004A2F")
                tab2.rows[0].cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)

            for _, row in counts.iterrows():
                r = tab2.add_row().cells
                r[0].text = str(row[0]); r[1].text = str(row[1])

            # Conclusión (Sangría 7.5)
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            p_conc = doc.add_paragraph(f"Conforme a los antecedentes, se estima que el entorno cercano al domicilio se considera de riesgo bajo para el funcionario... sin evidenciarse una concentración significativa ni reiteración sistemática en el entorno inmediato del inmueble.")
            p_conc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_conc.paragraph_format.first_line_indent = Inches(2.95)

            # Firma Diana Sandoval
            for _ in range(4): doc.add_paragraph()
            doc.add_paragraph("DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME INSTITUCIONAL", data=out.getvalue(), file_name=f"Informe_Geo_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")