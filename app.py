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
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO IA"])

# --- PESTAÑA 1: ACTA STOP MENSUAL (RECUPERADA) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta_mensual"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio")
        c1.text_input("Fecha de sesión")
        c2.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('**🖋️ PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="f1_m")
        f2.text_input("Grado", value="C.P.R. Analista Social", key="f2_m")
        f3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="f3_m")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

# --- PESTAÑA 2: STOP TRIMESTRAL (RECUPERADA Y BLINDADA) ---
with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_trimestral"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo (Ej: Oct-Nov-Dic)")
        ct1.text_input("Fecha Sesión")
        ct2.text_input("Nombre Asistente") 
        ct2.text_input("Grado Asistente")
        
        st.markdown('**🖋️ PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="f1_t")
        ft2.text_input("Grado", value="C.P.R. Analista Social", key="f2_t")
        ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="f3_t")
        st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO IA (ESTILO TANIA - AUTÓNOMO) ---
with t3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORME GEORREFERENCIADO</div>', unsafe_allow_html=True)
    with st.form("f_geo_ia"):
        st.markdown("### I. DATOS DEL FUNCIONARIO Y SOLICITUD")
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", placeholder="Ej: 247205577")
        v_fdoe = col1.text_input("Fecha DOE", placeholder="dd/mm/aaaa")
        v_sub = col1.text_input("Subcomisaría Jurisdiccional", placeholder="Hernán Merino Correa")
        
        v_sol = col2.text_input("Nombre y Grado Solicitante")
        v_unid = col2.text_input("Unidad de Origen del Solicitante")
        v_cua = col2.text_input("Cuadrante", value="231")
        
        v_dom = col3.text_input("Dirección a Analizar")
        v_ini = col3.text_input("Inicio Periodo Análisis")
        v_fin = col3.text_input("Fin Periodo Análisis")

        st.markdown("### II. CARGA DE SUMINISTROS")
        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel de Delitos", type=['xlsx', 'csv'])
        
        st.markdown("### III. FIRMA RESPONSABLE")
        rf1, rf2 = st.columns(2)
        v_f_n = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_g = rf2.text_input("Grado/Cargo Firma", value="C.P.R. Analista Social - OFICINA DE OPERACIONES")

        btn = st.form_submit_button("🛡️ CONSTRUIR INFORME DESDE CERO")

    if btn and f_excel and f_mapa:
        try:
            # 1. ANÁLISIS IA
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            total = len(df)
            delito_frec = df['DELITO'].mode()[0]
            dia_max = df['DIA'].mode()[0]
            hora_max = df['RANGO HORA'].mode()[0]
            riesgo = "BAJO" if total < 20 else "MODERADO"

            # 2. CONSTRUCCIÓN AUTÓNOMA (DISEÑO TANIA)
            doc = Document()
            for s in doc.sections: s.left_margin = s.right_margin = Inches(0.8)

            # Membrete
            h = doc.add_paragraph()
            h.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            doc.paragraphs[-1].runs[0].font.size = Pt(8)

            # Título
            t_p = doc.add_paragraph()
            t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            t_p.add_run(f"\nINFORME DELICTUAL EN {v_dom.upper()}\n").bold = True
            doc.add_paragraph(f"PUDAHUEL, {datetime.now().strftime('%d de %B del año %Y')}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Secciones Romanas
            def sec(t, c):
                doc.add_paragraph(f"\n{t}").runs[0].bold = True
                doc.add_paragraph(c)

            sec("I.- ANTECEDENTES:", f"Solicitud DOE/ N° {v_doe} para pernoctar fuera del cuartel en {v_dom}, presentada por el {v_sol} de la {v_unid}.")
            sec("II.- PERIODO Y LUGAR:", f"Análisis entre el {v_ini} y {v_fin} en {v_dom}, Cuadrante {v_cua}.")
            
            # Gráficos (Tablas-Imagen)
            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

            df_t = df['DELITO'].value_counts().reset_index(); df_t.columns = ['DELITO', 'CANT.']
            fig, ax = plt.subplots(figsize=(5, len(df_t)*0.35 + 0.5)); ax.axis('off')
            ax.table(cellText=df_t.values, colLabels=df_t.columns, loc='center', cellLoc='left', colColours=['#004A2F']*2)
            buf = io.BytesIO(); plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.01, dpi=200); buf.seek(0); plt.close()
            
            doc.add_picture(buf, width=Inches(4))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Conclusión
            sec("V.- CONCLUSIÓN:", f"Riesgo estimado: {riesgo}. Frecuencia mayor de '{delito_frec}' los días {dia_max} en el tramo {hora_max}.")

            # Firma
            doc.add_paragraph(f"\n\n\n{v_f_n}\n{v_f_g}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            out = io.BytesIO(); doc.save(out)
            st.success("Informe procesado correctamente.")
            st.download_button("📂 DESCARGAR", data=out.getvalue(), file_name=f"Informe_{v_sol}.docx")
        except Exception as e: st.error(f"Error: {e}")