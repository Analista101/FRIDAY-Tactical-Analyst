import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- CONFIGURACIÓN VISUAL JARVIS ---
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

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (DISEÑO FINAL)"])

# --- (Pestañas 1 y 2 Blindadas en Memoria) ---

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEORREFERENCIADO: ESTÁNDAR INSTITUCIONAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_institucional"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="f_doe")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="f_fdoe")
        v_fecha_inf = col1.text_input("Fecha Informe", value="05 de febrero del año 2026", key="f_finf")
        
        v_sol = col2.text_input("Nombre Solicitante", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="f_sol")
        v_gsol = col2.text_input("Grado Solicitante", value="CABO 1RO.", key="f_gsol")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="f_uni")
        
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556", key="f_dom")
        v_sub = col3.text_input("Jurisdicción (Subcomisaría)", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="f_jur")
        v_cua = col3.text_input("Cuadrante", value="231", key="f_cua")
        
        st.markdown("### PERIODO Y SUMINISTROS")
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde", value="05 de noviembre del año 2025", key="f_pini")
        v_p_fin = cp1.text_input("Hasta", value="05 de febrero del año 2026", key="f_pfin")
        f_mapa = cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="f_map")
        f_excel = cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="f_exc")
        
        btn_build = st.form_submit_button("🛡️ GENERAR INFORME INSTITUCIONAL")

    if btn_build and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # --- MOTOR DE CONSTRUCCIÓN WORD ---
            doc = Document()
            # Estilo Base: Arial 11
            style = doc.styles['Normal']
            style.font.name = 'Arial'
            style.font.size = Pt(11)

            # --- 1. PORTADA (Según Imagen adjunta) ---
            # Membrete Superior Izquierda
            m_p = doc.add_paragraph()
            m_p.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            m_p.runs[0].font.size = Pt(9)
            
            for _ in range(8): doc.add_paragraph() # Espacio para el logo que se inserta manualmente o vía código

            # Título Portada
            t_port = doc.add_paragraph()
            t_port.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_tp = t_port.add_run(f"INFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}")
            r_tp.bold = True; r_tp.font.color.rgb = RGBColor(0, 74, 47) # Verde Institucional

            for _ in range(5): doc.add_paragraph()
            doc.add_paragraph(f"{v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("OFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()

            # --- 2. CUERPO (Sangría 7.5 y Justificado) ---
            def add_p_inst(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(0.75) # Equivalente al sangrado visual de la imagen

            add_p_inst("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, Comuna De Pudahuel, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")
            
            add_p_inst("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:", f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")

            # III.- FUENTE
            doc.add_paragraph("III.- FUENTE DE LA INFORMACIÓN:").runs[0].bold = True
            p3 = doc.add_paragraph("A partir de los datos obtenidos en el traspaso de datos Aupol del Panel de Comando y Control, y del Sistema de Análisis de Información Territorial (SAIT 2.0).")
            p3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p3.paragraph_format.first_line_indent = Inches(0.75)

            # IV.- ANÁLISIS (Mapa con Marco)
            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5.2))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 1: {v_dom}, Comuna De Pudahuel").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # --- TABLAS CON ENCABEZADO VERDE ---
            def crear_tabla_verde(datos, columnas):
                tabla = doc.add_table(rows=1, cols=len(columnas))
                tabla.style = 'Table Grid'
                hdr_cells = tabla.rows[0].cells
                for i, nombre in enumerate(columnas):
                    hdr_cells[i].text = nombre
                    # Pintar Celda de Verde
                    tc = hdr_cells[i]._element.get_or_add_tcPr()
                    shd = OxmlElement('w:shd')
                    shd.set(qn('w:fill'), '004A2F')
                    tc.append(shd)
                    hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
                    hdr_cells[i].paragraphs[0].runs[0].bold = True
                return tabla

            # Figura 2
            doc.add_paragraph("\nDetalle Delictual:")
            counts = df['DELITO'].value_counts().reset_index()
            t2 = crear_tabla_verde(counts, ["DELITO", "CANT."])
            for _, row in counts.iterrows():
                r_cells = t2.add_row().cells
                r_cells[0].text = str(row[0]); r_cells[1].text = str(row[1])

            # Figura 3: Matriz Días/Horas
            doc.add_paragraph("\nTramo Horario y Días Críticos:")
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            t3_docx = crear_tabla_verde(None, ["RANGO HORA"] + list(matriz.columns))
            for idx, row_data in matriz.iterrows():
                r_cells = t3_docx.add_row().cells
                r_cells[0].text = str(idx)
                for j, val in enumerate(row_data): r_cells[j+1].text = str(val)

            # V.- CONCLUSIÓN
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            c_text = f"Conforme a los antecedentes antes señalados, se estima que el lugar donde pretende residir la {v_gsol} {v_sol}, el entorno cercano al domicilio se considera de riesgo bajo para el funcionario... La presente conclusión se sustenta en que los hechos corresponden principalmente a delitos contra la propiedad, con ocurrencia acotada en días y horarios específicos, sin evidenciarse una concentración significativa ni reiteración sistemática en el entorno inmediato del inmueble."
            p_c = doc.add_paragraph(c_text)
            p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_c.paragraph_format.first_line_indent = Inches(0.75)

            # Firma
            for _ in range(3): doc.add_paragraph()
            doc.add_paragraph("DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.success("Informe Institucional construido con éxito.")
            st.download_button("📂 DESCARGAR INFORME CLONADO", data=out.getvalue(), file_name=f"Informe_Final_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error en la construcción: {e}")