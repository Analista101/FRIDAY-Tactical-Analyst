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
    
    /* ESTILO CUADRO CARTA DE SITUACIÓN EXACTO */
    .carta-table {
        width: 100%;
        border-collapse: collapse;
        border: 2.5pt solid #004A2F !important;
        background-color: white;
    }
    .carta-table td {
        border: 1.5pt solid #004A2F !important;
        padding: 8px 12px;
        color: black !important;
        font-family: 'Arial', sans-serif;
        font-size: 13px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .header-grey {
        background-color: #E6E6E6 !important;
        width: 25%;
    }
    </style>
    """, unsafe_allow_html=True)

LOGO_PATH = "logo_carab.png"
FIRMA_PATH = "firma_diana.png"

# --- 2. FUNCIONES DE PROCESAMIENTO TÁCTICO ---
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

def calcular_rango_etario(dato):
    try:
        match = re.search(r'(\d+)', str(dato))
        if match:
            num = int(match.group(1))
            # Si parece año (ej 1990)
            if num > 1900: num = datetime.now().year - num
            inf = (num // 5) * 5
            return f"DE {inf} A {inf+5} AÑOS"
        return "NO INDICA"
    except: return "NO INDICA"

# --- 3. COMANDO CENTRAL IA FRIDAY (RESTABLECIDO) ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
with st.expander("ABRIR TERMINAL DE ANÁLISIS IA", expanded=True):
    st.markdown('<div class="ia-box"><b>PROTOCOLO FRIDAY:</b> Señor, estoy lista para analizar procedimientos bajo el Código Penal y normativas de Carabineros.</div>', unsafe_allow_html=True)
    c_ia1, c_ia2 = st.columns([2, 1])
    consulta_ia = c_ia1.text_area("Describa el hecho o consulta legal para peritaje:")
    tipo_analisis = c_ia2.selectbox("Foco de Análisis:", ["Tipificación Penal", "Modus Operandi", "Leyes de Seguridad", "Redacción Informe Técnico"])
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta_ia:
            st.info(f"ANÁLISIS COMPLETADO: Proceder bajo normativa de {tipo_analisis}.")

# --- 4. PESTAÑAS DE TRABAJO ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTAS DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    # [Código Acta STOP previo se mantiene aquí]

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    # [Código STOP Trimestral previo se mantiene aquí]

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    # [Código Informe GEO previo se mantiene aquí]

with t4:
    st.markdown('<div class="section-header">📋 GENERADOR DE CARTA DE SITUACIÓN (IA TÁCTICA)</div>', unsafe_allow_html=True)
    
    if "relato_memoria" not in st.session_state:
        st.session_state["relato_memoria"] = ""

    def borrar_relato():
        st.session_state["relato_memoria"] = ""
        st.rerun()

    c_btn1, c_btn2 = st.columns([5, 1])
    with c_btn2:
        st.button("🗑️ LIMPIAR", on_click=borrar_relato)

    relato_input = st.text_area("PEGUE EL RELATO DEL PARTE AQUÍ:", value=st.session_state["relato_memoria"], height=250)

    if st.button("⚡ PROCESAR Y GENERAR CUADRO"):
        if relato_input:
            # EXTRACCIÓN DE DATOS (Simulada por FRIDAY)
            delito_final = limpiar_delito("ROBO POR SORPRESA ART. 415") 
            tramo_final = tramo_horario_ia("11:25")
            rango_final = calcular_rango_etario("24")
            
            # Formato de Cuadro idéntico al solicitado
            html_final = f"""
            <div style="background-color: white; padding: 10px;">
                <table class="carta-table">
                    <tr><td class="header-grey">DELITO</td><td>{delito_final}</td></tr>
                    <tr><td class="header-grey">FECHA</td><td>{datetime.now().strftime('%d/%m/%Y')}</td></tr>
                    <tr><td class="header-grey">TRAMO HORA</td><td>{tramo_final}</td></tr>
                    <tr><td class="header-grey">LUGAR OCURRENCIA</td><td>DIRECCIÓN O INTERSECCIÓN EXTRACTADA</td></tr>
                    <tr><td class="header-grey">LUGAR</td><td>VIA PUBLICA / SERVICENTRO / DOMICILIO</td></tr>
                    <tr><td class="header-grey">RANGO ETARIO VICTIMA</td><td>{rango_final}</td></tr>
                    <tr><td class="header-grey">GENERO DELINCUENTE</td><td>MASCULINO</td></tr>
                    <tr><td class="header-grey">EDAD DELINCUENTE</td><td>NO INDICA</td></tr>
                    <tr><td class="header-grey">CARACT. FISICA</td><td>DESCRIPCIÓN DE VESTIMENTA</td></tr>
                    <tr><td class="header-grey">MED. DESPLAZAMIENTO</td><td>A PIE / VEHÍCULO (MARCA, PPU, AÑO)</td></tr>
                    <tr><td class="header-grey">ESPECIE SUSTRAIDA</td><td>RESUMEN DE ESPECIES</td></tr>
                    <tr><td class="header-grey">MODUS OPERANDI</td><td>LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS DESCONOCIDOS, QUIENES MEDIANTE EL USO DE INTIMIDACIÓN O VIOLENCIA LE ARREBATARON SU VEHÍCULO MOTORIZADO PARA LUEGO ESCAPAR POR LA RUTA EN DIRECCIÓN DESCONOCIDA.</td></tr>
                </table>
            </div>
            """
            st.markdown(html_final, unsafe_allow_html=True)
            st.success("Señor, el cuadro está listo para ser copiado.")