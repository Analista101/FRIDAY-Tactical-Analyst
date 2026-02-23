import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- CONFIGURACIÓN VISUAL JARVIS ---
st.set_page_config(page_title="PROYECTO JARVIS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { 
        background-color: #004A2F !important; color: white; 
        padding: 10px; border-radius: 5px; font-weight: bold; 
        margin-bottom: 15px; border-left: 10px solid #C5A059; 
    }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- PESTAÑA 1 Y 2: BLINDADAS (SIN CAMBIOS) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("f_mensual_fixed"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", key="m_s")
        c1.text_input("Fecha de sesión", key="m_f")
        c2.text_input("Compromiso Carabineros", key="m_c")
        st.text_area("Problemática Delictual 26ª Comisaría", key="m_p")
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="m_n")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="m_g")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="m_ca")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("f_trim_fixed"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo (Ej: Nov-Dic-Ene)", key="t_pe")
        ct1.text_input("Fecha Sesión", key="t_fe")
        ct2.text_input("Nombre Asistente", key="t_as_n")
        ct2.text_input("Grado Asistente", key="t_as_g")
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="t_n")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="t_gr")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="t_car")
        st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO (CORREGIDA Y FUNCIONAL) ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: CLON ESTÁNDAR TANIA</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_tania_reparado"):
        st.markdown("### I. ANTECEDENTES DEL DOCUMENTO")
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577", key="g_doe")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026", key="g_fdoe")
        v_fecha_inf = col1.text_input("Fecha del Informe", value="05 de febrero del año 2026", key="g_finf")
        
        v_sol = col2.text_input("Nombre Solicitante", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA", key="g_sol")
        v_gsol = col2.text_input("Grado Solicitante", value="CABO 1RO.", key="g_gsol")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE", key="g_uni")
        
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556", key="g_dom")
        v_sub = col3.text_input("Jurisdicción (Subcomisaría)", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA", key="g_jur")
        v_cua = col3.text_input("Cuadrante", value="231", key="g_cua")
        
        st.markdown("### II. PERIODO DE ANÁLISIS")
        cp1, cp2 = st.columns(2)
        v_p_ini = cp1.text_input("Desde (Fecha)", value="05 de noviembre del año 2025", key="g_pini")
        v_p_fin = cp2.text_input("Hasta (Fecha)", value="05 de febrero del año 2026", key="g_pfin")

        st.markdown("### III. SUMINISTROS")
        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'], key="g_map")
        f_excel = st.file_uploader("Subir Excel de Delitos", type=['xlsx', 'csv'], key="g_exc")
        
        # EL BOTÓN AHORA RESPONDE SIEMPRE
        btn_build = st.form_submit_button("🚀 CLONAR INFORME PROFESIONAL")

    if btn_build and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            total = len(df)
            
            # --- TABLA DE DELITOS (FIGURA 2) ---
            df_del = df['DELITO'].value_counts().reset_index(); df_del.columns = ['DELITO', 'CANT.']
            fig1, ax1 = plt.subplots(figsize=(5, len(df_del)*0.35 + 0.5)); ax1.axis('off')
            ax1.table(cellText=df_del.values, colLabels=df_del.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            buf_tab = io.BytesIO(); plt.savefig(buf_tab, format='png', bbox_inches='tight', dpi=200); buf_tab.seek(0); plt.close()

            # --- CONSTRUCCIÓN DEL DOCUMENTO ---
            doc = Document()
            for s in doc.sections: s.left_margin = s.right_margin = Inches(0.8)

            # Membrete y Títulos (Estilo Tania)
            h = doc.add_paragraph()
            h.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            doc.paragraphs[-1].runs[0].font.size = Pt(8)

            t = doc.add_paragraph()
            t.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_t = t.add_run(f"\nINFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}\n")
            run_t.bold = True; run_t.font.size = Pt(10)
            doc.add_paragraph(f"PUDAHUEL, {v_fecha_inf.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Secciones Romanas Reales
            doc.add_paragraph("\nI.- ANTECEDENTES:").runs[0].bold = True
            doc.add_paragraph(f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para ser adjuntado a solicitud para pernoctar fuera del cuartel en {v_dom}, presentada por el {v_gsol} {v_sol} Dependiente de la {v_unid}.")

            doc.add_paragraph("II.- PERIODO Y LUGAR QUE CONSIDERA EL ANÁLISIS:").runs[0].bold = True
            doc.add_paragraph(f"El presente análisis comprende la temporalidad durante el último trimestre móvil desde el {v_p_ini} al {v_p_fin} {v_dom}, Comuna De Pudahuel, e Inmediaciones en un radio de 300 mts. en el cuadrante {v_cua} perteneciente al sector jurisdiccional de la {v_sub}.")

            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 1: MAPA SECTOR {v_dom}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.add_paragraph(f"Al efectuar la georreferenciación correspondiente... se puede apreciar la ocurrencia de {total} delitos.")
            doc.add_picture(buf_tab, width=Inches(4.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Conclusión Técnica
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            doc.add_paragraph(f"Conforme a los antecedentes, se estima que el entorno cercano al domicilio se considera de RIESGO BAJO para el funcionario. La presente conclusión se sustenta en que los hechos corresponden principalmente a delitos con ocurrencia acotada, sin evidenciarse una concentración significativa ni reiteración sistemática en el entorno inmediato del inmueble.")

            # Firma Diana Sandoval
            doc.add_paragraph(f"\n\n\nDIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.success("Informe construido bajo el estándar Tania.")
            st.download_button("📂 DESCARGAR CLON", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Fallo en el núcleo: {e}")