import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import seaborn as sns
import io
from datetime import datetime

# --- ESTÉTICA JARVIS (VERDE OPACO / LETRA NEGRA) ---
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

# Uso de llaves únicas para evitar el error StreamlitAPIException
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO (CLON TANIA)"])

# --- PESTAÑA 1: ACTA STOP MENSUAL (BLINDADA) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_mensual_unique"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", key="sem_m")
        c1.text_input("Fecha de sesión", key="fec_m")
        c2.text_input("Compromiso Carabineros", key="com_m")
        st.text_area("Problemática Delictual 26ª Comisaría", key="prob_m")
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_m")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="g_m")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_m")
        st.form_submit_button("🛡️ GENERAR ACTA")

# --- PESTAÑA 2: STOP TRIMESTRAL (BLINDADA) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_trimestral_unique"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo (Ej: Nov-Dic-Ene)", key="per_t")
        ct1.text_input("Fecha Sesión", key="fec_t")
        ct2.text_input("Nombre Asistente", key="as_n_t")
        ct2.text_input("Grado Asistente", key="as_g_t")
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n_t")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="g_t")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_t")
        st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO (EL CLON REAL) ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR TÁCTICO: ESTÁNDAR TANIA GUTIÉRREZ</div>', unsafe_allow_html=True)
    with st.form("form_clon_tania_final"):
        st.markdown("### I. DATOS DINÁMICOS")
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577")
        v_fdoe = col1.text_input("Fecha DOE", value="05/02/2026")
        v_sol = col2.text_input("Grado y Nombre Funcionario", value="CABO 1RO. TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        v_unid = col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556")
        v_sub = col3.text_input("Jurisdicción", value="SUBCOMISARIA TENIENTE HERNÁN MERINO CORREA")
        
        st.markdown("### II. SUMINISTROS")
        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'], key="u_map")
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx', 'csv'], key="u_exc")
        
        btn_build = st.form_submit_button("🚀 CLONAR INFORME PROFESIONAL")

    if btn_build and f_excel and f_mapa:
        try:
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            
            # --- MOTOR DE IMÁGENES TÁCTICAS ---
            # Fig 2: Tabla Delitos
            df_del = df['DELITO'].value_counts().reset_index(); df_del.columns = ['DELITO', 'CANT.']
            fig1, ax1 = plt.subplots(figsize=(5, len(df_del)*0.35 + 0.5)); ax1.axis('off')
            ax1.table(cellText=df_del.values, colLabels=df_del.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            buf_tab = io.BytesIO(); plt.savefig(buf_tab, format='png', bbox_inches='tight', dpi=200); buf_tab.seek(0); plt.close()

            # Fig 3: Matriz de Calor (Día/Hora) - EL TOQUE PROFESIONAL
            matriz = pd.crosstab(df['RANGO HORA'], df['DIA'])
            fig2, ax2 = plt.subplots(figsize=(7, 4))
            sns.heatmap(matriz, annot=True, cmap="YlGnBu", cbar=False, ax=ax2)
            buf_mat = io.BytesIO(); plt.savefig(buf_mat, format='png', bbox_inches='tight', dpi=200); buf_mat.seek(0); plt.close()

            # --- CONSTRUCCIÓN DEL DOCUMENTO CLON ---
            doc = Document()
            # Encabezado Doble
            p = doc.add_paragraph()
            p.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            doc.paragraphs[-1].runs[0].font.size = Pt(8)

            # Título Centralizado
            t = doc.add_paragraph()
            t.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_t = t.add_run(f"\nINFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}\n")
            run_t.bold = True; run_t.font.size = Pt(10)

            # Cuerpo del Informe con redacción técnica de Tania
            doc.add_paragraph("I.- ANTECEDENTES:").runs[0].bold = True
            doc.add_paragraph(f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} se confecciona informe para pernoctar fuera del cuartel en {v_dom}, solicitado por {v_sol} de la {v_unid}.")

            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 1: MAPA SECTOR {v_dom}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.add_picture(buf_tab, width=Inches(4.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("FIGURA N° 2: DETALLE DELITOS DMCS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.add_picture(buf_mat, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph("FIGURA N° 3: TRAMO HORARIO Y DÍAS CRÍTICOS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Conclusión Clonada
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            doc.add_paragraph(f"Conforme a los antecedentes, el entorno cercano al domicilio de {v_sol} se considera de RIESGO BAJO. La presente conclusión se sustenta en que los hechos corresponden a delitos con ocurrencia acotada, sin evidenciarse una reiteración sistemática en el entorno inmediato del inmueble.")

            # Firma
            doc.add_paragraph(f"\n\n\nDIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.success("Informe 'Tania Protocol' generado con éxito.")
            st.download_button("📂 DESCARGAR CLON PROFESIONAL", data=out.getvalue(), file_name=f"Informe_Tania_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")