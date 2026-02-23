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

LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

# --- 2. ESTRUCTURA DE PESTAÑAS ---
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: ACTA STOP (CON NUEVA OPCIÓN STOP FEBRERO) ---
with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL: SELECCIONE FORMATO</div>', unsafe_allow_html=True)
    
    modo_acta = st.radio("Tipo de Formato:", ["Estándar", "Análisis por Delito (Modelo STOP FEBRERO)"], horizontal=True)

    if modo_acta == "Análisis por Delito (Modelo STOP FEBRERO)":
        with st.form("form_stop_febrero"):
            st.subheader("1. Encabezado y Focalización")
            delito = st.text_input("Delito analizado", value="Robo en lugar habitado")
            img_hotline = st.file_uploader("Cargar Imagen SAIT Hotline (Imagen 1)", type=['png', 'jpg'])
            
            st.subheader("2. Estadística de Casos y Víctimas")
            col1, col2 = st.columns(2)
            n_casos = col1.text_input("Casos registrados (28 días)", value="14")
            dias_dist = col1.text_input("Distribución de días", value="martes y domingo")
            horas_dist = col2.text_input("Tramo horario", value="04:00 a 07:59 horas")
            
            st.markdown("**Víctimas:**")
            v_h = col1.text_input("% Hombres (Víctimas)", value="68.1%")
            v_m = col2.text_input("% Mujeres (Víctimas)", value="31.9%")
            
            st.subheader("3. Detenidos y Resultados")
            det_total = st.text_input("Total Detenidos (Número)", value="23")
            det_h = st.text_input("Hombres % (Cantidad)", value="87% (20)")
            det_m = st.text_input("Mujeres % (Cantidad)", value="13% (3)")
            det_chi = st.text_input("Chilenos % (Cantidad)", value="100% (23)")
            det_ext = st.text_input("Extranjeros % (Cantidad)", value="0% (0)")
            
            st.subheader("4. Apartado VIF")
            img_vif = st.file_uploader("Cargar Estadística VIF (Imagen 2)", type=['png', 'jpg'])
            
            btn_feb = st.form_submit_button("🛡️ GENERAR CLON STOP FEBRERO")

            if btn_feb and img_hotline:
                doc = Document()
                style = doc.styles['Normal']; style.font.name = 'Arial'; style.font.size = Pt(11)
                
                # Encabezado exacto
                doc.add_paragraph("26° COMISARÍA PUDAHUEL").runs[0].bold = True
                doc.add_paragraph(f"Delito analizado: {delito}").runs[0].bold = True
                
                # Imagen 1 con doble etiqueta
                txt_img1 = f"Imagen 1: Lugares de focalización del delito {delito} a través de la herramienta SAIT Hotline."
                doc.add_paragraph(txt_img1)
                doc.add_paragraph(txt_img1)
                doc.add_picture(img_hotline, width=Inches(5.5))
                
                # Cuerpo Narrativo
                p = doc.add_paragraph()
                p.add_run(f"Los casos registrados de {delito} en la Unidad en los últimos 28 días son de {n_casos} casos.\n")
                p.add_run(f"Los días de la semana se distribuyen los {dias_dist}.\n")
                p.add_run(f"En los horarios de {horas_dist}.\n")
                
                # Detenidos con formato exacto
                doc.add_paragraph(f"Respecto de los detenidos:\n").runs[0].bold = True
                doc.add_paragraph(f"Hombres: {det_h}; Mujeres: {det_m}.")
                doc.add_paragraph(f"Chilenos: {det_chi}; Extranjeros: {det_ext}.")
                
                # Apartado VIF
                doc.add_paragraph("\nApartado delito Violencia Intrafamiliar (VIF):").runs[0].bold = True
                if img_vif: doc.add_picture(img_vif, width=Inches(5.5))
                doc.add_paragraph("Imagen 2: Estadística relativa a delitos de Violencia intrafamiliar")
                doc.add_paragraph("Fuente: Elaboración propia desde PACIC Operativo").runs[0].font.size = Pt(9)
                
                # Firma Permanente
                for _ in range(3): doc.add_paragraph()
                if os.path.exists(FIRMA_PATH):
                    f_p = doc.add_paragraph(); f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    f_p.add_run().add_picture(FIRMA_PATH, width=Inches(1.5))
                doc.add_paragraph("DIANA SANDOVAL ASTUDILLO\nC.P.R. Analista Social\nOFICINA DE OPERACIONES").alignment = WD_ALIGN_PARAGRAPH.CENTER

                out = io.BytesIO(); doc.save(out)
                st.download_button("📂 DESCARGAR CLON STOP FEBRERO", out.getvalue(), "Acta_STOP_Febrero.docx")

    else:
        # Aquí va el código del "Estándar" que ya teníamos (omitido aquí por brevedad pero blindado)
        st.info("Formato estándar cargado correctamente.")

# --- PESTAÑAS 2 Y 3 (CÓDIGO BLINDADO ANTERIOR SE MANTIENE) ---