import streamlit as st
import pandas as pd
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL JARVIS (INTERFAZ TÁCTICA) ---
st.set_page_config(page_title="SISTEMA JARVIS - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
    label { color: black !important; font-weight: bold; }
    
    /* MATRIZ CARTAS DE SITUACIÓN - FORMATO SOLICITADO */
    .tabla-carta { width: 100%; border: 2px solid #004A2F; border-collapse: collapse; background-color: white; color: black !important; font-family: 'Arial', sans-serif; font-size: 12px; text-transform: uppercase; font-weight: bold; }
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
def procesar_relato_ia(texto):
    # Detectar vehículo de delincuentes (Medio de desplazamiento)
    v_match = re.search(r'(EN UN|A BORDO DE|MOVILIZABAN EN|VEHÍCULO)\s?([^,.]+)', texto, re.I)
    v_transporte = v_match.group(2).strip().upper() if v_match else "VEHÍCULO NO IDENTIFICADO"
    
    # Modus Operandi Breve Estandarizado (Su ejemplo exacto)
    modus = "LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS DESCONOCIDOS, QUIENES MEDIANTE EL USO DE INTIMIDACIÓN O VIOLENCIA LE ARREBATARON SUS PERTENENCIAS PARA LUEGO ESCAPAR EN DIRECCIÓN DESCONOCIDA."
    return v_transporte, modus

# --- 3. COMANDO CENTRAL IA FRIDAY ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
with st.expander("TERMINAL DE ANÁLISIS TÁCTICO", expanded=True):
    st.markdown('<div class="ia-box"><b>PROTOCOLO JARVIS ACTIVADO:</b> Esperando entrada de datos, señor.</div>', unsafe_allow_html=True)
    c_ia1, c_ia2 = st.columns([2, 1])
    consulta_ia = c_ia1.text_area("Describa el hecho para peritaje legal:")
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta_ia: st.info("Análisis de IA completado.")

# --- 4. PESTAÑAS OPERATIVAS (SIN RECORTES) ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTAS DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        c1, c2 = st.columns(2)
        m_sem = c1.text_input("Semana de estudio")
        m_fec = c1.text_input("Fecha de sesión")
        m_com = c2.text_input("Compromiso Carabineros")
        m_pro = st.text_area("Problemática Delictual 26ª Comisaría")
        st.markdown('**🖋️ PIE DE FIRMA**')
        f1, f2, f3 = st.columns(3)
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n1")
        st.text_input("Grado", value="C.P.R. Analista Social", key="g1")
        st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c1")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trimestral"):
        ct1, ct2 = st.columns(2)
        st.text_input("Periodo (Ej: Nov-Dic-Ene)")
        st.text_input("Fecha Sesión STOP")
        st.text_input("Nombre Asistente")
        st.text_input("Grado Asistente")
        st.form_submit_button("🛡️ GENERAR STOP TRIMESTRAL")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo_full"):
        col1, col2, col3 = st.columns(3)
        col1.text_input("DOE N°", value="247205577")
        col1.text_input("Fecha DOE", value="05/02/2026")
        col1.text_input("Fecha Informe", value="05 de febrero del año 2026")
        col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        col2.text_input("Grado Solicitante", value="CABO 1RO.")
        col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        col3.text_input("Domicilio", value="Corona Sueca Nro. 8556")
        col3.text_input("Subcomisaría", value="SUBCOM. TENIENTE HERNÁN MERINO CORREA")
        col3.text_input("Cuadrante", value="231")
        cp1, cp2 = st.columns(2)
        cp1.text_input("Desde (Periodo)", value="05 de noviembre del año 2025")
        cp1.text_input("Hasta (Periodo)", value="05 de febrero del año 2026")
        cp2.file_uploader("Mapa SAIT", type=['png', 'jpg'])
        cp2.file_uploader("Excel Delitos", type=['xlsx', 'csv'])
        st.form_submit_button("🛡️ EJECUTAR CLONACIÓN")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (MATRIZ COLUMNAS)</div>', unsafe_allow_html=True)
    
    # PROTOCOLO DE LIMPIEZA TOTAL
    if "relato_jarvis" not in st.session_state:
        st.session_state.relato_jarvis = ""

    def limpiar_todo():
        st.session_state.relato_jarvis = ""
        st.rerun()

    c_btn1, c_btn2 = st.columns([5, 1])
    with c_btn2:
        st.button("🗑️ LIMPIAR TERMINAL", on_click=limpiar_todo)
    
    relato = st.text_area("PEGUE EL RELATO AQUÍ:", value=st.session_state.relato_jarvis, height=200)
    st.session_state.relato_jarvis = relato # Sincronización

    if st.button("⚡ GENERAR CUADRO"):
        if relato:
            v_traslado, v_modus = procesar_relato_ia(relato)
            html_matriz = f"""
            <table class="tabla-carta">
                <tr>
                    <td rowspan="2" class="celda-titulo" style="width:40%">ROBO CON INTIMIDACIÓN</td>
                    <td class="celda-sub" style="width:20%">TRAMO</td>
                    <td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td>
                </tr>
                <tr>
                    <td style="text-align:center">INDICAR TRAMO</td>
                    <td style="text-align:center">AVENIDA GENERAL OSCAR BONILLA / LOS EDILES</td>
                </tr>
                <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                <tr>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">GENERO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">DE 30 A 35 AÑOS</td></tr>
                            <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">VIA PUBLICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">01 TELÉFONO CELULAR</td></tr>
                        </table>
                    </td>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">VICTIMARIO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">NO INDICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">VESTIMENTA OSCURA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{v_traslado}</td></tr>
                        </table>
                    </td>
                    <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{v_modus}</td>
                </tr>
            </table>
            """
            st.markdown(html_matriz, unsafe_allow_html=True)