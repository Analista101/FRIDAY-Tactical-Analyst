import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
from datetime import datetime

# --- CONFIGURACIÓN JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #C5A059; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- (Pestañas 1 y 2 se mantienen intactas y blindadas internamente) ---

with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: CLONACIÓN NIVEL TANIA</div>', unsafe_allow_html=True)
    with st.form("form_geo_final_clon"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="k1")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="k2")
        v_fecha_inf = col1.text_input("Fecha Informe (Texto)", value="05 de febrero del año 2026", key="k3")
        
        v_sol = col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="k4")
        v_gsol = col2.text_input("Grado", value="CABO 1RO.", key="k5")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="k6")
        
        v_dom = col3.text_input("Domicilio Análisis", value="Corona Sueca Nro. 8556", key="k7")
        v_sub = col3.text_input("Subcomisaría/Unidad", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="k8")
        v_cua = col3.text_input("Cuadrante", value="231", key="k9")
        
        st.markdown("### PERIODO DE ANÁLISIS")
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde", value="05 de noviembre del año 2025", key="k10")
        v_p_fin = cp2.text_input("Hasta", value="05 de febrero del año 2026", key="k11")

        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="k12")
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="k13")
        
        btn_run = st.form_submit_button("🛡️ EJECUTAR CLONACIÓN ESTRUCTURAL")

    if btn_run and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # PROCESAMIENTO IA PARA RELATO
            total = len(df)
            delito_top = df['DELITO'].mode()[0]
            dia_top = df['DIA'].mode()[0]
            hora_top = df['RANGO HORA'].mode()[0]

            # CONSTRUCCIÓN DEL DOCUMENTO
            doc = Document()
            for s in doc.sections: s.left_margin = s.right_margin = Inches(0.8)

            # --- 1. PORTADA ---
            h1 = doc.add_paragraph(); h1.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            h1.runs[0].font.size = Pt(9)
            
            for _ in range(3): doc.add_paragraph() # Espaciado
            
            p_tit = doc.add_paragraph()
            p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_tit = p_tit.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            run_tit.bold = True; run_tit.font.size = Pt(11)
            
            doc.add_paragraph(f"\n\nPUDAHUEL, {v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            doc.add_page_break() # SALTO A PÁGINA 2 (CUERPO)

            # --- 2. CUERPO DEL INFORME ---
            doc.add_paragraph("I.- ANTECEDENTES:").runs[0].bold = True
            doc.add_paragraph(f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")

            doc.add_paragraph("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:").runs[0].bold = True
            doc.add_paragraph(f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")

            doc.add_paragraph("III.- FUENTE DE LA INFORMACIÓN:").runs[0].bold = True
            doc.add_paragraph("A partir de los datos obtenidos en el traspaso de datos Aupol del Panel de Comando y Control, y del Sistema de Análisis de Información Territorial (SAIT 2.0).")

            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 1: MAPA SECTOR {v_dom}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # RELATO DE ANÁLISIS (CLONADO DE TANIA)
            doc.add_paragraph(f"\nAl efectuar la georreferenciación correspondiente al sector determinado... se puede apreciar la ocurrencia de {total} delitos de mayor connotación social (D.M.C.S) durante el periodo estudiado, siendo el más recurrente el delito de '{delito_top}'.")

            # TABLA 1: DETALLE DELITOS
            tab_del = doc.add_table(rows=1, cols=2)
            tab_del.style = 'Table Grid'
            hdr = tab_del.rows[0].cells
            hdr[0].text = 'DELITO'; hdr[1].text = 'CANT.'
            counts = df['DELITO'].value_counts()
            for d, c in counts.items():
                row = tab_del.add_row().cells
                row[0].text = str(d); row[1].text = str(c)

            doc.add_paragraph("FIGURA N° 2: DETALLE DELITOS DMCS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # TABLA 2: RANGOS HORARIOS Y DÍAS (FIGURA 3)
            doc.add_paragraph(f"\nComo se puede apreciar en el siguiente cuadro el día con mayor cantidad de casos es el {dia_top} en el tramo de {hora_top}.")
            
            # Crear matriz de días/horas en tabla Word
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            tab_mat = doc.add_table(rows=1, cols=len(matriz.columns)+1)
            tab_mat.style = 'Table Grid'
            h_cells = tab_mat.rows[0].cells
            h_cells[0].text = 'RANGO HORA'
            for i, col in enumerate(matriz.columns): h_cells[i+1].text = str(col)
            
            for idx, row_data in matriz.iterrows():
                r_cells = tab_mat.add_row().cells
                r_cells[0].text = str(idx)
                for j, val in enumerate(row_data): r_cells[j+1].text = str(val)

            doc.add_paragraph("FIGURA N° 3: TRAMO HORARIO Y DÍAS CRÍTICOS DMCS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # --- 3. CONCLUSIÓN Y FIRMA ---
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            doc.add_paragraph(f"Conforme a los antecedentes, se estima que el lugar donde pretende residir el {v_gsol} {v_sol}, se considera de RIESGO BAJO para el funcionario. La presente conclusión se sustenta en que los hechos corresponden principalmente a delitos con ocurrencia acotada, sin evidenciarse una concentración significativa ni reiteración sistemática en el entorno inmediato del inmueble.")

            doc.add_paragraph(f"\n\n\nDIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.success("Informe Nivel Tania generado con éxito.")
            st.download_button("📂 DESCARGAR INFORME COMPLETO", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")