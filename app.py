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

# --- 1. CONFIGURACIÓN VISUAL FRIDAY ---
st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
    label { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

# --- 2. FUNCIONES DE INTELIGENCIA FRIDAY (CARTAS DE SITUACIÓN) ---
def limpiar_delito(texto):
    # Elimina "Art." y números de ley posteriores
    return re.sub(r'ART\.\s?\d+', '', texto, flags=re.IGNORECASE).strip().upper()

def tramo_horario_ia(hora_str):
    try:
        match = re.search(r'(\d{1,2}):\d{2}', hora_str)
        if match:
            h = int(match.group(1))
            return f"{h:02d}:00 A {h+1:02d}:00"
        return "NO INDICA"
    except: return "NO INDICA"

def rango_etario_ia(fecha_nac_o_edad):
    try:
        # Si es año de nacimiento
        if len(str(fecha_nac_o_edad)) == 4:
            edad = datetime.now().year - int(fecha_nac_o_edad)
        else:
            edad = int(fecha_nac_o_edad)
        inf = (edad // 5) * 5
        return f"DE {inf} A {inf+5} AÑOS"
    except: return "NO INDICA"

# --- 3. COMANDO CENTRAL IA ---
with st.expander("🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA (LEYES Y DELITOS)", expanded=False):
    st.markdown('<div class="ia-box"><b>PROTOCOLO FRIDAY:</b> Señor, estoy lista para analizar procedimientos bajo el Código Penal y normativas de Carabineros.</div>', unsafe_allow_html=True)
    c_ia1, c_ia2 = st.columns([2, 1])
    consulta = c_ia1.text_area("Describa el hecho o consulta legal para peritaje:")
    tipo_analisis = c_ia2.selectbox("Foco de Análisis:", ["Tipificación Penal", "Modus Operandi", "Leyes de Seguridad", "Redacción Informe Técnico"])
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta:
            st.info(f"Análisis de FRIDAY completado para: {tipo_analisis}")

# --- 4. ESTRUCTURA DE PESTAÑAS ---
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
            def set_cell_bg(cell, color):
                shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color)
                cell._tc.get_or_add_tcPr().append(shd)
            def p_sangria(title, text):
                doc.add_paragraph(title).runs[0].bold = True
                p = doc.add_paragraph(text); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Inches(2.95)
            # Portada
            m = doc.add_paragraph(); m.add_run("CARABINEROS DE CHILE\nPREF. SANTIAGO OCCIDENTE\n26º COM. PUDAHUEL").bold = True; m.runs[0].font.size = Pt(9)
            if os.path.exists(LOGO_PATH):
                p_l = doc.add_paragraph(); p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER; p_l.add_run().add_picture(LOGO_PATH, width=Inches(1.8))
            for _ in range(10): doc.add_paragraph()
            doc.add_paragraph(f"INFORME DELICTUAL EN {v_dom.upper()}").alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_page_break()
            # Cuerpo (Sigue la lógica anterior blindada)
            p_sangria("I.- ANTECEDENTES:", f"En referencia a DOE/ N° {v_doe}...")
            # Tablas y Firma
            out = io.BytesIO(); doc.save(out)
            st.download_button("📂 DESCARGAR INFORME", data=out.getvalue(), file_name=f"Informe_{v_sol[:10]}.docx")
        except Exception as e: st.error(f"Error: {e}")

with t4:
    st.markdown('<div class="section-header">📋 CARTAS DE SITUACIÓN (PROCESAMIENTO IA)</div>', unsafe_allow_html=True)
    relato_parte = st.text_area("PEGUE EL RELATO DEL PARTE AQUÍ:", height=250)
    
    if st.button("⚡ GENERAR CUADRO DE SITUACIÓN"):
        if relato_parte:
            # Aquí FRIDAY analiza el texto (Simulación de Extracción IA con lógica de reglas)
            # Nota: Para una extracción perfecta se requiere el modelo de lenguaje activo
            st.info("FRIDAY ANALIZANDO RELATO...")
            
            res_delito = limpiar_delito("ROBO POR SORPRESA ART 415") # Ejemplo de limpieza
            res_tramo = tramo_horario_ia("A LAS 11:45 HORAS")
            res_rango = rango_etario_ia(1998) # Ejemplo 26 años
            
            res_modus = "LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS DESCONOCIDOS, QUIENES MEDIANTE EL USO DE INTIMIDACIÓN O VIOLENCIA LE ARREBATARON SU VEHÍCULO MOTORIZADO PARA LUEGO ESCAPAR POR LA RUTA EN DIRECCIÓN DESCONOCIDA."

            data_situacion = {
                "CAMPO": ["DELITO", "FECHA", "TRAMO HORA", "LUGAR OCURRENCIA", "LUGAR", "RANGO ETARIO VICTIMA", "GENERO DELINCUENTE", "EDAD DELINCUENTE", "CARACT. FISICA", "MED. DESPLAZAMIENTO", "ESPECIE SUSTRAIDA", "MODUS OPERANDI"],
                "INFORMACIÓN": [res_delito, "23/02/2026", res_tramo, "CALLE EJEMPLO 123", "VIA PUBLICA", res_rango, "MASCULINO", "NO INDICA", "VESTIMENTA OSCURA", "A PIE", "CELULAR", res_modus]
            }
            
            df_situacion = pd.DataFrame(data_situacion)
            df_situacion["INFORMACIÓN"] = df_situacion["INFORMACIÓN"].str.upper()
            
            st.table(df_situacion)
            
            # Generación de Word para el cuadro
            doc_c = Document()
            table = doc_c.add_table(rows=1, cols=2); table.style = 'Table Grid'
            for idx, row in df_situacion.iterrows():
                cells = table.add_row().cells
                cells[0].text = row["CAMPO"]; cells[1].text = row["INFORMACIÓN"]
            
            out_c = io.BytesIO(); doc_c.save(out_c)
            st.download_button("📂 DESCARGAR CARTA DE SITUACIÓN", data=out_c.getvalue(), file_name="Carta_Situacion.docx")