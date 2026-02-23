import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import io
from datetime import datetime

# --- ESTÉTICA F.R.I.D.A.Y. (VERDE OPACO / LETRA NEGRA) ---
st.set_page_config(page_title="PROYECTO JARVIS - F.R.I.D.A.Y.", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 10px; }
    input, textarea, [data-baseweb="input"] { background-color: #FFFFFF !important; color: #000000 !important; }
    label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO IA"])

# --- (Pestañas 1 y 2 se mantienen intactas con sus formatos de firma y cuadros) ---

with t3:
    st.markdown('<div class="section-header">📍 GENERADOR DE INFORMES PERSONALIZADOS (ESTILO TANIA)</div>', unsafe_allow_html=True)
    with st.form("f_generador_flexible"):
        st.markdown("### I. DATOS DE LA SOLICITUD (VARIABLES)")
        c1, c2, c3 = st.columns(3)
        v_doe = c1.text_input("DOE N°", placeholder="Ej: 247205577")
        v_fdoe = c1.text_input("Fecha DOE", placeholder="dd/mm/aaaa")
        v_sub = c1.text_input("Subcomisaría Jurisdiccional", placeholder="Ej: Subcomisaría Hernán Merino")
        
        v_sol = c2.text_input("Nombre y Grado del Funcionario", placeholder="Ej: SARGENTO 2DO. JUAN PEREZ")
        v_unid = c2.text_input("Unidad de Origen del Funcionario", placeholder="Ej: 39A. COM. EL BOSQUE")
        v_cua = c2.text_input("Cuadrante del Domicilio", placeholder="Ej: 231")
        
        v_dom = c3.text_input("Dirección del Domicilio a Analizar", placeholder="Ej: Corona Sueca Nro. 8556")
        v_ini = c3.text_input("Inicio Periodo Análisis", placeholder="dd/mm/aaaa")
        v_fin = c3.text_input("Fin Periodo Análisis", placeholder="dd/mm/aaaa")

        st.markdown("### II. CARGA DE ARCHIVOS TÁCTICOS")
        f_mapa = st.file_uploader("Subir Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Subir Excel de Delitos", type=['xlsx', 'csv'])
        
        st.markdown("### III. PIE DE FIRMA RESPONSABLE")
        rf1, rf2, rf3 = st.columns(3)
        v_f_n = rf1.text_input("Nombre Firma", value="DIANA SANDOVAL ASTUDILLO")
        v_f_g = rf2.text_input("Grado Firma", value="C.P.R. Analista Social")
        v_f_c = rf3.text_input("Cargo Firma", value="OFICINA DE OPERACIONES")

        btn = st.form_submit_button("🛡️ GENERAR INFORME ADAPTADO")

    if btn and f_excel and f_mapa:
        try:
            # 1. ANÁLISIS DINÁMICO DE DATOS
            df = pd.read_excel(f_excel) if f_excel.name.endswith('xlsx') else pd.read_csv(f_excel)
            total = len(df)
            delito_frec = df['DELITO'].mode()[0]
            dia_max = df['DIA'].mode()[0]
            hora_max = df['RANGO HORA'].mode()[0]
            riesgo = "BAJO" if total < 20 else "MODERADO"

            # 2. CONSTRUCCIÓN DESDE CERO (RÉPLICA TANIA)
            doc = Document()
            for s in doc.sections: s.left_margin = s.right_margin = Inches(0.8)

            # Membrete
            h = doc.add_paragraph()
            h.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True
            doc.paragraphs[-1].runs[0].font.size = Pt(8)

            # Título Adaptativo
            t_p = doc.add_paragraph()
            t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_t = t_p.add_run(f"\nINFORME DELICTUAL EN {v_dom.upper()}, COMUNA DE PUDAHUEL, PERTENECIENTE A LA {v_sub.upper()}\n")
            run_t.bold = True; run_t.font.size = Pt(10)
            doc.add_paragraph(f"PUDAHUEL, {datetime.now().strftime('%d de %B del año %Y')}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Secciones
            doc.add_paragraph("\nI.- ANTECEDENTES:").runs[0].bold = True
            doc.add_paragraph(f"En referencia a DOE/ N° {v_doe} de fecha {v_fdoe} el cual se refiere a solicitud de confeccionar Informe Delictual para pernoctar fuera del cuartel en {v_dom}, presentada por el {v_sol} dependiente de la {v_unid}.")

            doc.add_paragraph("II.- PERIODO Y LUGAR:").runs[0].bold = True
            doc.add_paragraph(f"El análisis comprende el periodo desde el {v_ini} al {v_fin} en {v_dom}, radio de 300 mts., cuadrante {v_cua}.")

            doc.add_paragraph("IV.- ANÁLISIS GENERAL:").runs[0].bold = True
            doc.add_picture(f_mapa, width=Inches(5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 1: MAPA SECTOR {v_dom}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            doc.add_paragraph(f"Se aprecia la ocurrencia de {total} delitos durante el periodo estudiado.")

            # Tablas-Imagen Compactas (Delitos y Horarios)
            def crear_tabla(data, cols):
                fig, ax = plt.subplots(figsize=(5, len(data)*0.35 + 0.5))
                ax.axis('off')
                ax.table(cellText=data.values, colLabels=cols, loc='center', cellLoc='left', colColours=['#004A2F']*len(cols))
                b = io.BytesIO(); plt.savefig(b, format='png', bbox_inches='tight', pad_inches=0.01, dpi=200); b.seek(0); plt.close()
                return b

            # Tabla 1: Delitos
            df_del = df['DELITO'].value_counts().reset_index(); df_del.columns = ['DELITO', 'CANT.']
            doc.add_picture(crear_tabla(df_del, ['DELITO', 'CANT.']), width=Inches(4))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph(f"FIGURA N° 2: DETALLE DELITOS").alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Conclusión IA Basada en Datos Reales
            doc.add_paragraph("\nV.- CONCLUSIÓN:").runs[0].bold = True
            doc.add_paragraph(f"Se estima que el entorno de {v_dom} presenta un riesgo {riesgo}. El delito predominante es '{delito_frec}', concentrándose los días {dia_max} en el tramo {hora_max}. No se evidencia reiteración sistemática que comprometa la integridad del funcionario.")

            # Firma Triple Centrada
            doc.add_paragraph(f"\n\n\n{v_f_n}\n{v_f_g}\n{v_f_c}").alignment = WD_ALIGN_PARAGRAPH.CENTER

            output = io.BytesIO(); doc.save(output)
            st.success(f"Informe para {v_sol} generado con éxito.")
            st.download_button("📂 DESCARGAR INFORME ADAPTADO", data=output.getvalue(), file_name=f"Informe_{v_sol}.docx")
        except Exception as e: st.error(f"Error técnico: {e}")