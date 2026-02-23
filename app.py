import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io
import os
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL FRIDAY (ESTILO INSTITUCIONAL) ---
st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
    label { color: black !important; font-weight: bold; }
    
    /* ESTILO CUADRO CARTA DE SITUACIÓN: BORDES VERDES, LETRA NEGRA */
    .carta-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 4px solid #004A2F;
    }
    .carta-table {
        width: 100%;
        border-collapse: collapse;
        color: black !important;
    }
    .carta-table td {
        border: 2px solid #004A2F;
        padding: 10px;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .header-col { background-color: #F0F0F0; width: 30%; }
    </style>
    """, unsafe_allow_html=True)

LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

# --- 2. MOTOR DE INTELIGENCIA FRIDAY ---
def limpiar_delito(texto):
    return re.sub(r'ART\.\s?\d+', '', texto, flags=re.IGNORECASE).strip().upper()

def tramo_horario_ia(hora_str):
    try:
        match = re.search(r'(\d{1,2}):', hora_str)
        if match:
            h = int(match.group(1))
            return f"{h:02d}:00 A {h+1:02d}:00"
        return "NO INDICA"
    except: return "NO INDICA"

def rango_etario_ia(dato):
    try:
        anio_match = re.search(r'(\d{4})', str(dato))
        if anio_match:
            edad = datetime.now().year - int(anio_match.group(1))
        else:
            edad = int(re.search(r'(\d+)', str(dato)).group(1))
        inf = (edad // 5) * 5
        return f"DE {inf} A {inf+5} AÑOS"
    except: return "NO INDICA"

# --- 3. ESTRUCTURA DE PESTAÑAS ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTAS DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
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

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_t"):
        ct1, ct2 = st.columns(2)
        t_per = ct1.text_input("Periodo", key="ts1")
        t_fec = ct1.text_input("Fecha Sesión", key="ts2")
        t_asn = ct2.text_input("Nombre Asistente", key="ts3")
        t_asg = ct2.text_input("Grado Asistente", key="ts4")
        st.markdown('**🖋️ DATOS PARA PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        t_nom = ft1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="ts5")
        t_gra = ft2.text_input("Grado", value="C.P.R. Analista Social", key="ts6")
        t_car = ft3.text_input("Cargo", value="OFICINA DE OPERACIONES", key="ts7")
        st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
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
            style = doc.styles['Normal']; style.font.name = 'Arial'; style.font.size = Pt(11)
            def p_sangria(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95)
            # Generación simplificada para el ejemplo
            doc.add_paragraph("INFORME GEO").bold = True
            p_sangria("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe}...")
            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")

with t4:
    st.markdown('<div class="section-header">📋 GENERADOR DE CARTA DE SITUACIÓN (COPIA DIRECTA)</div>', unsafe_allow_html=True)
    
    # Botón Limpiar con Session State
    if "relato_text" not in st.session_state:
        st.session_state["relato_text"] = ""

    def limpiar_area():
        st.session_state["relato_text"] = ""
        st.rerun()

    c_up1, c_up2 = st.columns([5, 1])
    with c_up2:
        st.button("🗑️ LIMPIAR TODO", on_click=limpiar_area)

    relato = st.text_area("PEGUE EL RELATO DEL PARTE AQUÍ:", value=st.session_state["relato_text"], height=250, key="relato_input")

    if st.button("⚡ GENERAR CUADRO PARA COPIAR"):
        if relato:
            # PROCESAMIENTO IA SIMULADO (Ajustar con modelo de lenguaje en producción)
            res_delito = limpiar_delito("ROBO CON INTIMIDACIÓN ART. 436")
            res_tramo = tramo_horario_ia("14:30")
            res_rango = rango_etario_ia("1995")
            res_modus = "LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS DESCONOCIDOS, QUIENES MEDIANTE EL USO DE INTIMIDACIÓN O VIOLENCIA LE ARREBATARON SU VEHÍCULO MOTORIZADO PARA LUEGO ESCAPAR POR LA RUTA EN DIRECCIÓN DESCONOCIDA."

            # Estructura de Tabla HTML para copia directa
            html_table = f"""
            <div class="carta-container">
                <table class="carta-table">
                    <tr><td class="header-col">DELITO</td><td>{res_delito}</td></tr>
                    <tr><td class="header-col">FECHA</td><td>{datetime.now().strftime('%d/%m/%Y')}</td></tr>
                    <tr><td class="header-col">TRAMO HORA</td><td>{res_tramo}</td></tr>
                    <tr><td class="header-col">LUGAR OCURRENCIA</td><td>DIRECCIÓN DETECTADA POR FRIDAY</td></tr>
                    <tr><td class="header-col">LUGAR</td><td>VIA PUBLICA / SERVICENTRO</td></tr>
                    <tr><td class="header-col">RANGO ETARIO VICTIMA</td><td>{res_rango}</td></tr>
                    <tr><td class="header-col">GENERO DELINCUENTE</td><td>MASCULINO</td></tr>
                    <tr><td class="header-col">EDAD DELINCUENTE</td><td>NO INDICA</td></tr>
                    <tr><td class="header-col">CARACT. FISICA</td><td>VESTIMENTA DETECTADA</td></tr>
                    <tr><td class="header-col">MED. DESPLAZAMIENTO</td><td>VEHÍCULO (MARCA, PPU, AÑO)</td></tr>
                    <tr><td class="header-col">ESPECIE SUSTRAIDA</td><td>DETALLE RESUMIDO</td></tr>
                    <tr><td class="header-col">MODUS OPERANDI</td><td>{res_modus}</td></tr>
                </table>
            </div>
            """
            st.markdown(html_table, unsafe_allow_html=True)
            st.success("Señor, el cuadro ha sido generado. Puede seleccionarlo y copiarlo directamente.")
        else:
            st.warning("Señor, el relato está vacío.")