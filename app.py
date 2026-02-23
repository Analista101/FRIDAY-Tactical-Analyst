import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- ENTORNO JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

# Pestañas Blindadas
t1, t2, t3 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON FINAL)"])

with t3:
    st.markdown('<div class="section-header">📍 SISTEMA DE CLONACIÓN: PORTADA INSTITUCIONAL Y MATRIZ</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_v4"):
        c1, c2, c3 = st.columns(3)
        v_doe = c1.text_input("DOE N°", value="247205577", key="geo_1")
        v_fdoe = c1.text_input("Fecha DOE", value="05/02/2026", key="geo_2")
        v_fecha_inf = c1.text_input("Fecha Informe", value="05 de febrero del año 2026", key="geo_3")
        
        v_sol = c2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="geo_4")
        v_gsol = c2.text_input("Grado", value="CABO 1RO.", key="geo_5")
        v_unid = c2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="geo_6")
        
        v_dom = c3.text_input("Domicilio Análisis", value="Corona Sueca Nro. 8556", key="geo_7")
        v_sub = c3.text_input("Subcomisaría", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="geo_8")
        v_cua = c3.text_input("Cuadrante", value="231", key="geo_9")
        
        st.markdown("---")
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde", value="05 de noviembre del año 2025", key="geo_10")
        v_p_fin = cp1.text_input("Hasta", value="05 de febrero del año 2026", key="geo_11")
        f_logo = cp2.file_uploader("Cargar Logo Carabineros", type=['png', 'jpg'], key="geo_logo")
        f_mapa = cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="geo_map")
        f_excel = cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="geo_exc")
        
        btn_run = st.form_submit_button("🛡️ EJECUTAR CLONACIÓN DE PORTADA Y MATRIZ")

    if btn_run and f_excel and f_mapa and f_logo:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            doc = Document()
            
            # --- 1. PORTADA INSTITUCIONAL (Clon e3d01b) ---
            # Membrete
            m = doc.add_paragraph()
            m.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            m.runs[0].font.size = Pt(9)
            
            # Logo Centrado
            p_logo = doc.add_paragraph(); p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_logo.add_run().add_picture(f_logo, width=Inches(2.0))
            
            for _ in range(5): doc.add_paragraph()

            # Título Grande (Clon e3db67)
            p_tit = doc.add_paragraph()
            p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_tit = p_tit.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            run_tit.bold = True; run_tit.font.size = Pt(14); run_tit.font.color.rgb = RGBColor(0, 74, 47)
            
            for _ in range(6): doc.add_paragraph()
            doc.add_paragraph(f"{v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()

            # --- 2. CUERPO CON SANGRÍA 7.5 (Clon e3d05b) ---
            def p_clon(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95) # Sangría de 7.5cm aprox.

            p_clon("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, Comuna De Pudahuel, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")
            
            p_clon("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:", f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")

            # --- 3. ANÁLISIS Y MATRIZ HORARIA (Figura 3) ---
            doc.add_paragraph("\nIV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.5)) # Mapa con marco implícito
            
            # Matriz de Tiempo (Clon exacto de la tabla de la imagen)
            doc.add_paragraph("\nTramo Horario y Días Críticos:")
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            tab = doc.add_table(rows=1, cols=len(matriz.columns)+1); tab.style = 'Table Grid'
            
            # Encabezado Verde
            hdr = tab.rows[0].cells; hdr[0].text = "TRAMO HORA/DIA"
            for i, col in enumerate(matriz.columns): hdr[i+1].text = str(col)
            for cell in hdr:
                shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), '004A2F')
                cell._tc.get_or_add_tcPr().append(shd)
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)

            for idx, row in matriz.iterrows():
                r_cells = tab.add_row().cells; r_cells[0].text = str(idx)
                for j, val in enumerate(row): r_cells[j+1].text = str(val)

            doc.add_paragraph("FIGURA N° 3: SAIT 2.0 Tramo horario y días críticos DMCS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Firma
            for _ in range(4): doc.add_paragraph()
            doc.add_paragraph(f"DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME CLONADO", data=out.getvalue(), file_name=f"Informe_Final_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")