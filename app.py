import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io
import os

# --- 1. CONFIGURACIÓN VISUAL JARVIS (BLINDAJE DE ESTILOS) ---
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

# Rutas de archivos permanentes en GitHub
LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

# --- 2. ESTRUCTURA DE PESTAÑAS ---
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (FINAL)"])

# --- PESTAÑA 1: ACTA STOP MENSUAL (RECUPERADA) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL - CONFIGURACIÓN DE FIRMA</div>', unsafe_allow_html=True)
    with st.form("form_stop_m"):
        c1, c2 = st.columns(2)
        m_sem = c1.text_input("Semana de estudio", key="ms1")
        m_fec = c1.text_input("Fecha de sesión", key="ms2")
        m_com = c2.text_input("Compromiso Carabineros", key="ms3")
        m_pro = st.text_area("Problemática Delictual 26ª Comisaría", key="ms4")
        
        st.markdown('**🖋️ DATOS PARA PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        m_nom = f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="ms5")
        m_gra = f2.text_input("Grado", value="C.P.R. Analista Social", key="ms6")
        m_car = f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ms7")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- PESTAÑA 2: STOP TRIMESTRAL (RECUPERADA) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL - CONFIGURACIÓN DE FIRMA</div>', unsafe_allow_html=True)
    with st.form("form_stop_t"):
        ct1, ct2 = st.columns(2)
        t_per = ct1.text_input("Periodo (Ej: Nov-Dic-Ene)", key="ts1")
        t_fec = ct1.text_input("Fecha Sesión", key="ts2")
        t_asn = ct2.text_input("Nombre Asistente", key="ts3")
        t_asg = ct2.text_input("Grado Asistente", key="ts4")
        
        st.markdown('**🖋️ DATOS PARA PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        t_nom = ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="ts5")
        t_gra = ft2.text_input("Grado", value="C.P.R. Analista Social", key="ts6")
        t_car = ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ts7")
        st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO (CLONACIÓN NIVEL PREFECTURA) ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: ARIAL MT + SANGRÍA 7.5 + FIRMA AUTO</div>', unsafe_allow_html=True)
    with st.form("form_geo_final_blindado"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026")
        v_finf = col1.text_input("Fecha Informe", value="05 de febrero del año 2026")
        
        v_sol = col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        v_gsol = col2.text_input("Grado", value="CABO 1RO.")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556")
        v_sub = col3.text_input("Subcomisaría", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA")
        v_cua = col3.text_input("Cuadrante", value="231")
        
        st.markdown("---")
        cp1, cp2 = st.columns(2)
        v_pini = cp1.text_input("Desde", value="05 de noviembre del año 2025")
        v_pfin = cp1.text_input("Hasta", value="05 de febrero del año 2026")
        f_mapa = cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        f_excel = cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'])
        
        btn_run = st.form_submit_button("🛡️ EJECUTAR CLONACIÓN DEFINITIVA")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            doc = Document()
            
            # --- BLINDAJE ARIAL MT ---
            style = doc.styles['Normal']
            style.font.name = 'Arial'
            style.font.size = Pt(11)

            def set_cell_bg(cell, color):
                shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color)
                cell._tc.get_or_add_tcPr().append(shd)

            def p_sangria(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95)

            # 1. PORTADA INSTITUCIONAL
            m = doc.add_paragraph()
            m.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            m.runs[0].font.size = Pt(9)
            
            if os.path.exists(LOGO_PATH):
                doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.paragraphs[-1].add_run().add_picture(LOGO_PATH, width=Inches(1.8))
            
            for _ in range(5): doc.add_paragraph()
            p_tit = doc.add_paragraph(); p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_tit = p_tit.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            r_tit.bold = True; r_tit.font.size = Pt(14); r_tit.font.color.rgb = RGBColor(0, 74, 47)
            
            for _ in range(6): doc.add_paragraph()
            doc.add_paragraph(f"PUDAHUEL, {v_finf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()

            # 2. CUERPO
            p_sangria("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")
            p_sangria("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:", f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_pini} al {v_pfin} {v_dom}, Comuna De Pudahuel, en el cuadrante {v_cua}.")
            p_sangria("III.- FUENTE DE LA INFORMACIÓN:", "A partir de los datos obtenidos en el Panel de Comando y Control, y del Sistema de Análisis de Información Territorial (SAIT 2.0).")

            # 3. ANALISIS + LOS DOS CUADROS (DMCS Y TIEMPO)
            doc.add_paragraph("\nIV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.5))
            
            # Cuadro 1: Delitos
            doc.add_paragraph("\nDetalle Delitos DMCS:")
            counts = df['DELITO'].value_counts().reset_index()
            t_dmcs = doc.add_table(rows=1, cols=2); t_dmcs.style = 'Table Grid'
            hdr = t_dmcs.rows[0].cells; hdr[0].text = "DELITO"; hdr[1].text = "CANT."
            for cell in hdr:
                set_cell_bg(cell, "004A2F")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
            for _, r in counts.iterrows():
                row = t_dmcs.add_row().cells; row[0].text = str(r[0]); row[1].text = str(r[1])

            # Cuadro 2: Matriz
            doc.add_paragraph("\nTramo Horario y Días Críticos:")
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            t_mat = doc.add_table(rows=1, cols=len(matriz.columns)+1); t_mat.style = 'Table Grid'
            hdr2 = t_mat.rows[0].cells; hdr2[0].text = "TRAMO HORA/DIA"
            for i, c in enumerate(matriz.columns): hdr2[i+1].text = str(c)
            for cell in hdr2:
                set_cell_bg(cell, "004A2F")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
            for idx, r_data in matriz.iterrows():
                row = t_mat.add_row().cells; row[0].text = str(idx)
                for j, v in enumerate(r_data): row[j+1].text = str(v)

            # 4. CONCLUSIÓN Y FIRMA AUTO
            p_sangria("V.- CONCLUSIÓN:", f"El entorno cercano al domicilio se considera de RIESGO BAJO para el funcionario {v_sol}.")
            for _ in range(2): doc.add_paragraph()
            if os.path.exists(FIRMA_PATH):
                f_para = doc.add_paragraph(); f_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                f_para.add_run().add_picture(FIRMA_PATH, width=Inches(1.5))
            doc.add_paragraph("DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME BLINDADO", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")