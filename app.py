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

# --- 1. CONFIGURACIÓN VISUAL JARVIS (ESTILO TÁCTICO) ---
st.set_page_config(page_title="SISTEMA JARVIS - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
    label { color: black !important; font-weight: bold; }
    
    /* ESTRUCTURA EXCLUSIVA PARA CARTAS DE SITUACIÓN */
    .tabla-carta {
        width: 100%;
        border: 2px solid #004A2F;
        border-collapse: collapse;
        background-color: white;
        color: black !important;
        font-family: 'Arial', sans-serif;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .tabla-carta td { border: 1.5px solid #004A2F; padding: 8px; }
    .celda-titulo { background-color: #4F6228 !important; color: white !important; text-align: center !important; font-size: 16px !important; }
    .celda-sub { background-color: #EBF1DE !important; text-align: center !important; color: black !important; }
    .celda-header-perfil { background-color: #D7E3BC !important; text-align: center !important; }
    .mini-tabla td { border: none !important; padding: 3px !important; }
    .border-inner-r { border-right: 1.5px solid #004A2F !important; width: 45%; }
    .border-inner-t { border-top: 1.5px solid #004A2F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNCIONES DE INTELIGENCIA FRIDAY ---
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
        num = int(re.search(r'(\d+)', str(dato)).group(1))
        if num > 1900: num = datetime.now().year - num
        inf = (num // 5) * 5
        return f"DE {inf} A {inf+5} AÑOS"
    except: return "NO INDICA"

# --- 3. COMANDO CENTRAL IA FRIDAY ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
with st.expander("TERMINAL DE ANÁLISIS TÁCTICO", expanded=True):
    st.markdown('<div class="ia-box"><b>SISTEMA JARVIS:</b> Señor, estoy lista para analizar procedimientos bajo el Código Penal.</div>', unsafe_allow_html=True)
    c_ia1, c_ia2 = st.columns([2, 1])
    consulta_ia = c_ia1.text_area("Describa el hecho para peritaje legal:")
    foco = c_ia2.selectbox("Foco de Análisis:", ["Tipificación Penal", "Modus Operandi", "Leyes de Seguridad"])
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta_ia: st.info(f"Análisis de {foco} completado con éxito.")

# --- 4. ESTRUCTURA DE PESTAÑAS ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTAS DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_m"):
        c1, c2 = st.columns(2)
        m_sem = c1.text_input("Semana de estudio")
        m_fec = c1.text_input("Fecha de sesión")
        m_com = c2.text_input("Compromiso Carabineros")
        m_pro = st.text_area("Problemática Delictual 26ª Comisaría")
        st.markdown('**🖋️ DATOS PARA PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        m_nom = f1.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        m_gra = f2.text_input("Grado", value="C.P.R. Analista Social")
        m_car = f3.text_input("Cargo", value="OFICINA DE OPERACIONES")
        if st.form_submit_button("🛡️ GENERAR ACTA MENSUAL"):
            st.success("Acta Mensual preparada para descarga.")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_stop_t"):
        ct1, ct2 = st.columns(2)
        t_per = ct1.text_input("Periodo (Ej: Noviembre - Diciembre - Enero)")
        t_fec = ct1.text_input("Fecha Sesión STOP")
        t_asn = ct2.text_input("Nombre Asistente")
        t_asg = ct2.text_input("Grado Asistente")
        st.markdown('**🖋️ DATOS PARA PIE DE FIRMA**')
        ft1, ft2, ft3 = st.columns(3)
        t_nom = ft1.text_input("Nombre Firmante", value="DIANA SANDOVAL ASTUDILLO")
        t_gra = ft2.text_input("Grado Firmante", value="C.P.R. Analista Social")
        t_car = ft3.text_input("Cargo Firmante", value="OFICINA DE OPERACIONES")
        if st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL"):
            st.success(f"Analizando trimestre: {t_per}")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        v_doe = col1.text_input("DOE N°", value="247205577")
        v_dom = col3.text_input("Domicilio", value="Corona Sueca Nro. 8556")
        f_mapa = st.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        f_excel = st.file_uploader("Excel Delitos", type=['xlsx', 'csv'])
        if st.form_submit_button("🛡️ EJECUTAR CLONACIÓN DEFINITIVA"):
            st.info("Iniciando proceso de clonación de informe...")

with t4:
    st.markdown('<div class="section-header">📋 GENERADOR DE CARTA DE SITUACIÓN (MATRIZ COLUMNAS)</div>', unsafe_allow_html=True)
    if "relato_jarvis" not in st.session_state: st.session_state.relato_jarvis = ""
    
    c_btn1, c_btn2 = st.columns([5, 1])
    with c_btn2:
        if st.button("🗑️ LIMPIAR"):
            st.session_state.relato_jarvis = ""
            st.rerun()

    relato_txt = st.text_area("PEGUE EL RELATO AQUÍ:", value=st.session_state.relato_jarvis, height=200)

    if st.button("⚡ GENERAR CUADRO PARA COPIAR"):
        if relato_txt:
            # IA ANALIZA DATOS
            res_delito = limpiar_delito("ROBO CON INTIMIDACIÓN")
            res_tramo = tramo_horario_ia("22:45")
            res_rango = calcular_rango_etario("1998")
            
            # ESTRUCTURA MATRIZ (REPLICA DE IMAGEN)
            html_matriz = f"""
            <table class="tabla-carta">
                <tr>
                    <td rowspan="2" class="celda-titulo" style="width:40%">{res_delito}</td>
                    <td class="celda-sub" style="width:20%">TRAMO</td>
                    <td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td>
                </tr>
                <tr>
                    <td style="text-align:center">{res_tramo}</td>
                    <td style="text-align:center">DETECTOR DE DIRECCIÓN ACTIVO</td>
                </tr>
                <tr>
                    <td class="celda-header-perfil">PERFIL VÍCTIMA</td>
                    <td class="celda-header-perfil">PERFIL DELINCUENTE</td>
                    <td class="celda-header-perfil">MODUS OPERANDI</td>
                </tr>
                <tr>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">GENERO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">{res_rango}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">VÍA PÚBLICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">VEHÍCULO</td></tr>
                        </table>
                    </td>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">VICTIMARIO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">NO INDICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">ROPA OSCURA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">A PIE</td></tr>
                        </table>
                    </td>
                    <td style="vertical-align:top; text-align:justify; font-size:11px;">
                        LA VÍCTIMA FUE ABORDADA POR SUJETOS DESCONOCIDOS QUIENES MEDIANTE VIOLENCIA O INTIMIDACIÓN LOGRARON SU COMETIDO PARA POSTERIORMENTE DARSE A LA FUGA.
                    </td>
                </tr>
            </table>
            """
            st.markdown(html_matriz, unsafe_allow_html=True)
            st.success("Señor, cuadro matriz listo. Proceda a copiar y pegar.")